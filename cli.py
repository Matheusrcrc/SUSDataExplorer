#!/usr/bin/env python3
"""
CLI do SUS Data Explorer.

Este módulo implementa a interface de linha de comando (CLI) do SUS Data Explorer,
permitindo acessar dados do SUS de diferentes fontes através do terminal.
"""

import os
import sys
import asyncio
import typer
import pandas as pd
from typing import Optional, List, Dict, Any
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

# Inicializa a aplicação Typer
app = typer.Typer(
    help="SUS Data Explorer CLI - Ferramenta para acessar dados oficiais do SUS"
)

@app.command()
def list_sources():
    """
    Lista todas as fontes de dados disponíveis.
    """
    typer.echo("Fontes de dados disponíveis:")
    typer.echo("---------------------------")
    typer.echo("1. CKAN OpenDataSUS - Datasets em CSV/Parquet via API CKAN")
    typer.echo("2. DEMAS - Dados do Departamento de Monitoramento e Avaliação do SUS")
    typer.echo("3. DATASUS TABNET - Dados do DATASUS TABNET via PySUS")
    typer.echo("4. e-Gestor AB - Dados da Atenção Básica via e-Gestor AB")
    typer.echo("\nUse 'sus-explorer list-datasets [fonte]' para listar os datasets disponíveis em uma fonte específica.")

@app.command()
def list_datasets(source: Optional[str] = typer.Argument(None, help="Fonte de dados (ckan, demas, tabnet, egestor)")):
    """
    Lista os datasets disponíveis em uma fonte específica ou em todas as fontes.
    
    Args:
        source: Fonte de dados (ckan, demas, tabnet, egestor). Se não for fornecida, lista datasets de todas as fontes.
    """
    if source and source not in ["ckan", "demas", "tabnet", "egestor"]:
        typer.echo(f"Erro: Fonte '{source}' não encontrada.")
        typer.echo("Fontes disponíveis: ckan, demas, tabnet, egestor")
        return
    
    datasets = []
    
    try:
        if not source or source == "ckan":
            typer.echo("\nDatasets do CKAN OpenDataSUS:")
            typer.echo("---------------------------")
            ckan_datasets = asyncio.run(ckan_connector.list_datasets())
            for dataset in ckan_datasets:
                typer.echo(f"- {dataset.get('name', 'N/A')} (ID: {dataset.get('id', 'N/A')})")
                datasets.extend(ckan_datasets)
        
        if not source or source == "demas":
            typer.echo("\nDatasets do DEMAS:")
            typer.echo("---------------------------")
            demas_datasets = asyncio.run(demas_connector.list_datasets())
            for dataset in demas_datasets:
                typer.echo(f"- {dataset.get('name', 'N/A')} (ID: {dataset.get('id', 'N/A')})")
                datasets.extend(demas_datasets)
        
        if not source or source == "tabnet":
            typer.echo("\nDatasets do DATASUS TABNET:")
            typer.echo("---------------------------")
            tabnet_datasets = asyncio.run(tabnet_connector.list_datasets())
            for dataset in tabnet_datasets:
                typer.echo(f"- {dataset.get('name', 'N/A')} (ID: {dataset.get('id', 'N/A')})")
                datasets.extend(tabnet_datasets)
        
        if not source or source == "egestor":
            typer.echo("\nDatasets do e-Gestor AB:")
            typer.echo("---------------------------")
            egestor_datasets = asyncio.run(egestor_connector.list_datasets())
            for dataset in egestor_datasets:
                typer.echo(f"- {dataset.get('name', 'N/A')} (ID: {dataset.get('id', 'N/A')})")
                datasets.extend(egestor_datasets)
    
    except Exception as e:
        typer.echo(f"Erro ao listar datasets: {e}")
        return
    
    return datasets

