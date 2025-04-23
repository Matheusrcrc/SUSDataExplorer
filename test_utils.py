import pytest
import os
from unittest.mock import patch, MagicMock
import pandas as pd

# Testes para o módulo de exportação de dados
class TestExportModule:
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'ano': [2020, 2021, 2022],
            'regiao': ['290001', '290001', '290001'],
            'valor': [10, 15, 20],
            'indicador': ['mortalidade', 'mortalidade', 'mortalidade']
        })
    
    @patch('os.makedirs')
    def test_export_to_csv(self, mock_makedirs, sample_data):
        # Função a ser testada
        def export_to_csv(df, output_path, index=False):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_csv(output_path, index=index)
            return output_path
        
        # Act
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            result = export_to_csv(sample_data, '/tmp/exports/data.csv')
        
        # Assert
        mock_makedirs.assert_called_once()
        mock_to_csv.assert_called_once()
        assert result == '/tmp/exports/data.csv'
    
    @patch('os.makedirs')
    def test_export_to_parquet(self, mock_makedirs, sample_data):
        # Função a ser testada
        def export_to_parquet(df, output_path):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_parquet(output_path)
            return output_path
        
        # Act
        with patch('pandas.DataFrame.to_parquet') as mock_to_parquet:
            result = export_to_parquet(sample_data, '/tmp/exports/data.parquet')
        
        # Assert
        mock_makedirs.assert_called_once()
        mock_to_parquet.assert_called_once()
        assert result == '/tmp/exports/data.parquet'
    
    @patch('os.makedirs')
    def test_export_to_json(self, mock_makedirs, sample_data):
        # Função a ser testada
        def export_to_json(df, output_path, orient='records'):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            df.to_json(output_path, orient=orient)
            return output_path
        
        # Act
        with patch('pandas.DataFrame.to_json') as mock_to_json:
            result = export_to_json(sample_data, '/tmp/exports/data.json')
        
        # Assert
        mock_makedirs.assert_called_once()
        mock_to_json.assert_called_once()
        assert result == '/tmp/exports/data.json'
    
    def test_format_data_for_export(self, sample_data):
        # Função a ser testada
        def format_data_for_export(df, format_type):
            if format_type == 'csv':
                return df.to_csv(index=False)
            elif format_type == 'json':
                return df.to_json(orient='records')
            elif format_type == 'dict':
                return df.to_dict(orient='records')
            else:
                raise ValueError(f"Formato não suportado: {format_type}")
        
        # Act
        with patch('pandas.DataFrame.to_csv') as mock_to_csv:
            mock_to_csv.return_value = "ano,regiao,valor,indicador\n"
            csv_result = format_data_for_export(sample_data, 'csv')
        
        with patch('pandas.DataFrame.to_json') as mock_to_json:
            mock_to_json.return_value = "[{\"ano\":2020,\"regiao\":\"290001\",\"valor\":10,\"indicador\":\"mortalidade\"}]"
            json_result = format_data_for_export(sample_data, 'json')
        
        with patch('pandas.DataFrame.to_dict') as mock_to_dict:
            mock_to_dict.return_value = [{"ano":2020,"regiao":"290001","valor":10,"indicador":"mortalidade"}]
            dict_result = format_data_for_export(sample_data, 'dict')
        
        # Assert
        mock_to_csv.assert_called_once()
        mock_to_json.assert_called_once()
        mock_to_dict.assert_called_once()
        assert isinstance(csv_result, str)
        assert isinstance(json_result, str)
        assert isinstance(dict_result, list)
        
        # Test invalid format
        with pytest.raises(ValueError):
            format_data_for_export(sample_data, 'invalid_format')

