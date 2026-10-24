"""
auth.py
Módulo de Autenticación Profesional y Persistencia de Sesión Biomecánica.
Soporta persistencia multicapa (st.query_params, cookies seguras HTTP y localStorage)
con cifrado simétrico autenticado Fernet (AES-128-CBC + HMAC-SHA256).
"""

import base64
from datetime import datetime
import hashlib
import json
import ssl
from typing import Any, Dict, Optional, Tuple

from cryptography.fernet import Fernet
import httpx
import streamlit as st
import streamlit.components.v1 as components
from supabase import Client, ClientOptions, create_client

AUTH_TOKEN_PARAM = "auth_token"
AUTH_COOKIE_NAME = "sacro_auth_token"
TOKEN_MAX_AGE_DAYS = 14


class CachedUser:
    """Representación liviana de usuario autenticado para contingencia de red."""

    def __init__(self, user_id: str, email: str):
        self.id = user_id
        self.email = email
        self.user_metadata: Dict[str, Any] = {}


def _get_cipher() -> Fernet:
    """Obtiene el cifrador Fernet a partir del secreto configurado."""
    secret = st.secrets.get("AUTH_SECRET") or st.secrets.get(
        "SUPABASE_KEY", "sacro_clinica_master_key_default"
    )
    key_bytes = hashlib.sha256(secret.encode("utf-8")).digest()
    fernet_key = base64.urlsafe_b64encode(key_bytes)
    return Fernet(fernet_key)


def generar_token_sesion(session: Any, user: Any) -> str:
    """Genera un token cifrado URL-safe que encapsula la sesión del usuario."""
    f = _get_cipher()
    payload = {
        "user_id": getattr(user, "id", str(user)),
        "email": getattr(user, "email", ""),
        "access_token": getattr(session, "access_token", ""),
        "refresh_token": getattr(session, "refresh_token", ""),
        "created_at": datetime.now().timestamp(),
    }
    raw_json = json.dumps(payload).encode("utf-8")
    return f.encrypt(raw_json).decode("utf-8")


def descifrar_token_sesion(
    token_str: str, max_age_days: int = TOKEN_MAX_AGE_DAYS
) -> Optional[Dict[str, Any]]:
    """Descifra y valida un token de sesión. Retorna el payload o None si es inválido/expirado."""
    if not token_str or not isinstance(token_str, str):
        return None
    try:
        f = _get_cipher()
        ttl_seconds = max(1, max_age_days * 86400)
        decrypted = f.decrypt(token_str.strip().encode("utf-8"), ttl=ttl_seconds)
        payload = json.loads(decrypted.decode("utf-8"))

        # Validación explícita de vigencia basada en created_at
        if max_age_days <= 0:
            return None
        created_at = payload.get("created_at")
        if created_at is not None:
            if (datetime.now().timestamp() - created_at) > (max_age_days * 86400):
                return None

        return payload
    except Exception:
        return None


def es_error_red_dns(err: Exception) -> bool:
    """Detecta si la excepción corresponde a un fallo de red o resolución DNS ([Errno -2])."""
    err_msg = str(err).lower()
    tipo = type(err).__name__.lower()
    return (
        "errno -2" in err_msg
        or "name or service not known" in err_msg
        or "getaddrinfo failed" in err_msg
        or "errno 11001" in err_msg
        or "nodename nor servname provided" in err_msg
        or "connecterror" in tipo
        or "networkerror" in tipo
        or "timeoutexception" in tipo
        or "dns" in err_msg
    )


MSG_ERROR_CONEXION_SECRETS = (
    "Error de conexión con el servidor de autenticación. "
    "Verifique la URL de conexión en los secrets de Streamlit."
)