@app.command()
def pull_data(
    source: str = typer.Argument(..., help="Fonte de dados (ckan, demas, tabnet, egestor)"),
    dataset: str = typer.Argument(..., help="ID do dataset"),
    region: str = typer.Argument(..., help="Código IBGE da região ou município"),
    years: str = typer.Argument(..., help="Anos dos dados (formato: YYYY ou YYYY:YYYY)"),
    output: str = typer.Argument(..., help="Caminho do arquivo de saída (CSV, JSON, Parquet)")
):
    """
    Obtém dados de um dataset específico e salva em um arquivo.
    
    Args:
        source: Fonte de dados (ckan, demas, tabnet, egestor).
        dataset: ID do dataset.
        region: Código IBGE da região ou município.
        years: Anos dos dados (formato: YYYY ou YYYY:YYYY).
        output: Caminho do arquivo de saída (CSV, JSON, Parquet).
    """
    if source not in ["ckan", "demas", "tabnet", "egestor"]:
        typer.echo(f"Erro: Fonte '{source}' não encontrada.")
        typer.echo("Fontes disponíveis: ckan, demas, tabnet, egestor")
        return
    
    # Processa o parâmetro de anos
    if ":" in years:
        start_year, end_year = map(int, years.split(":"))
        years_list = list(range(start_year, end_year + 1))
    else:
        years_list = [int(years)]
    
    try:
        # Seleciona o conector apropriado
        connector = None
        if source == "ckan":
            connector = ckan_connector
        elif source == "demas":
            connector = demas_connector
        elif source == "tabnet":
            connector = tabnet_connector
        elif source == "egestor":
            connector = egestor_connector
        
        # Prepara a consulta
        all_data = []
        for year in years_list:
            typer.echo(f"Obtendo dados para o ano {year}...")
            
            # Adapta a consulta para o formato específico do conector
            if source == "ckan":
                query = {
                    "dataset_id": dataset,
                    "filters": {"ano": year, "regiao": region}
                }
            elif source == "demas":
                query = {
                    "dataset": dataset,
                    "filters": {"uf": region[:2], "municipio": region},
                    "year": year
                }
            elif source == "tabnet":
                query = {
                    "system": dataset,
                    "state": region[:2],
                    "year": year
                }
            elif source == "egestor":
                query = {
                    "report": dataset,
                    "state": region[:2],
                    "year": year,
                    "municipality": region
                }
            
            # Obtém os dados
            data = asyncio.run(connector.get_data(query))
            
            # Adiciona à lista de dados
            if isinstance(data, pd.DataFrame):
                all_data.append(data)
            else:
                all_data.append(pd.DataFrame(data))
        
        # Combina os dados de todos os anos
        if all_data:
            combined_data = pd.concat(all_data, ignore_index=True)
            
            # Salva os dados no formato especificado
            output_format = os.path.splitext(output)[1].lower()
            if output_format == ".csv":
                combined_data.to_csv(output, index=False)
            elif output_format == ".json":
                combined_data.to_json(output, orient="records")
            elif output_format == ".parquet":
                combined_data.to_parquet(output, index=False)
            else:
                typer.echo(f"Erro: Formato de saída '{output_format}' não suportado.")
                typer.echo("Formatos suportados: .csv, .json, .parquet")
                return
            
            typer.echo(f"Dados salvos com sucesso em {output}")
            typer.echo(f"Total de registros: {len(combined_data)}")
        else:
            typer.echo("Nenhum dado encontrado para os parâmetros especificados.")
    
    except Exception as e:
        typer.echo(f"Erro ao obter dados: {e}")
        return

@app.command()
def info():
    """
    Exibe informações sobre o SUS Data Explorer.
    """
    typer.echo("SUS Data Explorer - Versão 1.0.0")
    typer.echo("----------------------------------")
    typer.echo("Sistema AI first, mobile first, community first para buscar,")
    typer.echo("unificar e servir dados oficiais do SUS.")
    typer.echo("\nFontes de dados suportadas:")
    typer.echo("- CKAN OpenDataSUS")
    typer.echo("- DEMAS")
    typer.echo("- DATASUS TABNET")
    typer.echo("- e-Gestor AB")
    typer.echo("\nPara mais informações, visite: https://github.com/sus-data-explorer")

if __name__ == "__main__":
    app()
