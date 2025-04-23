import React, { useState, useEffect } from 'react';
import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import * as AuthSession from 'expo-auth-session';
import * as WebBrowser from 'expo-web-browser';

// Registra o navegador para redirecionamento de autenticação
WebBrowser.maybeCompleteAuthSession();

// Configuração para autenticação GitHub OAuth
const discovery = {
  authorizationEndpoint: 'https://github.com/login/oauth/authorize',
  tokenEndpoint: 'https://github.com/login/oauth/access_token',
  revocationEndpoint: 'https://github.com/settings/connections/applications/{clientId}',
};

// Componente de tela para autenticação
const AuthScreen = () => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Configuração da requisição de autenticação
  const [request, response, promptAsync] = AuthSession.useAuthRequest(
    {
      clientId: 'CLIENT_ID_PLACEHOLDER', // Substituir pelo Client ID real em produção
      scopes: ['identity', 'user:email'],
      redirectUri: AuthSession.makeRedirectUri({ useProxy: true }),
    },
    discovery
  );

  // Efeito para processar a resposta da autenticação
  useEffect(() => {
    if (response?.type === 'success') {
      const { code } = response.params;
      
      // Em um app real, este código seria enviado para o backend
      // para troca por um token de acesso
      console.log('Código de autorização:', code);
      
      // Simulação de obtenção de dados do usuário
      setLoading(true);
      setTimeout(() => {
        setUser({
          name: 'Usuário do SUS Data Explorer',
          email: 'usuario@exemplo.com',
          avatar: 'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png'
        });
        setLoading(false);
      }, 1000);
    } else if (response?.type === 'error') {
      setError(response.error?.message || 'Erro na autenticação');
    }
  }, [response]);

  // Função para logout
  const handleLogout = () => {
    setUser(null);
  };

  // Renderização condicional baseada no estado de autenticação
  if (user) {
    return (
      <ScrollView style={styles.container}>
        <View style={styles.profileContainer}>
          <Text style={styles.title}>Perfil do Usuário</Text>
          
          <View style={styles.userInfo}>
            <Text style={styles.userName}>{user.name}</Text>
            <Text style={styles.userEmail}>{user.email}</Text>
          </View>
          
          <View style={styles.statsContainer}>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>12</Text>
              <Text style={styles.statLabel}>Consultas</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>5</Text>
              <Text style={styles.statLabel}>Compartilhamentos</Text>
            </View>
            <View style={styles.statItem}>
              <Text style={styles.statValue}>3</Text>
              <Text style={styles.statLabel}>Contribuições</Text>
            </View>
          </View>
          
          <TouchableOpacity style={styles.logoutButton} onPress={handleLogout}>
            <Text style={styles.logoutButtonText}>Sair</Text>
          </TouchableOpacity>
        </View>
        
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Consultas Recentes</Text>
          <View style={styles.listItem}>
            <Text style={styles.listItemTitle}>Mortalidade - Bahia (2020-2023)</Text>
            <Text style={styles.listItemDate}>Acessado em: 22/04/2025</Text>
          </View>
          <View style={styles.listItem}>
            <Text style={styles.listItemTitle}>Cobertura AB - Salvador (2018-2022)</Text>
            <Text style={styles.listItemDate}>Acessado em: 20/04/2025</Text>
          </View>
        </View>
        
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Dados Salvos</Text>
          <View style={styles.listItem}>
            <Text style={styles.listItemTitle}>Internações - Região Nordeste (2015-2023)</Text>
            <Text style={styles.listItemDate}>Salvo em: 15/04/2025</Text>
          </View>
        </View>
      </ScrollView>
    );
  }

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Autenticação</Text>
      
      {error && (
        <View style={styles.errorContainer}>
          <Text style={styles.errorText}>{error}</Text>
        </View>
      )}
      
      <Text style={styles.description}>
        Faça login com sua conta GitHub para salvar suas consultas, 
        compartilhar resultados e contribuir com o projeto.
      </Text>
      
      <TouchableOpacity 
        style={styles.authButton}
        onPress={() => promptAsync({ useProxy: true })}
        disabled={!request || loading}
      >
        <Text style={styles.authButtonText}>
          {loading ? 'Processando...' : 'Entrar com GitHub'}
        </Text>
      </TouchableOpacity>
      
      <View style={styles.infoContainer}>
        <Text style={styles.infoTitle}>Benefícios da autenticação:</Text>
        <Text style={styles.infoItem}>• Salvar histórico de consultas</Text>
        <Text style={styles.infoItem}>• Compartilhar resultados com outros usuários</Text>
        <Text style={styles.infoItem}>• Contribuir com o projeto open source</Text>
        <Text style={styles.infoItem}>• Receber notificações sobre atualizações</Text>
      </View>
      
      <Text style={styles.privacyNote}>
        Não coletamos dados pessoais. A autenticação é usada apenas para 
        identificação e rastreamento de contribuições.
      </Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#0066cc',
  },
  description: {
    fontSize: 16,
    lineHeight: 24,
    color: '#444',
    marginBottom: 25,
  },
  authButton: {
    backgroundColor: '#333',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginBottom: 30,
  },
  authButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
  errorContainer: {
    backgroundColor: '#ffebee',
    padding: 15,
    borderRadius: 5,
    marginBottom: 20,
    borderLeftWidth: 5,
    borderLeftColor: '#f44336',
  },
  errorText: {
    color: '#b71c1c',
  },
  infoContainer: {
    backgroundColor: '#e3f2fd',
    padding: 15,
    borderRadius: 5,
    marginBottom: 20,
  },
  infoTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#0066cc',
  },
  infoItem: {
    fontSize: 14,
    marginBottom: 5,
    color: '#333',
  },
  privacyNote: {
    fontSize: 12,
    fontStyle: 'italic',
    color: '#666',
    textAlign: 'center',
  },
  profileContainer: {
    backgroundColor: 'white',
    borderRadius: 10,
    padding: 20,
    marginBottom: 20,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  userInfo: {
    alignItems: 'center',
    marginBottom: 20,
  },
  userName: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  userEmail: {
    fontSize: 14,
    color: '#666',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginBottom: 20,
    paddingVertical: 15,
    borderTopWidth: 1,
    borderBottomWidth: 1,
    borderColor: '#eee',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#0066cc',
  },
  statLabel: {
    fontSize: 12,
    color: '#666',
  },
  logoutButton: {
    backgroundColor: '#f5f5f5',
    padding: 10,
    borderRadius: 5,
    alignItems: 'center',
  },
  logoutButtonText: {
    color: '#666',
    fontWeight: 'bold',
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
  sectionTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginBottom: 15,
    color: '#333',
  },
  listItem: {
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#eee',
  },
  listItemTitle: {
    fontSize: 14,
    fontWeight: 'bold',
    color: '#333',
    marginBottom: 5,
  },
  listItemDate: {
    fontSize: 12,
    color: '#666',
  },
});

export default AuthScreen;
