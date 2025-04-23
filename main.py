"""
API principal do SUS Data Explorer.

Este módulo implementa a API FastAPI do SUS Data Explorer, fornecendo endpoints
para acessar dados do SUS de diferentes fontes.
"""

import os
import asyncio
from typing import Dict, List, Any, Optional, Union
from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import logging

# Importa os conectores
from connectors import CkanConnector, DemasConnector, TabnetConnector, EGestorConnector

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Inicializa os conectores
ckan_connector = CkanConnector()
demas_connector = DemasConnector()
tabnet_connector = TabnetConnector()
egestor_connector = EGestorConnector()

# Inicializa a aplicação FastAPI
app = FastAPI(
    title="SUS Data Explorer API",
    description="API para acessar dados oficiais do SUS de diferentes fontes",
    version="1.0.0"
)

# Configuração de CORS para permitir acesso de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos de dados
class Source(BaseModel):
    """
    Modelo para representar uma fonte de dados.
    
    Attributes:
        id (str): Identificador único da fonte.
        name (str): Nome da fonte.
        description (str): Descrição da fonte.
    """
    id: str
    name: str
    description: str

class Dataset(BaseModel):
    """
    Modelo para representar um dataset.
    
    Attributes:
        id (str): Identificador único do dataset.
        name (str): Nome do dataset.
        description (str): Descrição do dataset.
        source (str): Fonte de dados do dataset.
    """
    id: str
    name: str
    description: str
    source: str

class IndicatorResponse(BaseModel):
    """
    Modelo para representar a resposta de um indicador.
    
    Attributes:
        data (List[Dict[str, Any]]): Dados do indicador.
        metadata (Dict[str, Any]): Metadados do indicador.
    """
    data: List[Dict[str, Any]]
    metadata: Dict[str, Any]

class ExportResponse(BaseModel):
    """
    Modelo para representar a resposta de uma exportação.
    
    Attributes:
        url (str): URL para download do arquivo exportado.
        format (str): Formato do arquivo exportado.
    """
    url: str
    format: str

# Endpoints da API
@app.get("/")
async def read_root():
    """
    Endpoint raiz da API.
    
    Returns:
        Dict[str, str]: Informações básicas sobre a API.
    """
    return {
        "title": "SUS Data Explorer API",
        "version": "1.0.0",
        "description": "API para acessar dados oficiais do SUS de diferentes fontes"
    }

@app.get("/sources", response_model=Dict[str, List[Source]])
async def get_sources():
    """
    Lista todas as fontes de dados disponíveis.
    
    Returns:
        Dict[str, List[Source]]: Lista de fontes de dados.
    """
    sources = [
        {
            "id": "ckan",
            "name": "CKAN OpenDataSUS",
            "description": "Datasets em CSV/Parquet via API CKAN"
        },
        {
            "id": "demas",
            "name": "DEMAS",
            "description": "Dados do Departamento de Monitoramento e Avaliação do SUS"
        },
        {
            "id": "tabnet",
            "name": "DATASUS TABNET",
            "description": "Dados do DATASUS TABNET via PySUS"
        },
        {
            "id": "egestor",
            "name": "e-Gestor AB",
            "description": "Dados da Atenção Básica via e-Gestor AB"
        }
    ]
    
    return {"sources": sources}

