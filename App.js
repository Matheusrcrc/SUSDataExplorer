import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity, TextInput, ActivityIndicator, Platform } from 'react-native';
import { Picker } from '@react-native-picker/picker';
import { LineChart } from 'react-native-chart-kit';
import { Dimensions } from 'react-native';

const API_URL = 'http://localhost:8000'; // Alterar para URL pública em produção

const App = () => {
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);
  const [selectedSource, setSelectedSource] = useState('');
  const [indicators, setIndicators] = useState([
    { id: 'mortalidade', name: 'Mortalidade' },
    { id: 'internacoes', name: 'Internações' },
    { id: 'cobertura_ab', name: 'Cobertura da Atenção Básica' },
    { id: 'estabelecimentos', name: 'Estabelecimentos de Saúde' },
    { id: 'leitos', name: 'Leitos Hospitalares' },
  ]);
  const [selectedIndicator, setSelectedIndicator] = useState('');
  const [region, setRegion] = useState('290000'); // Código da Bahia
  const [startYear, setStartYear] = useState('2013');
  const [endYear, setEndYear] = useState('2023');
  const [data, setData] = useState(null);
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState(null);

  // Buscar fontes de dados ao carregar o app
  useEffect(() => {
    fetchSources();
  }, []);

  // Preparar dados do gráfico quando os dados forem carregados
  useEffect(() => {
    if (data && data.data && data.data.length > 0) {
      prepareChartData();
    }
  }, [data]);

  const fetchSources = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_URL}/sources`);
      const result = await response.json();
      setSources(result.sources);
      setLoading(false);
    } catch (err) {
      setError('Erro ao carregar fontes de dados');
      setLoading(false);
      console.error(err);
    }
  };

  const fetchData = async () => {
    if (!selectedIndicator || !region || !startYear) {
      setError('Por favor, preencha todos os campos obrigatórios');
      return;
    }

    try {
      setLoading(true);
      setError(null);
      
      const url = `${API_URL}/indicators/${selectedIndicator}?region=${region}&start_year=${startYear}${endYear ? `&end_year=${endYear}` : ''}${selectedSource ? `&source=${selectedSource}` : ''}`;
      
      const response = await fetch(url);
      
      if (!response.ok) {
        throw new Error(`Erro ${response.status}: ${response.statusText}`);
      }
      
      const result = await response.json();
      setData(result);
      setLoading(false);
    } catch (err) {
      setError(`Erro ao buscar dados: ${err.message}`);
      setLoading(false);
      console.error(err);
    }
  };

  const prepareChartData = () => {
    // Esta função é simplificada e deve ser adaptada para cada tipo de indicador
    try {
      // Agrupa dados por ano
      const groupedByYear = {};
      
      data.data.forEach(item => {
        const year = item.ano || item.year || 2023; // Fallback para 2023 se não houver ano
        if (!groupedByYear[year]) {
          groupedByYear[year] = [];
        }
        groupedByYear[year].push(item);
      });
      
      // Calcula valores médios por ano
      const years = Object.keys(groupedByYear).sort();
      const values = years.map(year => {
        const yearData = groupedByYear[year];
        
        // Tenta encontrar um campo numérico para o gráfico
        // Esta lógica deve ser adaptada para cada tipo de indicador
        let sum = 0;
        let count = 0;
        
        yearData.forEach(item => {
          // Procura por campos numéricos comuns
          const numericFields = ['valor', 'value', 'cobertura_ab', 'cobertura_esf', 
                                'quantidade', 'count', 'total'];
          
          for (const field of numericFields) {
            if (item[field] && !isNaN(parseFloat(item[field]))) {
              sum += parseFloat(item[field]);
              count++;
              break;
            }
          }
        });
        
        return count > 0 ? sum / count : 0;
      });
      
      setChartData({
        labels: years,
        datasets: [
          {
            data: values,
            color: (opacity = 1) => `rgba(0, 102, 204, ${opacity})`,
            strokeWidth: 2
          }
        ],
        legend: [selectedIndicator]
      });
      
    } catch (err) {
      console.error('Erro ao preparar dados do gráfico:', err);
      setError('Não foi possível gerar o gráfico com os dados disponíveis');
    }
  };

  const exportData = async (format) => {
    if (!data) {
      setError('Nenhum dado para exportar');
      return;
    }

    try {
      setLoading(true);
      const url = `${API_URL}/exports?indicator=${selectedIndicator}&region=${region}&start_year=${startYear}${endYear ? `&end_year=${endYear}` : ''}&format=${format}`;
      
      // Em um app real, isso baixaria o arquivo
      // Aqui apenas simulamos a exportação
      await fetch(url);
      
      setLoading(false);
      alert(`Dados exportados com sucesso no formato ${format.toUpperCase()}`);
    } catch (err) {
      setError(`Erro ao exportar dados: ${err.message}`);
      setLoading(false);
    }
  };

  return (
    <ScrollView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>SUS Data Explorer</Text>
        <Text style={styles.subtitle}>Explore dados oficiais do SUS</Text>
      </View>

      <View style={styles.formContainer}>
        <Text style={styles.sectionTitle}>Parâmetros de Consulta</Text>
        
        <Text style={styles.label}>Indicador:</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={selectedIndicator}
            onValueChange={(value) => setSelectedIndicator(value)}
            style={styles.picker}
          >
            <Picker.Item label="Selecione um indicador" value="" />
            {indicators.map(indicator => (
              <Picker.Item key={indicator.id} label={indicator.name} value={indicator.id} />
            ))}
          </Picker>
        </View>

        <Text style={styles.label}>Fonte de dados (opcional):</Text>
        <View style={styles.pickerContainer}>
          <Picker
            selectedValue={selectedSource}
            onValueChange={(value) => setSelectedSource(value)}
            style={styles.picker}
          >
            <Picker.Item label="Fonte padrão do indicador" value="" />
            {sources.map(source => (
              <Picker.Item key={source.id} label={source.name} value={source.id} />
            ))}
          </Picker>
        </View>

        <Text style={styles.label}>Região/Município (código IBGE):</Text>
        <TextInput
          style={styles.input}
          value={region}
          onChangeText={setRegion}
          placeholder="Ex: 290000 (Bahia)"
          keyboardType="numeric"
        />

        <View style={styles.rowContainer}>
          <View style={styles.halfInput}>
            <Text style={styles.label}>Ano inicial:</Text>
            <TextInput
              style={styles.input}
              value={startYear}
              onChangeText={setStartYear}
              placeholder="Ex: 2013"
              keyboardType="numeric"
            />
          </View>
          
          <View style={styles.halfInput}>
            <Text style={styles.label}>Ano final (opcional):</Text>
            <TextInput
              style={styles.input}
              value={endYear}
              onChangeText={setEndYear}
              placeholder="Ex: 2023"
              keyboardType="numeric"
            />
          </View>
        </View>

        <TouchableOpacity 
          style={styles.button} 
          onPress={fetchData}
          disabled={loading}
        >
          <Text style={styles.buttonText}>
            {loading ? 'Carregando...' : 'Buscar Dados'}
          </Text>
        </TouchableOpacity>
      </View>

      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#0066cc" />
          <Text style={styles.loadingText}>Carregando dados...</Text>
        </View>
      )}

      {data && data.data && data.data.length > 0 && (
        <View style={styles.resultsContainer}>
          <Text style={styles.sectionTitle}>Resultados</Text>
          
          <View style={styles.metadataContainer}>
            <Text style={styles.metadataText}>
              <Text style={styles.bold}>Indicador:</Text> {selectedIndicator}
            </Text>
            <Text style={styles.metadataText}>
              <Text style={styles.bold}>Região:</Text> {region}
            </Text>
            <Text style={styles.metadataText}>
              <Text style={styles.bold}>Período:</Text> {startYear}{endYear ? ` a ${endYear}` : ''}
            </Text>
            <Text style={styles.metadataText}>
              <Text style={styles.bold}>Registros:</Text> {data.data.length}
            </Text>
          </View>

          {chartData && (
            <View style={styles.chartContainer}>
              <Text style={styles.chartTitle}>Evolução Temporal</Text>
              <LineChart
                data={chartData}
                width={Dimensions.get('window').width - 40}
                height={220}
                chartConfig={{
                  backgroundColor: '#ffffff',
                  backgroundGradientFrom: '#ffffff',
                  backgroundGradientTo: '#ffffff',
                  decimalPlaces: 1,
                  color: (opacity = 1) => `rgba(0, 102, 204, ${opacity})`,
                  labelColor: (opacity = 1) => `rgba(0, 0, 0, ${opacity})`,
                  style: {
                    borderRadius: 16
                  },
                  propsForDots: {
                    r: '6',
                    strokeWidth: '2',
                    stroke: '#0066cc'
                  }
                }}
                bezier
                style={styles.chart}
              />
            </View>
          )}

          <View style={styles.exportContainer}>
            <Text style={styles.exportTitle}>Exportar dados:</Text>
            <View style={styles.exportButtons}>
              <TouchableOpacity 
                style={[styles.exportButton, styles.csvButton]} 
                onPress={() => exportData('csv')}
              >
                <Text style={styles.exportButtonText}>CSV</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.exportButton, styles.jsonButton]} 
                onPress={() => exportData('json')}
              >
                <Text style={styles.exportButtonText}>JSON</Text>
              </TouchableOpacity>
              
              <TouchableOpacity 
                style={[styles.exportButton, styles.parquetButton]} 
                onPress={() => exportData('parquet')}
              >
                <Text style={styles.exportButtonText}>Parquet</Text>
              </TouchableOpacity>
            </View>
          </View>

          <View style={styles.dataPreviewContainer}>
            <Text style={styles.dataPreviewTitle}>Prévia dos dados:</Text>
            <ScrollView style={styles.dataPreview}>
              {data.data.slice(0, 10).map((item, index) => (
                <View key={index} style={styles.dataItem}>
                  {Object.entries(item).map(([key, value]) => (
                    <Text key={key} style={styles.dataItemText}>
                      <Text style={styles.bold}>{key}:</Text> {value}
                    </Text>
                  ))}
                </View>
              ))}
              {data.data.length > 10 && (
                <Text style={styles.moreDataText}>
                  ... mais {data.data.length - 10} registros
                </Text>
              )}
            </ScrollView>
          </View>
        </View>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  header: {
    backgroundColor: '#0066cc',
    padding: 20,
    alignItems: 'center',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: 'white',
  },
  subtitle: {
    fontSize: 16,
    color: 'white',
    marginTop: 5,
  },
  formContainer: {
    backgroundColor: 'white',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  label: {
    fontSize: 14,
    marginBottom: 5,
    color: '#555',
  },
  pickerContainer: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  picker: {
    height: 50,
    width: '100%',
  },
  input: {
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
    padding: 10,
    marginBottom: 15,
    backgroundColor: '#fff',
  },
  rowContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  halfInput: {
    width: '48%',
  },
  button: {
    backgroundColor: '#0066cc',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
  },
  buttonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  errorContainer: {
    backgroundColor: '#ffebee',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    borderLeftWidth: 5,
    borderLeftColor: '#f44336',
  },
  errorText: {
    color: '#b71c1c',
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  loadingText: {
    marginTop: 10,
    color: '#0066cc',
  },
  resultsContainer: {
    backgroundColor: 'white',
    margin: 15,
    padding: 15,
    borderRadius: 10,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  metadataContainer: {
    backgroundColor: '#f5f5f5',
    padding: 10,
    borderRadius: 5,
    marginBottom: 15,
  },
  metadataText: {
    fontSize: 14,
    marginBottom: 5,
  },
  bold: {
    fontWeight: 'bold',
  },
  chartContainer: {
    marginVertical: 15,
    alignItems: 'center',
  },
  chartTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  chart: {
    borderRadius: 10,
  },
  exportContainer: {
    marginVertical: 15,
  },
  exportTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  exportButtons: {
    flexDirection: 'row',
    justifyContent: 'space-between',
  },
  exportButton: {
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
    width: '30%',
  },
  csvButton: {
    backgroundColor: '#4caf50',
  },
  jsonButton: {
    backgroundColor: '#ff9800',
  },
  parquetButton: {
    backgroundColor: '#9c27b0',
  },
  exportButtonText: {
    color: 'white',
    fontWeight: 'bold',
  },
  dataPreviewContainer: {
    marginTop: 15,
  },
  dataPreviewTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#333',
  },
  dataPreview: {
    maxHeight: 300,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 5,
  },
  dataItem: {
    padding: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  dataItemText: {
    fontSize: 12,
    marginBottom: 3,
  },
  moreDataText: {
    padding: 10,
    fontStyle: 'italic',
    color: '#666',
    textAlign: 'center',
  },
});

export default App;
