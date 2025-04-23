"""
Conector para o DATASUS TABNET via biblioteca PySUS.

Este módulo implementa o conector para acessar dados do DATASUS TABNET utilizando
a biblioteca PySUS, que facilita o acesso a dados de sistemas como SIM, SINAN, SINASC e SIH.
"""

import os
import pandas as pd
from typing import Dict, List, Any, Union, Optional
import logging
import tempfile

# Importações condicionais para lidar com possíveis erros de importação
try:
    import pysus
    from pysus.online_data import SIM, SINAN, SINASC, SIH
except ImportError:
    logging.warning("PySUS not installed. Install it with 'pip install pysus'")

from .base import DataConnector

logger = logging.getLogger(__name__)

class TabnetConnector(DataConnector):
    """
    Conector para o DATASUS TABNET via biblioteca PySUS.
    
    Este conector permite acessar dados dos sistemas de informação do DATASUS,
    como SIM (Sistema de Informações sobre Mortalidade), SINAN (Sistema de Informação
    de Agravos de Notificação), SINASC (Sistema de Informações sobre Nascidos Vivos)
    e SIH (Sistema de Informações Hospitalares).
    
    Attributes:
        data_dir (str): Diretório para armazenamento temporário de arquivos baixados.
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """
        Inicializa o conector TABNET.
        
        Args:
            data_dir (str, optional): Diretório para armazenamento temporário de arquivos.
                Se não for fornecido, será usado um diretório temporário.
        """
        self.data_dir = data_dir or tempfile.mkdtemp()
        os.makedirs(self.data_dir, exist_ok=True)
    
    async def list_datasets(self) -> List[Dict[str, Any]]:
        """
        Lista os datasets disponíveis via PySUS.
        
        Returns:
            List[Dict[str, Any]]: Lista de dicionários contendo informações sobre os datasets.
                Cada dicionário contém pelo menos as chaves 'id' e 'description'.
        """
        return [
            {
                "id": "sim",
                "name": "SIM",
                "description": "Sistema de Informações sobre Mortalidade",
                "years_available": list(range(1996, 2023))
            },
            {
                "id": "sinan",
                "name": "SINAN",
                "description": "Sistema de Informação de Agravos de Notificação",
                "years_available": list(range(2001, 2023))
            },
            {
                "id": "sinasc",
                "name": "SINASC",
                "description": "Sistema de Informações sobre Nascidos Vivos",
                "years_available": list(range(1994, 2023))
            },
            {
                "id": "sih",
                "name": "SIH",
                "description": "Sistema de Informações Hospitalares",
                "years_available": list(range(2008, 2023))
            }
        ]
    
    async def fetch(self, query: Dict[str, Any]) -> pd.DataFrame:
        """
        Busca dados do DATASUS TABNET de acordo com os parâmetros de consulta.
        
        Args:
            query (Dict[str, Any]): Parâmetros de consulta. Deve conter as seguintes chaves:
                - system (str): Sistema de informação (sim, sinan, sinasc, sih).
                - state (str): Sigla do estado (ex: BA, SP, RJ).
                - year (int): Ano dos dados.
                - disease (str, optional): Código da doença para SINAN.
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados brutos.
        
        Raises:
            ValueError: Se os parâmetros de consulta forem inválidos.
            ImportError: Se a biblioteca PySUS não estiver instalada.
            Exception: Se ocorrer um erro ao buscar os dados.
        """
        if "system" not in query:
            raise ValueError("Query must contain 'system' parameter")
        
        if "state" not in query:
            raise ValueError("Query must contain 'state' parameter")
        
        if "year" not in query:
            raise ValueError("Query must contain 'year' parameter")
        
        system = query["system"].lower()
        state = query["state"].upper()
        year = int(query["year"])
        
        try:
            if system == "sim":
                # Sistema de Informações sobre Mortalidade
                df = SIM.download(state, year, self.data_dir)
            
            elif system == "sinan":
                # Sistema de Informação de Agravos de Notificação
                if "disease" not in query:
                    raise ValueError("Query must contain 'disease' parameter for SINAN")
                
                disease = query["disease"].lower()
                df = SINAN.download(disease, state, year, self.data_dir)
            
            elif system == "sinasc":
                # Sistema de Informações sobre Nascidos Vivos
                df = SINASC.download(state, year, self.data_dir)
            
            elif system == "sih":
                # Sistema de Informações Hospitalares
                df = SIH.download(state, year, self.data_dir)
            
            else:
                raise ValueError(f"Unknown system: {system}")
            
            return df
        
        except ImportError:
            logger.error("PySUS not installed")
            raise ImportError("PySUS not installed. Install it with 'pip install pysus'")
        
        except Exception as e:
            logger.error(f"Error fetching data: {e}")
            raise
    
    async def normalize(self, data: pd.DataFrame) -> pd.DataFrame:
        """
        Normaliza os dados brutos retornados pelo método fetch() em um DataFrame pandas.
        
        Para o conector TABNET, o método fetch() já retorna um DataFrame pandas,
        então este método apenas faz algumas limpezas e transformações adicionais.
        
        Args:
            data (pd.DataFrame): DataFrame pandas retornado pelo método fetch().
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados normalizados.
        
        Raises:
            ValueError: Se os dados não puderem ser normalizados.
        """
        try:
            if not isinstance(data, pd.DataFrame):
                raise ValueError("Input data must be a pandas DataFrame")
            
            # Cópia para evitar modificar o DataFrame original
            df = data.copy()
            
            # Converte colunas de texto para string
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].astype(str)
            
            # Remove espaços em branco extras
            for col in df.select_dtypes(include=['object']).columns:
                df[col] = df[col].str.strip()
            
            return df
        
        except Exception as e:
            logger.error(f"Error normalizing data: {e}")
            raise ValueError(f"Could not normalize data: {e}")
    
    def schema(self) -> Dict[str, Any]:
        """
        Retorna o schema do conector TABNET, incluindo metadados e informações sobre os parâmetros aceitos.
        
        Returns:
            Dict[str, Any]: Dicionário contendo informações sobre o conector.
        """
        return {
            "name": "DATASUS TABNET",
            "description": "Conector para acessar dados do DATASUS TABNET via PySUS",
            "systems": {
                "sim": "Sistema de Informações sobre Mortalidade",
                "sinan": "Sistema de Informação de Agravos de Notificação",
                "sinasc": "Sistema de Informações sobre Nascidos Vivos",
                "sih": "Sistema de Informações Hospitalares"
            },
            "parameters": {
                "system": "Sistema de informação (sim, sinan, sinasc, sih)",
                "state": "Sigla do estado (ex: BA, SP, RJ)",
                "year": "Ano dos dados",
                "disease": "Código da doença para SINAN"
            },
            "data_dir": self.data_dir
        }
