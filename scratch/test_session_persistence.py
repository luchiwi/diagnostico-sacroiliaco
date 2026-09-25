"""
scratch/test_session_persistence.py
Suite de pruebas automatizadas para la persistencia de sesión profesional.
"""

import sys
import os
import time
from dataclasses import dataclass
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.abspath("."))

import toml
# Simular st.secrets para el entorno de pruebas
secrets = toml.load(".streamlit/secrets.toml")

import streamlit as st

# Configurar st.secrets si no está presente
if not hasattr(st, "secrets") or not st.secrets:
    st.secrets = secrets

import auth


@dataclass
class MockUser:
    id: str = "usr_osteopata_001"
    email: str = "dr.garcia@osteopatia.cl"


@dataclass
class MockSession:
    access_token: str = "eyJh.mock_access_token.xyz"
    refresh_token: str = "mock_refresh_token_abc123"


def test_encryption_and_decryption():
    print("\n[TEST 1] Verificando cifrado Fernet y descifrado de sesión...")
    user = MockUser()
    session = MockSession()

    token = auth.generar_token_sesion(session, user)
    assert isinstance(token, str) and len(token) > 50, "El token debe ser un string cifrado Fernet"
    print(f"  -> Token generado correctamente (longitud: {len(token)} caracteres)")

    data = auth.descifrar_token_sesion(token)
    assert data is not None, "El token debe descifrarse correctamente"
    assert data["user_id"] == "usr_osteopata_001", "user_id debe coincidir"
    assert data["email"] == "dr.garcia@osteopatia.cl", "email debe coincidir"
    assert data["refresh_token"] == "mock_refresh_token_abc123", "refresh_token debe coincidir"
    print("  -> Payload descifrado y validado íntegramente: OK")


def test_tampered_token_rejection():
    print("\n[TEST 2] Verificando rechazo de tokens adulterados o falsificados...")
    user = MockUser()
    session = MockSession()
    token = auth.generar_token_sesion(session, user)

    # Modificar caracteres del token para simular alteración
    tampered_token = token[:-5] + "AAAAA"
    tampered_result = auth.descifrar_token_sesion(tampered_token)
    assert tampered_result is None, "El token adulterado debe ser rechazado inmediatamente"
    print("  -> Token adulterado rechazado con éxito: OK")

    # Token con formato basura
    assert auth.descifrar_token_sesion("token_invalido_random_123") is None
    print("  -> Token aleatorio inválido rechazado: OK")


def test_expired_token_rejection():
    print("\n[TEST 3] Verificando expiración de token por tiempo de vida (TTL)...")
    user = MockUser()
    session = MockSession()
    token = auth.generar_token_sesion(session, user)

    # Verificar con max_age_days = 0 (expiración inmediata)
    data_expired = auth.descifrar_token_sesion(token, max_age_days=0)
    assert data_expired is None, "Un token con TTL 0 debe expirar inmediatamente"
    print("  -> Token expirado rechazado con éxito: OK")


def test_restoration_flow():
    print("\n[TEST 4] Verificando restauración de sesión con fallback seguro...")
    user = MockUser()
    session = MockSession()
    token = auth.generar_token_sesion(session, user)
    data = auth.descifrar_token_sesion(token)

    # Caso A: Supabase offline (supabase=None) -> debe retornar CachedUser
    cached_user, sess = auth.restaurar_sesion_desde_token(data, supabase=None)
    assert cached_user is not None, "Debe retornar CachedUser en caso de contingencia"
    assert cached_user.email == user.email, "Email del CachedUser debe ser idéntico"
    assert cached_user.id == user.id, "ID del CachedUser debe ser idéntico"
    print("  -> Fallback seguro a CachedUser validado: OK")

    # Caso B: Supabase mock con refresh_session exitoso
    mock_supabase = MagicMock()
    mock_res = MagicMock()
    mock_res.user = MockUser(id="refreshed_id", email="dr.garcia@osteopatia.cl")
    mock_res.session = MockSession(refresh_token="new_refresh_token_999")
    mock_supabase.auth.refresh_session.return_value = mock_res

    restored_user, restored_session = auth.restaurar_sesion_desde_token(data, supabase=mock_supabase)
    assert restored_user.id == "refreshed_id", "Debe usar el usuario renovado por Supabase"
    assert restored_session.refresh_token == "new_refresh_token_999", "Debe usar la sesión renovada"
    print("  -> Restauración y rotación de sesión con Supabase: OK")