@app.get("/datasets", response_model=Dict[str, List[Dataset]])
async def get_datasets():
    """
    Lista todos os datasets disponíveis em todas as fontes.
    
    Returns:
        Dict[str, List[Dataset]]: Lista de datasets.
    """
    datasets = []
    
    # Obtém datasets do CKAN
    try:
        ckan_datasets = await ckan_connector.list_datasets()
        for dataset in ckan_datasets:
            datasets.append({
                "id": dataset.get("id", ""),
                "name": dataset.get("name", ""),
                "description": dataset.get("description", ""),
                "source": "ckan"
            })
    except Exception as e:
        logger.error(f"Error getting CKAN datasets: {e}")
    
    # Obtém datasets do DEMAS
    try:
        demas_datasets = await demas_connector.list_datasets()
        for dataset in demas_datasets:
            datasets.append({
                "id": dataset.get("id", ""),
                "name": dataset.get("name", ""),
                "description": dataset.get("description", ""),
                "source": "demas"
            })
    except Exception as e:
        logger.error(f"Error getting DEMAS datasets: {e}")
    
    # Obtém datasets do TABNET
    try:
        tabnet_datasets = await tabnet_connector.list_datasets()
        for dataset in tabnet_datasets:
            datasets.append({
                "id": dataset.get("id", ""),
                "name": dataset.get("name", ""),
                "description": dataset.get("description", ""),
                "source": "tabnet"
            })
    except Exception as e:
        logger.error(f"Error getting TABNET datasets: {e}")
    
    # Obtém datasets do e-Gestor AB
    try:
        egestor_datasets = await egestor_connector.list_datasets()
        for dataset in egestor_datasets:
            datasets.append({
                "id": dataset.get("id", ""),
                "name": dataset.get("name", ""),
                "description": dataset.get("description", ""),
                "source": "egestor"
            })
    except Exception as e:
        logger.error(f"Error getting e-Gestor AB datasets: {e}")
    
    return {"datasets": datasets}

@app.get("/datasets/{source}", response_model=Dict[str, List[Dataset]])
async def get_datasets_by_source(source: str):
    """
    Lista os datasets disponíveis em uma fonte específica.
    
    Args:
        source (str): Fonte de dados (ckan, demas, tabnet, egestor).
    
    Returns:
        Dict[str, List[Dataset]]: Lista de datasets da fonte especificada.
    
    Raises:
        HTTPException: Se a fonte não for encontrada.
    """
    if source not in ["ckan", "demas", "tabnet", "egestor"]:
        raise HTTPException(status_code=404, detail=f"Source '{source}' not found")
    
    datasets = []
    
    try:
        if source == "ckan":
            source_datasets = await ckan_connector.list_datasets()
        elif source == "demas":
            source_datasets = await demas_connector.list_datasets()
        elif source == "tabnet":
            source_datasets = await tabnet_connector.list_datasets()
        elif source == "egestor":
            source_datasets = await egestor_connector.list_datasets()
        
        for dataset in source_datasets:
            datasets.append({
                "id": dataset.get("id", ""),
                "name": dataset.get("name", ""),
                "description": dataset.get("description", ""),
                "source": source
            })
    
    except Exception as e:
        logger.error(f"Error getting datasets from {source}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting datasets: {str(e)}")
    
    return {"datasets": datasets}

@app.get("/indicators/{code}", response_model=IndicatorResponse)
async def get_indicator(
    code: str,
    region: str = Query(..., description="Código IBGE da região ou município"),
    start_year: int = Query(..., description="Ano inicial"),
    end_year: Optional[int] = Query(None, description="Ano final (opcional)"),
    source: Optional[str] = Query(None, description="Fonte de dados (opcional)")
):
    """
    Obtém dados de um indicador específico.
    
    Args:
        code (str): Código do indicador.
        region (str): Código IBGE da região ou município.
        start_year (int): Ano inicial.
        end_year (Optional[int], optional): Ano final. Se não for fornecido, apenas o ano inicial será considerado.
        source (Optional[str], optional): Fonte de dados. Se não for fornecida, será usada a fonte padrão do indicador.
    
    Returns:
        IndicatorResponse: Dados do indicador e metadados.
    
    Raises:
        HTTPException: Se ocorrer um erro ao obter os dados.
    """
    try:
        # Determina a fonte de dados a ser usada
        connector = None
        if source == "ckan":
            connector = ckan_connector
        elif source == "demas":
            connector = demas_connector
        elif source == "tabnet":
            connector = tabnet_connector
        elif source == "egestor":
            connector = egestor_connector
        else:
            # Se a fonte não for especificada, usa a fonte padrão do indicador
            if code in ["mortalidade", "nascimentos", "doencas"]:
                connector = tabnet_connector
            elif code in ["leitos", "estabelecimentos"]:
                connector = demas_connector
            elif code in ["cobertura_ab", "indicadores_ab"]:
                connector = egestor_connector
            else:
                connector = ckan_connector
        
        # Prepara a consulta
        query = {
            "indicator": code,
            "region": region,
            "start_year": start_year
        }
        
        if end_year:
            query["end_year"] = end_year
        
        # Adapta a consulta para o formato específico do conector
        if connector == tabnet_connector:
            system = "sim" if code == "mortalidade" else "sinasc" if code == "nascimentos" else "sinan"
            query = {
                "system": system,
                "state": region[:2],  # Primeiros 2 dígitos do código IBGE representam o estado
                "year": start_year
            }
        elif connector == demas_connector:
            dataset = "leitos" if code == "leitos" else "estabelecimentos"
            query = {
                "dataset": dataset,
                "filters": {"uf": region[:2], "municipio": region},
                "year": start_year
            }
        elif connector == egestor_connector:
            report = "cobertura" if code == "cobertura_ab" else "indicadores"
            query = {
                "report": report,
                "state": region[:2],
                "year": start_year,
                "municipality": region
            }
        
        # Obtém os dados
        data = await connector.get_data(query)
        
        # Converte o DataFrame para lista de dicionários
        if isinstance(data, pd.DataFrame):
            data_list = data.to_dict(orient="records")
        else:
            data_list = data
        
        # Prepara os metadados
        metadata = {
            "indicator": code,
            "region": region,
            "start_year": start_year,
            "end_year": end_year,
            "source": source or "auto",
            "count": len(data_list)
        }
        
        return {
            "data": data_list,
            "metadata": metadata
        }
    
    except Exception as e:
        logger.error(f"Error getting indicator {code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting indicator: {str(e)}")

