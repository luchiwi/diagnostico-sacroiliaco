import streamlit as st

st.set_page_config(page_title="Diagnóstico Sacroilíaco", page_icon="🦴", layout="centered")

st.title("🦴 Diagnóstico Sacroilíaco y Pelviano")
st.caption("Asistente Biomecánico - Criterios Quiroprácticos")

st.subheader("Datos del Examen Físico")

lado = st.radio("1. Lado de restricción (Quick Scan / Gillet):", ["Derecho", "Izquierdo"], horizontal=True)

col1, col2 = st.columns(2)
with col1:
    eias = st.selectbox("EIAS:", ["Neutra", "Alta", "Baja"])
    maleolo_supino = st.selectbox("Maléolo en supino:", ["Simétrico", "Corto", "Largo"])
    inversion_prono = st.checkbox("Inversión de longitud en prono (sit-to-stand/supine-to-prone)")
    escalon_pubis = st.selectbox("Escalón de pubis:", ["Ninguno", "Descendido", "Ascendido"])

with col2:
    eips = st.selectbox("EIPS:", ["Neutra", "Alta", "Baja"])
    piramidal_tenso = st.checkbox("Tensión notable en piramidal homolateral")
    surco_profundo = st.checkbox("Surco sacro ipsilateral profundo")
    ail_descendido = st.checkbox("AIL descendido/posterior")

st.divider()

if st.button("Evaluar Disfunción Biomecánica", type="primary", use_container_width=True):
    # Lógica de interpretación básica
    st.subheader("📋 Diagnóstico y Hallazgos")
    
    hallazgos = []
    
    # Evaluación de Ilíaco anterior / posterior / upslip
    if eias == "Baja" and eips == "Alta":
        hallazgos.append(f"**Ilíaco Anterior {lado}:** Rotación anterior del ilíaco con flexión de la articulación sacroilíaca.")
    elif eias == "Alta" and eips == "Baja":
        hallazgos.append(f"**Ilíaco Posterior {lado}:** Rotación posterior del ilíaco con extensión sacroilíaca.")
    elif eias == "Alta" and eips == "Alta":
        hallazgos.append(f"**Ilíaco Ascendido (Upslip) {lado}:** Traslación superior en bloque del hueso coxal.")
        
    if escalon_pubis == "Descendido":
        hallazgos.append(f"**Pubis Descendido {lado}:** Mayor resistencia al descenso en el lado contralateral.")
    elif escalon_pubis == "Ascendido":
        hallazgos.append(f"**Pubis Ascendido {lado}.**")
        
    if not hallazgos:
        st.info("Sin disfunción evidente con los parámetros ingresados. Verificar datos articulares.")
    else:
        for item in hallazgos:
            st.success(item)