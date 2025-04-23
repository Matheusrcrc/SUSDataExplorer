"""
Módulo de inicialização para os conectores de dados do SUS.

Este módulo exporta todos os conectores implementados para facilitar a importação.
"""

from connectors.base import DataConnector
from connectors.ckan import CkanConnector
from connectors.demas import DemasConnector
from connectors.egestor import EGestorConnector
from connectors.tabnet import TabnetConnector

__all__ = [
    "DataConnector",
    "CkanConnector",
    "DemasConnector",
    "TabnetConnector",
    "EGestorConnector"
]
