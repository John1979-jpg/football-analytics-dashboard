"""
Controlador de estadisticas.
Gestiona la logica de procesamiento de datos estadisticos.
"""
import pandas as pd
import numpy as np
from models import DatabaseManager, FootballAPIClient
from common import Config


class StatsController:
    """Controlador para operaciones de estadisticas."""
    
    def __init__(self):
        """Inicializa el controlador con acceso a datos."""
        self.config = Config()
        self.db = DatabaseManager(self.config.db_full_path)
        self.api = FootballAPIClient(self.config.api_key)
    
    def get_dashboard_metrics(self):
        """
        Obtiene las metricas principales para el dashboard.
        
        Returns:
            dict: Metricas del dashboard
        """
        resumen = self.db.get_resumen_liga()
        standings = self.api.get_la_liga_standings()
        
        metrics = {
            'total_equipos': int(resumen['total_equipos']),
            'total_jugadores': int(resumen['total_jugadores']),
            'total_goles': int(resumen['total_goles']),
            'total_asistencias': int(resumen['total_asistencias']),
            'valor_medio': round(resumen['valor_medio'], 2),
            'edad_media': round(resumen['edad_media'], 1),
            'lider': standings.iloc[0]['equipo'] if not standings.empty else '-',
            'lider_puntos': int(standings.iloc[0]['pts']) if not standings.empty else 0,
        }
        return metrics
    
    def get_classification_data(self):
        """
        Obtiene datos de clasificacion combinando ambas fuentes.
        
        Returns:
            pd.DataFrame: Datos de clasificacion
        """
        api_standings = self.api.get_la_liga_standings()
        db_stats = self.db.get_estadisticas_equipos()
        
        if not api_standings.empty:
            return api_standings
        return db_stats
    
    def get_players_analysis(self, equipo_id=None):
        """
        Obtiene analisis de jugadores.
        
        Args:
            equipo_id: ID del equipo para filtrar
        
        Returns:
            pd.DataFrame: Datos de jugadores
        """
        return self.db.get_jugadores(equipo_id)
    
    def get_top_scorers_combined(self):
        """
        Obtiene goleadores combinando fuentes.
        
        Returns:
            pd.DataFrame: Datos de goleadores
        """
        api_scorers = self.api.get_top_scorers_api()
        db_scorers = self.db.get_top_goleadores()
        
        if not api_scorers.empty:
            return api_scorers
        return db_scorers
    
    def get_matches_data(self):
        """
        Obtiene datos de partidos proximos y resultados.
        
        Returns:
            tuple: (proximos_partidos, resultados_recientes)
        """
        upcoming = self.api.get_upcoming_matches()
        recent = self.api.get_recent_results()
        return upcoming, recent
    
    def calculate_efficiency_stats(self):
        """
        Calcula estadisticas de eficiencia de equipos.
        
        Returns:
            pd.DataFrame: Estadisticas de eficiencia
        """
        stats = self.db.get_estadisticas_equipos()
        
        if stats.empty:
            return pd.DataFrame()
        
        stats['goles_por_partido'] = (stats['goles_favor'] / stats['partidos_jugados']).round(2)
        stats['goles_contra_partido'] = (stats['goles_contra'] / stats['partidos_jugados']).round(2)
        stats['efectividad'] = ((stats['victorias'] / stats['partidos_jugados']) * 100).round(1)
        stats['puntos_por_partido'] = (stats['puntos'] / stats['partidos_jugados']).round(2)
        
        return stats
    
    def get_comparison_data(self, team1, team2):
        """
        Obtiene datos para comparar dos equipos.
        
        Args:
            team1: Nombre del primer equipo
            team2: Nombre del segundo equipo
        
        Returns:
            dict: Datos de comparacion
        """
        stats = self.db.get_estadisticas_equipos()
        
        team1_stats = stats[stats['nombre'] == team1]
        team2_stats = stats[stats['nombre'] == team2]
        
        comparison = {
            'team1': {
                'nombre': team1,
                'stats': team1_stats.iloc[0].to_dict() if not team1_stats.empty else {},
                'form': self.api.get_team_form(team1)
            },
            'team2': {
                'nombre': team2,
                'stats': team2_stats.iloc[0].to_dict() if not team2_stats.empty else {},
                'form': self.api.get_team_form(team2)
            }
        }
        return comparison
    
    def get_position_distribution(self):
        """
        Obtiene la distribucion de jugadores por posicion.
        
        Returns:
            pd.DataFrame: Distribucion por posicion
        """
        players = self.db.get_jugadores()
        
        if players.empty:
            return pd.DataFrame()
        
        distribution = players.groupby('posicion').agg({
            'nombre': 'count',
            'goles': 'sum',
            'asistencias': 'sum',
            'valor_mercado': 'mean'
        }).reset_index()
        
        distribution.columns = ['Posicion', 'Jugadores', 'Goles', 'Asistencias', 'Valor Medio']
        distribution['Valor Medio'] = distribution['Valor Medio'].round(2)
        
        return distribution
    
    def get_nationality_stats(self):
        """
        Obtiene estadisticas por nacionalidad.
        
        Returns:
            pd.DataFrame: Estadisticas por nacionalidad
        """
        players = self.db.get_jugadores()
        
        if players.empty:
            return pd.DataFrame()
        
        nationality_stats = players.groupby('nacionalidad').agg({
            'nombre': 'count',
            'goles': 'sum',
            'valor_mercado': 'sum'
        }).reset_index()
        
        nationality_stats.columns = ['Nacionalidad', 'Jugadores', 'Goles Totales', 'Valor Total']
        nationality_stats = nationality_stats.sort_values('Jugadores', ascending=False)
        
        return nationality_stats
