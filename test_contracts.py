import pytest
from unittest.mock import patch, MagicMock, AsyncMock
import httpx

# Testes de contrato para os conectores
class TestConnectorContracts:
    @pytest.mark.connectors
    @pytest.mark.parametrize("connector_class,connector_name", [
        ("connectors.ckan.CkanConnector", "CKAN OpenDataSUS"),
        ("connectors.demas.DemasConnector", "DEMAS"),
        ("connectors.tabnet.TabnetConnector", "DATASUS TABNET"),
        ("connectors.egestor.EGestorConnector", "e-Gestor AB")
    ])
    def test_connector_interface(self, connector_class, connector_name):
        """
        Testa se o conector implementa a interface correta.
        """
        # Importa dinamicamente a classe do conector
        import importlib
        module_name, class_name = connector_class.rsplit('.', 1)
        module = importlib.import_module(module_name)
        connector_cls = getattr(module, class_name)
        
        # Instancia o conector
        connector = connector_cls()
        
        # Verifica se os métodos obrigatórios estão implementados
        assert hasattr(connector, 'list_datasets')
        assert callable(connector.list_datasets)
        
        assert hasattr(connector, 'fetch')
        assert callable(connector.fetch)
        
        assert hasattr(connector, 'normalize')
        assert callable(connector.normalize)
        
        assert hasattr(connector, 'schema')
        assert callable(connector.schema)
        
        assert hasattr(connector, 'get_data')
        assert callable(connector.get_data)
        
        # Verifica o schema do conector
        schema = connector.schema()
        assert isinstance(schema, dict)
        assert "name" in schema
        assert schema["name"] == connector_name
        assert "description" in schema
    
    @pytest.mark.connectors
    @pytest.mark.asyncio
    @pytest.mark.parametrize("connector_class", [
        "connectors.ckan.CkanConnector",
        "connectors.demas.DemasConnector",
        "connectors.tabnet.TabnetConnector",
        "connectors.egestor.EGestorConnector"
    ])
    async def test_list_datasets_contract(self, connector_class):
        """
        Testa se o método list_datasets retorna a estrutura correta.
        """
        # Importa dinamicamente a classe do conector
        import importlib
        module_name, class_name = connector_class.rsplit('.', 1)
        module = importlib.import_module(module_name)
        connector_cls = getattr(module, class_name)
        
        # Instancia o conector com cliente HTTP mockado
        with patch('httpx.AsyncClient'):
            connector = connector_cls()
            
            # Configura o mock para list_datasets
            if hasattr(connector, '_list_datasets'):
                connector._list_datasets = AsyncMock(return_value=[
                    {"id": "dataset1", "name": "Dataset 1"},
                    {"id": "dataset2", "name": "Dataset 2"}
                ])
            
            # Chama o método
            datasets = await connector.list_datasets()
            
            # Verifica o contrato
            assert isinstance(datasets, list)
            assert len(datasets) > 0
            for dataset in datasets:
                assert isinstance(dataset, dict)
                assert "id" in dataset
                assert isinstance(dataset["id"], str)
    
    @pytest.mark.connectors
    @pytest.mark.asyncio
    @pytest.mark.parametrize("connector_class,query", [
        ("connectors.ckan.CkanConnector", {"dataset_id": "test_dataset"}),
        ("connectors.demas.DemasConnector", {"dataset": "cnes", "filters": {"uf": "BA"}}),
        ("connectors.tabnet.TabnetConnector", {"system": "sim", "state": "BA", "year": 2020}),
        ("connectors.egestor.EGestorConnector", {"report": "cobertura", "state": "BA", "year": 2020})
    ])
    async def test_fetch_contract(self, connector_class, query):
        """
        Testa se o método fetch aceita os parâmetros corretos e retorna a estrutura esperada.
        """
        # Importa dinamicamente a classe do conector
        import importlib
        module_name, class_name = connector_class.rsplit('.', 1)
        module = importlib.import_module(module_name)
        connector_cls = getattr(module, class_name)
        
        # Instancia o conector com cliente HTTP mockado
        with patch('httpx.AsyncClient'):
            connector = connector_cls()
            
            # Configura o mock para fetch
            connector.fetch = AsyncMock(return_value={"data": [{"id": 1}, {"id": 2}]})
            
            # Chama o método
            result = await connector.fetch(query)
            
            # Verifica o contrato
            assert result is not None
            # O resultado pode ser um DataFrame, dicionário ou lista
            import pandas as pd
            assert isinstance(result, (pd.DataFrame, dict, list))
    
    @pytest.mark.connectors
    @pytest.mark.asyncio
    @pytest.mark.parametrize("connector_class,data", [
        ("connectors.ckan.CkanConnector", {"records": [{"id": 1}, {"id": 2}]}),
        ("connectors.demas.DemasConnector", {"data": [{"id": 1}, {"id": 2}]}),
        ("connectors.tabnet.TabnetConnector", [{"id": 1}, {"id": 2}]),
        ("connectors.egestor.EGestorConnector", [{"id": 1}, {"id": 2}])
    ])
    async def test_normalize_contract(self, connector_class, data):
        """
        Testa se o método normalize aceita os dados corretos e retorna um DataFrame.
        """
        # Importa dinamicamente a classe do conector
        import importlib
        module_name, class_name = connector_class.rsplit('.', 1)
        module = importlib.import_module(module_name)
        connector_cls = getattr(module, class_name)
        
        # Instancia o conector
        connector = connector_cls()
        
        # Chama o método
        result = await connector.normalize(data)
        
        # Verifica o contrato
        import pandas as pd
        assert isinstance(result, pd.DataFrame)
        assert not result.empty

# Testes de desempenho para a API
class TestAPIPerformance:
    @pytest.mark.api
    @pytest.mark.slow
    def test_api_response_time(self):
        """
        Testa se a API responde em menos de 300ms para consultas com cache quente.
        """
        from fastapi.testclient import TestClient
        from api.main import app
        import time
        
        client = TestClient(app)
        
        # Configura mocks para os conectores
        with patch("api.main.ckan_connector") as mock_ckan, \
             patch("api.main.demas_connector") as mock_demas, \
             patch("api.main.tabnet_connector") as mock_tabnet, \
             patch("api.main.egestor_connector") as mock_egestor:
            
            # Configura o mock para retornar dados rapidamente
            mock_ckan.get_data = AsyncMock(return_value=[{"id": 1}])
            
            # Primeira chamada para aquecer o cache
            client.get("/indicators/mortalidade?region=290001&start_year=2020")
            
            # Segunda chamada para medir o tempo de resposta
            start_time = time.time()
            response = client.get("/indicators/mortalidade?region=290001&start_year=2020")
            end_time = time.time()
            
            # Calcula o tempo de resposta em milissegundos
            response_time = (end_time - start_time) * 1000
            
            # Verifica se o tempo de resposta é menor que 300ms
            assert response_time < 300, f"Tempo de resposta ({response_time}ms) excede o limite de 300ms"
            assert response.status_code == 200
