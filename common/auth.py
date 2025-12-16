"""
Modulo de autenticacion y manejo de sesiones.
Implementa el sistema de login y control de acceso.
"""
import streamlit as st
from .config import Config


class AuthManager:
    """Gestor de autenticacion y sesiones de usuario."""
    
    def __init__(self):
        self.config = Config()
        self._initialize_session_state()
    
    def _initialize_session_state(self):
        """Inicializa las variables de estado de sesion."""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'login_attempts' not in st.session_state:
            st.session_state.login_attempts = 0
    
    def validate_credentials(self, username, password):
        """
        Valida las credenciales del usuario.
        
        Args:
            username: Nombre de usuario
            password: Contrasena
        
        Returns:
            bool: True si las credenciales son validas
        """
        return (username == self.config.admin_user and 
                password == self.config.admin_password)
    
    def login(self, username, password):
        """
        Intenta iniciar sesion con las credenciales proporcionadas.
        
        Args:
            username: Nombre de usuario
            password: Contrasena
        
        Returns:
            bool: True si el login fue exitoso
        """
        if self.validate_credentials(username, password):
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.login_attempts = 0
            return True
        else:
            st.session_state.login_attempts += 1
            return False
    
    def logout(self):
        """Cierra la sesion del usuario."""
        st.session_state.authenticated = False
        st.session_state.username = None
    
    def is_authenticated(self):
        """
        Verifica si el usuario esta autenticado.
        
        Returns:
            bool: True si el usuario esta autenticado
        """
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """
        Obtiene el usuario actual.
        
        Returns:
            str: Nombre del usuario actual o None
        """
        return st.session_state.get('username', None)
    
    def get_login_attempts(self):
        """
        Obtiene el numero de intentos de login fallidos.
        
        Returns:
            int: Numero de intentos fallidos
        """
        return st.session_state.get('login_attempts', 0)
    
    def render_login_form(self):
        """Renderiza el formulario de login."""
        st.markdown("""
            <style>
            .login-container {
                max-width: 400px;
                margin: 0 auto;
                padding: 40px;
                background-color: #f8f9fa;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            }
            .login-title {
                text-align: center;
                color: #1E88E5;
                margin-bottom: 30px;
            }
            </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            st.markdown("<h2 class='login-title'>Iniciar Sesion</h2>", unsafe_allow_html=True)
            
            with st.form("login_form", clear_on_submit=False):
                username = st.text_input(
                    "Usuario",
                    placeholder="Ingrese su usuario",
                    key="login_username"
                )
                password = st.text_input(
                    "Contrasena",
                    type="password",
                    placeholder="Ingrese su contrasena",
                    key="login_password"
                )
                
                submit_button = st.form_submit_button(
                    "Acceder",
                    use_container_width=True
                )
                
                if submit_button:
                    if username and password:
                        if self.login(username, password):
                            st.success("Acceso concedido")
                            st.rerun()
                        else:
                            attempts = self.get_login_attempts()
                            st.error(f"Credenciales incorrectas. Intentos fallidos: {attempts}")
                    else:
                        st.warning("Por favor, complete todos los campos")
            
            st.markdown("---")
            st.caption("Usuario: admin | Contrasena: admin")
    
    def render_logout_button(self):
        """Renderiza el boton de logout en la barra lateral."""
        with st.sidebar:
            st.markdown("---")
            user = self.get_current_user()
            st.markdown(f"**Usuario:** {user}")
            if st.button("Cerrar Sesion", use_container_width=True):
                self.logout()
                st.rerun()
