"""
Conector para a API do DEMAS (Departamento de Monitoramento e Avaliação do SUS).

Este módulo implementa o conector para acessar dados do DEMAS através da API
apidadosabertos.saude.gov.br, que disponibiliza informações sobre estabelecimentos
de saúde, leitos e outros recursos do SUS.
"""

import httpx
import pandas as pd
from typing import Dict, List, Any, Union, Optional
import json
import asyncio
import logging

from .base import DataConnector

logger = logging.getLogger(__name__)

class DemasConnector(DataConnector):
    """
    Conector para a API do DEMAS.
    
    Este conector permite acessar dados do Departamento de Monitoramento e Avaliação do SUS,
    incluindo informações sobre estabelecimentos de saúde, leitos e outros recursos.
    
    Attributes:
        base_url (str): URL base da API do DEMAS.
        client (httpx.AsyncClient): Cliente HTTP assíncrono para fazer requisições à API.
    """
    
    def __init__(self, base_url: str = "https://apidadosabertos.saude.gov.br/api"):
        """
        Inicializa o conector DEMAS.
        
        Args:
            base_url (str, optional): URL base da API do DEMAS. 
                Padrão: "https://apidadosabertos.saude.gov.br/api".
        """
        self.base_url = base_url
        self.client = httpx.AsyncClient(timeout=30.0)
        self._endpoints = {
            "cnes": "/cnes/estabelecimentos",
            "leitos": "/cnes/leitos",
            "estabelecimentos": "/cnes/estabelecimentos"
        }
    
    async def list_datasets(self) -> List[Dict[str, Any]]:
        """
        Lista os datasets disponíveis na API do DEMAS.
        
        Returns:
            List[Dict[str, Any]]: Lista de dicionários contendo informações sobre os datasets.
                Cada dicionário contém pelo menos as chaves 'id' e 'name'.
        """
        # A API do DEMAS não tem um endpoint para listar datasets,
        # então retornamos uma lista estática dos datasets conhecidos
        return [
            {
                "id": "cnes",
                "name": "CNES - Cadastro Nacional de Estabelecimentos de Saúde",
                "description": "Dados do Cadastro Nacional de Estabelecimentos de Saúde",
                "url": f"{self.base_url}/cnes/estabelecimentos"
            },
            {
                "id": "leitos",
                "name": "Leitos Hospitalares",
                "description": "Informações sobre leitos hospitalares disponíveis no SUS",
                "url": f"{self.base_url}/cnes/leitos"
            },
            {
                "id": "estabelecimentos",
                "name": "Estabelecimentos de Saúde",
                "description": "Dados detalhados sobre estabelecimentos de saúde",
                "url": f"{self.base_url}/cnes/estabelecimentos"
            }
        ]
    
    async def fetch(self, query: Dict[str, Any]) -> Any:
        """
        Busca dados da API do DEMAS de acordo com os parâmetros de consulta.
        
        Args:
            query (Dict[str, Any]): Parâmetros de consulta. Deve conter as seguintes chaves:
                - dataset (str): ID do dataset (cnes, leitos, estabelecimentos).
                - filters (Dict[str, Any], optional): Filtros a serem aplicados na consulta.
                - limit (int, optional): Número máximo de registros a serem retornados.
                - year (int, optional): Ano de referência dos dados.
        
        Returns:
            Any: Dados brutos retornados pela API do DEMAS.
        
        Raises:
            ValueError: Se os parâmetros de consulta forem inválidos.
            httpx.HTTPError: Se ocorrer um erro na requisição HTTP.
        """
        if "dataset" not in query:
            raise ValueError("Query must contain 'dataset' parameter")
        
        dataset = query["dataset"]
        if dataset not in self._endpoints:
            raise ValueError(f"Unknown dataset: {dataset}")
        
        endpoint = self._endpoints[dataset]
        url = f"{self.base_url}{endpoint}"
        
        # Prepara os parâmetros da consulta
        params = {}
        
        # Adiciona filtros se fornecidos
        if "filters" in query and isinstance(query["filters"], dict):
            for key, value in query["filters"].items():
                params[key] = value
        
        # Adiciona limite se fornecido
        if "limit" in query:
            params["limit"] = query["limit"]
        
        # Adiciona ano se fornecido
        if "year" in query:
            params["ano"] = query["year"]
        
        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            return data
        
        except httpx.HTTPError as e:
            logger.error(f"HTTP error occurred: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise
    
    async def normalize(self, data: Any) -> pd.DataFrame:
        """
        Normaliza os dados brutos retornados pelo método fetch() em um DataFrame pandas.
        
        Args:
            data (Any): Dados brutos retornados pelo método fetch().
                Pode ser um dicionário com chave 'data' ou 'records' contendo os registros.
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados normalizados.
        
        Raises:
            ValueError: Se os dados não puderem ser normalizados.
        """
        try:
            if isinstance(data, dict) and "data" in data:
                # Formato comum da API do DEMAS
                records = data["data"]
                return pd.DataFrame(records)
            
            elif isinstance(data, dict) and "records" in data:
                # Formato alternativo
                records = data["records"]
                return pd.DataFrame(records)
            
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
        Retorna o schema do conector DEMAS, incluindo metadados e informações sobre os parâmetros aceitos.
        
        Returns:
            Dict[str, Any]: Dicionário contendo informações sobre o conector.
        """
        return {
            "name": "DEMAS",
            "description": "Conector para acessar dados do Departamento de Monitoramento e Avaliação do SUS",
            "base_url": self.base_url,
            "endpoints": self._endpoints,
            "parameters": {
                "dataset": "ID do dataset (cnes, leitos, estabelecimentos)",
                "filters": "Filtros a serem aplicados na consulta",
                "limit": "Número máximo de registros a serem retornados",
                "year": "Ano de referência dos dados"
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
