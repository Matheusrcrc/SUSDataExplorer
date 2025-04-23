"""
Base de conectores para o SUS Data Explorer.

Este módulo define a classe base para todos os conectores de dados do SUS Data Explorer.
Cada conector específico deve herdar desta classe e implementar os métodos abstratos.
"""

import abc
import pandas as pd
from typing import Dict, List, Any, Union, Optional


class DataConnector(abc.ABC):
    """
    Classe base abstrata para conectores de dados.
    
    Todos os conectores de dados do SUS Data Explorer devem herdar desta classe
    e implementar os métodos abstratos para garantir uma interface consistente.
    """
    
    @abc.abstractmethod
    async def list_datasets(self) -> List[Dict[str, Any]]:
        """
        Lista os datasets disponíveis nesta fonte de dados.
        
        Returns:
            List[Dict[str, Any]]: Lista de dicionários contendo informações sobre os datasets.
                Cada dicionário deve conter pelo menos as chaves 'id' e 'name'.
        """
        pass
    
    @abc.abstractmethod
    async def fetch(self, query: Dict[str, Any]) -> Any:
        """
        Busca dados da fonte de acordo com os parâmetros de consulta.
        
        Args:
            query (Dict[str, Any]): Parâmetros de consulta específicos para a fonte de dados.
                Os parâmetros variam de acordo com o conector.
        
        Returns:
            Any: Dados brutos retornados pela fonte, que serão normalizados pelo método normalize().
        """
        pass
    
    @abc.abstractmethod
    async def normalize(self, data: Any) -> pd.DataFrame:
        """
        Normaliza os dados brutos retornados pelo método fetch() em um DataFrame pandas.
        
        Args:
            data (Any): Dados brutos retornados pelo método fetch().
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados normalizados.
        """
        pass
    
    @abc.abstractmethod
    def schema(self) -> Dict[str, Any]:
        """
        Retorna o schema do conector, incluindo metadados e informações sobre os parâmetros aceitos.
        
        Returns:
            Dict[str, Any]: Dicionário contendo informações sobre o conector.
                Deve incluir pelo menos as chaves 'name' e 'description'.
        """
        pass
    
    async def get_data(self, query: Dict[str, Any]) -> pd.DataFrame:
        """
        Método de conveniência que combina fetch() e normalize() em uma única operação.
        
        Args:
            query (Dict[str, Any]): Parâmetros de consulta específicos para a fonte de dados.
        
        Returns:
            pd.DataFrame: DataFrame pandas contendo os dados normalizados.
        """
        data = await self.fetch(query)
        return await self.normalize(data)
