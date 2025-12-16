"""
Cliente para APIs externas de futbol.
Maneja las conexiones con APIs de datos de futbol.
"""
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


class FootballAPIClient:
    """Cliente para obtener datos de APIs externas de futbol."""
    
    API_FOOTBALL_DATA_URL = "https://api.football-data.org/v4"
    
    def __init__(self, api_key=None):
        """
        Inicializa el cliente de API.
        
        Args:
            api_key: Clave de API (opcional)
        """
        self.api_key = api_key
        self.headers = {}
        if api_key:
            self.headers['X-Auth-Token'] = api_key
    
    def _make_request(self, endpoint, params=None):
        """
        Realiza una peticion a la API.
        
        Args:
            endpoint: Endpoint de la API
            params: Parametros de la peticion
        
        Returns:
            dict: Respuesta JSON o None si hay error
        """
        try:
            url = f"{self.API_FOOTBALL_DATA_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
    
    @st.cache_data(ttl=3600)
    def get_la_liga_standings(_self):
        """
        Obtiene la clasificacion de La Liga desde datos simulados.
        Como la API requiere key, usamos datos de ejemplo actualizados.
        """
        standings_data = [
            {'posicion': 1, 'equipo': 'Real Madrid', 'pj': 28, 'pg': 20, 'pe': 5, 'pp': 3, 'gf': 58, 'gc': 22, 'dg': 36, 'pts': 65},
            {'posicion': 2, 'equipo': 'FC Barcelona', 'pj': 28, 'pg': 19, 'pe': 6, 'pp': 3, 'gf': 62, 'gc': 28, 'dg': 34, 'pts': 63},
            {'posicion': 3, 'equipo': 'Atletico Madrid', 'pj': 28, 'pg': 15, 'pe': 8, 'pp': 5, 'gf': 42, 'gc': 25, 'dg': 17, 'pts': 53},
            {'posicion': 4, 'equipo': 'Real Sociedad', 'pj': 28, 'pg': 14, 'pe': 7, 'pp': 7, 'gf': 38, 'gc': 28, 'dg': 10, 'pts': 49},
            {'posicion': 5, 'equipo': 'Athletic Bilbao', 'pj': 28, 'pg': 14, 'pe': 6, 'pp': 8, 'gf': 42, 'gc': 32, 'dg': 10, 'pts': 48},
            {'posicion': 6, 'equipo': 'Real Betis', 'pj': 28, 'pg': 13, 'pe': 8, 'pp': 7, 'gf': 40, 'gc': 35, 'dg': 5, 'pts': 47},
            {'posicion': 7, 'equipo': 'Villarreal CF', 'pj': 28, 'pg': 12, 'pe': 10, 'pp': 6, 'gf': 36, 'gc': 30, 'dg': 6, 'pts': 46},
            {'posicion': 8, 'equipo': 'Sevilla FC', 'pj': 28, 'pg': 12, 'pe': 9, 'pp': 7, 'gf': 35, 'gc': 32, 'dg': 3, 'pts': 45},
            {'posicion': 9, 'equipo': 'Osasuna', 'pj': 28, 'pg': 11, 'pe': 9, 'pp': 8, 'gf': 38, 'gc': 36, 'dg': 2, 'pts': 42},
            {'posicion': 10, 'equipo': 'Valencia CF', 'pj': 28, 'pg': 10, 'pe': 10, 'pp': 8, 'gf': 32, 'gc': 35, 'dg': -3, 'pts': 40},
        ]
        return pd.DataFrame(standings_data)
    
    @st.cache_data(ttl=1800)
    def get_upcoming_matches(_self):
        """
        Obtiene los proximos partidos (datos simulados).
        """
        today = datetime.now()
        matches_data = [
            {'fecha': (today + timedelta(days=1)).strftime('%Y-%m-%d'), 'hora': '21:00', 'local': 'Real Madrid', 'visitante': 'Sevilla FC', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=2)).strftime('%Y-%m-%d'), 'hora': '18:30', 'local': 'FC Barcelona', 'visitante': 'Athletic Bilbao', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=2)).strftime('%Y-%m-%d'), 'hora': '21:00', 'local': 'Atletico Madrid', 'visitante': 'Real Sociedad', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=3)).strftime('%Y-%m-%d'), 'hora': '16:00', 'local': 'Real Betis', 'visitante': 'Villarreal CF', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=3)).strftime('%Y-%m-%d'), 'hora': '18:30', 'local': 'Valencia CF', 'visitante': 'Osasuna', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=5)).strftime('%Y-%m-%d'), 'hora': '21:00', 'local': 'Sevilla FC', 'visitante': 'FC Barcelona', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=6)).strftime('%Y-%m-%d'), 'hora': '21:00', 'local': 'Real Sociedad', 'visitante': 'Real Madrid', 'competicion': 'La Liga'},
        ]
        return pd.DataFrame(matches_data)
    
    @st.cache_data(ttl=1800)
    def get_recent_results(_self):
        """
        Obtiene los resultados recientes (datos simulados).
        """
        today = datetime.now()
        results_data = [
            {'fecha': (today - timedelta(days=1)).strftime('%Y-%m-%d'), 'local': 'Real Madrid', 'resultado': '3 - 1', 'visitante': 'Osasuna', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=2)).strftime('%Y-%m-%d'), 'local': 'Athletic Bilbao', 'resultado': '2 - 2', 'visitante': 'FC Barcelona', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=2)).strftime('%Y-%m-%d'), 'local': 'Atletico Madrid', 'resultado': '1 - 0', 'visitante': 'Villarreal CF', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=3)).strftime('%Y-%m-%d'), 'local': 'Sevilla FC', 'resultado': '2 - 1', 'visitante': 'Valencia CF', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=4)).strftime('%Y-%m-%d'), 'local': 'Real Betis', 'resultado': '3 - 0', 'visitante': 'Real Sociedad', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=7)).strftime('%Y-%m-%d'), 'local': 'FC Barcelona', 'resultado': '4 - 2', 'visitante': 'Real Betis', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=7)).strftime('%Y-%m-%d'), 'local': 'Osasuna', 'resultado': '1 - 1', 'visitante': 'Athletic Bilbao', 'competicion': 'La Liga'},
        ]
        return pd.DataFrame(results_data)
    
    @st.cache_data(ttl=3600)
    def get_top_scorers_api(_self):
        """
        Obtiene los maximos goleadores de La Liga (datos simulados actualizados).
        """
        scorers_data = [
            {'jugador': 'Kylian Mbappe', 'equipo': 'Real Madrid', 'goles': 18, 'asistencias': 5, 'partidos': 26, 'minutos': 2180},
            {'jugador': 'Robert Lewandowski', 'equipo': 'FC Barcelona', 'goles': 14, 'asistencias': 4, 'partidos': 25, 'minutos': 2050},
            {'jugador': 'Vinicius Junior', 'equipo': 'Real Madrid', 'goles': 15, 'asistencias': 7, 'partidos': 25, 'minutos': 2100},
            {'jugador': 'Ante Budimir', 'equipo': 'Osasuna', 'goles': 13, 'asistencias': 2, 'partidos': 27, 'minutos': 2350},
            {'jugador': 'Julian Alvarez', 'equipo': 'Atletico Madrid', 'goles': 12, 'asistencias': 6, 'partidos': 27, 'minutos': 2280},
            {'jugador': 'Jude Bellingham', 'equipo': 'Real Madrid', 'goles': 12, 'asistencias': 8, 'partidos': 28, 'minutos': 2450},
            {'jugador': 'Hugo Duro', 'equipo': 'Valencia CF', 'goles': 11, 'asistencias': 3, 'partidos': 24, 'minutos': 1980},
            {'jugador': 'Antoine Griezmann', 'equipo': 'Atletico Madrid', 'goles': 10, 'asistencias': 8, 'partidos': 26, 'minutos': 2150},
            {'jugador': 'Youssef En-Nesyri', 'equipo': 'Sevilla FC', 'goles': 9, 'asistencias': 3, 'partidos': 23, 'minutos': 1850},
            {'jugador': 'Lamine Yamal', 'equipo': 'FC Barcelona', 'goles': 8, 'asistencias': 12, 'partidos': 27, 'minutos': 2300},
        ]
        return pd.DataFrame(scorers_data)
    
    @st.cache_data(ttl=3600)
    def get_team_form(_self, team_name):
        """
        Obtiene la forma reciente de un equipo.
        
        Args:
            team_name: Nombre del equipo
        """
        form_mapping = {
            'Real Madrid': ['V', 'V', 'V', 'E', 'V'],
            'FC Barcelona': ['V', 'E', 'V', 'V', 'D'],
            'Atletico Madrid': ['V', 'V', 'E', 'V', 'E'],
            'Real Sociedad': ['E', 'D', 'V', 'V', 'E'],
            'Athletic Bilbao': ['V', 'E', 'V', 'D', 'V'],
            'Real Betis': ['V', 'V', 'D', 'E', 'V'],
            'Villarreal CF': ['E', 'V', 'E', 'V', 'E'],
            'Sevilla FC': ['V', 'E', 'V', 'D', 'E'],
            'Osasuna': ['E', 'V', 'D', 'V', 'V'],
            'Valencia CF': ['D', 'E', 'V', 'E', 'D'],
        }
        return form_mapping.get(team_name, ['?', '?', '?', '?', '?'])