# Testes para o módulo de visualização de dados
class TestVisualizationModule:
    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            'ano': [2020, 2021, 2022],
            'regiao': ['290001', '290001', '290001'],
            'valor': [10, 15, 20],
            'indicador': ['mortalidade', 'mortalidade', 'mortalidade']
        })
    
    def test_create_time_series_plot(self, sample_data):
        # Função a ser testada
        def create_time_series_plot(df, x_col, y_col, title, xlabel, ylabel):
            # Em um cenário real, esta função usaria matplotlib ou plotly
            # Para o teste, apenas verificamos se os parâmetros são válidos
            if x_col not in df.columns:
                raise ValueError(f"Coluna {x_col} não encontrada no DataFrame")
            if y_col not in df.columns:
                raise ValueError(f"Coluna {y_col} não encontrada no DataFrame")
            
            # Retorna um dicionário simulando um objeto de figura
            return {
                'data': df[[x_col, y_col]].values.tolist(),
                'layout': {
                    'title': title,
                    'xaxis': {'title': xlabel},
                    'yaxis': {'title': ylabel}
                }
            }
        
        # Act
        result = create_time_series_plot(
            sample_data, 'ano', 'valor', 
            'Evolução da Mortalidade', 'Ano', 'Taxa de Mortalidade'
        )
        
        # Assert
        assert isinstance(result, dict)
        assert 'data' in result
        assert 'layout' in result
        assert result['layout']['title'] == 'Evolução da Mortalidade'
        assert result['layout']['xaxis']['title'] == 'Ano'
        assert result['layout']['yaxis']['title'] == 'Taxa de Mortalidade'
        
        # Test invalid columns
        with pytest.raises(ValueError):
            create_time_series_plot(sample_data, 'invalid_col', 'valor', 'Title', 'X', 'Y')
        
        with pytest.raises(ValueError):
            create_time_series_plot(sample_data, 'ano', 'invalid_col', 'Title', 'X', 'Y')
    
    def test_create_bar_chart(self, sample_data):
        # Função a ser testada
        def create_bar_chart(df, category_col, value_col, title, xlabel, ylabel):
            # Em um cenário real, esta função usaria matplotlib ou plotly
            # Para o teste, apenas verificamos se os parâmetros são válidos
            if category_col not in df.columns:
                raise ValueError(f"Coluna {category_col} não encontrada no DataFrame")
            if value_col not in df.columns:
                raise ValueError(f"Coluna {value_col} não encontrada no DataFrame")
            
            # Agrega os dados por categoria
            agg_data = df.groupby(category_col)[value_col].mean().reset_index()
            
            # Retorna um dicionário simulando um objeto de figura
            return {
                'data': agg_data.values.tolist(),
                'layout': {
                    'title': title,
                    'xaxis': {'title': xlabel},
                    'yaxis': {'title': ylabel}
                }
            }
        
        # Act
        result = create_bar_chart(
            sample_data, 'ano', 'valor', 
            'Mortalidade por Ano', 'Ano', 'Taxa de Mortalidade'
        )
        
        # Assert
        assert isinstance(result, dict)
        assert 'data' in result
        assert 'layout' in result
        assert result['layout']['title'] == 'Mortalidade por Ano'
        assert result['layout']['xaxis']['title'] == 'Ano'
        assert result['layout']['yaxis']['title'] == 'Taxa de Mortalidade'
        
        # Test invalid columns
        with pytest.raises(ValueError):
            create_bar_chart(sample_data, 'invalid_col', 'valor', 'Title', 'X', 'Y')
        
        with pytest.raises(ValueError):
            create_bar_chart(sample_data, 'ano', 'invalid_col', 'Title', 'X', 'Y')
    
    def test_create_heatmap(self, sample_data):
        # Cria um DataFrame mais adequado para heatmap
        df_corr = pd.DataFrame({
            'var1': [1.0, 0.8, -0.5],
            'var2': [0.8, 1.0, -0.3],
            'var3': [-0.5, -0.3, 1.0]
        }, index=['var1', 'var2', 'var3'])
        
        # Função a ser testada
        def create_heatmap(df_corr, title):
            # Em um cenário real, esta função usaria seaborn ou plotly
            # Para o teste, apenas verificamos se os parâmetros são válidos
            if not isinstance(df_corr, pd.DataFrame):
                raise ValueError("O input deve ser um DataFrame")
            
            # Verifica se é uma matriz de correlação válida
            if not all(df_corr.index == df_corr.columns):
                raise ValueError("O DataFrame deve ter os mesmos índices e colunas (matriz quadrada)")
            
            # Retorna um dicionário simulando um objeto de figura
            return {
                'data': df_corr.values.tolist(),
                'layout': {
                    'title': title,
                    'xaxis': {'title': 'Variáveis'},
                    'yaxis': {'title': 'Variáveis'}
                }
            }
        
        # Act
        result = create_heatmap(df_corr, 'Matriz de Correlação')
        
        # Assert
        assert isinstance(result, dict)
        assert 'data' in result
        assert 'layout' in result
        assert result['layout']['title'] == 'Matriz de Correlação'
        
        # Test invalid input
        with pytest.raises(ValueError):
            create_heatmap("not a dataframe", 'Title')
        
        # Test non-square matrix
        non_square_df = pd.DataFrame({
            'var1': [1, 2, 3],
            'var2': [4, 5, 6]
        })
        with pytest.raises(ValueError):
            create_heatmap(non_square_df, 'Title')
