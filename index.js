import React from 'react';
import { View, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { Ionicons } from '@expo/vector-icons';
import App from './App';
import AuthScreen from './AuthScreen';
import AboutScreen from './AboutScreen';

// Configuração do navegador de abas
const Tab = createBottomTabNavigator();

export default function Main() {
  return (
    <NavigationContainer>
      <Tab.Navigator
        screenOptions={({ route }) => ({
          tabBarIcon: ({ focused, color, size }) => {
            let iconName;

            if (route.name === 'Explorar') {
              iconName = focused ? 'search' : 'search-outline';
            } else if (route.name === 'Autenticação') {
              iconName = focused ? 'person' : 'person-outline';
            } else if (route.name === 'Sobre') {
              iconName = focused ? 'information-circle' : 'information-circle-outline';
            }

            return <Ionicons name={iconName} size={size} color={color} />;
          },
          tabBarActiveTintColor: '#0066cc',
          tabBarInactiveTintColor: 'gray',
          headerShown: false,
        })}
      >
        <Tab.Screen name="Explorar" component={App} />
        <Tab.Screen name="Autenticação" component={AuthScreen} />
        <Tab.Screen name="Sobre" component={AboutScreen} />
      </Tab.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  screenContainer: {
    flex: 1,
    padding: 20,
    backgroundColor: '#f5f5f5',
  },
  screenTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    color: '#0066cc',
  },
  screenSubtitle: {
    fontSize: 18,
    fontWeight: 'bold',
    marginTop: 15,
    marginBottom: 10,
    color: '#333',
  },
  screenText: {
    fontSize: 16,
    lineHeight: 24,
    color: '#444',
    marginBottom: 15,
  },
  authButton: {
    backgroundColor: '#333',
    padding: 15,
    borderRadius: 5,
    alignItems: 'center',
    marginTop: 20,
  },
  authButtonText: {
    color: 'white',
    fontWeight: 'bold',
    fontSize: 16,
  },
});
