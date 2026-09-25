import streamlit as st
from streamlit.testing.v1 import AppTest

code = '''
import streamlit as st

OPCIONES_MENU_PRINCIPAL = [
    "1. Anamnesis y Banderas Rojas",
    "2. Provocacion y Palpacion",
    "3. Visualizacion y Cinematica",
    "4. Juicio Clinico y Exportacion"
]

tab_url = st.query_params.get("tab") or st.query_params.get("modulo") or ""

index = 0
if tab_url in OPCIONES_MENU_PRINCIPAL:
    index = OPCIONES_MENU_PRINCIPAL.index(tab_url)
elif tab_url in ("1", "anamnesis"):
    index = 0
elif tab_url in ("2", "exploracion", "palpacion"):
    index = 1
elif tab_url in ("3", "visualizador", "cinematica", "a", "b", "c", "modulo_a", "modulo_b", "modulo_c"):
    index = 2
elif tab_url in ("4", "juicio", "prescripcion", "exportacion"):
    index = 3

def _on_nav_change():
    sel = st.session_state.get("nav_menu_principal", OPCIONES_MENU_PRINCIPAL[0])
    st.query_params["tab"] = sel

nav_activa = st.radio(
    "Navegacion del Sistema:",
    options=OPCIONES_MENU_PRINCIPAL,
    index=index,
    key="nav_menu_principal",
    horizontal=True,
    on_change=_on_nav_change
)

if "diag_titulo" not in st.session_state:
    st.session_state["diag_titulo"] = "Torsion Sacra Anterior Derecha (R on R)"

if nav_activa == OPCIONES_MENU_PRINCIPAL[0]:
    st.markdown("### Pagina 1: Anamnesis")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[1]:
    st.markdown("### Pagina 2: Exploracion")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[2]:
    st.markdown(f"### Pagina 3: Visualizacion - {st.session_state['diag_titulo']}")
elif nav_activa == OPCIONES_MENU_PRINCIPAL[3]:
    st.markdown(f"### Pagina 4: Juicio Clinico - {st.session_state['diag_titulo']}")
'''

# Test F5 on Page 3
at = AppTest.from_string(code)
at.query_params['tab'] = '3. Visualizacion y Cinematica'
at.run()
assert 'Pagina 3: Visualizacion' in at.markdown[0].value
print('Test 1: F5 reload on Page 3 directly renders Page 3 without error: OK')

# Test F5 on Page 2
at2 = AppTest.from_string(code)
at2.query_params['tab'] = '2. Provocacion y Palpacion'
at2.run()
assert 'Pagina 2: Exploracion' in at2.markdown[0].value
print('Test 2: F5 reload on Page 2 directly renders Page 2: OK')

# Test F5 with tab='c'
at3 = AppTest.from_string(code)
at3.query_params['tab'] = 'c'
at3.run()
assert 'Pagina 3: Visualizacion' in at3.markdown[0].value
print('Test 3: F5 reload with tab=c resolves dynamically to Page 3: OK')

# Test UI interaction: user clicks Page 4
at.radio[0].set_value(at.radio[0].options[3]).run()
assert 'Pagina 4: Juicio Clinico' in at.markdown[0].value
assert at.query_params.get('tab') == '4. Juicio Clinico y Exportacion' or at.query_params.get('tab') == ['4. Juicio Clinico y Exportacion']
print('Test 4: User click changes to Page 4 and updates query_params synchronously: OK')
