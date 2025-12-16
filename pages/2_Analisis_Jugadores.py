"""
Pagina de Analisis de Jugadores.
Permite explorar estadisticas detalladas de jugadores de La Liga.
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


def render_top_scorers_chart(scorers_df):
    """Renderiza el grafico de maximos goleadores."""
    if scorers_df.empty:
        st.warning("No hay datos de goleadores disponibles")
        return
    
    fig = px.bar(
        scorers_df,
        x='jugador' if 'jugador' in scorers_df.columns else 'nombre',
        y='goles',
        color='equipo' if 'equipo' in scorers_df.columns else 'equipo_nombre',
        labels={
            'jugador': 'Jugador',
            'nombre': 'Jugador',
            'goles': 'Goles',
            'equipo': 'Equipo',
            'equipo_nombre': 'Equipo'
        },
        title='Maximos Goleadores de La Liga'
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=450,
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_goals_assists_scatter(players_df):
    """Renderiza grafico de dispersion goles vs asistencias."""
    if players_df.empty:
        return
    
    fig = px.scatter(
        players_df,
        x='goles',
        y='asistencias',
        size='partidos',
        color='posicion',
        hover_name='nombre',
        hover_data=['equipo_nombre', 'nacionalidad'],
        labels={
            'goles': 'Goles',
            'asistencias': 'Asistencias',
            'posicion': 'Posicion',
            'partidos': 'Partidos'
        },
        title='Relacion Goles - Asistencias por Jugador'
    )
    
    fig.update_layout(
        height=450
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_position_distribution(distribution_df):
    """Renderiza la distribucion por posiciones."""
    if distribution_df.empty:
        return
    
    fig = px.pie(
        distribution_df,
        values='Jugadores',
        names='Posicion',
        title='Distribucion de Jugadores por Posicion',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)


def render_nationality_chart(nationality_df):
    """Renderiza estadisticas por nacionalidad."""
    if nationality_df.empty:
        return
    
    fig = px.treemap(
        nationality_df,
        path=['Nacionalidad'],
        values='Jugadores',
        color='Goles Totales',
        color_continuous_scale='Blues',
        title='Jugadores por Nacionalidad'
    )
    
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)


def render_player_comparison(players_df, selected_players):
    """Renderiza comparacion entre jugadores seleccionados."""
    if len(selected_players) < 2:
        st.info("Seleccione al menos 2 jugadores para comparar")
        return
    
    comparison_df = players_df[players_df['nombre'].isin(selected_players)]
    
    if comparison_df.empty:
        return
    
    categories = ['goles', 'asistencias', 'partidos']
    
    fig = go.Figure()
    
    for _, player in comparison_df.iterrows():
        values = [player[cat] for cat in categories]
        values.append(values[0])
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories + [categories[0]],
            fill='toself',
            name=player['nombre']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True)
        ),
        showlegend=True,
        title='Comparacion de Jugadores',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)


def render_players_table(players_df):
    """Renderiza la tabla de jugadores."""
    if players_df.empty:
        st.warning("No hay datos de jugadores disponibles")
        return
    
    display_df = players_df.copy()
    
    if 'valor_mercado' in display_df.columns:
        display_df['valor_mercado'] = display_df['valor_mercado'].apply(lambda x: f"{x:.1f}M")
    
    column_config = {
        "nombre": st.column_config.TextColumn("Jugador", width="medium"),
        "posicion": st.column_config.TextColumn("Posicion", width="medium"),
        "nacionalidad": st.column_config.TextColumn("Nacionalidad", width="small"),
        "edad": st.column_config.NumberColumn("Edad", width="small"),
        "goles": st.column_config.NumberColumn("Goles", width="small"),
        "asistencias": st.column_config.NumberColumn("Asistencias", width="small"),
        "partidos": st.column_config.NumberColumn("Partidos", width="small"),
        "equipo_nombre": st.column_config.TextColumn("Equipo", width="medium"),
        "valor_mercado": st.column_config.TextColumn("Valor", width="small")
    }
    
    available_config = {k: v for k, v in column_config.items() if k in display_df.columns}
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        column_config=available_config,
        height=400
    )


def run():
    """Funcion principal de la pagina de Analisis de Jugadores."""
    auth = AuthManager()
    
    if not auth.is_authenticated():
        st.warning("Por favor, inicie sesion para acceder al analisis de jugadores")
        return
    
    st.title("Analisis de Jugadores")
    st.markdown("---")
    
    controller = StatsController()
    export_controller = ExportController()
    
    with st.sidebar:
        st.subheader("Filtros")
        
        equipos_df = controller.db.get_equipos()
        equipos_list = ['Todos'] + equipos_df['nombre'].tolist()
        selected_equipo = st.selectbox("Equipo", equipos_list)
        
        equipo_id = None
        if selected_equipo != 'Todos':
            equipo_row = equipos_df[equipos_df['nombre'] == selected_equipo]
            if not equipo_row.empty:
                equipo_id = equipo_row.iloc[0]['id']
    
    players_df = controller.get_players_analysis(equipo_id)
    scorers_df = controller.get_top_scorers_combined()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Jugadores", len(players_df))
    
    with col2:
        avg_goals = players_df['goles'].mean() if not players_df.empty else 0
        st.metric("Media Goles", f"{avg_goals:.1f}")
    
    with col3:
        avg_assists = players_df['asistencias'].mean() if not players_df.empty else 0
        st.metric("Media Asistencias", f"{avg_assists:.1f}")
    
    with col4:
        top_scorer = players_df.loc[players_df['goles'].idxmax()]['nombre'] if not players_df.empty else "-"
        st.metric("Maximo Goleador", top_scorer)
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["Goleadores", "Analisis", "Comparacion"])
    
    with tab1:
        render_top_scorers_chart(scorers_df)
        
        st.subheader("Tabla de Goleadores")
        st.dataframe(
            scorers_df,
            use_container_width=True,
            hide_index=True
        )
    
    with tab2:
        col_a, col_b = st.columns(2)
        
        with col_a:
            render_goals_assists_scatter(players_df)
        
        with col_b:
            position_dist = controller.get_position_distribution()
            render_position_distribution(position_dist)
        
        nationality_stats = controller.get_nationality_stats()
        render_nationality_chart(nationality_stats)
    
    with tab3:
        st.subheader("Comparar Jugadores")
        
        if not players_df.empty:
            player_names = players_df['nombre'].tolist()
            selected_players = st.multiselect(
                "Seleccione jugadores a comparar",
                player_names,
                default=player_names[:2] if len(player_names) >= 2 else player_names
            )
            
            render_player_comparison(players_df, selected_players)
    
    st.markdown("---")
    
    st.subheader("Todos los Jugadores")
    render_players_table(players_df)
    
    st.markdown("---")
    st.subheader("Exportar Datos")
    
    col_exp1, col_exp2 = st.columns(2)
    
    with col_exp1:
        if not players_df.empty:
            pdf_data = export_controller.generate_players_pdf(players_df)
            export_controller.render_export_button(pdf_data, "analisis_jugadores.pdf")
    
    with col_exp2:
        export_controller.render_print_button()
    
    st.markdown("---")
    st.caption("Datos de Base de Datos SQL y API Externa | Football Analytics Dashboard - John Triguero")


if __name__ == "__main__":
    run()
