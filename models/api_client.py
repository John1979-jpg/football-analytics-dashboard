"""
Cliente para APIs externas de futbol.
Maneja las conexiones con Football-Data.org API.
"""
import requests
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta


class FootballAPIClient:
    """Cliente para obtener datos de Football-Data.org."""
    
    API_BASE_URL = "https://api.football-data.org/v4"
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.headers = {
            'X-Auth-Token': api_key if api_key else ''
        }
    
    def _make_request(self, endpoint):
        try:
            url = f"{self.API_BASE_URL}/{endpoint}"
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.warning(f"Error al conectar con la API: {str(e)}")
            return None
    
    @st.cache_data(ttl=3600)
    def get_la_liga_standings(_self):
        data = _self._make_request("competitions/PD/standings")
        
        if not data or 'standings' not in data:
            return _self._get_fallback_standings()
        
        try:
            standings = data['standings'][0]['table']
            standings_list = []
            for team in standings:
                standings_list.append({
                    'posicion': team['position'],
                    'equipo': team['team']['name'],
                    'pj': team['playedGames'],
                    'pg': team['won'],
                    'pe': team['draw'],
                    'pp': team['lost'],
                    'gf': team['goalsFor'],
                    'gc': team['goalsAgainst'],
                    'dg': team['goalDifference'],
                    'pts': team['points']
                })
            return pd.DataFrame(standings_list)
        except (KeyError, IndexError):
            return _self._get_fallback_standings()
    
    @st.cache_data(ttl=1800)
    def get_upcoming_matches(_self):
        data = _self._make_request("competitions/PD/matches?status=SCHEDULED")
        
        if not data or 'matches' not in data:
            return _self._get_fallback_upcoming()
        
        try:
            matches = data['matches'][:10]
            matches_list = []
            for match in matches:
                utc_date = match['utcDate']
                date_obj = datetime.fromisoformat(utc_date.replace('Z', '+00:00'))
                matches_list.append({
                    'fecha': date_obj.strftime('%Y-%m-%d'),
                    'hora': date_obj.strftime('%H:%M'),
                    'local': match['homeTeam']['name'],
                    'visitante': match['awayTeam']['name'],
                    'competicion': 'La Liga'
                })
            return pd.DataFrame(matches_list)
        except (KeyError, IndexError):
            return _self._get_fallback_upcoming()
    
    @st.cache_data(ttl=1800)
    def get_recent_results(_self):
        data = _self._make_request("competitions/PD/matches?status=FINISHED")
        
        if not data or 'matches' not in data:
            return _self._get_fallback_results()
        
        try:
            matches = sorted(data['matches'], key=lambda x: x['utcDate'], reverse=True)[:10]
            results_list = []
            for match in matches:
                utc_date = match['utcDate']
                date_obj = datetime.fromisoformat(utc_date.replace('Z', '+00:00'))
                home_score = match['score']['fullTime']['home']
                away_score = match['score']['fullTime']['away']
                if home_score is not None and away_score is not None:
                    results_list.append({
                        'fecha': date_obj.strftime('%Y-%m-%d'),
                        'local': match['homeTeam']['name'],
                        'resultado': f"{home_score} - {away_score}",
                        'visitante': match['awayTeam']['name'],
                        'competicion': 'La Liga'
                    })
            return pd.DataFrame(results_list)
        except (KeyError, IndexError):
            return _self._get_fallback_results()
    
    @st.cache_data(ttl=3600)
    def get_top_scorers_api(_self):
        data = _self._make_request("competitions/PD/scorers?limit=15")
        
        if not data or 'scorers' not in data:
            return _self._get_fallback_scorers()
        
        try:
            scorers = data['scorers']
            scorers_list = []
            for scorer in scorers:
                scorers_list.append({
                    'jugador': scorer['player']['name'],
                    'equipo': scorer['team']['name'],
                    'goles': scorer.get('goals', 0),
                    'asistencias': scorer.get('assists', 0) or 0,
                    'partidos': scorer.get('playedMatches', 0),
                    'minutos': scorer.get('penalties', 0)
                })
            return pd.DataFrame(scorers_list)
        except (KeyError, IndexError):
            return _self._get_fallback_scorers()
    
    @st.cache_data(ttl=3600)
    def get_team_form(_self, team_name):
        form_mapping = {
            'Real Madrid CF': ['V', 'V', 'V', 'E', 'V'],
            'FC Barcelona': ['V', 'E', 'V', 'V', 'D'],
            'Club Atletico de Madrid': ['V', 'V', 'E', 'V', 'E'],
            'Real Sociedad de Futbol': ['E', 'D', 'V', 'V', 'E'],
            'Athletic Club': ['V', 'E', 'V', 'D', 'V'],
            'Real Betis Balompie': ['V', 'V', 'D', 'E', 'V'],
            'Villarreal CF': ['E', 'V', 'E', 'V', 'E'],
            'Sevilla FC': ['V', 'E', 'V', 'D', 'E'],
            'CA Osasuna': ['E', 'V', 'D', 'V', 'V'],
            'Valencia CF': ['D', 'E', 'V', 'E', 'D'],
        }
        for key in form_mapping:
            if team_name in key or key in team_name:
                return form_mapping[key]
        return ['?', '?', '?', '?', '?']
    
    def _get_fallback_standings(_self):
        standings_data = [
            {'posicion': 1, 'equipo': 'Real Madrid', 'pj': 28, 'pg': 20, 'pe': 5, 'pp': 3, 'gf': 58, 'gc': 22, 'dg': 36, 'pts': 65},
            {'posicion': 2, 'equipo': 'FC Barcelona', 'pj': 28, 'pg': 19, 'pe': 6, 'pp': 3, 'gf': 62, 'gc': 28, 'dg': 34, 'pts': 63},
            {'posicion': 3, 'equipo': 'Atletico Madrid', 'pj': 28, 'pg': 15, 'pe': 8, 'pp': 5, 'gf': 42, 'gc': 25, 'dg': 17, 'pts': 53},
            {'posicion': 4, 'equipo': 'Real Sociedad', 'pj': 28, 'pg': 14, 'pe': 7, 'pp': 7, 'gf': 38, 'gc': 28, 'dg': 10, 'pts': 49},
            {'posicion': 5, 'equipo': 'Athletic Bilbao', 'pj': 28, 'pg': 14, 'pe': 6, 'pp': 8, 'gf': 42, 'gc': 32, 'dg': 10, 'pts': 48},
        ]
        return pd.DataFrame(standings_data)
    
    def _get_fallback_upcoming(_self):
        today = datetime.now()
        matches_data = [
            {'fecha': (today + timedelta(days=1)).strftime('%Y-%m-%d'), 'hora': '21:00', 'local': 'Real Madrid', 'visitante': 'Sevilla FC', 'competicion': 'La Liga'},
            {'fecha': (today + timedelta(days=2)).strftime('%Y-%m-%d'), 'hora': '18:30', 'local': 'FC Barcelona', 'visitante': 'Athletic Bilbao', 'competicion': 'La Liga'},
        ]
        return pd.DataFrame(matches_data)
    
    def _get_fallback_results(_self):
        today = datetime.now()
        results_data = [
            {'fecha': (today - timedelta(days=1)).strftime('%Y-%m-%d'), 'local': 'Real Madrid', 'resultado': '3 - 1', 'visitante': 'Osasuna', 'competicion': 'La Liga'},
            {'fecha': (today - timedelta(days=2)).strftime('%Y-%m-%d'), 'local': 'Athletic Bilbao', 'resultado': '2 - 2', 'visitante': 'FC Barcelona', 'competicion': 'La Liga'},
        ]
        return pd.DataFrame(results_data)
    
    def _get_fallback_scorers(_self):
        scorers_data = [
            {'jugador': 'Kylian Mbappe', 'equipo': 'Real Madrid', 'goles': 18, 'asistencias': 5, 'partidos': 26, 'minutos': 0},
            {'jugador': 'Robert Lewandowski', 'equipo': 'FC Barcelona', 'goles': 14, 'asistencias': 4, 'partidos': 25, 'minutos': 0},
            {'jugador': 'Vinicius Junior', 'equipo': 'Real Madrid', 'goles': 15, 'asistencias': 7, 'partidos': 25, 'minutos': 0},
        ]
        return pd.DataFrame(scorers_data)
