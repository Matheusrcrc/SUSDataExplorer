import pytest
import pandas as pd
from unittest.mock import AsyncMock, patch, MagicMock

from connectors.base import DataConnector
from connectors.ckan import CkanConnector
from connectors.demas import DemasConnector
from connectors.tabnet import TabnetConnector
from connectors.egestor import EGestorConnector

# Testes para a classe base DataConnector
class TestDataConnector:
    class ConcreteConnector(DataConnector):
        async def list_datasets(self):
            return [{"id": "test", "name": "Test Dataset"}]
        
        async def fetch(self, query):
            return pd.DataFrame({"col1": [1, 2, 3]})
        
        async def normalize(self, data):
            return data
        
        def schema(self):
            return {"name": "Test Connector"}
    
    @pytest.mark.asyncio
    async def test_get_data(self):
        # Arrange
        connector = self.ConcreteConnector()
        query = {"param": "value"}
        
        # Mock the fetch and normalize methods
        connector.fetch = AsyncMock(return_value=pd.DataFrame({"col1": [1, 2, 3]}))
        connector.normalize = AsyncMock(return_value=pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]}))
        
        # Act
        result = await connector.get_data(query)
        
        # Assert
        connector.fetch.assert_called_once_with(query)
        connector.normalize.assert_called_once()
        assert isinstance(result, pd.DataFrame)
        assert "col2" in result.columns
        assert len(result) == 3

# Testes para o CkanConnector
class TestCkanConnector:
    @pytest.fixture
    def connector(self):
        with patch("httpx.AsyncClient") as mock_client:
            connector = CkanConnector()
            connector.client = mock_client
            yield connector
    
    @pytest.mark.asyncio
    async def test_list_datasets(self, connector):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["dataset1", "dataset2"]
        }
        mock_response.raise_for_status = MagicMock()
        connector.client.get = AsyncMock(return_value=mock_response)
        
        # Act
        result = await connector.list_datasets()
        
        # Assert
        connector.client.get.assert_called_once()
        assert len(result) == 2
        assert "dataset1" in result
        assert "dataset2" in result
    
    @pytest.mark.asyncio
    async def test_fetch_dataset_info(self, connector):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": {"id": "dataset1", "name": "Dataset 1"}
        }
        mock_response.raise_for_status = MagicMock()
        connector.client.get = AsyncMock(return_value=mock_response)
        
        # Act
        result = await connector.fetch({"dataset_id": "dataset1"})
        
        # Assert
        connector.client.get.assert_called_once()
        assert result["id"] == "dataset1"
        assert result["name"] == "Dataset 1"
    
    @pytest.mark.asyncio
    async def test_fetch_resource_data(self, connector):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "success": True,
            "result": {
                "records": [
                    {"id": 1, "name": "Record 1"},
                    {"id": 2, "name": "Record 2"}
                ]
            }
        }
        mock_response.raise_for_status = MagicMock()
        connector.client.get = AsyncMock(return_value=mock_response)
        
        # Act
        result = await connector.fetch({"dataset_id": "dataset1", "resource_id": "resource1"})
        
        # Assert
        connector.client.get.assert_called_once()
        assert "records" in result
        assert len(result["records"]) == 2
    
    @pytest.mark.asyncio
    async def test_normalize_records(self, connector):
        # Arrange
        data = {
            "records": [
                {"id": 1, "name": "Record 1"},
                {"id": 2, "name": "Record 2"}
            ]
        }
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "id" in result.columns
        assert "name" in result.columns
    
    @pytest.mark.asyncio
    async def test_normalize_list(self, connector):
        # Arrange
        data = [
            {"id": 1, "name": "Record 1"},
            {"id": 2, "name": "Record 2"}
        ]
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "id" in result.columns
        assert "name" in result.columns
    
    def test_schema(self, connector):
        # Act
        schema = connector.schema()
        
        # Assert
        assert "name" in schema
        assert "description" in schema
        assert "endpoints" in schema
        assert "datasets" in schema

