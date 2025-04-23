import pytest
import json
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from api.main import app
from connectors.base import DataConnector

client = TestClient(app)

# Testes para os endpoints da API
class TestAPI:
    @pytest.fixture
    def mock_connectors(self):
        with patch("api.main.ckan_connector") as mock_ckan, \
             patch("api.main.demas_connector") as mock_demas, \
             patch("api.main.tabnet_connector") as mock_tabnet, \
             patch("api.main.egestor_connector") as mock_egestor:
            
            # Configurar mocks para os conectores
            mock_ckan.list_datasets = AsyncMock(return_value=[
                {"id": "dataset1", "name": "Dataset 1"}
            ])
            mock_ckan.get_data = AsyncMock(return_value=MagicMock())
            
            mock_demas.list_datasets = AsyncMock(return_value=[
                {"id": "dataset2", "name": "Dataset 2"}
            ])
            mock_demas.get_data = AsyncMock(return_value=MagicMock())
            
            mock_tabnet.list_datasets = AsyncMock(return_value=[
                {"id": "dataset3", "name": "Dataset 3"}
            ])
            mock_tabnet.get_data = AsyncMock(return_value=MagicMock())
            
            mock_egestor.list_datasets = AsyncMock(return_value=[
                {"id": "dataset4", "name": "Dataset 4"}
            ])
            mock_egestor.get_data = AsyncMock(return_value=MagicMock())
            
            yield {
                "ckan": mock_ckan,
                "demas": mock_demas,
                "tabnet": mock_tabnet,
                "egestor": mock_egestor
            }
    
    def test_read_root(self):
        # Act
        response = client.get("/")
        
        # Assert
        assert response.status_code == 200
        assert "SUS Data Explorer API" in response.json()["title"]
    
    def test_get_sources(self, mock_connectors):
        # Act
        response = client.get("/sources")
        
        # Assert
        assert response.status_code == 200
        assert "sources" in response.json()
        assert len(response.json()["sources"]) == 4  # ckan, demas, tabnet, egestor
    
    def test_get_datasets(self, mock_connectors):
        # Act
        response = client.get("/datasets")
        
        # Assert
        assert response.status_code == 200
        assert "datasets" in response.json()
        assert len(response.json()["datasets"]) == 4  # Um de cada conector
    
    def test_get_datasets_by_source(self, mock_connectors):
        # Act
        response = client.get("/datasets/ckan")
        
        # Assert
        assert response.status_code == 200
        assert "datasets" in response.json()
        assert len(response.json()["datasets"]) == 1
        assert response.json()["datasets"][0]["id"] == "dataset1"
    
    def test_get_indicator(self, mock_connectors):
        # Arrange
        mock_connectors["ckan"].get_data.return_value = [
            {"ano": 2020, "valor": 10},
            {"ano": 2021, "valor": 15}
        ]
        
        # Act
        response = client.get("/indicators/mortalidade?region=290001&start_year=2020&end_year=2021")
        
        # Assert
        assert response.status_code == 200
        assert "data" in response.json()
        assert "metadata" in response.json()
    
    def test_export_data(self, mock_connectors):
        # Arrange
        mock_connectors["ckan"].get_data.return_value = [
            {"ano": 2020, "valor": 10},
            {"ano": 2021, "valor": 15}
        ]
        
        # Act
        response = client.get("/exports?indicator=mortalidade&region=290001&start_year=2020&end_year=2021&format=csv")
        
        # Assert
        assert response.status_code == 200
        assert "url" in response.json()
        assert response.json()["format"] == "csv"

# Testes para a CLI
class TestCLI:
    @pytest.fixture
    def mock_connectors_cli(self):
        with patch("api.cli.ckan_connector") as mock_ckan, \
             patch("api.cli.demas_connector") as mock_demas, \
             patch("api.cli.tabnet_connector") as mock_tabnet, \
             patch("api.cli.egestor_connector") as mock_egestor:
            
            # Configurar mocks para os conectores
            mock_ckan.list_datasets = AsyncMock(return_value=[
                {"id": "dataset1", "name": "Dataset 1"}
            ])
            mock_ckan.get_data = AsyncMock(return_value=[
                {"ano": 2020, "valor": 10},
                {"ano": 2021, "valor": 15}
            ])
            
            mock_demas.list_datasets = AsyncMock(return_value=[
                {"id": "dataset2", "name": "Dataset 2"}
            ])
            mock_demas.get_data = AsyncMock(return_value=[
                {"ano": 2020, "valor": 20},
                {"ano": 2021, "valor": 25}
            ])
            
            mock_tabnet.list_datasets = AsyncMock(return_value=[
                {"id": "dataset3", "name": "Dataset 3"}
            ])
            mock_tabnet.get_data = AsyncMock(return_value=[
                {"ano": 2020, "valor": 30},
                {"ano": 2021, "valor": 35}
            ])
            
            mock_egestor.list_datasets = AsyncMock(return_value=[
                {"id": "dataset4", "name": "Dataset 4"}
            ])
            mock_egestor.get_data = AsyncMock(return_value=[
                {"ano": 2020, "valor": 40},
                {"ano": 2021, "valor": 45}
            ])
            
            yield {
                "ckan": mock_ckan,
                "demas": mock_demas,
                "tabnet": mock_tabnet,
                "egestor": mock_egestor
            }
    
    @patch("api.cli.typer.echo")
    def test_list_sources(self, mock_echo, mock_connectors_cli):
        # Import here to avoid circular imports
        from api.cli import list_sources
        
        # Act
        list_sources()
        
        # Assert
        assert mock_echo.call_count >= 4  # Pelo menos uma chamada para cada fonte
    
    @patch("api.cli.typer.echo")
    @patch("api.cli.asyncio.run")
    def test_list_datasets(self, mock_run, mock_echo, mock_connectors_cli):
        # Import here to avoid circular imports
        from api.cli import list_datasets
        
        # Arrange
        mock_run.return_value = [
            {"id": "dataset1", "name": "Dataset 1"},
            {"id": "dataset2", "name": "Dataset 2"}
        ]
        
        # Act
        list_datasets(None)
        
        # Assert
        assert mock_echo.call_count >= 2  # Pelo menos uma chamada para cada dataset
    
    @patch("api.cli.typer.echo")
    @patch("api.cli.asyncio.run")
    @patch("api.cli.pd.DataFrame.to_csv")
    def test_pull_data(self, mock_to_csv, mock_run, mock_echo, mock_connectors_cli):
        # Import here to avoid circular imports
        from api.cli import pull_data
        
        # Arrange
        mock_run.return_value = [
            {"ano": 2020, "valor": 10},
            {"ano": 2021, "valor": 15}
        ]
        
        # Act
        pull_data("ckan", "dataset1", "290001", "2020:2021", "output.csv")
        
        # Assert
        mock_to_csv.assert_called_once()
        assert mock_echo.call_count >= 1
