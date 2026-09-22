import streamlit as st
from supabase import Client, create_client


def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)


def render_auth_screen() -> bool:
    """Muestra la pantalla de acceso.

    Retorna True si el usuario está autenticado, False en caso contrario.
    """
    # 1. Verificar si ya existe una sesión en memoria
    if "user" in st.session_state and st.session_state["user"] is not None:
        # Botón discreto en la barra lateral para cerrar sesión
        with st.sidebar:
            st.write(
                f"👤 **{st.session_state['user'].email.split('@')[0]}**"
            )
            if st.button("Cerrar Sesión", use_container_width=True):
                st.session_state["user"] = None
                st.session_state["session"] = None
                st.rerun()
        return True

    # 2. Si no hay sesión, inicializar cliente y mostrar formulario centrado
    try:
        supabase = init_supabase()
    except Exception as e:
        st.error(f"Error al conectar con Supabase: {e}")
        return False

    st.markdown(
        """
        <div style="text-align: center; margin-top: 2rem; margin-bottom: 2rem;">
            <h2 style="color: #4da6ff;">Suite Clínica & Biomecánica 3D</h2>
            <p style="color: #94a3b8; font-size: 0.95rem;">Ingreso profesional exclusivo. Inicia sesión o crea tu cuenta.</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    _, col, _ = st.columns([1, 1.4, 1])

    with col:
        modo = st.radio(
            "Acción",
            ["Iniciar Sesión", "Registrarse"],
            horizontal=True,
            label_visibility="collapsed",
        )
        email = st.text_input("Correo Electrónico", placeholder="nombre@ejemplo.com")
        password = st.text_input(
            "Contraseña", type="password", placeholder="Mínimo 6 caracteres"
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if modo == "Iniciar Sesión":
            if st.button("Ingresar", type="primary", use_container_width=True):
                if not email or not password:
                    st.warning("Ingresa tu correo y contraseña.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password(
                            {"email": email.strip(), "password": password}
                        )
                        st.session_state["user"] = res.user
                        st.session_state["session"] = res.session
                        st.success("Acceso concedido.")
                        st.rerun()
                    except Exception as err:
                        st.error(f"Credenciales no válidas: {err}")

        else:
            if st.button("Crear Cuenta", type="primary", use_container_width=True):
                if not email or not password:
                    st.warning("Completa todos los campos.")
                elif len(password) < 6:
                    st.warning("La contraseña debe tener al menos 6 caracteres.")
                else:
                    try:
                        res = supabase.auth.sign_up(
                            {"email": email.strip(), "password": password}
                        )
                        st.success(
                            "Cuenta registrada. Si Supabase requiere confirmación de email, revisa tu bandeja de entrada."
                        )
                    except Exception as err:
                        st.error(f"Error en registro: {err}")

    return False