# Testes para o DemasConnector
class TestDemasConnector:
    @pytest.fixture
    def connector(self):
        with patch("httpx.AsyncClient") as mock_client:
            connector = DemasConnector()
            connector.client = mock_client
            yield connector
    
    @pytest.mark.asyncio
    async def test_list_datasets(self, connector):
        # Act
        result = await connector.list_datasets()
        
        # Assert
        assert len(result) == 3  # cnes, leitos, estabelecimentos
        assert all("id" in dataset for dataset in result)
        assert all("url" in dataset for dataset in result)
    
    @pytest.mark.asyncio
    async def test_fetch(self, connector):
        # Arrange
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": [{"id": 1}, {"id": 2}]}
        mock_response.raise_for_status = MagicMock()
        connector.client.get = AsyncMock(return_value=mock_response)
        
        # Act
        result = await connector.fetch({"dataset": "cnes", "filters": {"uf": "BA"}})
        
        # Assert
        connector.client.get.assert_called_once()
        assert "data" in result
        assert len(result["data"]) == 2
    
    @pytest.mark.asyncio
    async def test_normalize_data_key(self, connector):
        # Arrange
        data = {"data": [{"id": 1}, {"id": 2}]}
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "id" in result.columns
    
    @pytest.mark.asyncio
    async def test_normalize_records_key(self, connector):
        # Arrange
        data = {"records": [{"id": 1}, {"id": 2}]}
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "id" in result.columns
    
    def test_schema(self, connector):
        # Act
        schema = connector.schema()
        
        # Assert
        assert "name" in schema
        assert "description" in schema
        assert "endpoints" in schema
        assert "parameters" in schema

# Testes para o TabnetConnector
class TestTabnetConnector:
    @pytest.fixture
    def connector(self):
        connector = TabnetConnector()
        yield connector
    
    @pytest.mark.asyncio
    async def test_list_datasets(self, connector):
        # Act
        result = await connector.list_datasets()
        
        # Assert
        assert len(result) == 4  # sim, sinan, sinasc, sih
        assert all("id" in dataset for dataset in result)
        assert all("description" in dataset for dataset in result)
    
    @pytest.mark.asyncio
    @patch("pysus.online_data.SIM.download")
    async def test_fetch_sim(self, mock_download, connector):
        # Arrange
        mock_download.return_value = pd.DataFrame({"id": [1, 2], "causa": ["A00", "B01"]})
        
        # Act
        result = await connector.fetch({"system": "sim", "state": "BA", "year": 2020})
        
        # Assert
        mock_download.assert_called_once_with("BA", 2020, connector.data_dir)
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "causa" in result.columns
    
    @pytest.mark.asyncio
    async def test_normalize(self, connector):
        # Arrange
        data = pd.DataFrame({"id": [1, 2], "idade": ["010", "230"]})
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert "id" in result.columns
        assert "idade" in result.columns
    
    def test_schema(self, connector):
        # Act
        schema = connector.schema()
        
        # Assert
        assert "name" in schema
        assert "description" in schema
        assert "systems" in schema
        assert "parameters" in schema

# Testes para o EGestorConnector
class TestEGestorConnector:
    @pytest.fixture
    def connector(self):
        with patch("httpx.AsyncClient") as mock_client:
            connector = EGestorConnector()
            connector.client = mock_client
            yield connector
    
    @pytest.mark.asyncio
    async def test_list_datasets(self, connector):
        # Act
        result = await connector.list_datasets()
        
        # Assert
        assert len(result) == 4  # cobertura, indicadores, financiamento, equipes
        assert all("id" in dataset for dataset in result)
        assert all("description" in dataset for dataset in result)
    
    @pytest.mark.asyncio
    async def test_fetch_cobertura(self, connector):
        # Act
        result = await connector.fetch({"report": "cobertura", "state": "BA", "year": 2020})
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert "municipio" in result.columns
        assert "cobertura_ab" in result.columns
        assert len(result) > 0
    
    @pytest.mark.asyncio
    async def test_normalize_dataframe(self, connector):
        # Arrange
        data = pd.DataFrame({"municipio": ["Mun1", "Mun2"], "valor": [10, 20]})
        
        # Act
        result = await connector.normalize(data)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert result.equals(data)
    
    def test_schema(self, connector):
        # Act
        schema = connector.schema()
        
        # Assert
        assert "name" in schema
        assert "description" in schema
        assert "reports" in schema
        assert "parameters" in schema
        assert "limitations" in schema