def init_supabase() -> Client:
    """Inicializa el cliente Supabase con soporte robusto de certificados SSL en Windows y limpieza de URL."""
    url = str(st.secrets.get("SUPABASE_URL", "")).strip().rstrip("/")
    key = str(st.secrets.get("SUPABASE_KEY", "")).strip()
    try:
        ssl_ctx = ssl.create_default_context()
        http_client = httpx.Client(verify=ssl_ctx)
        opts = ClientOptions(httpx_client=http_client)
        return create_client(url, key, options=opts)
    except Exception:
        return create_client(url, key)


def restaurar_sesion_desde_token(
    data: Dict[str, Any], supabase: Optional[Client]
) -> Tuple[Optional[Any], Optional[Any]]:
    """Restaura el usuario y sesión de Supabase a partir de los datos descifrados."""
    if not data:
        return None, None

    user_id = data.get("user_id")
    email = data.get("email")
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")

    if not user_id or not email:
        return None, None

    if supabase is not None:
        # 1. Intentar refrescar la sesión con el refresh_token
        if refresh_token:
            try:
                res = supabase.auth.refresh_session(refresh_token)
                if res and res.user:
                    return res.user, res.session
            except Exception:
                pass

        # 2. Intentar validar con get_user usando el access_token
        if access_token:
            try:
                user_res = supabase.auth.get_user(access_token)
                if user_res and user_res.user:
                    return user_res.user, None
            except Exception:
                pass

    # 3. Fallback: Si el token criptográfico firmado por nuestro servidor es válido
    # pero Supabase está momentáneamente fuera de línea o sin conectividad externa,
    # permitir el trabajo clínico usando el usuario verificado en el token.
    return CachedUser(user_id=user_id, email=email), None


def _guardar_storage_js(token: str):
    """Escribe el token en cookie y localStorage mediante script del navegador."""
    components.html(
        f"""
        <script>
        try {{
            const tok = "{token}";
            document.cookie = "{AUTH_COOKIE_NAME}=" + tok + "; path=/; max-age=1209600; SameSite=Lax";
            localStorage.setItem("{AUTH_COOKIE_NAME}", tok);
        }} catch(e) {{}}
        </script>
        """,
        height=0,
        width=0,
    )


def _limpiar_storage_js():
    """Limpia el token de cookies y localStorage en el navegador."""
    components.html(
        f"""
        <script>
        try {{
            document.cookie = "{AUTH_COOKIE_NAME}=; path=/; max-age=0; SameSite=Lax";
            localStorage.removeItem("{AUTH_COOKIE_NAME}");
            const u = new URL(window.location.href);
            u.searchParams.delete("{AUTH_TOKEN_PARAM}");
            window.history.replaceState({{}}, "", u.toString());
        }} catch(e) {{}}
        </script>
        """,
        height=0,
        width=0,
    )


def _intentar_recuperar_localstorage_js():
    """Si el usuario abrió la URL limpia sin query param, comprueba localStorage o hash de recuperación."""
    if st.session_state.get("logout_requested"):
        return
    components.html(
        f"""
        <script>
        try {{
            if (window.location.hash && window.location.hash.includes("access_token=")) {{
                const hashStr = window.location.hash.startsWith("#") ? window.location.hash.substring(1) : window.location.hash;
                const p = new URLSearchParams(hashStr);
                const at = p.get("access_token");
                const rt = p.get("refresh_token") || "";
                const ty = p.get("type") || "";
                if (at) {{
                    const u = new URL(window.location.href);
                    u.hash = "";
                    u.searchParams.set("sb_access_token", at);
                    if (rt) u.searchParams.set("sb_refresh_token", rt);
                    if (ty) u.searchParams.set("sb_auth_type", ty);
                    window.location.replace(u.toString());
                    return;
                }}
            }}
            const tok = localStorage.getItem("{AUTH_COOKIE_NAME}");
            if (tok && !window.location.search.includes("{AUTH_TOKEN_PARAM}=")) {{
                const u = new URL(window.location.href);
                u.searchParams.set("{AUTH_TOKEN_PARAM}", tok);
                window.location.replace(u.toString());
            }}
        }} catch(e) {{}}
        </script>
        """,
        height=0,
        width=0,
    )