@app.get("/exports", response_model=ExportResponse)
async def export_data(
    indicator: str = Query(..., description="Código do indicador"),
    region: str = Query(..., description="Código IBGE da região ou município"),
    start_year: int = Query(..., description="Ano inicial"),
    end_year: Optional[int] = Query(None, description="Ano final (opcional)"),
    format: str = Query("csv", description="Formato de exportação (csv, json, parquet)"),
    source: Optional[str] = Query(None, description="Fonte de dados (opcional)")
):
    """
    Exporta dados de um indicador para um formato específico.
    
    Args:
        indicator (str): Código do indicador.
        region (str): Código IBGE da região ou município.
        start_year (int): Ano inicial.
        end_year (Optional[int], optional): Ano final. Se não for fornecido, apenas o ano inicial será considerado.
        format (str, optional): Formato de exportação. Padrão: "csv".
        source (Optional[str], optional): Fonte de dados. Se não for fornecida, será usada a fonte padrão do indicador.
    
    Returns:
        ExportResponse: URL para download do arquivo exportado e formato.
    
    Raises:
        HTTPException: Se ocorrer um erro ao exportar os dados.
    """
    try:
        # Obtém os dados do indicador
        indicator_data = await get_indicator(
            indicator,
            region=region,
            start_year=start_year,
            end_year=end_year,
            source=source
        )
        
        # Converte para DataFrame
        df = pd.DataFrame(indicator_data["data"])
        
        # Gera um nome de arquivo único
        filename = f"{indicator}_{region}_{start_year}"
        if end_year:
            filename += f"_{end_year}"
        
        # Diretório para armazenar os arquivos exportados
        export_dir = os.path.join(os.getcwd(), "exports")
        os.makedirs(export_dir, exist_ok=True)
        
        # Exporta para o formato especificado
        file_path = ""
        if format.lower() == "csv":
            file_path = os.path.join(export_dir, f"{filename}.csv")
            df.to_csv(file_path, index=False)
        elif format.lower() == "json":
            file_path = os.path.join(export_dir, f"{filename}.json")
            df.to_json(file_path, orient="records")
        elif format.lower() == "parquet":
            file_path = os.path.join(export_dir, f"{filename}.parquet")
            df.to_parquet(file_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        # Gera uma URL para download
        # Em um ambiente de produção, isso seria uma URL real
        download_url = f"/download/{os.path.basename(file_path)}"
        
        return {
            "url": download_url,
            "format": format.lower()
        }
    
    except Exception as e:
        logger.error(f"Error exporting data: {e}")
        raise HTTPException(status_code=500, detail=f"Error exporting data: {str(e)}")

# Execução da aplicação
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
