"""
scratch/test_sacral_inference.py
Verificación automatizada de la inferencia biomecánica sacra y recuperación de fichas clínicas.
"""
import sys
sys.path.insert(0, ".")

from app import (
    ExamenPalpatorio,
    BanderasRojas,
    ClusterLaslett,
    LadoRestriccion,
    PosicionNivel,
    HitoOseoPosicion,
    EscalonPubico,
    MaleoloSupino,
    LongSittingTest,
    SurcoSacro,
    AnguloInferolateral,
    EstadoTejidoBlando,
    inferir_diagnostico,
    generar_diagrama_vectorial_ajuste,
)
from clinical_knowledge import CLINICAL_KNOWLEDGE_BASE, get_disfuncion_info

def run_tests():
    banderas = BanderasRojas()
    cluster = ClusterLaslett(distraccion=True, compresion=True, thigh_thrust=True)

    print("--- INICIANDO SUITE DE PRUEBAS DE INFERENCIA SACRA ---")

    # 1. SACRO ANTERO-INFERIOR DERECHO
    # Hallazgos: Sulcus derecho profundo, ILA izquierdo superficial, pierna funcionalmente larga derecha, piramidal derecho tenso.
    palp_sai = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.LARGO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.PROFUNDO,
        ail=AnguloInferolateral.SUPERFICIAL,
        piramidal=EstadoTejidoBlando.HIPERTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_sai = inferir_diagnostico(palp_sai, banderas, cluster)
    print(f"[TEST 1] Sacro Antero-Inferior: {diag_sai.titulo} | Clave: {diag_sai.clave_conocimiento}")
    assert "SACRO_ANTERO_INFERIOR" in diag_sai.clave_conocimiento, f"Error en clave SAI: {diag_sai.clave_conocimiento}"
    assert "PA + LM" in diag_sai.vector_ajuste, f"Vector SAI incorrecto: {diag_sai.vector_ajuste}"
    assert "ILA izquierdo" in diag_sai.vector_ajuste or "pcp" in diag_sai.vector_ajuste.lower(), f"Contacto SAI incorrecto: {diag_sai.vector_ajuste}"

    # 2. SACRO POSTERO-SUPERIOR IZQUIERDO
    # Hallazgos: Base sacra izquierda superficial, ILA derecho profundo, maléolo izquierdo más alto en supino.
    palp_sps = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.IZQUIERDO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.CORTO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.SUPERFICIAL,
        ail=AnguloInferolateral.PROFUNDO,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_sps = inferir_diagnostico(palp_sps, banderas, cluster)
    print(f"[TEST 2] Sacro Postero-Superior: {diag_sps.titulo} | Clave: {diag_sps.clave_conocimiento}")
    assert "SACRO_POSTERO_SUPERIOR" in diag_sps.clave_conocimiento, f"Error en clave SPS: {diag_sps.clave_conocimiento}"
    assert "PA + ML" in diag_sps.vector_ajuste, f"Vector SPS incorrecto: {diag_sps.vector_ajuste}"
    assert "EIPS" in diag_sps.vector_ajuste, f"Contacto SPS incorrecto: {diag_sps.vector_ajuste}"

    # 3. SACRO EN FLEXIÓN UNILATERAL
    # Hallazgos: Base profunda e ILA más bajo del lado hipomóvil, sin bandas tensas.
    palp_sfu = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.SIMETRICO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.PROFUNDO,
        ail=AnguloInferolateral.MAS_BAJO,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_sfu = inferir_diagnostico(palp_sfu, banderas, cluster)
    print(f"[TEST 3] Sacro Flexión Unilateral: {diag_sfu.titulo} | Clave: {diag_sfu.clave_conocimiento}")
    assert diag_sfu.clave_conocimiento == "SACRO_FLEXION_UNILATERAL", f"Error en clave SFU: {diag_sfu.clave_conocimiento}"
    assert "torque hacia arriba" in diag_sfu.vector_ajuste.lower(), f"Vector SFU incorrecto: {diag_sfu.vector_ajuste}"

    # 4. SACRO EN EXTENSIÓN UNILATERAL
    # Hallazgos: Base más posterior e ILA más craneal del lado hipomóvil, sin bandas tensas.
    palp_seu = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.SIMETRICO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.SUPERFICIAL,
        ail=AnguloInferolateral.MAS_CRANEAL,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_seu = inferir_diagnostico(palp_seu, banderas, cluster)
    print(f"[TEST 4] Sacro Extensión Unilateral: {diag_seu.titulo} | Clave: {diag_seu.clave_conocimiento}")
    assert diag_seu.clave_conocimiento == "SACRO_EXTENSION_UNILATERAL", f"Error en clave SEU: {diag_seu.clave_conocimiento}"
    assert "descendiendo el ila" in diag_seu.vector_ajuste.lower(), f"Vector SEU incorrecto: {diag_seu.vector_ajuste}"

    # 5. SACRO EN FLEXIÓN BILATERAL
    # Hallazgos: Base anterior y profunda bilateralmente, ápex postero-superior, sulcus bilateral profundo, maléolos sin cambios.
    palp_sfb = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.SIMETRICO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.PROFUNDO,
        ail=AnguloInferolateral.SUPERFICIAL,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_sfb = inferir_diagnostico(palp_sfb, banderas, cluster)
    print(f"[TEST 5] Sacro Flexión Bilateral: {diag_sfb.titulo} | Clave: {diag_sfb.clave_conocimiento}")
    assert diag_sfb.clave_conocimiento == "SACRO_FLEXION", f"Error en clave SFB: {diag_sfb.clave_conocimiento}"
    assert "PA + SI" in diag_sfb.vector_ajuste, f"Vector SFB incorrecto: {diag_sfb.vector_ajuste}"

    # 6. SACRO EN EXTENSIÓN BILATERAL
    # Hallazgos: Base postero-superior, ápex antero-inferior, sulcus superficial bilateral.
    palp_seb = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.NEUTRA,
        eips=HitoOseoPosicion.NEUTRA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.SIMETRICO,
        long_sitting=LongSittingTest.NEUTRO,
        surco_sacro=SurcoSacro.SUPERFICIAL,
        ail=AnguloInferolateral.PROFUNDO,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=False
    )
    diag_seb = inferir_diagnostico(palp_seb, banderas, cluster)
    print(f"[TEST 6] Sacro Extensión Bilateral: {diag_seb.titulo} | Clave: {diag_seb.clave_conocimiento}")
    assert diag_seb.clave_conocimiento == "SACRO_EXTENSION", f"Error en clave SEB: {diag_seb.clave_conocimiento}"
    assert "pa puro" in diag_seb.vector_ajuste.lower(), f"Vector SEB incorrecto: {diag_seb.vector_ajuste}"

    # Verificar que el diagrama vectorial genera HTML válido para todas las disfunciones
    for diag in [diag_sai, diag_sps, diag_sfu, diag_seu, diag_sfb, diag_seb]:
        html = generar_diagrama_vectorial_ajuste("Derecho", diag)
        assert "<svg" in html or "SVG" in html or "scene" in html or "canvas" in html or "LOD:" in html
        print(f"  -> Diagrama verificado para {diag.clave_conocimiento}")

    print("\n[SUCCESS] TODAS LAS PRUEBAS DE INFERENCIA SACRA PASARON EXITOSAMENTE!")

if __name__ == "__main__":
    run_tests()
