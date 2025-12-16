"""
Pagina de Dashboard principal.
Muestra metricas generales y visualizaciones de La Liga.
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


def render_metrics(metrics):
    """Renderiza las metricas principales del dashboard."""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Equipos",
            value=metrics['total_equipos'],
            delta=None
        )
    
    with col2:
        st.metric(
            label="Jugadores",
            value=metrics['total_jugadores'],
            delta=None
        )
    
    with col3:
        st.metric(
            label="Goles Totales",
            value=metrics['total_goles'],
            delta=None
        )
    
    with col4:
        st.metric(
            label="Lider",
            value=metrics['lider'],
            delta=f"{metrics['lider_puntos']} pts"
        )


def render_classification_chart(standings_df):
    """Renderiza el grafico de clasificacion."""
    if standings_df.empty:
        st.warning("No hay datos de clasificacion disponibles")
        return
    
    fig = px.bar(
        standings_df.head(10),
        x='equipo',
        y='pts',
        color='pts',
        color_continuous_scale='Blues',
        labels={'equipo': 'Equipo', 'pts': 'Puntos'},
        title='Clasificacion La Liga - Top 10'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=50, b=100)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_goals_analysis(standings_df):
    """Renderiza el analisis de goles."""
    if standings_df.empty:
        return
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        name='Goles a Favor',
        x=standings_df['equipo'],
        y=standings_df['gf'],
        marker_color='#4CAF50'
    ))
    
    fig.add_trace(go.Bar(
        name='Goles en Contra',
        x=standings_df['equipo'],
        y=standings_df['gc'],
        marker_color='#F44336'
    ))
    
    fig.update_layout(
        barmode='group',
        title='Goles a Favor vs Goles en Contra',
        xaxis_tickangle=-45,
        height=400,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_efficiency_scatter(stats_df):
    """Renderiza grafico de dispersion de eficiencia."""
    if stats_df.empty:
        return
    
    fig = px.scatter(
        stats_df,
        x='posesion_media',
        y='puntos',
        size='goles_favor',
        color='nombre',
        hover_data=['victorias', 'derrotas'],
        labels={
            'posesion_media': 'Posesion Media (%)',
            'puntos': 'Puntos',
            'nombre': 'Equipo'
        },
        title='Relacion Posesion - Puntos'
    )
    
    fig.update_layout(
        height=400,
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_upcoming_matches(matches_df):
    """Renderiza los proximos partidos."""
    if matches_df.empty:
        st.info("No hay partidos programados")
        return
    
    st.dataframe(
        matches_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "hora": "Hora",
            "local": "Local",
            "visitante": "Visitante",
            "competicion": "Competicion"
        }
    )


def render_recent_results(results_df):
    """Renderiza los resultados recientes."""
    if results_df.empty:
        st.info("No hay resultados disponibles")
        return
    
    st.dataframe(
        results_df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "fecha": st.column_config.DateColumn("Fecha", format="DD/MM/YYYY"),
            "local": "Local",
            "resultado": "Resultado",
            "visitante": "Visitante",
            "competicion": "Competicion"
        }
    )


def run():
    """Funcion principal de la pagina Dashboard."""
    auth = AuthManager()
    
    if not auth.is_authenticated():
        st.warning("Por favor, inicie sesion para acceder al dashboard")
        return
    
    st.title("Dashboard - La Liga")
    st.markdown("---")
    
    controller = StatsController()
    export_controller = ExportController()
    
    metrics = controller.get_dashboard_metrics()
    render_metrics(metrics)
    
    st.markdown("---")
    
    standings = controller.get_classification_data()
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_classification_chart(standings)
    
    with col2:
        render_goals_analysis(standings)
    
    st.markdown("---")
    
    efficiency_stats = controller.calculate_efficiency_stats()
    if not efficiency_stats.empty:
        render_efficiency_scatter(efficiency_stats)
    
    st.markdown("---")
    
    col3, col4 = st.columns(2)
    
    upcoming, recent = controller.get_matches_data()
    
    with col3:
        st.subheader("Proximos Partidos")
        render_upcoming_matches(upcoming)
    
    with col4:
        st.subheader("Resultados Recientes")
        render_recent_results(recent)
    
    st.markdown("---")
    st.subheader("Exportar Datos")
    
    col_exp1, col_exp2, col_exp3 = st.columns(3)
    
    with col_exp1:
        if not standings.empty:
            pdf_data = export_controller.generate_classification_pdf(standings, metrics)
            export_controller.render_export_button(pdf_data, "clasificacion_laliga.pdf")
    
    with col_exp2:
        export_controller.render_print_button()
    
    st.markdown("---")
    st.caption("Datos actualizados desde Base de Datos SQL y API Externa | Football Analytics Dashboard - John Triguero")


if __name__ == "__main__":
    run()
