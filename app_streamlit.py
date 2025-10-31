"""
SUS Data Explorer - Aplicação Streamlit
Sistema AI first, mobile first, community first para explorar dados do SUS
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import asyncio
import json
from typing import Dict, Any, List

# Importar conectores
from ckan import CkanConnector
from demas import DemasConnector
from tabnet import TabnetConnector
from egestor import EGestorConnector

# Configuração da página
st.set_page_config(
    page_title="SUS Data Explorer",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Helper para rodar funções assíncronas
def run_async(coro):
    """Wrapper para executar código assíncrono em Streamlit"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)

# Cache para conectores
def get_connectors():
    """Inicializa e retorna os conectores de dados"""
    if 'connectors' not in st.session_state:
        st.session_state['connectors'] = {
            "CKAN OpenDataSUS": CkanConnector(),
            "DEMAS": DemasConnector(),
            "DATASUS TABNET": TabnetConnector(),
            "e-Gestor AB": EGestorConnector()
        }
    return st.session_state['connectors']

# Cache para datasets
def load_datasets(source_name: str):
    """Carrega lista de datasets de uma fonte"""
    connectors = get_connectors()
    connector = connectors[source_name]
    try:
        datasets = run_async(connector.list_datasets())
        return datasets
    except Exception as e:
        st.error(f"Erro ao carregar datasets: {str(e)}")
        return []

# Cache para dados
@st.cache_data(ttl=1800)
def load_data(source_name: str, query: Dict[str, Any]):
    """Carrega dados de uma fonte com query específica"""
    connectors = get_connectors()
    connector = connectors[source_name]
    try:
        data = run_async(connector.get_data(query))
        return data
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return None