def cerrar_sesion():
    """Cierra la sesión activa y elimina toda persistencia en URL, memoria, cookies y almacenamiento local."""
    st.session_state["user"] = None
    st.session_state["session"] = None
    st.session_state["logout_requested"] = True
    st.session_state["password_recovery_mode"] = False

    for param in [AUTH_TOKEN_PARAM, "code", "sb_access_token", "sb_refresh_token", "sb_auth_type"]:
        if param in st.query_params:
            del st.query_params[param]

    try:
        supabase = init_supabase()
        supabase.auth.sign_out()
    except Exception:
        pass

    _limpiar_storage_js()
    st.rerun()


def cambiar_contrasena(nueva_clave: str) -> Tuple[bool, str]:
    """Actualiza la contraseña del usuario actualmente autenticado en Supabase."""
    if not nueva_clave or len(nueva_clave) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    try:
        supabase = init_supabase()
        supabase.auth.update_user({"password": nueva_clave})
        return True, "Contraseña actualizada exitosamente."
    except Exception as e:
        if es_error_red_dns(e):
            return False, MSG_ERROR_CONEXION_SECRETS
        return False, f"Error al actualizar la contraseña: {e}"


def _render_sidebar_user():
    """Muestra información del usuario, cambio de contraseña y botón de cerrar sesión en la barra lateral."""
    user = st.session_state.get("user")
    if not user:
        return
    email = getattr(user, "email", "Usuario")
    username = email.split("@")[0] if "@" in email else email

    with st.sidebar:
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #334155; border-radius: 8px; padding: 10px 14px; margin-bottom: 12px;">
                <div style="font-size: 0.70rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.05em;">Sesión Profesional</div>
                <div style="font-size: 0.95rem; font-weight: 600; color: #38bdf8; overflow: hidden; text-overflow: ellipsis;">👤 {username}</div>
                <div style="font-size: 0.75rem; color: #64748b; overflow: hidden; text-overflow: ellipsis;">{email}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        is_rec = bool(st.session_state.get("password_recovery_mode", False))
        with st.expander("🔑 Cambiar Contraseña", expanded=is_rec):
            if is_rec:
                st.info("⚠️ Sesión iniciada por recuperación. Define tu nueva contraseña:")
            sb_p1 = st.text_input("Nueva contraseña", type="password", key="sb_pass1", placeholder="Mínimo 6 caracteres")
            sb_p2 = st.text_input("Confirmar contraseña", type="password", key="sb_pass2", placeholder="Repite contraseña")
            if st.button("Guardar Contraseña", use_container_width=True, key="sb_btn_save_pass"):
                if not sb_p1:
                    st.warning("Ingresa la nueva contraseña.")
                elif sb_p1 != sb_p2:
                    st.error("Las contraseñas no coinciden.")
                else:
                    ok, msg = cambiar_contrasena(sb_p1)
                    if ok:
                        st.session_state["password_recovery_mode"] = False
                        st.success(msg)
                    else:
                        st.error(msg)

        if st.button(
            "🚪 Cerrar Sesión", use_container_width=True, key="btn_logout_sidebar"
        ):
            cerrar_sesion()


