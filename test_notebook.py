import pytest
import pandas as pd
import numpy as np
from unittest.mock import patch, MagicMock, AsyncMock

# Testes para o notebook iam_bahia.ipynb
# Como o notebook é um arquivo .ipynb, testamos as funções principais que seriam extraídas dele

class TestIAMBahiaNotebook:
    @pytest.fixture
    def mock_connectors(self):
        with patch("connectors.CkanConnector") as mock_ckan, \
             patch("connectors.DemasConnector") as mock_demas, \
             patch("connectors.TabnetConnector") as mock_tabnet, \
             patch("connectors.EGestorConnector") as mock_egestor:
            
            # Configurar mocks para os conectores
            mock_ckan_instance = MagicMock()
            mock_ckan_instance.fetch = AsyncMock()
            mock_ckan_instance.normalize = AsyncMock()
            mock_ckan.return_value = mock_ckan_instance
            
            mock_demas_instance = MagicMock()
            mock_demas_instance.fetch = AsyncMock()
            mock_demas_instance.normalize = AsyncMock()
            mock_demas.return_value = mock_demas_instance
            
            mock_tabnet_instance = MagicMock()
            mock_tabnet_instance.fetch = AsyncMock()
            mock_tabnet_instance.normalize = AsyncMock()
            mock_tabnet.return_value = mock_tabnet_instance
            
            mock_egestor_instance = MagicMock()
            mock_egestor_instance.fetch = AsyncMock()
            mock_egestor_instance.normalize = AsyncMock()
            mock_egestor.return_value = mock_egestor_instance
            
            yield {
                "ckan": mock_ckan_instance,
                "demas": mock_demas_instance,
                "tabnet": mock_tabnet_instance,
                "egestor": mock_egestor_instance
            }
    
    def test_processar_indicadores_estrutura(self):
        # Arrange
        df_estabelecimentos = pd.DataFrame({
            'tipo_unidade': ['HOSPITAL DE URGENCIA', 'POSTO DE SAUDE', 'PRONTO SOCORRO'],
            'regiao_saude': ['290001', '290001', '290002'],
            'ano': [2020, 2020, 2020]
        })
        
        df_leitos = pd.DataFrame({
            'tipo_leito': ['UTI ADULTO', 'CLINICO', 'UTI PEDIATRICA'],
            'regiao_saude': ['290001', '290001', '290002'],
            'ano': [2020, 2020, 2020],
            'quantidade': [10, 20, 15]
        })
        
        # Função a ser testada (extraída do notebook)
        def processar_indicadores_estrutura():
            # Filtra estabelecimentos de urgência e emergência
            df_urgencia = df_estabelecimentos[
                df_estabelecimentos['tipo_unidade'].str.contains('URGENCIA|EMERGENCIA|PRONTO|SOCORRO', 
                                                                case=False, na=False)
            ].copy()
            
            # Filtra leitos de UTI
            df_uti = df_leitos[
                df_leitos['tipo_leito'].str.contains('UTI|INTENSIV', case=False, na=False)
            ].copy()
            
            # Agrega dados por região de saúde e ano
            indicadores_estrutura = []
            
            regioes_saude = {
                '290001': 'Região 1',
                '290002': 'Região 2'
            }
            
            for codigo, nome in regioes_saude.items():
                for ano in [2020]:
                    # Filtra por região e ano
                    estab_regiao_ano = df_urgencia[
                        (df_urgencia['regiao_saude'] == codigo) & 
                        (df_urgencia['ano'] == ano)
                    ]
                    
                    leitos_regiao_ano = df_uti[
                        (df_uti['regiao_saude'] == codigo) & 
                        (df_uti['ano'] == ano)
                    ]
                    
                    # Calcula indicadores
                    n_estabelecimentos = len(estab_regiao_ano)
                    n_leitos_uti = leitos_regiao_ano['quantidade'].sum() if 'quantidade' in leitos_regiao_ano.columns else 0
                    
                    indicadores_estrutura.append({
                        'codigo_regiao': codigo,
                        'nome_regiao': nome,
                        'ano': ano,
                        'estabelecimentos_urgencia': n_estabelecimentos,
                        'leitos_uti': n_leitos_uti
                    })
            
            return pd.DataFrame(indicadores_estrutura)
        
        # Act
        result = processar_indicadores_estrutura()
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # Uma linha para cada região
        assert 'estabelecimentos_urgencia' in result.columns
        assert 'leitos_uti' in result.columns
        assert result.loc[result['codigo_regiao'] == '290001', 'estabelecimentos_urgencia'].values[0] == 2
        assert result.loc[result['codigo_regiao'] == '290001', 'leitos_uti'].values[0] == 10
    
    def test_processar_indicadores_resultado(self):
        # Arrange
        df_mortalidade = pd.DataFrame({
            'regiao_saude': ['290001', '290001', '290002'],
            'ano': [2020, 2020, 2020],
            'causa': ['I21', 'I64', 'V01']  # IAM, AVC, Trauma
        })
        
        df_internacoes = pd.DataFrame({
            'regiao_saude': ['290001', '290001', '290002'],
            'ano': [2020, 2020, 2020],
            'procedimento': ['0303010010', '0303010029', '0303010037']  # Códigos fictícios
        })
        
        # Função a ser testada (extraída do notebook)
        def processar_indicadores_resultado():
            # Implementação simulada para calcular indicadores de resultado
            indicadores_resultado = []
            
            regioes_saude = {
                '290001': 'Região 1',
                '290002': 'Região 2'
            }
            
            for codigo, nome in regioes_saude.items():
                for ano in [2020]:
                    # Filtra dados de mortalidade por região e ano
                    mortalidade_regiao_ano = df_mortalidade[
                        (df_mortalidade['regiao_saude'] == codigo) & 
                        (df_mortalidade['ano'] == ano)
                    ]
                    
                    internacoes_regiao_ano = df_internacoes[
                        (df_internacoes['regiao_saude'] == codigo) & 
                        (df_internacoes['ano'] == ano)
                    ]
                    
                    # Calcula indicadores (simplificado para o teste)
                    mortalidade_iam = len(mortalidade_regiao_ano[mortalidade_regiao_ano['causa'] == 'I21'])
                    mortalidade_avc = len(mortalidade_regiao_ano[mortalidade_regiao_ano['causa'] == 'I64'])
                    mortalidade_trauma = len(mortalidade_regiao_ano[mortalidade_regiao_ano['causa'] == 'V01'])
                    
                    internacoes_evitaveis = len(internacoes_regiao_ano)
                    
                    indicadores_resultado.append({
                        'codigo_regiao': codigo,
                        'nome_regiao': nome,
                        'ano': ano,
                        'mortalidade_iam': mortalidade_iam,
                        'mortalidade_avc': mortalidade_avc,
                        'mortalidade_trauma': mortalidade_trauma,
                        'internacoes_evitaveis': internacoes_evitaveis
                    })
            
            return pd.DataFrame(indicadores_resultado)
        
        # Act
        result = processar_indicadores_resultado()
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2  # Uma linha para cada região
        assert 'mortalidade_iam' in result.columns
        assert 'mortalidade_avc' in result.columns
        assert 'mortalidade_trauma' in result.columns
        assert 'internacoes_evitaveis' in result.columns
        assert result.loc[result['codigo_regiao'] == '290001', 'mortalidade_iam'].values[0] == 1
        assert result.loc[result['codigo_regiao'] == '290001', 'mortalidade_avc'].values[0] == 1
    
    def test_analisar_correlacoes(self):
        # Arrange
        df_estrutura = pd.DataFrame({
            'codigo_regiao': ['290001', '290002'],
            'nome_regiao': ['Região 1', 'Região 2'],
            'ano': [2020, 2020],
            'estabelecimentos_urgencia': [10, 5],
            'leitos_uti': [20, 10],
            'cobertura_samu': [0.8, 0.6]
        })
        
        df_processo = pd.DataFrame({
            'codigo_regiao': ['290001', '290002'],
            'nome_regiao': ['Região 1', 'Região 2'],
            'ano': [2020, 2020],
            'tempo_resposta': [15, 25],
            'taxa_regulacao': [0.9, 0.7]
        })
        
        df_resultado = pd.DataFrame({
            'codigo_regiao': ['290001', '290002'],
            'nome_regiao': ['Região 1', 'Região 2'],
            'ano': [2020, 2020],
            'mortalidade_iam': [8, 12],
            'mortalidade_avc': [15, 20],
            'internacoes_evitaveis': [150, 200]
        })
        
        # Função a ser testada (extraída do notebook)
        def analisar_correlacoes(df_estrutura, df_processo, df_resultado, ano=2020):
            # Filtra os dados para o ano especificado
            df_estrutura_ano = df_estrutura[df_estrutura['ano'] == ano].copy()
            df_processo_ano = df_processo[df_processo['ano'] == ano].copy()
            df_resultado_ano = df_resultado[df_resultado['ano'] == ano].copy()
            
            # Mescla os dataframes
            df_merged = pd.merge(df_estrutura_ano, df_processo_ano, on=['codigo_regiao', 'nome_regiao', 'ano'])
            df_merged = pd.merge(df_merged, df_resultado_ano, on=['codigo_regiao', 'nome_regiao', 'ano'])
            
            # Seleciona colunas para análise de correlação
            colunas_correlacao = [
                'estabelecimentos_urgencia', 'leitos_uti', 'cobertura_samu',
                'tempo_resposta', 'taxa_regulacao',
                'mortalidade_iam', 'mortalidade_avc', 'internacoes_evitaveis'
            ]
            
            # Calcula a matriz de correlação
            corr_matrix = df_merged[colunas_correlacao].corr()
            
            return corr_matrix
        
        # Act
        result = analisar_correlacoes(df_estrutura, df_processo, df_resultado)
        
        # Assert
        assert isinstance(result, pd.DataFrame)
        assert result.shape == (8, 8)  # Matriz 8x8 para as 8 colunas
        assert 'estabelecimentos_urgencia' in result.columns
        assert 'mortalidade_iam' in result.columns
        # Verificar correlação negativa entre leitos_uti e mortalidade_iam
        assert result.loc['leitos_uti', 'mortalidade_iam'] < 0
    
    def test_analisar_disparidades_regionais(self):
        # Arrange
        df_estrutura = pd.DataFrame({
            'codigo_regiao': ['290001', '290002'],
            'nome_regiao': ['Região 1', 'Região 2'],
            'ano': [2020, 2020],
            'leitos_uti': [20, 10]
        })
        
        df_resultado = pd.DataFrame({
            'codigo_regiao': ['290001', '290002'],
            'nome_regiao': ['Região 1', 'Região 2'],
            'ano': [2020, 2020],
            'mortalidade_iam': [8, 12]
        })
        
        # Função a ser testada (extraída do notebook)
        def analisar_disparidades_regionais(df_estrutura, df_resultado, indicador_estrutura, indicador_resultado, ano=2020):
            # Filtra os dados para o ano especificado
            df_estrutura_ano = df_estrutura[df_estrutura['ano'] == ano].copy()
            df_resultado_ano = df_resultado[df_resultado['ano'] == ano].copy()
            
            # Mescla os dataframes
            df_merged = pd.merge(df_estrutura_ano, df_resultado_ano, on=['codigo_regiao', 'nome_regiao', 'ano'])
            
            # Calcula o coeficiente de correlação
            corr = df_merged[[indicador_estrutura, indicador_resultado]].corr().iloc[0, 1]
            
            return {
                'correlacao': corr,
                'dados': df_merged
            }
        
        # Act
        result = analisar_disparidades_regionais(df_estrutura, df_resultado, 'leitos_uti', 'mortalidade_iam')
        
        # Assert
        assert isinstance(result, dict)
        assert 'correlacao' in result
        assert 'dados' in result
        assert isinstance(result['correlacao'], float)
        assert isinstance(result['dados'], pd.DataFrame)
        assert result['correlacao'] < 0  # Correlação negativa entre leitos_uti e mortalidade_iam
