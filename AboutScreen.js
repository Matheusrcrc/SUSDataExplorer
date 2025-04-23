import React from 'react';
import { View, Text, StyleSheet, ScrollView, Linking } from 'react-native';

const AboutScreen = () => {
  return (
    <ScrollView style={styles.container}>
      <View style={styles.section}>
        <Text style={styles.title}>Sobre o SUS Data Explorer</Text>
        <Text style={styles.description}>
          O SUS Data Explorer é um sistema AI first, mobile first, community first para buscar, 
          unificar e servir dados oficiais do SUS, começando pela pesquisa "Avaliação da efetividade 
          da Rede de Atenção às Urgências no Estado da Bahia (2013-2023)".
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Missão & Visão</Text>
        <Text style={styles.description}>
          Construir um OSS resiliente que simplifique o acesso aos bancos públicos do SUS, 
          gere insights reproduzíveis e permita evolução colaborativa.
        </Text>
        <Text style={styles.description}>
          <Text style={styles.bold}>Meta Fase 1:</Text> entregar todos os indicadores de estrutura, 
          processo e resultado, filtráveis por Região de Saúde/município e exportáveis (CSV/Parquet/JSON).
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Fontes de Dados</Text>
        <Text style={styles.listItem}>• CKAN OpenDataSUS - Datasets em CSV/Parquet (ex.: PNI, SIM, SIH)</Text>
        <Text style={styles.listItem}>• DEMAS / apidadosabertos.saude.gov.br - CNES, leitos, estabelecimentos</Text>
        <Text style={styles.listItem}>• DATASUS TABNET - Endpoints HTTP + downloads DBC via PySUS</Text>
        <Text style={styles.listItem}>• e-Gestor AB - Dados da Atenção Básica via scraping</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Pilares de Arquitetura</Text>
        <Text style={styles.subSectionTitle}>AI first</Text>
        <Text style={styles.description}>
          Uso de agentes de IA como par-programmer para code-gen, refatoração contínua, 
          testes, documentação e análise de qualidade.
        </Text>
        
        <Text style={styles.subSectionTitle}>Mobile first</Text>
        <Text style={styles.description}>
          REST/GraphQL + OpenAPI → Gateway → App Flutter/React Native com UI responsiva; 
          priorização de requests assíncronos, cache local e fallback offline.
        </Text>
        
        <Text style={styles.subSectionTitle}>Community first</Text>
        <Text style={styles.description}>
          Repositório público (MIT). Inclui guia CONTRIBUTING.md, Code of Conduct, 
          templates de PR e GitHub Actions integrando CI/CD e SonarCloud.
        </Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Stack Tecnológica</Text>
        <Text style={styles.listItem}>• Backend: Python 3.10, FastAPI, AsyncIO, Pydantic, SQLModel, Redis cache</Text>
        <Text style={styles.listItem}>• Data layer: DuckDB + Parquet para portabilidade</Text>
        <Text style={styles.listItem}>• ETL helpers: PySUS, pandas, polars, httpx, orjson</Text>
        <Text style={styles.listItem}>• Frontend: React Native</Text>
        <Text style={styles.listItem}>• Testes: pytest, coverage >90%, contract tests nos conectores</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Políticas de Qualidade & Compliance</Text>
        <Text style={styles.listItem}>• LGPD: apenas dados públicos anônimos; sem PII</Text>
        <Text style={styles.listItem}>• Segurança: dependabot, SAST, SBOM CycloneDX</Text>
        <Text style={styles.listItem}>• Desempenho: respostas < 300 ms (cache quente) nos top-queries</Text>
        <Text style={styles.listItem}>• Observabilidade: Prometheus + Grafana, tracing OTLP</Text>
      </View>

      <View style={styles.section}>
        <Text style={styles.sectionTitle}>Licença</Text>
        <Text style={styles.description}>
          Este projeto é open source, licenciado sob a licença MIT.
        </Text>
        <Text style={styles.link} onPress={() => Linking.openURL('https://github.com/seu-usuario/sus-data-explorer')}>
          Visite o repositório no GitHub
        </Text>
      </View>

      <View style={styles.footer}>
        <Text style={styles.footerText}>SUS Data Explorer v1.0.0</Text>
        <Text style={styles.footerText}>© 2025 SUS Data Explorer Team</Text>
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
    padding: 20,
  },
  section: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 15,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#0066cc',
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  subSectionTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginTop: 10,
    marginBottom: 5,
    color: '#555',
  },
  description: {
    fontSize: 14,
    lineHeight: 22,
    color: '#444',
    marginBottom: 10,
  },
  listItem: {
    fontSize: 14,
    lineHeight: 22,
    color: '#444',
    marginBottom: 8,
    paddingLeft: 5,
  },
  bold: {
    fontWeight: 'bold',
  },
  link: {
    fontSize: 14,
    color: '#0066cc',
    textDecorationLine: 'underline',
    marginTop: 10,
  },
  footer: {
    marginTop: 10,
    marginBottom: 30,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 12,
    color: '#666',
    marginBottom: 5,
  },
});

export default AboutScreen;
