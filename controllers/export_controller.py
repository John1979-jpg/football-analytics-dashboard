"""
Controlador de exportacion.
Gestiona la generacion de PDFs y exportacion de datos.
"""
import io
import streamlit as st
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd


class ExportController:
    """Controlador para exportacion de datos y generacion de PDFs."""
    
    def __init__(self):
        """Inicializa el controlador de exportacion."""
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Configura estilos personalizados para los documentos."""
        self.title_style = ParagraphStyle(
            'CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=20,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1E88E5'),
            fontName='Helvetica-Bold'
        )
        
        self.subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=self.styles['Heading2'],
            fontSize=14,
            spaceBefore=20,
            spaceAfter=15,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#424242'),
            fontName='Helvetica-Bold'
        )
        
        self.normal_style = ParagraphStyle(
            'CustomNormal',
            parent=self.styles['Normal'],
            fontSize=10,
            spaceAfter=10,
            alignment=TA_LEFT,
            textColor=colors.HexColor('#212121')
        )
        
        self.footer_style = ParagraphStyle(
            'CustomFooter',
            parent=self.styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
    
    def _create_table_from_df(self, df, col_widths=None):
        """
        Crea una tabla de ReportLab desde un DataFrame.
        
        Args:
            df: DataFrame a convertir
            col_widths: Anchos de columnas (opcional)
        
        Returns:
            Table: Objeto tabla de ReportLab
        """
        if df is None or df.empty:
            return None
        
        table_data = [df.columns.tolist()] + df.values.tolist()
        
        if col_widths is None:
            available_width = A4[0] - 3*cm
            num_cols = len(df.columns)
            col_widths = [available_width / num_cols] * num_cols
        
        table = Table(table_data, colWidths=col_widths)
        
        table_style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
            ('TOPPADDING', (0, 0), (-1, 0), 10),
            ('BACKGROUND', (0, 1), (-1, -1), colors.white),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#BDBDBD')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ])
        table.setStyle(table_style)
        
        return table
    
    def generate_classification_pdf(self, standings_df, metrics=None):
        """
        Genera un PDF con la clasificacion de La Liga.
        
        Args:
            standings_df: DataFrame con la clasificacion
            metrics: Metricas adicionales (opcional)
        
        Returns:
            bytes: Contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elements = []
        
        elements.append(Paragraph("La Liga - Clasificacion", self.title_style))
        
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f"Generado: {current_date}", self.footer_style))
        elements.append(Spacer(1, 20))
        
        if metrics:
            metrics_text = f"Temporada 2024-25 | Lider: {metrics.get('lider', '-')} ({metrics.get('lider_puntos', 0)} pts)"
            elements.append(Paragraph(metrics_text, self.normal_style))
            elements.append(Spacer(1, 15))
        
        elements.append(Paragraph("Tabla de Posiciones", self.subtitle_style))
        
        if standings_df is not None and not standings_df.empty:
            table = self._create_table_from_df(standings_df)
            if table:
                elements.append(table)
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Football Analytics Dashboard - John Triguero", self.footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_players_pdf(self, players_df, title="Analisis de Jugadores"):
        """
        Genera un PDF con el analisis de jugadores.
        
        Args:
            players_df: DataFrame con datos de jugadores
            title: Titulo del documento
        
        Returns:
            bytes: Contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=landscape(A4),
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elements = []
        
        elements.append(Paragraph(title, self.title_style))
        
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f"Generado: {current_date}", self.footer_style))
        elements.append(Spacer(1, 20))
        
        if players_df is not None and not players_df.empty:
            display_cols = ['nombre', 'posicion', 'nacionalidad', 'edad', 'goles', 'asistencias', 'partidos', 'equipo_nombre']
            available_cols = [col for col in display_cols if col in players_df.columns]
            
            if available_cols:
                display_df = players_df[available_cols].copy()
                display_df.columns = ['Jugador', 'Posicion', 'Nacionalidad', 'Edad', 'Goles', 'Asistencias', 'Partidos', 'Equipo'][:len(available_cols)]
                
                table = self._create_table_from_df(display_df)
                if table:
                    elements.append(table)
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Football Analytics Dashboard - John Triguero", self.footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    def generate_full_report_pdf(self, standings_df, players_df, metrics):
        """
        Genera un reporte completo en PDF.
        
        Args:
            standings_df: DataFrame con clasificacion
            players_df: DataFrame con jugadores
            metrics: Metricas del dashboard
        
        Returns:
            bytes: Contenido del PDF
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5*cm,
            leftMargin=1.5*cm,
            topMargin=2*cm,
            bottomMargin=2*cm
        )
        
        elements = []
        
        elements.append(Paragraph("Football Analytics Dashboard", self.title_style))
        elements.append(Paragraph("Reporte Completo - La Liga 2024-25", self.subtitle_style))
        
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f"Generado: {current_date}", self.footer_style))
        elements.append(Spacer(1, 30))
        
        elements.append(Paragraph("Resumen Ejecutivo", self.subtitle_style))
        
        if metrics:
            summary_data = [
                ['Metrica', 'Valor'],
                ['Total Equipos', str(metrics.get('total_equipos', '-'))],
                ['Total Jugadores', str(metrics.get('total_jugadores', '-'))],
                ['Total Goles', str(metrics.get('total_goles', '-'))],
                ['Lider', metrics.get('lider', '-')],
                ['Puntos Lider', str(metrics.get('lider_puntos', '-'))],
            ]
            
            summary_table = Table(summary_data, colWidths=[8*cm, 6*cm])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
            ]))
            elements.append(summary_table)
        
        elements.append(PageBreak())
        
        elements.append(Paragraph("Clasificacion", self.subtitle_style))
        if standings_df is not None and not standings_df.empty:
            table = self._create_table_from_df(standings_df.head(10))
            if table:
                elements.append(table)
        
        elements.append(PageBreak())
        
        elements.append(Paragraph("Maximos Goleadores", self.subtitle_style))
        if players_df is not None and not players_df.empty:
            top_scorers = players_df.nlargest(10, 'goles') if 'goles' in players_df.columns else players_df.head(10)
            display_cols = ['nombre', 'goles', 'asistencias', 'equipo_nombre']
            available_cols = [col for col in display_cols if col in top_scorers.columns]
            
            if available_cols:
                display_df = top_scorers[available_cols].copy()
                display_df.columns = ['Jugador', 'Goles', 'Asistencias', 'Equipo'][:len(available_cols)]
                table = self._create_table_from_df(display_df)
                if table:
                    elements.append(table)
        
        elements.append(Spacer(1, 30))
        elements.append(Paragraph("Football Analytics Dashboard - John Triguero", self.footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def render_print_button():
        """Renderiza el boton de imprimir pagina."""
        print_js = """
        <script>
        function printPage() {
            window.print();
        }
        </script>
        <button onclick="printPage()" style="
            background-color: #1E88E5;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 14px;
            margin: 5px;
        ">Imprimir Pagina</button>
        """
        st.markdown(print_js, unsafe_allow_html=True)
    
    @staticmethod
    def render_export_button(pdf_data, filename):
        """
        Renderiza el boton de exportar a PDF.
        
        Args:
            pdf_data: Datos del PDF
            filename: Nombre del archivo
        """
        st.download_button(
            label="Exportar a PDF",
            data=pdf_data,
            file_name=filename,
            mime="application/pdf",
            use_container_width=False
        )
