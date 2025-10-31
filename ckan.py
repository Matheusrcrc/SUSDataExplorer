"""
Conector para a API CKAN do OpenDataSUS.

Este módulo implementa o conector para acessar dados do OpenDataSUS via API CKAN.
"""

import httpx
import pandas as pd
from typing import Dict, List, Any, Union, Optional
import json
import asyncio
import logging

from base import DataConnector

logger = logging.getLogger(__name__)

class CkanConnector(DataConnector):
    """
    Conector para a API CKAN do OpenDataSUS.
    
    Este conector permite acessar datasets disponíveis no portal OpenDataSUS,
    que utiliza a plataforma CKAN para disponibilização de dados abertos.
    
    Attributes:
        base_url (str): URL base da API CKAN.
        client (httpx.AsyncClient): Cliente HTTP assíncrono para fazer requisições à API.
    """
    
    def __init__(self, base_url: str = "https://opendatasus.saude.gov.br/api/3"):
        """
        Inicializa o conector CKAN.
        
        Args:
            base_url (str, optional): URL base da API CKAN. 
                Padrão: "https://opendatasus.saude.gov.br/api/3".
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def list_datasets(self) -> List[Dict[str, Any]]:
        """
        Lista os datasets disponíveis no OpenDataSUS.
        
        Returns:
            List[Dict[str, Any]]: Lista de dicionários contendo informações sobre os datasets.
                Cada dicionário contém pelo menos as chaves 'id' e 'name'.
        
        Raises:
            httpx.HTTPError: Se ocorrer um erro na requisição HTTP.
            ValueError: Se a resposta da API não estiver no formato esperado.
        """
        try:
            url = f"{self.base_url}/action/package_list"
            response = await self.client.get(url)
            response.raise_for_status()
            
            data = response.json()
            if not data.get("success", False):
                raise ValueError(f"API returned error: {data.get('error', 'Unknown error')}")
            
            # Obtém a lista de IDs de datasets
            dataset_ids = data.get("result", [])
            
            # Para cada ID, obtém informações detalhadas
            datasets = []
            for dataset_id in dataset_ids[:10]:  # Limita a 10 para não sobrecarregar a API
                try:
                    dataset_info = await self._get_dataset_info(dataset_id)
                    datasets.append(dataset_info)
                except Exception as e:
                    logger.warning(f"Failed to get info for dataset {dataset_id}: {e}")
            
            return datasets
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Error listing datasets: {e}")
            raise
    
    async def _get_dataset_info(self, dataset_id: str) -> Dict[str, Any]:
        """
        Obtém informações detalhadas sobre um dataset específico.
        
        Args:
            dataset_id (str): ID do dataset.
        
        Returns:
            Dict[str, Any]: Dicionário contendo informações detalhadas sobre o dataset.
        
        Raises:
            httpx.HTTPError: Se ocorrer um erro na requisição HTTP.
            ValueError: Se a resposta da API não estiver no formato esperado.
        """
        url = f"{self.base_url}/action/package_show?id={dataset_id}"
        response = await self.client.get(url)
        response.raise_for_status()
        
        data = response.json()
        if not data.get("success", False):
            raise ValueError(f"API returned error: {data.get('error', 'Unknown error')}")
        
        result = data.get("result", {})
        return {
            "id": result.get("id", ""),
            "name": result.get("title", ""),
            "description": result.get("notes", ""),
            "resources": [
                {
                    "id": res.get("id", ""),
                    "name": res.get("name", ""),
                    "format": res.get("format", ""),
                    "url": res.get("url", "")
                }
                for res in result.get("resources", [])
            ]
        }
    
    async def fetch(self, query: Dict[str, Any]) -> Any:
        """
        Busca dados do OpenDataSUS de acordo com os parâmetros de consulta.
        
        Args:
            query (Dict[str, Any]): Parâmetros de consulta. Deve conter pelo menos uma das seguintes chaves:
                - dataset_id (str): ID do dataset para obter informações.
                - resource_id (str): ID do recurso para obter dados.
        
        Returns:
            Any: Dados brutos retornados pela API CKAN.
        
        Raises:
            ValueError: Se os parâmetros de consulta forem inválidos.
            httpx.HTTPError: Se ocorrer um erro na requisição HTTP.
        """
        if "dataset_id" in query and "resource_id" not in query:
            # Busca informações sobre o dataset
            return await self._get_dataset_info(query["dataset_id"])
        
        elif "resource_id" in query:
            # Busca dados do recurso
            limit = query.get("limit", 100)
            offset = query.get("offset", 0)
            filters = query.get("filters", {})
            
            url = f"{self.base_url}/action/datastore_search"
            params = {
                "resource_id": query["resource_id"],
                "limit": limit,
                "offset": offset
            }
            
            if filters:
                params["filters"] = json.dumps(filters)
            
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            if not data.get("success", False):
                raise ValueError(f"API returned error: {data.get('error', 'Unknown error')}")
            
            return data.get("result", {})
        
        else:
            raise ValueError("Query must contain either 'dataset_id' or 'resource_id'")
    
    async def normalize(self, data: Any) -> pd.DataFrame:
        """
        Normaliza os dados brutos retornados pelo método fetch() em um DataFrame pandas.
        
        Args:
            data (Any): Dados brutos retornados pelo método fetch().
                Pode ser um dicionário com informações do dataset ou dados de um recurso.
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados normalizados.
        
        Raises:
            ValueError: Se os dados não puderem ser normalizados.
        """
        try:
            if isinstance(data, dict) and "records" in data:
                # Dados de um recurso
                records = data["records"]
                return pd.DataFrame(records)
            
            elif isinstance(data, dict) and "resources" in data:
                # Informações de um dataset
                resources = data["resources"]
                return pd.DataFrame(resources)
            
            elif isinstance(data, list):
                # Lista de registros
                return pd.DataFrame(data)
            
            else:
                # Tenta converter o dicionário em um DataFrame
                return pd.DataFrame([data])
        
        except Exception as e:
            logger.error(f"Error normalizing data: {e}")
            raise ValueError(f"Could not normalize data: {e}")
    
    def schema(self) -> Dict[str, Any]:
        """
        Retorna o schema do conector CKAN, incluindo metadados e informações sobre os parâmetros aceitos.
        
        Returns:
            Dict[str, Any]: Dicionário contendo informações sobre o conector.
        """
        return {
            "name": "CKAN OpenDataSUS",
            "description": "Conector para acessar dados do OpenDataSUS via API CKAN",
            "base_url": self.base_url,
            "endpoints": {
                "package_list": "/action/package_list",
                "package_show": "/action/package_show",
                "datastore_search": "/action/datastore_search"
            },
            "datasets": [
                "pni", "sim", "sinasc", "sih", "sinan", "cnes"
            ],
            "parameters": {
                "dataset_id": "ID do dataset para obter informações",
                "resource_id": "ID do recurso para obter dados",
                "limit": "Número máximo de registros a serem retornados",
                "offset": "Índice inicial para paginação",
                "filters": "Filtros a serem aplicados na consulta"
            }
        }
    
    async def __aenter__(self):
        """
        Método para suporte ao uso do conector como gerenciador de contexto assíncrono.
        """
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        Método para suporte ao uso do conector como gerenciador de contexto assíncrono.
        Fecha o cliente HTTP ao sair do contexto.
        """
        await self.client.aclose()