def render_user_badge():
    """Renderiza un badge de usuario activo con botón de cerrar sesión en la cabecera principal."""
    user = st.session_state.get("user")
    if not user:
        return
    email = getattr(user, "email", "Profesional")
    username = email.split("@")[0] if "@" in email else email

    col_badge, col_btn = st.columns([3, 1.2])
    with col_badge:
        st.markdown(
            f"""
            <div style="background: rgba(15, 23, 42, 0.7); border: 1px solid #334155; border-radius: 8px; padding: 6px 12px; display: flex; align-items: center; gap: 8px;">
                <span style="font-size: 1.1rem;">🩺</span>
                <div>
                    <div style="font-size: 0.68rem; color: #94a3b8; line-height: 1; text-transform: uppercase; letter-spacing: 0.04em;">Clínico Autenticado</div>
                    <div style="font-size: 0.88rem; font-weight: 600; color: #38bdf8; line-height: 1.2;">{username} <span style="font-size: 0.75rem; color: #64748b; font-weight: normal;">({email})</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col_btn:
        if st.button(
            "🚪 Salir",
            key="btn_logout_header",
            use_container_width=True,
            help="Cerrar sesión y limpiar persistencia",
        ):
            cerrar_sesion()

    if st.session_state.get("password_recovery_mode"):
        st.warning("🔑 **Modo de recuperación activo**: Por favor actualiza tu contraseña en el menú lateral para asegurar tu cuenta.")


def render_auth_screen() -> bool:
    """Muestra la pantalla de acceso o restaura la sesión persistente activa.

    Retorna True si el usuario está autenticado, False en caso contrario.
    """
    # 0. Si el usuario solicitó cerrar sesión en este ciclo
    if st.session_state.get("logout_requested"):
        st.session_state["logout_requested"] = False
        st.session_state["user"] = None
        st.session_state["session"] = None
        st.session_state["password_recovery_mode"] = False
        for param in [AUTH_TOKEN_PARAM, "code", "sb_access_token", "sb_refresh_token", "sb_auth_type"]:
            if param in st.query_params:
                del st.query_params[param]
        _limpiar_storage_js()

    # 1. Verificar si ya existe una sesión en memoria
    if "user" in st.session_state and st.session_state["user"] is not None:
        _render_sidebar_user()
        return True

    # 2. Intercambio de código PKCE (?code=...) desde enlace de correo
    if "code" in st.query_params:
        auth_code = st.query_params.get("code")
        try:
            supabase = init_supabase()
            res = supabase.auth.exchange_code_for_session({"auth_code": auth_code})
            if res and res.user:
                st.session_state["user"] = res.user
                st.session_state["session"] = res.session
                st.session_state["password_recovery_mode"] = True
                token = generar_token_sesion(res.session, res.user)
                st.query_params[AUTH_TOKEN_PARAM] = token
                _guardar_storage_js(token)
                del st.query_params["code"]
                _render_sidebar_user()
                return True
        except Exception:
            pass

    # 2.1 Enlace de recuperación implícito redirigido desde hash JS (sb_access_token)
    if "sb_access_token" in st.query_params:
        at = st.query_params.get("sb_access_token")
        rt = st.query_params.get("sb_refresh_token", "")
        ty = st.query_params.get("sb_auth_type", "")
        try:
            supabase = init_supabase()
            res = supabase.auth.set_session(at, rt or "")
            if res and res.user:
                st.session_state["user"] = res.user
                st.session_state["session"] = res.session
                if ty == "recovery":
                    st.session_state["password_recovery_mode"] = True
                token = generar_token_sesion(res.session, res.user)
                st.query_params[AUTH_TOKEN_PARAM] = token
                _guardar_storage_js(token)
                del st.query_params["sb_access_token"]
                if "sb_refresh_token" in st.query_params:
                    del st.query_params["sb_refresh_token"]
                if "sb_auth_type" in st.query_params:
                    del st.query_params["sb_auth_type"]
                _render_sidebar_user()
                return True
        except Exception:
            pass

    # 2.2 Intentar restaurar sesión persistente desde query_params o cookies HTTP
    token_candidato = st.query_params.get(AUTH_TOKEN_PARAM)

    # Búsqueda secundaria en cookies HTTP (Streamlit 1.64+)
    if (
        not token_candidato
        and hasattr(st, "context")
        and hasattr(st.context, "cookies")
    ):
        try:
            token_candidato = st.context.cookies.get(AUTH_COOKIE_NAME)
        except Exception:
            pass

    if token_candidato:
        data = descifrar_token_sesion(
            token_candidato, max_age_days=TOKEN_MAX_AGE_DAYS
        )
        if data:
            supabase = None
            try:
                supabase = init_supabase()
            except Exception:
                pass

            user, session = restaurar_sesion_desde_token(data, supabase)
            if user:
                st.session_state["user"] = user
                st.session_state["session"] = session

                # Sincronizar query_params si se renovó el token
                nuevo_token = token_candidato
                if session and getattr(session, "refresh_token", None):
                    nuevo_token = generar_token_sesion(session, user)

                if st.query_params.get(AUTH_TOKEN_PARAM) != nuevo_token:
                    st.query_params[AUTH_TOKEN_PARAM] = nuevo_token
                _guardar_storage_js(nuevo_token)

                _render_sidebar_user()
                return True
        else:
            # Token corrupto, alterado o expirado: limpiarlo
            if AUTH_TOKEN_PARAM in st.query_params:
                del st.query_params[AUTH_TOKEN_PARAM]
            _limpiar_storage_js()

    # 3. Si no hay sesión válida, mostrar formulario de acceso
    try:
        supabase = init_supabase()
    except Exception as e:
        if es_error_red_dns(e):
            st.error(MSG_ERROR_CONEXION_SECRETS)
        else:
            st.error(f"Error al conectar con Supabase: {e}")
        return False

    # Verificar si hay token en localStorage (caso de navegación a raíz limpia)
    _intentar_recuperar_localstorage_js()

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
        opciones = ["Iniciar Sesión", "Registrarse", "Recuperar Contraseña"]
        modo = st.radio(
            "Acción",
            opciones,
            horizontal=True,
            label_visibility="collapsed",
        )

        st.markdown("<br>", unsafe_allow_html=True)

        if modo == "Iniciar Sesión":
            email = st.text_input("Correo Electrónico", placeholder="nombre@ejemplo.com", key="auth_email_login")
            password = st.text_input(
                "Contraseña", type="password", placeholder="Mínimo 6 caracteres", key="auth_pass_login"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Ingresar", type="primary", use_container_width=True, key="btn_login_submit"):
                if not email or not password:
                    st.warning("Ingresa tu correo y contraseña.")
                else:
                    try:
                        res = supabase.auth.sign_in_with_password(
                            {"email": email.strip(), "password": password}
                        )
                        st.session_state["user"] = res.user
                        st.session_state["session"] = res.session
                        st.session_state["password_recovery_mode"] = False

                        # Generar y persistir token cifrado
                        token = generar_token_sesion(res.session, res.user)
                        st.query_params[AUTH_TOKEN_PARAM] = token
                        _guardar_storage_js(token)

                        st.success("Acceso concedido.")
                        st.rerun()
                    except Exception as err:
                        if es_error_red_dns(err):
                            st.error(MSG_ERROR_CONEXION_SECRETS)
                        else:
                            st.error(f"Credenciales no válidas: {err}")

        elif modo == "Registrarse":
            email = st.text_input("Correo Electrónico", placeholder="nombre@ejemplo.com", key="auth_email_reg")
            password = st.text_input(
                "Contraseña", type="password", placeholder="Mínimo 6 caracteres", key="auth_pass_reg"
            )
            confirm_password = st.text_input(
                "Confirmar Contraseña", type="password", placeholder="Repite tu contraseña", key="auth_pass_reg_conf"
            )

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Crear Cuenta", type="primary", use_container_width=True, key="btn_register_submit"):
                if not email or not password or not confirm_password:
                    st.warning("Completa todos los campos.")
                elif len(password) < 6:
                    st.warning("La contraseña debe tener al menos 6 caracteres.")
                elif password != confirm_password:
                    st.error("Las contraseñas no coinciden.")
                else:
                    try:
                        res = supabase.auth.sign_up(
                            {"email": email.strip(), "password": password}
                        )
                        st.success(
                            "Cuenta registrada. Si Supabase requiere confirmación de email, revisa tu bandeja de entrada."
                        )
                    except Exception as err:
                        if es_error_red_dns(err):
                            st.error(MSG_ERROR_CONEXION_SECRETS)
                        else:
                            st.error(f"Error en registro: {err}")

        else:  # "Recuperar Contraseña"
            st.markdown(
                """
                <div style="background: rgba(30, 41, 59, 0.45); border: 1px solid #334155; border-radius: 8px; padding: 12px 14px; margin-bottom: 14px;">
                    <div style="font-weight: 600; color: #38bdf8; font-size: 0.95rem; margin-bottom: 2px;">Recuperar Contraseña</div>
                    <div style="color: #94a3b8; font-size: 0.83rem;">
                        Ingresa el correo asociado a tu cuenta para recibir las instrucciones de recuperación.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            rec_email = st.text_input("Correo Registrado", placeholder="nombre@ejemplo.com", key="rec_correo_registrado")

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Enviar enlace de recuperación", type="primary", use_container_width=True, key="btn_enviar_recuperacion"):
                if not rec_email:
                    st.warning("Por favor ingrese su correo electrónico registrado.")
                elif "@" not in rec_email or "." not in rec_email:
                    st.warning("Por favor ingrese una dirección de correo válida.")
                else:
                    try:
                        email_clean = rec_email.strip()
                        if hasattr(supabase.auth, "reset_password_email"):
                            supabase.auth.reset_password_email(email_clean)
                        else:
                            supabase.auth.reset_password_for_email(email_clean)
                        st.success(
                            f"Se enviaron las instrucciones de recuperación a su correo electrónico ({email_clean}). "
                            "Por favor revise su bandeja de entrada y la carpeta de correo no deseado (spam)."
                        )
                    except Exception as err:
                        if es_error_red_dns(err):
                            st.error(MSG_ERROR_CONEXION_SECRETS)
                        else:
                            st.error(f"Error al enviar correo de recuperación: {err}")

            with st.expander("🔑 ¿Ya tienes un código o token de recuperación?"):
                otp_email = st.text_input("Confirmar Correo Electrónico", value=rec_email, key="otp_email_exp")
                otp_code = st.text_input("Código de Verificación (OTP) o Token", placeholder="Ej: 123456", key="otp_code_exp")
                new_pass = st.text_input("Nueva Contraseña", type="password", placeholder="Mínimo 6 caracteres", key="otp_pass1_exp")
                new_pass_conf = st.text_input("Confirmar Nueva Contraseña", type="password", placeholder="Repite la contraseña", key="otp_pass2_exp")

                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Restablecer Contraseña e Ingresar", key="btn_otp_exp_submit", use_container_width=True):
                    if not otp_email or not otp_code or not new_pass or not new_pass_conf:
                        st.warning("Por favor completa todos los campos.")
                    elif len(new_pass) < 6:
                        st.warning("La nueva contraseña debe tener al menos 6 caracteres.")
                    elif new_pass != new_pass_conf:
                        st.error("Las contraseñas no coinciden.")
                    else:
                        try:
                            res = supabase.auth.verify_otp({
                                "email": otp_email.strip(),
                                "token": otp_code.strip(),
                                "type": "recovery"
                            })
                            if res and res.user:
                                supabase.auth.update_user({"password": new_pass})
                                st.session_state["user"] = res.user
                                st.session_state["session"] = res.session
                                st.session_state["password_recovery_mode"] = False
                                token = generar_token_sesion(res.session, res.user)
                                st.query_params[AUTH_TOKEN_PARAM] = token
                                _guardar_storage_js(token)
                                st.success("🎉 ¡Contraseña restablecida exitosamente! Ingresando a la suite...")
                                st.rerun()
                            else:
                                st.error("No fue posible validar el código. Comprueba que sea correcto.")
                        except Exception as err:
                            if es_error_red_dns(err):
                                st.error(MSG_ERROR_CONEXION_SECRETS)
                            else:
                                st.error(f"Error al verificar el código: {err}")

    return False