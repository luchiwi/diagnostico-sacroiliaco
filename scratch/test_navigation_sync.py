"""
scratch/test_navigation_sync.py
Pruebas automatizadas de sincronización estricta del menú principal con st.query_params.
"""

import sys
import os

sys.path.insert(0, os.path.abspath("."))

OPCIONES_MENU_PRINCIPAL = [
    "1. 📋 Anamnesis y Banderas Rojas",
    "2. 🔍 Provocación y Palpación",
    "3. 🦴 Visualización y Cinemática",
    "4. ⚖️ Juicio Clínico y Exportación"
]


def resolver_indice_menu(tab_url: str) -> int:
    """Calcula dinámicamente el índice del menú principal a partir del parámetro de URL."""
    if tab_url in OPCIONES_MENU_PRINCIPAL:
        return OPCIONES_MENU_PRINCIPAL.index(tab_url)
    elif str(tab_url).strip().lower() in ("1", "anamnesis"):
        return 0
    elif str(tab_url).strip().lower() in ("2", "exploracion", "palpacion"):
        return 1
    elif str(tab_url).strip().lower() in ("3", "visualizador", "cinematica", "a", "b", "c", "modulo_a", "modulo_b", "modulo_c"):
        return 2
    elif str(tab_url).strip().lower() in ("4", "juicio", "prescripcion", "exportacion"):
        return 3
    return 0


def test_menu_resolution():
    print("\n[TEST 1] Verificando cálculo dinámico del índice del menú principal:")
    # Coincidencia exacta de string
    for idx, opt in enumerate(OPCIONES_MENU_PRINCIPAL):
        assert resolver_indice_menu(opt) == idx, f"Fallo al resolver {opt}"
        print(f"  -> Coincidencia exacta opcion {idx + 1} resuelve a indice {idx}: OK")

    # Mapeos de compatibilidad clínica (slugs, números y submódulos)
    assert resolver_indice_menu("1") == 0
    assert resolver_indice_menu("2") == 1
    assert resolver_indice_menu("3") == 2
    assert resolver_indice_menu("4") == 3
    assert resolver_indice_menu("c") == 2
    assert resolver_indice_menu("modulo_c") == 2
    assert resolver_indice_menu("a") == 2
    print("  -> Slugs numéricos y submódulos resuelven a sus páginas correspondientes: OK")

    # Parámetros inválidos o vacíos
    assert resolver_indice_menu("") == 0
    assert resolver_indice_menu(None) == 0
    assert resolver_indice_menu("desconocido") == 0
    print("  -> Parámetros vacíos o desconocidos resuelven a índice 0 (página inicial): OK")


def test_apptest_menu_navigation_lifecycle():
    print("\n[TEST 2] Verificando ciclo de vida del selector st.radio con Streamlit AppTest:")
    from streamlit.testing.v1 import AppTest

    code = '''
import streamlit as st

OPCIONES_MENU_PRINCIPAL = [
    "1. 📋 Anamnesis y Banderas Rojas",
    "2. 🔍 Provocación y Palpación",
    "3. 🦴 Visualización y Cinemática",
    "4. ⚖️ Juicio Clínico y Exportación"
]

# 1. Al inicio de la app, lee el parámetro st.query_params.get("tab") o "modulo"
tab_url = st.query_params.get("tab") or st.query_params.get("modulo") or ""

# 2. Si ese parámetro existe en la URL y coincide con alguna de las opciones del menú de navegación,
# calcula su índice dinámicamente (index = opciones.index(tab_url)). Si no existe, usa 0.
index = 0
if tab_url in OPCIONES_MENU_PRINCIPAL:
    index = OPCIONES_MENU_PRINCIPAL.index(tab_url)
elif str(tab_url).strip().lower() in ("1", "anamnesis"):
    index = 0
elif str(tab_url).strip().lower() in ("2", "exploracion", "palpacion"):
    index = 1
elif str(tab_url).strip().lower() in ("3", "visualizador", "cinematica", "a", "b", "c", "modulo_a", "modulo_b", "modulo_c"):
    index = 2
elif str(tab_url).strip().lower() in ("4", "juicio", "prescripcion", "exportacion"):
    index = 3

# 3. Callback para actualizar st.query_params["tab"] = seleccion cada vez que el usuario haga clic en otro módulo
def _on_menu_principal_change():
    seleccion = st.session_state.get("nav_menu_principal", OPCIONES_MENU_PRINCIPAL[0])
    st.query_params["tab"] = seleccion

nav_activa = st.radio(
    "Menú de Navegación:",
    options=OPCIONES_MENU_PRINCIPAL,
    index=index,
    key="nav_menu_principal",
    horizontal=True,
    on_change=_on_menu_principal_change
)

if nav_activa == OPCIONES_MENU_PRINCIPAL[0]:
    st.markdown("### Página 1: Anamnesis")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[1]:
    st.markdown("### Página 2: Exploración")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[2]:
    st.markdown("### Página 3: Visualización")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[3]:
    st.markdown("### Página 4: Juicio Clínico")
'''

    # Caso 1: Inicio por defecto (sin parámetros) -> Página 1
    at0 = AppTest.from_string(code)
    at0.run()
    assert "Página 1" in at0.markdown[0].value
    print("  -> Inicio limpio carga Página 1 (Anamnesis): OK")

    # Caso 2: Carga directa con tab="3. 🦴 Visualización y Cinemática"
    at3 = AppTest.from_string(code)
    at3.query_params["tab"] = OPCIONES_MENU_PRINCIPAL[2]
    at3.run()
    assert "Página 3" in at3.markdown[0].value
    print("  -> Carga con tab exacta de Página 3 carga Página 3 directamente: OK")

    # Caso 3: Carga con modulo="c" (proveniente del visor 3D) -> Resuelve a Página 3
    at_mod_c = AppTest.from_string(code)
    at_mod_c.query_params["modulo"] = "c"
    at_mod_c.run()
    assert "Página 3" in at_mod_c.markdown[0].value
    print("  -> Carga con modulo=c resuelve dinámicamente a Página 3: OK")

    # Caso 4: Interacción en UI -> Clic en Página 4 (Juicio Clínico)
    at0.radio[0].set_value(OPCIONES_MENU_PRINCIPAL[3]).run()
    assert "Página 4" in at0.markdown[0].value
    assert at0.query_params.get("tab") == OPCIONES_MENU_PRINCIPAL[3] or at0.query_params.get("tab") == [OPCIONES_MENU_PRINCIPAL[3]]
    print("  -> Clic en Página 4 actualiza query_params['tab'] síncronamente: OK")

    # Caso 5: Recarga F5 simulada tras haber hecho clic en Página 4
    at_f5 = AppTest.from_string(code)
    at_f5.query_params["tab"] = OPCIONES_MENU_PRINCIPAL[3]
    at_f5.run()
    assert "Página 4" in at_f5.markdown[0].value
    print("  -> Recarga F5 con query param preservado permanece exactamente en Página 4: OK")


if __name__ == "__main__":
    print("=== INICIANDO SUITE DE PRUEBAS DE MENÚ PRINCIPAL Y PERSISTENCIA ===")
    test_menu_resolution()
    test_apptest_menu_navigation_lifecycle()
    print("\n[SUCCESS] TODAS LAS PRUEBAS DE MENÚ PRINCIPAL PASARON EXITOSAMENTE!")
