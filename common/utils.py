"""
Modulo de utilidades generales.
Contiene funciones auxiliares utilizadas en toda la aplicacion.
"""
import io
import base64
from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import pandas as pd


class Utils:
    """Clase con utilidades generales de la aplicacion."""
    
    @staticmethod
    def format_date(date_str, input_format='%Y-%m-%d', output_format='%d/%m/%Y'):
        """Formatea una fecha de un formato a otro."""
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except (ValueError, TypeError):
            return date_str
    
    @staticmethod
    def format_number(number, decimals=2):
        """Formatea un numero con separador de miles."""
        try:
            return f"{float(number):,.{decimals}f}".replace(',', ' ')
        except (ValueError, TypeError):
            return str(number)
    
    @staticmethod
    def calculate_percentage(value, total):
        """Calcula el porcentaje de un valor respecto al total."""
        try:
            if total == 0:
                return 0.0
            return round((value / total) * 100, 2)
        except (ValueError, TypeError, ZeroDivisionError):
            return 0.0
    
    @staticmethod
    def dataframe_to_pdf(df, title, filename=None):
        """
        Convierte un DataFrame a PDF y retorna los bytes.
        
        Args:
            df: DataFrame de pandas a convertir
            title: Titulo del documento
            filename: Nombre del archivo (opcional)
        
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
        styles = getSampleStyleSheet()
        
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
            textColor=colors.HexColor('#1E88E5')
        )
        elements.append(Paragraph(title, title_style))
        
        date_style = ParagraphStyle(
            'DateStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        current_date = datetime.now().strftime('%d/%m/%Y %H:%M')
        elements.append(Paragraph(f"Generado: {current_date}", date_style))
        elements.append(Spacer(1, 20))
        
        if df is not None and not df.empty:
            table_data = [df.columns.tolist()] + df.values.tolist()
            
            col_widths = []
            available_width = A4[0] - 3*cm
            num_cols = len(df.columns)
            col_width = available_width / num_cols
            col_widths = [col_width] * num_cols
            
            table = Table(table_data, colWidths=col_widths)
            
            table_style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E88E5')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('TOPPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#F5F5F5')]),
                ('BOTTOMPADDING', (0, 1), (-1, -1), 8),
                ('TOPPADDING', (0, 1), (-1, -1), 8),
            ])
            table.setStyle(table_style)
            elements.append(table)
        
        elements.append(Spacer(1, 30))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            alignment=TA_CENTER,
            textColor=colors.grey
        )
        elements.append(Paragraph("Football Analytics Dashboard - John Triguero", footer_style))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
    
    @staticmethod
    def get_download_link(data, filename, text):
        """
        Genera un enlace de descarga para datos binarios.
        
        Args:
            data: Datos binarios a descargar
            filename: Nombre del archivo
            text: Texto del enlace
        
        Returns:
            str: HTML del enlace de descarga
        """
        b64 = base64.b64encode(data).decode()
        return f'<a href="data:application/pdf;base64,{b64}" download="{filename}">{text}</a>'
    
    @staticmethod
    def clean_dataframe(df):
        """Limpia un DataFrame eliminando valores nulos y duplicados."""
        if df is None:
            return pd.DataFrame()
        df_clean = df.drop_duplicates()
        df_clean = df_clean.fillna('-')
        return df_clean
