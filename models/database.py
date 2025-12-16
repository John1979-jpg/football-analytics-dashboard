"""
Modulo de gestion de base de datos SQLite.
Maneja todas las operaciones de base de datos de la aplicacion.
"""
import sqlite3
import pandas as pd
from pathlib import Path
from contextlib import contextmanager
import streamlit as st


class DatabaseManager:
    """Gestor de base de datos SQLite."""
    
    def __init__(self, db_path):
        """
        Inicializa el gestor de base de datos.
        
        Args:
            db_path: Ruta al archivo de base de datos
        """
        self.db_path = Path(db_path)
        self._ensure_directory()
        self._initialize_database()
    
    def _ensure_directory(self):
        """Asegura que el directorio de la base de datos exista."""
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
    
    @contextmanager
    def _get_connection(self):
        """Context manager para conexiones a la base de datos."""
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()
    
    def _initialize_database(self):
        """Inicializa las tablas de la base de datos."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS equipos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    liga TEXT NOT NULL,
                    pais TEXT NOT NULL,
                    fundacion INTEGER,
                    estadio TEXT,
                    capacidad INTEGER
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jugadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    equipo_id INTEGER,
                    posicion TEXT,
                    nacionalidad TEXT,
                    edad INTEGER,
                    valor_mercado REAL,
                    goles INTEGER DEFAULT 0,
                    asistencias INTEGER DEFAULT 0,
                    partidos INTEGER DEFAULT 0,
                    FOREIGN KEY (equipo_id) REFERENCES equipos(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS partidos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha TEXT,
                    equipo_local_id INTEGER,
                    equipo_visitante_id INTEGER,
                    goles_local INTEGER,
                    goles_visitante INTEGER,
                    competicion TEXT,
                    temporada TEXT,
                    FOREIGN KEY (equipo_local_id) REFERENCES equipos(id),
                    FOREIGN KEY (equipo_visitante_id) REFERENCES equipos(id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS estadisticas_equipo (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    equipo_id INTEGER,
                    temporada TEXT,
                    partidos_jugados INTEGER,
                    victorias INTEGER,
                    empates INTEGER,
                    derrotas INTEGER,
                    goles_favor INTEGER,
                    goles_contra INTEGER,
                    puntos INTEGER,
                    posesion_media REAL,
                    tiros_partido REAL,
                    pases_completados REAL,
                    FOREIGN KEY (equipo_id) REFERENCES equipos(id)
                )
            ''')
            
            conn.commit()
            
            cursor.execute("SELECT COUNT(*) FROM equipos")
            if cursor.fetchone()[0] == 0:
                self._insert_sample_data(cursor)
                conn.commit()
    
    def _insert_sample_data(self, cursor):
        """Inserta datos de ejemplo en la base de datos."""
        equipos = [
            ('Real Madrid', 'La Liga', 'Espana', 1902, 'Santiago Bernabeu', 81044),
            ('FC Barcelona', 'La Liga', 'Espana', 1899, 'Spotify Camp Nou', 99354),
            ('Atletico Madrid', 'La Liga', 'Espana', 1903, 'Civitas Metropolitano', 68456),
            ('Sevilla FC', 'La Liga', 'Espana', 1890, 'Ramon Sanchez-Pizjuan', 43883),
            ('Real Sociedad', 'La Liga', 'Espana', 1909, 'Reale Arena', 39500),
            ('Real Betis', 'La Liga', 'Espana', 1907, 'Benito Villamarin', 60721),
            ('Villarreal CF', 'La Liga', 'Espana', 1923, 'Estadio de la Ceramica', 23500),
            ('Athletic Bilbao', 'La Liga', 'Espana', 1898, 'San Mames', 53289),
            ('Valencia CF', 'La Liga', 'Espana', 1919, 'Mestalla', 49430),
            ('Osasuna', 'La Liga', 'Espana', 1920, 'El Sadar', 23516),
        ]
        cursor.executemany(
            'INSERT INTO equipos (nombre, liga, pais, fundacion, estadio, capacidad) VALUES (?, ?, ?, ?, ?, ?)',
            equipos
        )
        
        jugadores = [
            ('Vinicius Junior', 1, 'Extremo Izquierdo', 'Brasil', 24, 180.0, 15, 7, 25),
            ('Jude Bellingham', 1, 'Centrocampista', 'Inglaterra', 21, 150.0, 12, 8, 28),
            ('Kylian Mbappe', 1, 'Delantero Centro', 'Francia', 26, 180.0, 18, 5, 26),
            ('Lamine Yamal', 2, 'Extremo Derecho', 'Espana', 17, 120.0, 8, 12, 27),
            ('Robert Lewandowski', 2, 'Delantero Centro', 'Polonia', 36, 15.0, 14, 4, 25),
            ('Pedri', 2, 'Centrocampista', 'Espana', 22, 100.0, 5, 9, 24),
            ('Antoine Griezmann', 3, 'Mediapunta', 'Francia', 33, 25.0, 10, 8, 26),
            ('Julian Alvarez', 3, 'Delantero Centro', 'Argentina', 24, 90.0, 12, 6, 27),
            ('Youssef En-Nesyri', 4, 'Delantero Centro', 'Marruecos', 27, 30.0, 9, 3, 23),
            ('Takefusa Kubo', 5, 'Extremo Derecho', 'Japon', 23, 60.0, 7, 6, 25),
            ('Isco', 6, 'Centrocampista', 'Espana', 32, 8.0, 4, 7, 22),
            ('Gerard Moreno', 7, 'Delantero Centro', 'Espana', 32, 20.0, 8, 4, 21),
            ('Nico Williams', 8, 'Extremo Izquierdo', 'Espana', 22, 70.0, 6, 10, 26),
            ('Hugo Duro', 9, 'Delantero Centro', 'Espana', 25, 25.0, 11, 3, 24),
            ('Ante Budimir', 10, 'Delantero Centro', 'Croacia', 33, 8.0, 13, 2, 27),
        ]
        cursor.executemany(
            '''INSERT INTO jugadores 
               (nombre, equipo_id, posicion, nacionalidad, edad, valor_mercado, goles, asistencias, partidos) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            jugadores
        )
        
        estadisticas = [
            (1, '2024-25', 28, 20, 5, 3, 58, 22, 65, 58.5, 16.2, 89.3),
            (2, '2024-25', 28, 19, 6, 3, 62, 28, 63, 62.1, 17.8, 90.1),
            (3, '2024-25', 28, 15, 8, 5, 42, 25, 53, 51.2, 13.4, 84.5),
            (4, '2024-25', 28, 12, 9, 7, 35, 32, 45, 48.3, 12.1, 82.7),
            (5, '2024-25', 28, 14, 7, 7, 38, 28, 49, 53.6, 14.2, 86.2),
            (6, '2024-25', 28, 13, 8, 7, 40, 35, 47, 55.4, 13.8, 85.9),
            (7, '2024-25', 28, 12, 10, 6, 36, 30, 46, 52.8, 14.5, 87.1),
            (8, '2024-25', 28, 14, 6, 8, 42, 32, 48, 50.1, 12.9, 83.4),
            (9, '2024-25', 28, 10, 10, 8, 32, 35, 40, 49.7, 11.8, 81.2),
            (10, '2024-25', 28, 11, 9, 8, 38, 36, 42, 45.2, 11.2, 79.8),
        ]
        cursor.executemany(
            '''INSERT INTO estadisticas_equipo 
               (equipo_id, temporada, partidos_jugados, victorias, empates, derrotas, 
                goles_favor, goles_contra, puntos, posesion_media, tiros_partido, pases_completados) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            estadisticas
        )
    
    @st.cache_data(ttl=3600)
    def get_equipos(_self):
        """Obtiene todos los equipos."""
        with _self._get_connection() as conn:
            df = pd.read_sql_query("SELECT * FROM equipos ORDER BY nombre", conn)
        return df
    
    @st.cache_data(ttl=3600)
    def get_jugadores(_self, equipo_id=None):
        """
        Obtiene jugadores, opcionalmente filtrados por equipo.
        
        Args:
            equipo_id: ID del equipo para filtrar (opcional)
        """
        query = '''
            SELECT j.*, e.nombre as equipo_nombre 
            FROM jugadores j 
            LEFT JOIN equipos e ON j.equipo_id = e.id
        '''
        if equipo_id:
            query += f' WHERE j.equipo_id = {equipo_id}'
        query += ' ORDER BY j.goles DESC'
        
        with _self._get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df
    
    @st.cache_data(ttl=3600)
    def get_estadisticas_equipos(_self, temporada='2024-25'):
        """
        Obtiene estadisticas de equipos para una temporada.
        
        Args:
            temporada: Temporada a consultar
        """
        query = '''
            SELECT e.nombre, e.liga, est.* 
            FROM estadisticas_equipo est
            JOIN equipos e ON est.equipo_id = e.id
            WHERE est.temporada = ?
            ORDER BY est.puntos DESC
        '''
        with _self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(temporada,))
        return df
    
    @st.cache_data(ttl=3600)
    def get_top_goleadores(_self, limit=10):
        """Obtiene los maximos goleadores."""
        query = '''
            SELECT j.nombre, j.posicion, j.nacionalidad, j.goles, j.asistencias, 
                   j.partidos, e.nombre as equipo
            FROM jugadores j
            JOIN equipos e ON j.equipo_id = e.id
            ORDER BY j.goles DESC
            LIMIT ?
        '''
        with _self._get_connection() as conn:
            df = pd.read_sql_query(query, conn, params=(limit,))
        return df
    
    @st.cache_data(ttl=3600)
    def get_resumen_liga(_self):
        """Obtiene un resumen general de la liga."""
        query = '''
            SELECT 
                COUNT(DISTINCT e.id) as total_equipos,
                COUNT(DISTINCT j.id) as total_jugadores,
                SUM(j.goles) as total_goles,
                SUM(j.asistencias) as total_asistencias,
                AVG(j.valor_mercado) as valor_medio,
                AVG(j.edad) as edad_media
            FROM equipos e
            LEFT JOIN jugadores j ON e.id = j.equipo_id
        '''
        with _self._get_connection() as conn:
            df = pd.read_sql_query(query, conn)
        return df.iloc[0].to_dict()
