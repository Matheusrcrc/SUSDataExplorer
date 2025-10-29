"""
Módulo de inicialização para os conectores de dados do SUS.

Este módulo exporta todos os conectores implementados para facilitar a importação.
"""

from base import DataConnector
from ckan import CkanConnector
from demas import DemasConnector
from egestor import EGestorConnector
from tabnet import TabnetConnector

__all__ = [
    "DataConnector",
    "CkanConnector",
    "DemasConnector",
    "TabnetConnector",
    "EGestorConnector"
]