# Header
st.markdown('<p class="main-header">🏥 SUS Data Explorer</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Explore dados oficiais do SUS de forma simples e interativa</p>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://raw.githubusercontent.com/FortAwesome/Font-Awesome/6.x/svgs/solid/hospital.svg", width=80)
    st.title("Navegação")

    page = st.radio(
        "Escolha uma página:",
        ["🏠 Início", "📊 Explorar Dados", "📈 Visualizações", "📥 Exportar", "ℹ️ Sobre"]
    )

    st.markdown("---")
    st.markdown("### Fontes de Dados")
    st.markdown("""
    - CKAN OpenDataSUS
    - DEMAS
    - DATASUS TABNET
    - e-Gestor AB
    """)

    st.markdown("---")
    st.markdown("### Links Úteis")
    st.markdown("[📖 Documentação](https://github.com)")
    st.markdown("[🐛 Reportar Bug](https://github.com)")
    st.markdown("[💡 Sugerir Feature](https://github.com)")

# Página: Início
if page == "🏠 Início":
    st.header("Bem-vindo ao SUS Data Explorer!")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(label="📊 Fontes de Dados", value="4", delta="Integradas")

    with col2:
        st.metric(label="📁 Datasets", value="100+", delta="Disponíveis")

    with col3:
        st.metric(label="🎯 Cobertura", value="2013-2023", delta="10 anos")

    st.markdown("---")

    st.subheader("🎯 Missão")
    st.write("""
    Construir um sistema open-source resiliente que simplifique o acesso aos bancos públicos do SUS,
    gere insights reproduzíveis e permita evolução colaborativa.
    """)

    st.subheader("🚀 Funcionalidades")

    col1, col2 = st.columns(2)

    with col1:
        st.info("""
        **📊 Exploração de Dados**
        - Acesso a múltiplas fontes do SUS
        - Filtros por região e período
        - Visualização interativa
        """)

        st.success("""
        **📥 Exportação Flexível**
        - CSV, JSON, Parquet
        - Excel com formatação
        - API REST disponível
        """)

    with col2:
        st.warning("""
        **📈 Visualizações**
        - Gráficos interativos
        - Mapas geográficos
        - Dashboards customizáveis
        """)

        st.error("""
        **🔍 Transparência**
        - Dados oficiais e verificados
        - Código aberto (MIT)
        - Documentação completa
        """)

    st.markdown("---")

    st.subheader("📌 Como Começar")
    st.write("""
    1. 👈 Use o menu lateral para navegar
    2. 📊 Vá para "Explorar Dados" para buscar informações
    3. 📈 Visualize os dados com gráficos interativos
    4. 📥 Exporte para o formato desejado
    """)

# Página: Explorar Dados
elif page == "📊 Explorar Dados":
    st.header("📊 Explorar Dados do SUS")

    # Seleção de fonte
    connectors = get_connectors()
    source = st.selectbox(
        "Escolha a fonte de dados:",
        list(connectors.keys())
    )

    # Informações sobre a fonte
    connector = connectors[source]
    schema = connector.schema()

    with st.expander("ℹ️ Informações sobre esta fonte"):
        st.write(f"**Nome:** {schema.get('name', 'N/A')}")
        st.write(f"**Descrição:** {schema.get('description', 'N/A')}")
        if 'update_frequency' in schema:
            st.write(f"**Frequência de Atualização:** {schema['update_frequency']}")
        if 'limitations' in schema:
            st.write(f"**Limitações:** {schema['limitations']}")

    st.markdown("---")

    # Formulário de consulta
    st.subheader("🔍 Parâmetros de Busca")

    # Carregar e selecionar dataset
    if 'datasets' not in st.session_state or st.session_state.get('current_source') != source:
        st.session_state['datasets'] = load_datasets(source)
        st.session_state['current_source'] = source

    datasets = st.session_state['datasets']
    if not datasets:
        st.warning("Nenhum dataset disponível para esta fonte.")
        st.stop()

    dataset_options = {ds.get("name", ds.get("id")): ds.get("id") for ds in datasets}
    selected_dataset_name = st.selectbox("Selecione o Dataset:", list(dataset_options.keys()))
    selected_dataset_id = dataset_options[selected_dataset_name]

    col1, col2 = st.columns(2)

    with col1:
        region = st.text_input(
            "Código IBGE da Região/Município:",
            value="29",
            help="Ex: 29 (Bahia), 2927408 (Salvador)"
        )

    with col2:
        year_start = st.number_input(
            "Ano Inicial:",
            min_value=2000,
            max_value=datetime.now().year,
            value=2013
        )

        year_end = st.number_input(
            "Ano Final:",
            min_value=2000,
            max_value=datetime.now().year,
            value=2023
        )

    # Botão de busca
    if st.button("🔍 Buscar Dados", type="primary"):
        with st.spinner("Carregando dados..."):
            # Preparar query
            query = {
                "dataset_id": selected_dataset_id,
                "region": region,
                "start_year": year_start,
                "end_year": year_end
            }

            # Carregar dados
            data = load_data(source, query)

            if data is not None and not data.empty:
                st.success(f"✅ {len(data)} registros encontrados!")

                # Armazenar no session state
                st.session_state['current_data'] = data
                st.session_state['current_query'] = query
                st.session_state['current_source'] = source

                # Mostrar preview
                st.subheader("📋 Preview dos Dados")
                st.dataframe(data.head(100), use_container_width=True)

                # Estatísticas básicas
                st.subheader("📊 Estatísticas")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total de Registros", len(data))
                with col2:
                    st.metric("Colunas", len(data.columns))
                with col3:
                    numeric_cols = data.select_dtypes(include=['number']).columns
                    st.metric("Colunas Numéricas", len(numeric_cols))
                with col4:
                    st.metric("Período", f"{year_start}-{year_end}")

            else:
                st.warning("⚠️ Nenhum dado encontrado para os parâmetros selecionados.")

# Página: Visualizações
elif page == "📈 Visualizações":
    st.header("📈 Visualizações Interativas")

    if 'current_data' not in st.session_state or st.session_state['current_data'] is None:
        st.info("👈 Primeiro, busque dados na página 'Explorar Dados'")
    else:
        data = st.session_state['current_data']

        # Tipo de visualização
        viz_type = st.selectbox(
            "Tipo de Visualização:",
            ["📊 Gráfico de Barras", "📈 Gráfico de Linhas", "🥧 Gráfico de Pizza",
             "🗺️ Mapa", "📉 Área", "📊 Histograma"]
        )

        # Selecionar colunas
        numeric_cols = data.select_dtypes(include=['number']).columns.tolist()
        all_cols = data.columns.tolist()

        col1, col2 = st.columns(2)

        with col1:
            x_col = st.selectbox("Eixo X:", all_cols)

        with col2:
            y_col = st.selectbox("Eixo Y:", numeric_cols if numeric_cols else all_cols)

        # Criar visualização
        try:
            if viz_type == "📊 Gráfico de Barras":
                fig = px.bar(data, x=x_col, y=y_col, title=f"{y_col} por {x_col}")
            elif viz_type == "📈 Gráfico de Linhas":
                fig = px.line(data, x=x_col, y=y_col, title=f"{y_col} ao longo de {x_col}")
            elif viz_type == "🥧 Gráfico de Pizza":
                fig = px.pie(data, names=x_col, values=y_col, title=f"Distribuição de {y_col}")
            elif viz_type == "📉 Área":
                fig = px.area(data, x=x_col, y=y_col, title=f"{y_col} por {x_col}")
            elif viz_type == "📊 Histograma":
                fig = px.histogram(data, x=y_col, title=f"Distribuição de {y_col}")
            else:
                fig = px.scatter(data, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")

            fig.update_layout(height=600)
            st.plotly_chart(fig, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao criar visualização: {str(e)}")

        # Visualizações adicionais
        st.markdown("---")
        st.subheader("📊 Análises Adicionais")

        tab1, tab2, tab3 = st.tabs(["📈 Tendências", "📊 Correlações", "📋 Resumo"])

        with tab1:
            st.write("### Análise de Tendências")
            if numeric_cols:
                selected_col = st.selectbox("Selecione uma coluna:", numeric_cols, key="trend")
                fig_trend = px.line(data, y=selected_col, title=f"Tendência de {selected_col}")
                st.plotly_chart(fig_trend, use_container_width=True)

        with tab2:
            st.write("### Matriz de Correlação")
            if len(numeric_cols) > 1:
                corr = data[numeric_cols].corr()
                fig_corr = px.imshow(corr, text_auto=True, aspect="auto",
                                    title="Correlação entre Variáveis")
                st.plotly_chart(fig_corr, use_container_width=True)
            else:
                st.info("É necessário ter pelo menos 2 colunas numéricas para calcular correlação.")

        with tab3:
            st.write("### Resumo Estatístico")
            st.dataframe(data.describe(), use_container_width=True)

# Página: Exportar
elif page == "📥 Exportar":
    st.header("📥 Exportar Dados")

    if 'current_data' not in st.session_state or st.session_state['current_data'] is None:
        st.info("👈 Primeiro, busque dados na página 'Explorar Dados'")
    else:
        data = st.session_state['current_data']
        query = st.session_state.get('current_query', {})
        source = st.session_state.get('current_source', 'unknown')

        st.success(f"✅ {len(data)} registros prontos para exportação")

        # Formato de exportação
        export_format = st.selectbox(
            "Escolha o formato:",
            ["CSV", "JSON", "Excel (XLSX)", "Parquet"]
        )

        # Nome do arquivo
        default_name = f"sus_data_{query.get('region', 'BR')}_{query.get('start_year', '2013')}"
        filename = st.text_input("Nome do arquivo:", value=default_name)

        # Botão de exportação
        col1, col2 = st.columns([1, 3])

        with col1:
            if st.button("📥 Exportar", type="primary"):
                try:
                    if export_format == "CSV":
                        csv = data.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv,
                            file_name=f"{filename}.csv",
                            mime="text/csv"
                        )

                    elif export_format == "JSON":
                        json_str = data.to_json(orient='records', indent=2)
                        st.download_button(
                            label="⬇️ Download JSON",
                            data=json_str,
                            file_name=f"{filename}.json",
                            mime="application/json"
                        )

                    elif export_format == "Excel (XLSX)":
                        # Criar Excel em memória
                        from io import BytesIO
                        buffer = BytesIO()
                        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                            data.to_excel(writer, index=False, sheet_name='Dados')

                        st.download_button(
                            label="⬇️ Download Excel",
                            data=buffer.getvalue(),
                            file_name=f"{filename}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )

                    elif export_format == "Parquet":
                        parquet = data.to_parquet(index=False)
                        st.download_button(
                            label="⬇️ Download Parquet",
                            data=parquet,
                            file_name=f"{filename}.parquet",
                            mime="application/octet-stream"
                        )

                    st.success("✅ Arquivo pronto para download!")

                except Exception as e:
                    st.error(f"Erro ao exportar: {str(e)}")

        # Preview dos dados
        st.markdown("---")
        st.subheader("📋 Preview dos Dados")
        st.dataframe(data.head(50), use_container_width=True)

# Página: Sobre
elif page == "ℹ️ Sobre":
    st.header("ℹ️ Sobre o SUS Data Explorer")

    st.markdown("""
    ## 🎯 Missão & Visão

    Construir um sistema **open-source resiliente** que simplifique o acesso aos bancos públicos do SUS,
    gere insights reproduzíveis e permita evolução colaborativa.

    ## 🏗️ Arquitetura

    O SUS Data Explorer integra dados de múltiplas fontes oficiais do SUS:

    - **CKAN OpenDataSUS**: Datasets em CSV/Parquet
    - **DEMAS**: Dados do Departamento de Monitoramento e Avaliação
    - **DATASUS TABNET**: Dados via PySUS
    - **e-Gestor AB**: Dados da Atenção Básica

    ## 🚀 Tecnologias

    - **Backend**: Python 3.10+, AsyncIO, Pandas
    - **Frontend**: Streamlit
    - **Data**: DuckDB, Parquet
    - **Deploy**: Streamlit Cloud, GitHub Pages

    ## 📊 Pilares

    - **AI First**: Desenvolvimento assistido por IA
    - **Mobile First**: Interface responsiva e acessível
    - **Community First**: Open source com documentação completa

    ## 📜 Licença

    Este projeto é licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes.

    ## 🤝 Como Contribuir

    Contribuições são bem-vindas! Veja nosso guia de contribuição no GitHub.

    ## 📞 Contato

    - GitHub: [github.com/seu-usuario/SUSDataExplorer](https://github.com)
    - Issues: [Reportar problemas](https://github.com)
    - Documentação: [Docs completa](https://github.com)
    """)

    st.markdown("---")
    st.markdown("Feito com ❤️ para melhorar o acesso a dados públicos de saúde no Brasil")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>SUS Data Explorer v1.0.0 | 2024</p>
    <p>Dados oficiais do Sistema Único de Saúde do Brasil</p>
</div>
""", unsafe_allow_html=True)