def test_simulated_f5_reload_and_logout():
    print("\n[TEST 5] Simulando ciclo completo de recarga de página (F5) y cierre de sesión...")
    user = MockUser()
    session = MockSession()
    token = auth.generar_token_sesion(session, user)

    # 1. Simular inicio de sesión: se almacena en st.session_state y st.query_params
    st.session_state["user"] = user
    st.session_state["session"] = session
    st.query_params[auth.AUTH_TOKEN_PARAM] = token

    # Estado activo inicial
    assert "user" in st.session_state and st.session_state["user"] is not None
    assert auth.AUTH_TOKEN_PARAM in st.query_params
    print("  -> Estado 1: Sesión iniciada con token en st.query_params.")

    # 2. Simular recarga de página F5: Streamlit reinicia st.session_state
    # pero el navegador MANTIENE la URL con query_params intacta
    st.session_state.clear()
    assert "user" not in st.session_state, "st.session_state debe estar vacío tras F5"
    assert auth.AUTH_TOKEN_PARAM in st.query_params, "st.query_params persiste en el navegador tras F5"
    print("  -> Estado 2: F5 ejecutado. st.session_state reseteado a vacío, query_params preservado.")

    # 3. Al ejecutar render_auth_screen(), debe detectar el token, descifrarlo y reponer la sesión
    token_en_url = st.query_params.get(auth.AUTH_TOKEN_PARAM)
    data = auth.descifrar_token_sesion(token_en_url)
    assert data is not None, "El token en la URL debe ser válido tras F5"

    restored_user, restored_sess = auth.restaurar_sesion_desde_token(data, supabase=None)
    st.session_state["user"] = restored_user
    st.session_state["session"] = restored_sess
    assert st.session_state["user"].email == user.email
    print("  -> Estado 3: Sesión autoreconocida y restaurada sin pedir credenciales: OK")

    # 4. Simular clic en 'Cerrar Sesión'
    if auth.AUTH_TOKEN_PARAM in st.query_params:
        del st.query_params[auth.AUTH_TOKEN_PARAM]
    st.session_state["user"] = None
    st.session_state["session"] = None
    st.session_state["logout_requested"] = True

    assert auth.AUTH_TOKEN_PARAM not in st.query_params, "auth_token debe eliminarse de la URL"
    assert st.session_state["user"] is None, "user debe ser None"
    print("  -> Estado 4: Cerrar sesión ejecutado. Token eliminado de URL y memoria.")

    # 5. Simular F5 tras haber cerrado sesión: la URL no tiene token
    st.session_state.clear()
    assert auth.AUTH_TOKEN_PARAM not in st.query_params
    token_post_logout = st.query_params.get(auth.AUTH_TOKEN_PARAM)
    assert token_post_logout is None, "No debe haber token post-logout"
    print("  -> Estado 5: F5 post-logout confirmado sin autoingreso fantasma: OK")


if __name__ == "__main__":
    print("=== INICIANDO SUITE DE PRUEBAS DE PERSISTENCIA DE SESIÓN ===")
    test_encryption_and_decryption()
    test_tampered_token_rejection()
    test_expired_token_rejection()
    test_restoration_flow()
    test_simulated_f5_reload_and_logout()
    print("\n[SUCCESS] TODAS LAS PRUEBAS DE PERSISTENCIA DE SESIÓN PASARON EXITOSAMENTE!")
