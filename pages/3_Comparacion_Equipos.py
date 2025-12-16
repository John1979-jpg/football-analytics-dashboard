"""
Pagina de Comparacion de Equipos.
Permite comparar estadisticas entre dos equipos de La Liga.
"""
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from controllers import StatsController, ExportController
from common import AuthManager


def render_team_card(team_data):
    """Renderiza una tarjeta con informacion del equipo."""
    stats = team_data.get('stats', {})
    form = team_data.get('form', [])
    
    st.markdown(f"### {team_data['nombre']}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric("Puntos", stats.get('puntos', '-'))
        st.metric("Victorias", stats.get('victorias', '-'))
        st.metric("Goles a Favor", stats.get('goles_favor', '-'))
    
    with col2:
        st.metric("Posesion", f"{stats.get('posesion_media', 0):.1f}%")
        st.metric("Derrotas", stats.get('derrotas', '-'))
        st.metric("Goles en Contra", stats.get('goles_contra', '-'))
    
    st.markdown("**Forma Reciente:**")
    form_html = ""
    for result in form:
        if result == 'V':
            form_html += '<span style="background-color:#4CAF50;color:white;padding:5px 10px;margin:2px;border-radius:3px;">V</span>'
        elif result == 'E':
            form_html += '<span style="background-color:#FFC107;color:black;padding:5px 10px;margin:2px;border-radius:3px;">E</span>'
        elif result == 'D':
            form_html += '<span style="background-color:#F44336;color:white;padding:5px 10px;margin:2px;border-radius:3px;">D</span>'
        else:
            form_html += '<span style="background-color:#9E9E9E;color:white;padding:5px 10px;margin:2px;border-radius:3px;">?</span>'
    
    st.markdown(form_html, unsafe_allow_html=True)


def render_radar_comparison(comparison_data):
    """Renderiza grafico radar de comparacion."""
    team1 = comparison_data['team1']
    team2 = comparison_data['team2']
    
    stats1 = team1.get('stats', {})
    stats2 = team2.get('stats', {})
    
    if not stats1 or not stats2:
        st.warning("No hay suficientes datos para la comparacion")
        return
    
    categories = ['Puntos', 'Victorias', 'Goles Favor', 'Posesion', 'Pases']
    
    max_puntos = max(stats1.get('puntos', 1), stats2.get('puntos', 1))
    max_victorias = max(stats1.get('victorias', 1), stats2.get('victorias', 1))
    max_goles = max(stats1.get('goles_favor', 1), stats2.get('goles_favor', 1))
    
    values1 = [
        (stats1.get('puntos', 0) / max_puntos) * 100,
        (stats1.get('victorias', 0) / max_victorias) * 100,
        (stats1.get('goles_favor', 0) / max_goles) * 100,
        stats1.get('posesion_media', 0),
        stats1.get('pases_completados', 0)
    ]
    
    values2 = [
        (stats2.get('puntos', 0) / max_puntos) * 100,
        (stats2.get('victorias', 0) / max_victorias) * 100,
        (stats2.get('goles_favor', 0) / max_goles) * 100,
        stats2.get('posesion_media', 0),
        stats2.get('pases_completados', 0)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values1 + [values1[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=team1['nombre'],
        line_color='#1E88E5'
    ))
    
    fig.add_trace(go.Scatterpolar(
        r=values2 + [values2[0]],
        theta=categories + [categories[0]],
        fill='toself',
        name=team2['nombre'],
        line_color='#F44336'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Comparacion de Rendimiento',
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_bar_comparison(comparison_data):
    """Renderiza grafico de barras comparativo."""
    team1 = comparison_data['team1']
    team2 = comparison_data['team2']
    
    stats1 = team1.get('stats', {})
    stats2 = team2.get('stats', {})
    
    categories = ['Puntos', 'Victorias', 'Empates', 'Derrotas', 'GF', 'GC']
    
    values1 = [
        stats1.get('puntos', 0),
        stats1.get('victorias', 0),
        stats1.get('empates', 0),
        stats1.get('derrotas', 0),
        stats1.get('goles_favor', 0),
        stats1.get('goles_contra', 0)
    ]
    
    values2 = [
        stats2.get('puntos', 0),
        stats2.get('victorias', 0),
        stats2.get('empates', 0),
        stats2.get('derrotas', 0),
        stats2.get('goles_favor', 0),
        stats2.get('goles_contra', 0)
    ]
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name=team1['nombre'],
        x=categories,
        y=values1,
        marker_color='#1E88E5'
    ))
    
    fig.add_trace(go.Bar(
        name=team2['nombre'],
        x=categories,
        y=values2,
        marker_color='#F44336'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Comparacion de Estadisticas',
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_detailed_table(comparison_data):
    """Renderiza tabla detallada de comparacion."""
    team1 = comparison_data['team1']
    team2 = comparison_data['team2']
    
    stats1 = team1.get('stats', {})
    stats2 = team2.get('stats', {})
    
    comparison_df = pd.DataFrame({
        'Estadistica': [
            'Partidos Jugados',
            'Victorias',
            'Empates',
            'Derrotas',
            'Goles a Favor',
            'Goles en Contra',
            'Diferencia de Goles',
            'Puntos',
            'Posesion Media (%)',
            'Tiros por Partido',
            'Pases Completados (%)'
        ],
        team1['nombre']: [
            stats1.get('partidos_jugados', '-'),
            stats1.get('victorias', '-'),
            stats1.get('empates', '-'),
            stats1.get('derrotas', '-'),
            stats1.get('goles_favor', '-'),
            stats1.get('goles_contra', '-'),
            stats1.get('goles_favor', 0) - stats1.get('goles_contra', 0),
            stats1.get('puntos', '-'),
            f"{stats1.get('posesion_media', 0):.1f}",
            f"{stats1.get('tiros_partido', 0):.1f}",
            f"{stats1.get('pases_completados', 0):.1f}"
        ],
        team2['nombre']: [
            stats2.get('partidos_jugados', '-'),
            stats2.get('victorias', '-'),
            stats2.get('empates', '-'),
            stats2.get('derrotas', '-'),
            stats2.get('goles_favor', '-'),
            stats2.get('goles_contra', '-'),
            stats2.get('goles_favor', 0) - stats2.get('goles_contra', 0),
            stats2.get('puntos', '-'),
            f"{stats2.get('posesion_media', 0):.1f}",
            f"{stats2.get('tiros_partido', 0):.1f}",
            f"{stats2.get('pases_completados', 0):.1f}"
        ]
    })
    
    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
        height=450
    )


def run():
    """Funcion principal de la pagina de Comparacion de Equipos."""
    auth = AuthManager()
    
    if not auth.is_authenticated():
        st.warning("Por favor, inicie sesion para acceder a la comparacion de equipos")
        return
    
    st.title("Comparacion de Equipos")
    st.markdown("---")
    
    controller = StatsController()
    export_controller = ExportController()
    
    equipos_df = controller.db.get_equipos()
    equipos_list = equipos_df['nombre'].tolist()
    
    col1, col2 = st.columns(2)
    
    with col1:
        team1_name = st.selectbox(
            "Equipo 1",
            equipos_list,
            index=0,
            key="team1_select"
        )
    
    with col2:
        remaining_teams = [t for t in equipos_list if t != team1_name]
        team2_name = st.selectbox(
            "Equipo 2",
            remaining_teams,
            index=0,
            key="team2_select"
        )
    
    st.markdown("---")
    
    comparison_data = controller.get_comparison_data(team1_name, team2_name)
    
    col_card1, col_card2 = st.columns(2)
    
    with col_card1:
        render_team_card(comparison_data['team1'])
    
    with col_card2:
        render_team_card(comparison_data['team2'])
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Grafico Radar", "Barras", "Tabla Detallada"])
    
    with tab1:
        render_radar_comparison(comparison_data)
    
    with tab2:
        render_bar_comparison(comparison_data)
    
    with tab3:
        render_detailed_table(comparison_data)
    
    st.markdown("---")
    st.subheader("Exportar Comparacion")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        standings = controller.get_classification_data()
        metrics = controller.get_dashboard_metrics()
        players = controller.get_players_analysis()
        pdf_data = export_controller.generate_full_report_pdf(standings, players, metrics)
        export_controller.render_export_button(pdf_data, f"comparacion_{team1_name}_{team2_name}.pdf")
    
    with col_exp2:
        export_controller.render_print_button()
    
    st.markdown("---")
    st.caption("Datos de Base de Datos SQL y API Externa | Football Analytics Dashboard - John Triguero")


if __name__ == "__main__":
    run()
