"""
scratch/test_navigation_sync.py
Pruebas automatizadas de sincronización de navegación y parámetros URL (modulo y tab).
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

OPCIONES_MODULO_VIS = [
    "🟢 Módulo A: Visor 3D Anatómico Interactivo 360° (Pre-Ajuste)",
    "🔵 Módulo B: Diagrama Vectorial de Ajuste y Puntos de Contacto (Post-Evaluación)",
    "🟣 Módulo C: Atlas Biomecánico Interactivo y Galería de Disfunciones 3D"
]

MODULO_KEY_TO_IDX = {
    "a": 0,
    "modulo_a": 0,
    "b": 1,
    "modulo_b": 1,
    "c": 2,
    "modulo_c": 2,
}


def calcular_modulo_idx(raw_modulo: str) -> int:
    return MODULO_KEY_TO_IDX.get(str(raw_modulo).strip().lower(), 0)


def calcular_tab_idx(param_tab: str, param_modulo: str) -> int:
    p_tab = str(param_tab).strip().lower()
    p_mod = str(param_modulo).strip().lower()

    if p_mod in ("a", "b", "c", "modulo_a", "modulo_b", "modulo_c"):
        return 2  # Pestaña 3: Visualizador
    elif p_tab in ("1", "anamnesis"):
        return 0
    elif p_tab in ("2", "exploracion", "palpacion"):
        return 1
    elif p_tab in ("3", "visualizador", "cinematica"):
        return 2
    elif p_tab in ("4", "juicio", "prescripcion", "exportacion"):
        return 3
    else:
        return 0


def test_modulo_resolution():
    print("\n[TEST 1] Verificando resolución de índice de módulo desde URL:")
    # Módulo C
    assert calcular_modulo_idx("c") == 2
    assert calcular_modulo_idx("C") == 2
    assert calcular_modulo_idx("modulo_c") == 2
    assert OPCIONES_MODULO_VIS[calcular_modulo_idx("c")].startswith("🟣 Módulo C")
    print("  -> Módulo C resuelve a índice 2: OK")

    # Módulo B
    assert calcular_modulo_idx("b") == 1
    assert calcular_modulo_idx("B") == 1
    assert calcular_modulo_idx("modulo_b") == 1
    assert OPCIONES_MODULO_VIS[calcular_modulo_idx("b")].startswith("🔵 Módulo B")
    print("  -> Módulo B resuelve a índice 1: OK")

    # Módulo A
    assert calcular_modulo_idx("a") == 0
    assert calcular_modulo_idx("A") == 0
    assert OPCIONES_MODULO_VIS[calcular_modulo_idx("a")].startswith("🟢 Módulo A")
    print("  -> Módulo A resuelve a índice 0: OK")

    # Inválido o vacío -> fallback a inicio (Módulo A)
    assert calcular_modulo_idx("") == 0
    assert calcular_modulo_idx("xyz") == 0
    assert calcular_modulo_idx("null") == 0
    assert calcular_modulo_idx(None) == 0
    print("  -> Valores vacíos o inválidos caen a 0 (inicio por defecto): OK")


def test_tab_activation_resolution():
    print("\n[TEST 2] Verificando activación de pestañas principales:")
    # Si viene modulo=c, debe activar Tab 3 (índice 2)
    assert calcular_tab_idx(param_tab="", param_modulo="c") == 2
    assert calcular_tab_idx(param_tab="", param_modulo="a") == 2
    assert calcular_tab_idx(param_tab="", param_modulo="b") == 2
    print("  -> Presencia de parámetro modulo activa automáticamente Tab 3 (Visualizador): OK")

    # Si viene tab específico sin modulo
    assert calcular_tab_idx(param_tab="1", param_modulo="") == 0
    assert calcular_tab_idx(param_tab="2", param_modulo="") == 1
    assert calcular_tab_idx(param_tab="3", param_modulo="") == 2
    assert calcular_tab_idx(param_tab="4", param_modulo="") == 3
    print("  -> Parámetros de pestaña 1, 2, 3, 4 resuelven a índices 0, 1, 2, 3: OK")

    # Inválido o sin parámetros -> Tab 1 (índice 0)
    assert calcular_tab_idx(param_tab="99", param_modulo="") == 0
    assert calcular_tab_idx(param_tab="", param_modulo="") == 0
    print("  -> Pestaña por defecto es Tab 1 (índice 0): OK")


def test_roundtrip_url_preservation():
    print("\n[TEST 3] Verificando compatibilidad con token de sesión en st.query_params:")
    import streamlit as st

    # Simular query_params con auth_token y modulo=c
    st.query_params["auth_token"] = "gAAAAABmock_auth_token_value=="
    st.query_params["modulo"] = "c"
    st.query_params["tab"] = "3"

    assert st.query_params.get("auth_token") == "gAAAAABmock_auth_token_value=="
    assert st.query_params.get("modulo") == "c"
    assert st.query_params.get("tab") == "3"

    # Al cambiar de módulo a 'b'
    st.query_params["modulo"] = "b"
    assert st.query_params.get("auth_token") == "gAAAAABmock_auth_token_value==", "auth_token no debe perderse"
    assert st.query_params.get("modulo") == "b"

    print("  -> st.query_params preserva auth_token y actualiza modulo sin interferencia: OK")


if __name__ == "__main__":
    print("=== INICIANDO SUITE DE PRUEBAS DE NAVEGACIÓN Y SINCRONIZACIÓN URL ===")
    test_modulo_resolution()
    test_tab_activation_resolution()
    test_roundtrip_url_preservation()
    print("\n[SUCCESS] TODAS LAS PRUEBAS DE NAVEGACIÓN PASARON EXITOSAMENTE!")
