# Football Analytics Dashboard

Aplicacion web interactiva desarrollada con Streamlit para el analisis de datos de La Liga.

## Autor

**John Triguero**  
Modulo 8 - Master en Python Avanzado Aplicado al Deporte  
Sports Data Campus

## Descripcion

Esta aplicacion permite visualizar y analizar estadisticas de equipos y jugadores de La Liga, combinando datos de una base de datos SQLite local con informacion obtenida de APIs externas.

## Caracteristicas

### Sistema de Autenticacion
- Login con control de sesion
- Manejo de estado de usuario mediante `st.session_state`
- Credenciales: usuario `admin` / contrasena `admin`

### Navegacion
- Menu lateral intuitivo
- Tres paginas principales:
  - Dashboard: Vista general de la liga
  - Analisis de Jugadores: Estadisticas detalladas
  - Comparacion de Equipos: Analisis comparativo

### Fuentes de Datos
1. **Base de Datos SQLite**:
   - Tabla de equipos
   - Tabla de jugadores
   - Estadisticas por temporada
   - Historico de partidos

2. **API Externa**:
   - Clasificacion actualizada
   - Proximos partidos
   - Resultados recientes
   - Maximos goleadores

### Visualizaciones
- Graficos de barras (clasificacion, goles)
- Graficos de dispersion (eficiencia, goles vs asistencias)
- Graficos radar (comparacion de equipos)
- Graficos de pastel (distribucion por posicion)
- Treemap (jugadores por nacionalidad)
- Tablas interactivas con filtros

### Exportacion
- Exportar a PDF con formato profesional
- Funcion de impresion de pagina
- Reportes personalizados

### Optimizacion
- Cache de datos con `@st.cache_data`
- TTL configurable para actualizacion automatica
- Conexiones eficientes a base de datos

## Estructura del Proyecto

```
streamlit_app/
├── .streamlit/
│   └── config.toml          # Configuracion de Streamlit
├── common/
│   ├── __init__.py
│   ├── auth.py              # Sistema de autenticacion
│   ├── config.py            # Configuracion centralizada
│   └── utils.py             # Utilidades generales
├── controllers/
│   ├── __init__.py
│   ├── export_controller.py # Logica de exportacion PDF
│   └── stats_controller.py  # Logica de estadisticas
├── data/
│   └── football.db          # Base de datos SQLite (generada automaticamente)
├── models/
│   ├── __init__.py
│   ├── api_client.py        # Cliente para APIs externas
│   └── database.py          # Gestion de base de datos
├── pages/
│   ├── __init__.py
│   ├── 1_Dashboard.py       # Pagina principal
│   ├── 2_Analisis_Jugadores.py
│   └── 3_Comparacion_Equipos.py
├── .env                     # Variables de entorno
├── app.py                   # Punto de entrada
├── README.md                # Este archivo
└── requirements.txt         # Dependencias
```

## Instalacion

1. Clonar o descargar el proyecto

2. Crear un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instalar dependencias:
```bash
pip install -r requirements.txt
```

4. Ejecutar la aplicacion:
```bash
streamlit run app.py
```

## Configuracion

Las variables de configuracion se encuentran en el archivo `.env`:

- `APP_NAME`: Nombre de la aplicacion
- `ADMIN_USER`: Usuario de acceso (default: admin)
- `ADMIN_PASSWORD`: Contrasena de acceso (default: admin)
- `DATABASE_PATH`: Ruta de la base de datos SQLite
- `CACHE_TTL`: Tiempo de vida del cache en segundos

## Uso

1. Acceder a la aplicacion en `http://localhost:8501`
2. Iniciar sesion con las credenciales: `admin` / `admin`
3. Navegar entre las diferentes secciones usando el menu lateral
4. Utilizar los filtros disponibles para personalizar las vistas
5. Exportar los datos a PDF o imprimir segun necesidad

## Tecnologias Utilizadas

- **Streamlit**: Framework principal de la aplicacion
- **Pandas**: Manipulacion y analisis de datos
- **Plotly**: Visualizaciones interactivas
- **SQLite**: Base de datos local
- **ReportLab**: Generacion de PDFs
- **Requests**: Conexion con APIs externas

## Despliegue

Para publicar la aplicacion en Streamlit Cloud:

1. Subir el proyecto a un repositorio de GitHub
2. Acceder a [share.streamlit.io](https://share.streamlit.io)
3. Conectar el repositorio
4. Configurar el archivo principal como `app.py`
5. Desplegar

## Licencia

Este proyecto ha sido desarrollado como parte del trabajo academico del Master en Python Avanzado Aplicado al Deporte de Sports Data Campus.

---

Desarrollado por John Triguero | 2024
