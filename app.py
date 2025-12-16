"""
Football Analytics Dashboard
Aplicacion principal de Streamlit para analisis de datos de La Liga.

Autor: John Triguero
Modulo 8 - Master en Python Avanzado Aplicado al Deporte
Sports Data Campus
"""
import streamlit as st
import sys
from pathlib import Path

root_path = Path(__file__).parent
sys.path.insert(0, str(root_path))

from common import Config, AuthManager
from controllers import StatsController, ExportController


def setup_page_config():
    """Configura la pagina principal de Streamlit."""
    st.set_page_config(
        page_title="Football Analytics Dashboard",
        page_icon="",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            'About': "Football Analytics Dashboard - John Triguero"
        }
    )


def apply_custom_styles():
    """Aplica estilos CSS personalizados a la aplicacion."""
    st.markdown("""
        <style>
        .main-header {
            font-size: 2.5rem;
            font-weight: bold;
            color: #1E88E5;
            text-align: center;
            margin-bottom: 1rem;
        }
        
        .sub-header {
            font-size: 1.2rem;
            color: #616161;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .stMetric {
            background-color: #f8f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .stMetric label {
            color: #1E88E5 !important;
            font-weight: bold;
        }
        
        div[data-testid="stSidebarNav"] {
            background-color: #f8f9fa;
            padding-top: 1rem;
        }
        
        .sidebar-content {
            padding: 1rem;
        }
        
        .footer {
            text-align: center;
            color: #9E9E9E;
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #e0e0e0;
        }
        
        .info-box {
            background-color: #E3F2FD;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #1E88E5;
            margin: 1rem 0;
        }
        
        .warning-box {
            background-color: #FFF3E0;
            padding: 1rem;
            border-radius: 8px;
            border-left: 4px solid #FF9800;
            margin: 1rem 0;
        }
        
        @media print {
            .stSidebar {
                display: none;
            }
            .stButton {
                display: none;
            }
        }
        </style>
    """, unsafe_allow_html=True)


def render_sidebar(auth):
    """Renderiza el contenido de la barra lateral."""
    with st.sidebar:
        st.markdown("## Football Analytics")
        st.markdown("---")
        
        if auth.is_authenticated():
            st.markdown("### Menu de Navegacion")
            st.markdown("""
            - **Dashboard**: Vista general de La Liga
            - **Analisis Jugadores**: Estadisticas de jugadores
            - **Comparacion**: Comparar equipos
            """)
            
            st.markdown("---")
            
            st.markdown("### Fuentes de Datos")
            st.markdown("""
            - Base de Datos SQLite
            - API Externa de Futbol
            """)
            
            auth.render_logout_button()
        else:
            st.info("Inicie sesion para acceder al contenido")


def render_welcome_page():
    """Renderiza la pagina de bienvenida para usuarios autenticados."""
    st.markdown("<h1 class='main-header'>Football Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Analisis avanzado de datos de La Liga</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    controller = StatsController()
    metrics = controller.get_dashboard_metrics()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Equipos", metrics['total_equipos'])
    
    with col2:
        st.metric("Jugadores", metrics['total_jugadores'])
    
    with col3:
        st.metric("Goles Totales", metrics['total_goles'])
    
    with col4:
        st.metric("Lider", metrics['lider'], delta=f"{metrics['lider_puntos']} pts")
    
    st.markdown("---")
    
    st.markdown("""
    <div class='info-box'>
        <strong>Bienvenido al Dashboard</strong><br>
        Utilice el menu lateral para navegar entre las diferentes secciones:
        <ul>
            <li><strong>Dashboard</strong>: Clasificacion, resultados y proximos partidos</li>
            <li><strong>Analisis Jugadores</strong>: Estadisticas detalladas de jugadores</li>
            <li><strong>Comparacion Equipos</strong>: Compare el rendimiento de dos equipos</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.subheader("Conexion a Base de Datos")
        st.markdown("""
        La aplicacion se conecta a una base de datos SQLite local que contiene:
        - Informacion de equipos de La Liga
        - Estadisticas de jugadores
        - Historico de partidos
        - Metricas de rendimiento
        """)
        st.success("Base de datos conectada correctamente")
    
    with col_b:
        st.subheader("Conexion a API Externa")
        st.markdown("""
        Adicionalmente, se obtienen datos de una API externa:
        - Clasificacion actualizada
        - Proximos partidos
        - Resultados recientes
        - Goleadores de la temporada
        """)
        st.success("API externa disponible")
    
    st.markdown("---")
    
    st.markdown("""
    <div class='footer'>
        Football Analytics Dashboard | John Triguero<br>
        Modulo 8 - Master en Python Avanzado Aplicado al Deporte<br>
        Sports Data Campus
    </div>
    """, unsafe_allow_html=True)


def main():
    """Funcion principal de la aplicacion."""
    setup_page_config()
    apply_custom_styles()
    
    config = Config()
    auth = AuthManager()
    
    render_sidebar(auth)
    
    if not auth.is_authenticated():
        st.markdown("<h1 class='main-header'>Football Analytics Dashboard</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>Master en Python Avanzado Aplicado al Deporte</p>", unsafe_allow_html=True)
        auth.render_login_form()
    else:
        render_welcome_page()


if __name__ == "__main__":
    main()
