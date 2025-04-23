import pytest
import os
import sys
from unittest.mock import patch, MagicMock
from pytest_cov.embed import cleanup_on_sigterm

# Configuração para cobertura de testes
cleanup_on_sigterm()

# Adiciona o diretório raiz ao path para importar os módulos do projeto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Configuração para os testes
def pytest_configure(config):
    """
    Configuração do pytest para o projeto SUS Data Explorer.
    """
    config.addinivalue_line(
        "markers", "slow: marca testes que são lentos para execução"
    )
    config.addinivalue_line(
        "markers", "integration: marca testes de integração que requerem recursos externos"
    )
    config.addinivalue_line(
        "markers", "api: marca testes que testam a API"
    )
    config.addinivalue_line(
        "markers", "connectors: marca testes que testam os conectores"
    )
    config.addinivalue_line(
        "markers", "notebook: marca testes que testam os notebooks"
    )

# Fixtures compartilhadas
@pytest.fixture
def sample_dataframe():
    """
    Fixture que retorna um DataFrame de exemplo para testes.
    """
    import pandas as pd
    return pd.DataFrame({
        'ano': [2020, 2021, 2022],
        'regiao': ['290001', '290001', '290001'],
        'valor': [10, 15, 20],
        'indicador': ['mortalidade', 'mortalidade', 'mortalidade']
    })

@pytest.fixture
def mock_http_client():
    """
    Fixture que retorna um cliente HTTP mockado para testes.
    """
    with patch('httpx.AsyncClient') as mock_client:
        yield mock_client
