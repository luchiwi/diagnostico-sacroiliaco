"""
================================================================================
SUITE CLÍNICA DE DIAGNÓSTICO BIOMECÁNICO SACROILÍACO E ILIOSACRO
Versión: 2.2.0 Pro - Grado Clínico y Quiropráctico (Gonstead, Downslip/Upslip, PDF)
Autor: Consultoría en Biomecánica Clínica y Software Médico
================================================================================
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional, Tuple
import streamlit as st
import streamlit.components.v1 as components
from fpdf import FPDF
from fpdf.enums import XPos, YPos

# ==============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CLÍNICOS
# ==============================================================================

st.set_page_config(
    page_title="BioPelvis Pro | Diagnóstico Sacroilíaco y Pelviano",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CUSTOM_CSS = """
<style>
    /* Tipografía y fondo sobrio clínico */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    .clinical-header {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 24px;
        margin-bottom: 24px;
        color: #f8fafc;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    
    .clinical-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
    }
    
    .badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .badge-safe { background-color: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
    .badge-warning { background-color: #fef9c3; color: #a16207; border: 1px solid #fde047; }
    .badge-danger { background-color: #fee2e2; color: #b91c1c; border: 1px solid #fca5a5; }
    .badge-info { background-color: #e0f2fe; color: #0369a1; border: 1px solid #bae6fd; }

    .metric-container {
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        text-align: center;
    }

    /* Tabs styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e2e8f0;
        padding-bottom: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 48px;
        border-radius: 8px 8px 0 0;
        padding: 0 20px;
        font-weight: 600;
        font-size: 0.95rem;
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# ENUMERACIONES Y MODELOS DE DATOS TIPADOS
# ==============================================================================

class TiempoEvolucion(str, Enum):
    AGUDO = "Agudo (< 6 semanas)"
    SUBAGUDO = "Subagudo (6 - 12 semanas)"
    CRONICO = "Crónico (> 3 meses)"


class MecanismoInicio(str, Enum):
    MICROTRAUMA = "Microtraumático repetitivo (sobreuso, carrera, asimetría funcional)"
    IMPACTO_AXIAL = "Impacto axial / Caída directa sobre isquion o nalga"
    FLEXO_ROTACION = "Flexo-rotación de tronco con carga mecánica"
    POSTPARTO = "Postparto / Laxitud ligamentosa gestacional"
    INSIDIOSO = "Inicio insidioso sin evento traumático aparente"


class LadoRestriccion(str, Enum):
    DERECHO = "Derecho"
    IZQUIERDO = "Izquierdo"


class PosicionNivel(str, Enum):
    ALTA = "Alta"
    NIVELADA = "Nivelada"
    BAJA = "Baja"


class HitoOseoPosicion(str, Enum):
    NEUTRA = "Neutra / Simétrica"
    ALTA = "Alta (Ascendida)"
    BAJA = "Baja (Descendida)"


class EscalonPubico(str, Enum):
    NEUTRO = "Neutro / Alineado"
    SUPERIOR = "Escalón Superior (Ascendido)"
    INFERIOR = "Escalón Inferior (Descendido)"


class MaleoloSupino(str, Enum):
    SIMETRICO = "Simétrico"
    CORTO = "Corto funcional"
    LARGO = "Largo funcional"


class LongSittingTest(str, Enum):
    NEUTRO = "Neutro / Sin cambio evidente"
    CORTO_A_LARGO = "Pierna corta en supino se alarga al sentarse"
    LARGO_A_CORTO = "Pierna larga en supino se acorta al sentarse"
    SE_MANTIENE_CORTO = "Pierna corta se mantiene corta al sentarse"


class SurcoSacro(str, Enum):
    NEUTRO = "Neutro / Simétrico"
    PROFUNDO = "Profundo (Base anteriorizada)"
    PLANO = "Plano / Superficial (Base posteriorizada)"


class AnguloInferolateral(str, Enum):
    SIMETRICO = "Simétrico"
    POSTERIOR_INFERIOR = "Posterior e Inferior (Descendido)"
    ANTERIOR_SUPERIOR = "Anterior y Superior (Ascendido)"


class EstadoTejidoBlando(str, Enum):
    NORMAL = "Normal / Eutónico"
    HIPERTONICO = "Hipertónico / Banda tensa y puntos gatillo activos"


@dataclass
class DatosPaciente:
    identificador: str
    edad: int
    sexo: str
    lateralidad: str
    ocupacion_deporte: str
    tiempo_evolucion: TiempoEvolucion
    mecanismo_inicio: MecanismoInicio


@dataclass
class BanderasRojas:
    dolor_nocturno: bool = False
    compromiso_esfinteres: bool = False
    sintomas_constitucionales: bool = False
    rigidez_axial_juvenil: bool = False

    @property
    def hay_bandera_roja(self) -> bool:
        return any([
            self.dolor_nocturno,
            self.compromiso_esfinteres,
            self.sintomas_constitucionales,
            self.rigidez_axial_juvenil,
        ])

    def obtener_alertas_activas(self) -> List[str]:
        alertas = []
        if self.dolor_nocturno:
            alertas.append("Dolor nocturno no mecánico que interrumpe el sueño y no cede con reposo.")
        if self.compromiso_esfinteres:
            alertas.append("Pérdida de control esfinteriano / parestesia en silla de montar (Sospecha Cauda Equina).")
        if self.sintomas_constitucionales:
            alertas.append("Fiebre inexplicable, pérdida ponderal no intencionada o antecedente oncológico.")
        if self.rigidez_axial_juvenil:
            alertas.append("Rigidez matutina axial >45 min en <45 años (Sospecha Espondiloartritis axial).")
        return alertas


@dataclass
class ClusterLaslett:
    distraccion: bool = False
    compresion: bool = False
    thigh_thrust: bool = False
    faber: bool = False
    gaenslen: bool = False

    @property
    def total_positivos(self) -> int:
        return sum([
            self.distraccion,
            self.compresion,
            self.thigh_thrust,
            self.faber,
            self.gaenslen,
        ])

    @property
    def interpretacion(self) -> Tuple[str, str, str]:
        tot = self.total_positivos
        if tot == 0:
            return (
                "Baja probabilidad intraarticular (<10%)",
                "Sospecha mínima de dolor articular primario sacroilíaco. Considerar etiología miofascial pura, síndrome facetario L4-S1 o discopatía lumbar.",
                "badge-safe"
            )
        elif 1 <= tot <= 2:
            return (
                "Sospecha articular indeterminada",
                "Pruebas de provocación insuficientes para confirmar origen articular. Se requiere correlación estricta con hitos óseos, palpación fascial y provocación dinámica.",
                "badge-warning"
            )
        else:
            return (
                "Alta especificidad sacroilíaca (Clúster de Laslett POSITIVO)",
                "Presencia de 3 o más pruebas positivas. Sensibilidad del 91% y Especificidad del 87% para patología articular sacroilíaca confirmada por bloqueos anestésicos controlados.",
                "badge-danger"
            )


@dataclass
class ExamenPalpatorio:
    lado_restriccion: LadoRestriccion
    cresta_iliaca: PosicionNivel
    tuberosidad_isquiatica: PosicionNivel
    eias: HitoOseoPosicion
    eips: HitoOseoPosicion
    escalon_pubis: EscalonPubico
    maleolo_supino: MaleoloSupino
    long_sitting: LongSittingTest
    surco_sacro: SurcoSacro
    ail: AnguloInferolateral
    piramidal: EstadoTejidoBlando
    ligamento_sacrotuberoso_tenso: bool


@dataclass
class DiagnosticoBiomecanico:
    titulo: str
    subtitulo: str
    clasificacion_tipo: str
    nivel_concordancia: str
    justificacion_clinica: List[str]
    vector_ajuste: str
    tecnica_met: str
    inhibicion_miofascial: List[str]
    contraindicacion_hvla: bool = False


# ==============================================================================
# MOTOR DE DECISIÓN BIOMECÁNICA (LÓGICA PURA Y REGLAS CLÍNICAS)
# ==============================================================================

def inferir_diagnostico(
    palpacion: ExamenPalpatorio,
    banderas_rojas: BanderasRojas,
    cluster: ClusterLaslett
) -> DiagnosticoBiomecanico:
    """
    Función pura y determinista para inferir la disfunción sacroilíaca/iliosacra:
    - Traslaciones en eje vertical (Downslip / Upslip)
    - Disfunciones combinadas (Ilíaco Postero-Inferior / Gonstead PI)
    - Rotaciones sagitales puras (Ilíaco Posterior / Ilíaco Anterior)
    - Disfunciones sacras primarias y patrones mixtos adaptativos.
    """
    lado = palpacion.lado_restriccion.value
    contraindicacion = banderas_rojas.hay_bandera_roja

    cresta_alta = palpacion.cresta_iliaca == PosicionNivel.ALTA
    cresta_baja = palpacion.cresta_iliaca == PosicionNivel.BAJA
    
    isquion_alto = palpacion.tuberosidad_isquiatica == PosicionNivel.ALTA
    isquion_bajo = palpacion.tuberosidad_isquiatica == PosicionNivel.BAJA
    
    eias_alta = palpacion.eias == HitoOseoPosicion.ALTA
    eias_baja = palpacion.eias == HitoOseoPosicion.BAJA
    
    eips_alta = palpacion.eips == HitoOseoPosicion.ALTA
    eips_baja = palpacion.eips == HitoOseoPosicion.BAJA
    
    maleolo_corto = palpacion.maleolo_supino == MaleoloSupino.CORTO
    maleolo_largo = palpacion.maleolo_supino == MaleoloSupino.LARGO
    
    sitting_alarga = palpacion.long_sitting == LongSittingTest.CORTO_A_LARGO
    sitting_acorta = palpacion.long_sitting == LongSittingTest.LARGO_A_CORTO
    sitting_fijo = palpacion.long_sitting == LongSittingTest.SE_MANTIENE_CORTO
    
    pubis_alto = palpacion.escalon_pubis == EscalonPubico.SUPERIOR
    pubis_bajo = palpacion.escalon_pubis == EscalonPubico.INFERIOR
    
    sacrotuberoso_tenso = palpacion.ligamento_sacrotuberoso_tenso
    piramidal_tenso = palpacion.piramidal == EstadoTejidoBlando.HIPERTONICO

    # --------------------------------------------------------------------------
    # 1. ILÍACO POSTERO-INFERIOR (DISFUNCIÓN COMBINADA / GONSTEAD PI)
    # Regla: Rotación Posterior (EIAS alta, EIPS baja, pierna corta funcional)
    #        + Descenso Global (Cresta baja y/o Tuberosidad isquiática baja)
    # --------------------------------------------------------------------------
    tiene_signos_rotacion_posterior = (eias_alta and eips_baja and maleolo_corto)
    tiene_signos_descenso_global = (cresta_baja or isquion_bajo)

    if tiene_signos_rotacion_posterior and tiene_signos_descenso_global:
        justificaciones = [
            f"Componente Rotacional Posterior: EIAS Alta combinada con EIPS Baja homolateral en la hemipelvis {lado}.",
            "Pierna funcionalmente corta en decúbito supino secundaria al retroceso y elevación relativa de la cavidad cotiloidea.",
            f"Componente de Cizallamiento Inferior: Descenso de la cresta ilíaca ({palpacion.cresta_iliaca.value}) y/o de la tuberosidad isquiática ({palpacion.tuberosidad_isquiatica.value}).",
            "Disfunción combinada característica de la subluxación 'PI' (Postero-Inferior) según el análisis y biomecánica quiropráctica de Gonstead."
        ]
        if sacrotuberoso_tenso:
            justificaciones.append("Tensión aumentada simultánea en el ligamento sacrotuberoso por combinación de retroversión y descenso.")
        if piramidal_tenso:
            justificaciones.append("Espasmo reactivo con puntos gatillo activos en el músculo piramidal homolateral.")

        return DiagnosticoBiomecanico(
            titulo=f"Ilíaco Postero-Inferior (PI) {lado}",
            subtitulo="Rotación Posterior con componente de Cizallamiento Inferior (Downslip)",
            clasificacion_tipo="Disfunción Combinada Sagital-Vertical (Quiropraxia Gonstead - PI)",
            nivel_concordancia="Alta (Concordancia de rotación posterior sagital + traslación vertical inferior)",
            justificacion_clinica=justificaciones,
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Ajuste en Decúbito Lateral (Side-Posture Gonstead PI) con hemipelvis {lado} hacia arriba. Punto de contacto: Pisiforme en el aspecto postero-inferior de la EIPS {lado}. Vector de corrección combinado: Posterior a Anterior (P-A) con línea de conducción oblicua antero-superior (vector de empuje de abajo hacia arriba en ángulo de 45°) para corregir simultáneamente la rotación posterior y la basculación inferior."
            ),
            tecnica_met=(
                f"MET combinada para PI {lado}: Paciente en decúbito supino con el miembro {lado} en el borde de la camilla. "
                "Contracción isométrica resistida de flexores de cadera (cuádriceps/psoas para inducir rotación anterior) "
                "asociada a contracción sincrónica del cuadrado lumbar homolateral para ascender el innominado en el plano frontal (3 a 5 ciclos de 7-10 s)."
            ),
            inhibicion_miofascial=[
                f"Músculo Piramidal {lado} (técnica neuromuscular y compresión isquémica)",
                f"Ligamento Sacrotuberoso homolateral",
                f"Porción proximal de Isquiotibiales (Bíceps Femoral y Semitendinoso {lado})",
                "Fibras inferiores del Glúteo Mayor"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 2. ILÍACO INFERIOR (DOWNSLIP) - TRASLACIÓN CAUDAL EN BLOQUE
    # Regla: Cresta baja + Isquion bajo + EIAS baja + EIPS baja + Maléolo funcional largo + Sacrotuberoso tenso
    # --------------------------------------------------------------------------
    es_downslip = (
        cresta_baja and isquion_bajo and (eias_baja and eips_baja) and maleolo_largo and sacrotuberoso_tenso
    ) or (
        cresta_baja and isquion_bajo and eias_baja and eips_baja and (maleolo_largo or sacrotuberoso_tenso or pubis_bajo)
    )

    if es_downslip:
        justificaciones = [
            f"Descenso global en bloque del hemicuerpo pélvico {lado}: Cresta ilíaca baja y Tuberosidad isquiática baja coincidentes.",
            f"Hitos ilíacos en descenso armónico homolateral: EIAS baja y EIPS baja en el lado afectado.",
            "Maléolo medial funcionalmente largo en decúbito supino por traslación caudal de la cavidad cotiloidea/acetábulo.",
            "Tensión reactiva aumentada en el ligamento sacrotuberoso por distensión y vector de tracción inferior del isquion.",
        ]
        if pubis_bajo:
            justificaciones.append("Escalón inferior evidente en la sínfisis púbica por descenso de la rama pubiana ipsilateral.")

        return DiagnosticoBiomecanico(
            titulo=f"Ilíaco Inferior (Downslip) {lado}",
            subtitulo="Subluxación o cizallamiento vertical inferior no fisiológico del hueso innominado (traslación caudal en bloque)",
            clasificacion_tipo="Disfunción Iliosacra en Cizallamiento Vertical (Downslip)",
            nivel_concordancia="Alta (Concordancia total de descenso óseo en bloque + tensión sacrotuberosa)",
            justificacion_clinica=justificaciones,
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Paciente en decúbito prono o supino. Contacto firme sobre la tuberosidad isquiática {lado} con el talón de la mano. Vector de empuje estrictamente Céfalo-Craneal (de Caudal a Craneal / empuje ascendente) para reducir el cizallamiento vertical inferior. Alternativa: técnica de bloqueo pélvico con cuña trocantérea inferior."
            ),
            tecnica_met=(
                f"Técnica de Mitchell para Downslip {lado}: Paciente en decúbito supino. El clínico estabiliza el hombro y pelvis opuesta mientras el paciente "
                "realiza una contracción isométrica concéntrica de la musculatura elevadora pélvica homolateral (Cuadrado Lumbar y oblicuos abdominales {lado}) "
                "intentando aproximar la cresta ilíaca hacia las costillas contra resistencia manual al 25% de esfuerzo por 7-10 s en inspiración profunda (3 a 5 ciclos)."
            ),
            inhibicion_miofascial=[
                f"Liberación por presión inhibitoria del Ligamento Sacrotuberoso {lado} (hipertenso)",
                f"Descarga de la musculatura Aductora homolateral (Aductor Mayor y Medio)",
                f"Inhibición fascial de la cintilla iliotibial y tensor de la fascia lata {lado}"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 3. ILÍACO SUPERIOR (UPSLIP) - CIZALLAMIENTO VERTICAL CRANEAL
    # Coherencia inversa: Cresta alta + Isquion alto + EIAS/EIPS altas + pierna corta
    # --------------------------------------------------------------------------
    es_upslip = (
        cresta_alta and isquion_alto and eias_alta and eips_alta and (maleolo_corto or sitting_fijo or pubis_alto)
    ) or (
        eias_alta and eips_alta and (pubis_alto or sitting_fijo or (cresta_alta and isquion_alto))
    )

    if es_upslip:
        justificaciones = [
            f"Ascenso en bloque de la hemipelvis {lado}: Cresta ilíaca Alta e Isquion Alto simultáneos.",
            f"EIAS Alta simultánea a EIPS Alta en el lado con restricción.",
            "Long-Sitting Test positivo para dismetría anatómica aparente: pierna corta que se mantiene corta al sentarse.",
            "Tensión reactiva secundaria severa en cuadrado lumbar homolateral y ligamento iliolumbar."
        ]
        if pubis_alto:
            justificaciones.append("Escalón de sínfisis púbica superior ipsilateral por ascenso de la rama pubiana.")

        return DiagnosticoBiomecanico(
            titulo=f"Ilíaco Superior (Upslip) {lado}",
            subtitulo="Subluxación o cizallamiento vertical superior no fisiológico del hueso innominado (traslación craneal en bloque)",
            clasificacion_tipo="Disfunción Iliosacra en Cizallamiento Vertical (Upslip)",
            nivel_concordancia="Alta (Tríada clásica de Cresta/Isquion/EIAS/EIPS elevadas + dismetría fija)",
            justificacion_clinica=justificaciones,
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Tracción axial caudal de la extremidad inferior {lado} en decúbito supino/prono con 15° de abducción y rotación interna de cadera. Impulso HVLA en dirección estrictamente céfalo-caudal."
            ),
            tecnica_met=(
                f"Técnica de Mitchell para Upslip {lado}: Paciente en decúbito supino. Cadera en abducción y tracción leve. "
                "Contracción isométrica resistida de la musculatura lateral del tronco (cuadrado lumbar homolateral) al 20% "
                "de fuerza máxima durante 7-10 s en espiración, seguida de elongación y tracción caudal en fase de relajación (3 ciclos)."
            ),
            inhibicion_miofascial=[
                f"Desactivación de puntos gatillo en Cuadrado Lumbar {lado}",
                "Inhibición de fibras del músculo Dorsal Ancho y psoas ilíaco",
                "Liberación fascial del ligamento iliolumbar y sacroilíaco posterior"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 4. ILÍACO POSTERIOR (ROTACIÓN SAGITAL PURA)
    # --------------------------------------------------------------------------
    if eias_alta and eips_baja:
        concordancias = [
            f"EIAS Alta con EIPS Baja homolateral en {lado} (rotación sagital posterior sin cizallamiento vertical global dominante)."
        ]
        if maleolo_corto:
            concordancias.append("Maléolo medial aparente corto en decúbito supino por posteriorización acetabular.")
        if sitting_alarga:
            concordancias.append("Long-Sitting Test clásico: Pierna corta funcional se alarga al pasar a sedente por palanca iliofemoral.")
        if piramidal_tenso or sacrotuberoso_tenso:
            concordancias.append("Hipertonía del piramidal y/o tensión aumentada en ligamento sacrotuberoso.")

        nivel = "Alta (Concordancia total de hitos rotacionales y pruebas dinámicas)" if (sitting_alarga and maleolo_corto) else "Moderada a Alta"

        return DiagnosticoBiomecanico(
            titulo=f"Ilíaco Posterior {lado}",
            subtitulo="Rotación posterior fija del hueso coxal sobre el eje transverso sacroilíaco",
            clasificacion_tipo="Disfunción Iliosacra Rotacional Sagital",
            nivel_concordancia=nivel,
            justificacion_clinica=concordancias,
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Decúbito lateral (Side-Posture) con hemipelvis {lado} hacia arriba. Contacto específico del pisiforme en la EIPS {lado}. Vector de empuje de Posterior a Anterior (P-A) con ligera inclinación superior y cefálica para rotar el innominado a anterior."
            ),
            tecnica_met=(
                f"MET para Ilíaco Posterior {lado}: Paciente en decúbito prono o supino con la extremidad {lado} colgando fuera de la camilla en extensión de cadera. "
                "El clínico estabiliza la pelvis y solicita una contracción isométrica del cuádriceps/recto femoral (flexores de cadera) "
                "hacia el techo al 25% de esfuerzo por 7-10 s. Tras la relajación, llevar la cadera a mayor extensión guiando el ilíaco a rotación anterior (3 a 5 repeticiones)."
            ),
            inhibicion_miofascial=[
                f"Músculo Piramidal {lado} (Puntos Gatillo y técnica de compresión isquémica)",
                f"Ligamento Sacrotuberoso homolateral",
                f"Isquiotibiales y Glúteo Mayor {lado}"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 5. ILÍACO ANTERIOR (ROTACIÓN SAGITAL PURA)
    # --------------------------------------------------------------------------
    if eias_baja and eips_alta:
        concordancias = [
            f"EIAS Baja con EIPS Alta homolateral en {lado} (rotación sagital anterior del coxal)."
        ]
        if maleolo_largo:
            concordancias.append("Maléolo medial aparente largo en supino por anteriorización y descenso acetabular.")
        if sitting_acorta:
            concordancias.append("Long-Sitting Test clásico: Pierna larga funcional se acorta al pasar a sedente.")
        if pubis_bajo:
            concordancias.append("Sínfisis púbica con escalón inferior en el lado ipsilateral.")

        nivel = "Alta (Concordancia ósea y dinámica confirmada)" if (sitting_acorta and maleolo_largo) else "Moderada a Alta"

        return DiagnosticoBiomecanico(
            titulo=f"Ilíaco Anterior {lado}",
            subtitulo="Rotación anterior fija del hueso coxal sobre el eje articular sacroilíaco",
            clasificacion_tipo="Disfunción Iliosacra Rotacional Sagital",
            nivel_concordancia=nivel,
            justificacion_clinica=concordancias,
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Decúbito lateral con hemipelvis {lado} hacia arriba. Contacto manual en la tuberosidad isquiática {lado}. Vector de empuje P-A con tracción anterior e inferior sobre el isquion para guiar la hemipelvis en rotación posterior."
            ),
            tecnica_met=(
                f"MET para Ilíaco Anterior {lado}: Paciente en decúbito supino. Rodilla y cadera {lado} en flexión máxima hacia el tórax. "
                "El clínico ofrece resistencia firme contra la rodilla mientras el paciente empuja hacia la extensión (activación isométrica de extensores de cadera: glúteo mayor e isquiotibiales) "
                "al 20-25% de esfuerzo por 7-10 s. Durante la relajación, ganar mayor flexión de cadera rotando el ilíaco a posterior (3 a 5 ciclos)."
            ),
            inhibicion_miofascial=[
                f"Músculo Psoas-Ilíaco {lado} (técnica de liberación en fosa ilíaca)",
                f"Músculo Recto Femoral y Tensor de la Fascia Lata",
                f"Cuádriceps y ligamento iliofemoral"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 6. DISFUNCIONES SACRAS PRIMARIAS (NUTACIÓN / CONTRANUTACIÓN)
    # --------------------------------------------------------------------------
    surco_profundo = palpacion.surco_sacro == SurcoSacro.PROFUNDO
    surco_plano = palpacion.surco_sacro == SurcoSacro.PLANO
    ail_descendido = palpacion.ail == AnguloInferolateral.POSTERIOR_INFERIOR
    ail_ascendido = palpacion.ail == AnguloInferolateral.ANTERIOR_SUPERIOR

    if surco_profundo and ail_descendido:
        return DiagnosticoBiomecanico(
            titulo=f"Nutación Sacra Unilateral {lado} (Sacro en Flexión)",
            subtitulo="Base sacra anteriorizada y ángulo inferolateral posterior/inferior ipsilateral",
            clasificacion_tipo="Disfunción Sacroilíaca Primaria (Sacro sobre Coxal)",
            nivel_concordancia="Alta (Surco profundo coincidente con AIL posterior)",
            justificacion_clinica=[
                f"Surco sacro {lado} marcadamente profundo por desplazamiento anterior de la base sacra.",
                f"AIL homolateral prominente hacia posterior e inferior.",
                "Compromiso de la cinemática sacroilíaca con alteración en la transferencia de cargas lumbosacras."
            ],
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Paciente en decúbito prono. Contacto sobre el AIL {lado} con el talón de la mano. Vector de empuje Antero-Superior coordinado con la fase inspiratoria para restaurar la contranutación fisiológica."
            ),
            tecnica_met=(
                "Técnica de MET sacra: Paciente en decúbito prono con apnea inspiratoria para favorecer la elevación de la base sacra. "
                "Contracción suave y sostenida del piramidal contralateral contra resistencia moderada."
            ),
            inhibicion_miofascial=[
                "Ligamento sacrotuberoso y sacroespinoso homolaterales",
                "Músculo Piramidal y multífidos lumbosacros L5-S1"
            ],
            contraindicacion_hvla=contraindicacion
        )

    if surco_plano and ail_ascendido:
        return DiagnosticoBiomecanico(
            titulo=f"Contranutación Sacra Unilateral {lado} (Sacro en Extensión)",
            subtitulo="Base sacra posteriorizada y ángulo inferolateral anterior/superior ipsilateral",
            clasificacion_tipo="Disfunción Sacroilíaca Primaria (Sacro sobre Coxal)",
            nivel_concordancia="Moderada a Alta",
            justificacion_clinica=[
                f"Surco sacro {lado} plano o superficial con resistencia a la traslación anterior.",
                f"AIL homolateral hundido (anteriorizado y superior)."
            ],
            vector_ajuste=(
                "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
                f"Paciente en prono. Contacto del carpo sobre la base sacra {lado}. Vector de empuje P-A puro mantenido durante la espiración forzada del paciente."
            ),
            tecnica_met=(
                "MET de flexión sacra: Paciente en esfinge / decúbito prono sobre codos. Espiración profunda mientras el terapeuta sostiene "
                "la base sacra guiándola hacia la nutación anterior."
            ),
            inhibicion_miofascial=[
                "Multífidos lumbares profundos",
                "Erectores espinales lumbosacros"
            ],
            contraindicacion_hvla=contraindicacion
        )

    # --------------------------------------------------------------------------
    # 7. CASO POR DEFECTO: PATRÓN COMPENSATORIO MIXTO
    # --------------------------------------------------------------------------
    return DiagnosticoBiomecanico(
        titulo=f"Patrón Biomecánico Mixto / Compensatorio ({lado})",
        subtitulo="Signos palpatorios cruzados o fijaciones adaptativas lumbopélvicas múltiples",
        clasificacion_tipo="Patrón Complejo Adaptativo No Concluyente",
        nivel_concordancia="Indeterminado (Requiere descarga miofascial diagnóstica)",
        justificacion_clinica=[
            "Los hitos óseos no encuadran en una traslación vertical pura ni en una rotación sagital aislada.",
            "Posible coexistencia de asimetría pélvica torsional adaptativa secundaria a escoliosis funcional, espasmo de psoas o sobrecarga asimétrica.",
            "Recomendación: Efectuar protocolo de descarga miofascial en pelvitrocantéreos y reevaluar movilidad dinámica articular."
        ],
        vector_ajuste=(
            "⛔ CONTRAINDICADO por Banderas Rojas" if contraindicacion else
            "No se recomienda manipulación forzada HVLA inmediata. Priorizar movilización oscilatoria grado II-III suave y desrotación pélvica pasiva."
        ),
        tecnica_met=(
            "Protocolo de MET global de normalización pélvica de Mitchell: Contracción isométrica alternada en abducción y aducción de caderas "
            "en decúbito supino (técnica de shotgun pélvico suave y liberación de aductores)."
        ),
        inhibicion_miofascial=[
            "Descarga neuromuscular completa de Piramidales, Obturadores y Cuadrado Lumbar bilateral",
            "Liberación fascial del diafragma pélvico y ligamentos sacrotuberosos"
        ],
        contraindicacion_hvla=contraindicacion
    )


# ==============================================================================
# COMPONENTE DE VISUALIZACIÓN DINÁMICA DE CINEMÁTICA PELVIANA (CANVAS HTML5)
# ==============================================================================

def generar_componente_cinematica(
    lado: str,
    disfuncion_clave: str
) -> str:
    """
    Genera un componente interactivo HTML5 Canvas vectorial para visualizar
    el complejo pelviano, las articulaciones sacroilíacas y los vectores de corrección,
    incluyendo traslaciones verticales (Downslip/Upslip) y combinadas (PI).
    """
    html_code = f"""
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <style>
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
                user-select: none;
            }}
            body {{
                background-color: #0f172a;
                color: #e2e8f0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                padding: 10px;
                overflow: hidden;
            }}
            .viewport-container {{
                background: radial-gradient(circle at center, #1e293b 0%, #0b1120 100%);
                border: 1px solid #334155;
                border-radius: 12px;
                box-shadow: inset 0 2px 8px rgba(0,0,0,0.5), 0 8px 24px rgba(0,0,0,0.3);
                width: 100%;
                max-width: 950px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .toolbar {{
                width: 100%;
                padding: 10px 14px;
                background: #1e293b;
                border-bottom: 1px solid #334155;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: center;
                gap: 6px;
                border-radius: 12px 12px 0 0;
            }}
            .btn-group {{
                display: flex;
                flex-wrap: wrap;
                gap: 5px;
            }}
            button {{
                background: #334155;
                color: #f8fafc;
                border: 1px solid #475569;
                padding: 5px 10px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.15s ease;
            }}
            button:hover {{
                background: #475569;
                border-color: #64748b;
            }}
            button.active {{
                background: #0284c7;
                border-color: #38bdf8;
                box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
            }}
            .canvas-wrapper {{
                position: relative;
                width: 100%;
                height: 440px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            canvas {{
                display: block;
            }}
            .legend-panel {{
                width: 100%;
                padding: 8px 14px;
                background: #111827;
                border-top: 1px solid #1f2937;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-around;
                font-size: 11px;
                color: #94a3b8;
                border-radius: 0 0 12px 12px;
                gap: 8px;
            }}
            .legend-item {{
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .dot {{
                width: 10px;
                height: 10px;
                border-radius: 50%;
                display: inline-block;
            }}
        </style>
    </head>
    <body>
        <div class="viewport-container">
            <div class="toolbar">
                <div style="font-weight: 600; font-size: 12px; color: #38bdf8; display:flex; align-items:center; gap:6px;">
                    <span>🦴 VISOR CINEMÁTICO PELVIANO</span>
                    <span style="color:#94a3b8; font-weight:400;">| Lado: <strong>{lado}</strong></span>
                </div>
                <div class="btn-group">
                    <button id="btn-auto" class="active" onclick="setMode('auto')">Auto-Clínico</button>
                    <button id="btn-pi" onclick="setMode('pi')">Ilíaco PI (Gonstead)</button>
                    <button id="btn-down" onclick="setMode('down')">Downslip (-Y)</button>
                    <button id="btn-up" onclick="setMode('up')">Upslip (+Y)</button>
                    <button id="btn-post" onclick="setMode('post')">Ilíaco Posterior</button>
                    <button id="btn-ant" onclick="setMode('ant')">Ilíaco Anterior</button>
                    <button id="btn-reset" onclick="setMode('neutral')">Neutro</button>
                    <button id="btn-anim" onclick="toggleAnimation()">▶ Animar</button>
                </div>
            </div>
            
            <div class="canvas-wrapper">
                <canvas id="pelvisCanvas" width="900" height="440"></canvas>
            </div>
            
            <div class="legend-panel">
                <div class="legend-item"><span class="dot" style="background:#f59e0b;"></span> Cuña Sacra Central</div>
                <div class="legend-item"><span class="dot" style="background:#38bdf8;"></span> Coxal Izquierdo</div>
                <div class="legend-item"><span class="dot" style="background:#818cf8;"></span> Coxal Derecho</div>
                <div class="legend-item"><span class="dot" style="background:#10b981;"></span> Vector LOD Correctivo</div>
                <div class="legend-item"><span class="dot" style="background:#ef4444;"></span> EIAS / EIPS / Cresta</div>
            </div>
        </div>

        <script>
            const canvas = document.getElementById('pelvisCanvas');
            const ctx = canvas.getContext('2d');
            const ladoAfecto = "{lado}";
            const disfuncionInicial = "{disfuncion_clave}";
            
            let currentMode = "auto";
            let isAnimating = false;
            let animTime = 0;
            let animationFrameId = null;

            let rotL = 0, rotR = 0;
            let transYL = 0, transYR = 0;
            let vectorLOD = null;

            function aplicarConfiguracion(modo) {{
                currentMode = modo;
                rotL = 0; rotR = 0;
                transYL = 0; transYR = 0;
                vectorLOD = null;

                const isRight = (ladoAfecto === "Derecho");

                if (modo === "auto") {{
                    if (disfuncionInicial.includes("Postero-Inferior") || disfuncionInicial.includes("(PI)")) {{
                        aplicarConfiguracion("pi");
                        currentMode = "auto";
                    }} else if (disfuncionInicial.includes("Downslip") || disfuncionInicial.includes("Inferior")) {{
                        aplicarConfiguracion("down");
                        currentMode = "auto";
                    }} else if (disfuncionInicial.includes("Upslip") || disfuncionInicial.includes("Superior")) {{
                        aplicarConfiguracion("up");
                        currentMode = "auto";
                    }} else if (disfuncionInicial.includes("Posterior")) {{
                        aplicarConfiguracion("post");
                        currentMode = "auto";
                    }} else if (disfuncionInicial.includes("Anterior")) {{
                        aplicarConfiguracion("ant");
                        currentMode = "auto";
                    }} else {{
                        aplicarConfiguracion("neutral");
                        currentMode = "auto";
                    }}
                    return;
                }}

                if (modo === "down") {{
                    if (isRight) {{
                        transYR = 24;
                        vectorLOD = {{ side: 'right', type: 'UPWARD', text: 'Empuje Isquiático Caudo-Craneal' }};
                    }} else {{
                        transYL = 24;
                        vectorLOD = {{ side: 'left', type: 'UPWARD', text: 'Empuje Isquiático Caudo-Craneal' }};
                    }}
                }} else if (modo === "pi") {{
                    if (isRight) {{
                        rotR = 0.15;
                        transYR = 18;
                        vectorLOD = {{ side: 'right', type: 'GONSTEAD_PI', text: 'Vector P-A y Antero-Superior (EIPS)' }};
                    }} else {{
                        rotL = -0.15;
                        transYL = 18;
                        vectorLOD = {{ side: 'left', type: 'GONSTEAD_PI', text: 'Vector P-A y Antero-Superior (EIPS)' }};
                    }}
                }} else if (modo === "up") {{
                    if (isRight) {{
                        transYR = -24;
                        vectorLOD = {{ side: 'right', type: 'TRACTION', text: 'Tracción Axial Caudal' }};
                    }} else {{
                        transYL = -24;
                        vectorLOD = {{ side: 'left', type: 'TRACTION', text: 'Tracción Axial Caudal' }};
                    }}
                }} else if (modo === "post") {{
                    if (isRight) {{
                        rotR = 0.16;
                        transYR = 4;
                        vectorLOD = {{ side: 'right', type: 'PA', text: 'Vector P-A en EIPS' }};
                    }} else {{
                        rotL = -0.16;
                        transYL = 4;
                        vectorLOD = {{ side: 'left', type: 'PA', text: 'Vector P-A en EIPS' }};
                    }}
                }} else if (modo === "ant") {{
                    if (isRight) {{
                        rotR = -0.16;
                        transYR = -4;
                        vectorLOD = {{ side: 'right', type: 'AP', text: 'Vector P-A en Isquion' }};
                    }} else {{
                        rotL = 0.16;
                        transYL = -4;
                        vectorLOD = {{ side: 'left', type: 'AP', text: 'Vector P-A en Isquion' }};
                    }}
                }}
            }}

            function setMode(modo) {{
                document.querySelectorAll('.btn-group button').forEach(b => b.classList.remove('active'));
                const btn = document.getElementById('btn-' + (modo === 'neutral' ? 'reset' : modo));
                if (btn) btn.classList.add('active');
                aplicarConfiguracion(modo);
                render();
            }}

            function toggleAnimation() {{
                isAnimating = !isAnimating;
                const btn = document.getElementById('btn-anim');
                if (isAnimating) {{
                    btn.textContent = '⏸ Pausar';
                    btn.classList.add('active');
                    animate();
                }} else {{
                    btn.textContent = '▶ Animar';
                    btn.classList.remove('active');
                    cancelAnimationFrame(animationFrameId);
                    render();
                }}
            }}

            function animate() {{
                if (!isAnimating) return;
                animTime += 0.04;
                render();
                animationFrameId = requestAnimationFrame(animate);
            }}

            function drawSacrum(cx, cy) {{
                ctx.save();
                ctx.translate(cx, cy);

                ctx.beginPath();
                ctx.moveTo(-45, -70);
                ctx.lineTo(45, -70);
                ctx.bezierCurveTo(48, -20, 30, 40, 0, 75);
                ctx.bezierCurveTo(-30, 40, -48, -20, -45, -70);
                ctx.closePath();

                const grad = ctx.createLinearGradient(0, -70, 0, 75);
                grad.addColorStop(0, '#d97706');
                grad.addColorStop(1, '#78350f');
                ctx.fillStyle = grad;
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = '#f59e0b';
                ctx.stroke();

                ctx.strokeStyle = '#fbbf24';
                ctx.lineWidth = 1.5;
                for (let y = -45; y <= 35; y += 22) {{
                    ctx.beginPath();
                    ctx.moveTo(-25 + Math.abs(y)*0.3, y);
                    ctx.lineTo(25 - Math.abs(y)*0.3, y);
                    ctx.stroke();
                }}

                ctx.fillStyle = '#1e1b4b';
                [ [-16, -45], [16, -45], [-13, -23], [13, -23], [-10, -1], [10, -1], [-7, 21], [7, 21] ].forEach(pos => {{
                    ctx.beginPath();
                    ctx.arc(pos[0], pos[1], 3.5, 0, Math.PI * 2);
                    ctx.fill();
                }});

                ctx.fillStyle = '#fef3c7';
                ctx.font = 'bold 11px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('SACRO', 0, -80);
                ctx.font = '9px Inter, sans-serif';
                ctx.fillStyle = '#fcd34d';
                ctx.fillText('S1 - S5', 0, 92);

                ctx.restore();
            }}

            function drawCoxal(cx, cy, isLeft, rotation, translateY) {{
                ctx.save();
                
                const pivotX = isLeft ? cx - 110 : cx + 110;
                const pivotY = cy + 40;

                ctx.translate(pivotX, pivotY + translateY);
                ctx.rotate(rotation);

                const dx = isLeft ? 110 : -110;
                const dy = -40;
                ctx.translate(dx, dy);

                const sign = isLeft ? -1 : 1;

                ctx.beginPath();
                ctx.moveTo(sign * 45, -70);
                ctx.bezierCurveTo(sign * 70, -130, sign * 170, -120, sign * 180, -60); 
                ctx.lineTo(sign * 185, -30);
                ctx.bezierCurveTo(sign * 180, 0, sign * 160, 40, sign * 140, 55); 
                ctx.arc(sign * 115, 60, 26, isLeft ? Math.PI*1.8 : Math.PI*1.2, isLeft ? Math.PI*0.7 : Math.PI*0.3, !isLeft);
                ctx.bezierCurveTo(sign * 100, 115, sign * 40, 120, sign * 15, 95); 
                ctx.lineTo(sign * 5, 80);
                ctx.bezierCurveTo(sign * 30, 40, sign * 40, -20, sign * 45, -70);
                ctx.closePath();

                const grad = ctx.createLinearGradient(0, -120, 0, 100);
                if (isLeft) {{
                    grad.addColorStop(0, '#0284c7');
                    grad.addColorStop(1, '#0c4a6e');
                }} else {{
                    grad.addColorStop(0, '#6366f1');
                    grad.addColorStop(1, '#312e81');
                }}
                ctx.fillStyle = grad;
                ctx.fill();
                ctx.lineWidth = 2;
                ctx.strokeStyle = isLeft ? '#38bdf8' : '#818cf8';
                ctx.stroke();

                // EIAS
                const eiasX = sign * 185;
                const eiasY = -30;
                ctx.fillStyle = '#ef4444';
                ctx.beginPath();
                ctx.arc(eiasX, eiasY, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.fillStyle = '#fca5a5';
                ctx.font = 'bold 10px Inter, sans-serif';
                ctx.textAlign = isLeft ? 'right' : 'left';
                ctx.fillText('EIAS ' + (isLeft ? 'IZQ' : 'DER'), eiasX + (isLeft ? -8 : 8), eiasY - 4);

                // EIPS
                const eipsX = sign * 50;
                const eipsY = -85;
                ctx.fillStyle = '#f59e0b';
                ctx.beginPath();
                ctx.arc(eipsX, eipsY, 5, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.fillStyle = '#fde68a';
                ctx.font = 'bold 10px Inter, sans-serif';
                ctx.textAlign = isLeft ? 'right' : 'left';
                ctx.fillText('EIPS ' + (isLeft ? 'IZQ' : 'DER'), eipsX + (isLeft ? -8 : 8), eipsY - 6);

                // Tuberosidad Isquiática
                const isquionX = sign * 80;
                const isquionY = 115;
                ctx.fillStyle = '#38bdf8';
                ctx.beginPath();
                ctx.arc(isquionX, isquionY, 4.5, 0, Math.PI * 2);
                ctx.fill();
                ctx.strokeStyle = '#ffffff';
                ctx.lineWidth = 1.2;
                ctx.stroke();

                ctx.fillStyle = '#bae6fd';
                ctx.font = '9px Inter, sans-serif';
                ctx.textAlign = isLeft ? 'right' : 'left';
                ctx.fillText('Isquion', isquionX + (isLeft ? -8 : 8), isquionY + 4);

                // Cresta Ilíaca
                const crestaX = sign * 125;
                const crestaY = -125;
                ctx.fillStyle = '#e2e8f0';
                ctx.font = 'bold 9px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.fillText('Cresta Ilíaca', crestaX, crestaY);

                // Articulación Sacroilíaca
                ctx.strokeStyle = '#34d399';
                ctx.lineWidth = 3.5;
                ctx.setLineDash([4, 4]);
                ctx.beginPath();
                ctx.moveTo(sign * 46, -68);
                ctx.lineTo(sign * 44, 25);
                ctx.stroke();
                ctx.setLineDash([]);

                // Acetábulo
                ctx.fillStyle = '#0f172a';
                ctx.beginPath();
                ctx.arc(sign * 115, 60, 16, 0, Math.PI * 2);
                ctx.fill();
                ctx.lineWidth = 1;
                ctx.strokeStyle = '#94a3b8';
                ctx.stroke();

                ctx.restore();
            }}

            function drawPubicSymphysis(cx, cy, transL, transR) {{
                ctx.save();
                const yL = cy + 80 + transL;
                const yR = cy + 80 + transR;

                ctx.fillStyle = '#38bdf8';
                ctx.beginPath();
                ctx.moveTo(cx - 8, yL - 10);
                ctx.lineTo(cx + 8, yR - 10);
                ctx.lineTo(cx + 8, yR + 15);
                ctx.lineTo(cx - 8, yL + 15);
                ctx.closePath();
                ctx.fill();
                ctx.strokeStyle = '#bae6fd';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                if (Math.abs(transL - transR) > 8) {{
                    ctx.strokeStyle = '#ef4444';
                    ctx.lineWidth = 2;
                    ctx.beginPath();
                    ctx.moveTo(cx - 20, Math.min(yL, yR) - 10);
                    ctx.lineTo(cx + 20, Math.min(yL, yR) - 10);
                    ctx.stroke();

                    ctx.fillStyle = '#f87171';
                    ctx.font = '10px Inter, sans-serif';
                    ctx.textAlign = 'center';
                    ctx.fillText('Escalón Púbico', cx, Math.max(yL, yR) + 30);
                }}

                ctx.restore();
            }}

            function drawVectorArrow(fromX, fromY, toX, toY, text, color) {{
                ctx.save();
                ctx.strokeStyle = color;
                ctx.fillStyle = color;
                ctx.lineWidth = 3.5;

                const headlen = 12;
                const dx = toX - fromX;
                const dy = toY - fromY;
                const angle = Math.atan2(dy, dx);

                ctx.beginPath();
                ctx.moveTo(fromX, fromY);
                ctx.lineTo(toX, toY);
                ctx.stroke();

                ctx.beginPath();
                ctx.moveTo(toX, toY);
                ctx.lineTo(toX - headlen * Math.cos(angle - Math.PI / 6), toY - headlen * Math.sin(angle - Math.PI / 6));
                ctx.lineTo(toX - headlen * Math.cos(angle + Math.PI / 6), toY - headlen * Math.sin(angle + Math.PI / 6));
                ctx.closePath();
                ctx.fill();

                ctx.font = 'bold 11px Inter, sans-serif';
                ctx.textAlign = 'center';
                ctx.shadowColor = 'rgba(0,0,0,0.8)';
                ctx.shadowBlur = 4;
                ctx.fillText(text, (fromX + toX) / 2, (fromY + toY) / 2 - 12);

                ctx.restore();
            }}

            function render() {{
                ctx.clearRect(0, 0, canvas.width, canvas.height);

                const cx = canvas.width / 2;
                const cy = canvas.height / 2 - 10;

                let dynamicRotL = rotL;
                let dynamicRotR = rotR;
                let dynamicTransYL = transYL;
                let dynamicTransYR = transYR;

                if (isAnimating) {{
                    const wave = Math.sin(animTime);
                    dynamicRotL = rotL * (0.6 + 0.4 * wave);
                    dynamicRotR = rotR * (0.6 + 0.4 * wave);
                    dynamicTransYL = transYL * (0.6 + 0.4 * wave);
                    dynamicTransYR = transYR * (0.6 + 0.4 * wave);
                }}

                drawSacrum(cx, cy);
                drawCoxal(cx, cy, true, dynamicRotL, dynamicTransYL);
                drawCoxal(cx, cy, false, dynamicRotR, dynamicTransYR);
                drawPubicSymphysis(cx, cy, dynamicTransYL, dynamicTransYR);

                if (vectorLOD) {{
                    const isR = vectorLOD.side === 'right';
                    const targetX = isR ? cx + 180 : cx - 180;
                    const targetY = cy - 20;

                    if (vectorLOD.type === 'PA') {{
                        drawVectorArrow(
                            targetX + (isR ? 60 : -60), targetY - 40,
                            targetX, targetY,
                            vectorLOD.text,
                            '#10b981'
                        );
                    }} else if (vectorLOD.type === 'AP') {{
                        drawVectorArrow(
                            targetX, targetY + 120,
                            targetX + (isR ? 40 : -40), targetY + 60,
                            vectorLOD.text,
                            '#38bdf8'
                        );
                    }} else if (vectorLOD.type === 'TRACTION') {{
                        drawVectorArrow(
                            targetX, targetY + 70,
                            targetX, targetY + 140,
                            vectorLOD.text,
                            '#f59e0b'
                        );
                    }} else if (vectorLOD.type === 'UPWARD') {{
                        drawVectorArrow(
                            targetX, targetY + 150,
                            targetX, targetY + 70,
                            vectorLOD.text,
                            '#10b981'
                        );
                    }} else if (vectorLOD.type === 'GONSTEAD_PI') {{
                        drawVectorArrow(
                            targetX + (isR ? 70 : -70), targetY + 50,
                            targetX, targetY - 20,
                            vectorLOD.text,
                            '#38bdf8'
                        );
                    }}
                }}

                ctx.fillStyle = '#94a3b8';
                ctx.font = '11px Inter, sans-serif';
                ctx.textAlign = 'left';
                ctx.fillText('MODO: ' + currentMode.toUpperCase(), 20, 30);
            }}

            aplicarConfiguracion('auto');
            render();
        </script>
    </body>
    </html>
    """
    return html_code


# ==============================================================================
# GENERADOR DEL INFORME CLÍNICO EN PDF (FPDF2 CON CODIFICACIÓN ESPAÑOL)
# ==============================================================================

def sanitizar_para_pdf(texto: str) -> str:
    """
    Sanitiza el texto eliminando emojis no compatibles con fuentes estándar,
    preservando de forma intacta todos los caracteres del idioma español
    (tildes, eñes, diéresis, signos de puntuación y aperturas ¿ ¡).
    """
    if not texto:
        return ""
    reemplazos = {
        "⚖️": "", "🦴": "", "📋": "", "🔍": "", "🛑": "[ALERTA CRÍTICA]",
        "⚠️": "[ALERTA]", "✅": "[OK]", "⚡": "[*]", "🌙": "", "📉": "",
        "🌅": "", "🎯": "", "📖": "", "📐": "", "📏": "", "🧬": "",
        "🎮": "", "▶": ">", "⏸": "||", "💊": "", "🔄": "", "🧘": "",
        "📄": "", "👁️": "", "📥": "", "👤": "", "✓": "[V]", "✗": "[X]",
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "-", "≥": ">=", "≤": "<="
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    
    # Preservar caracteres en latin-1 (incluye el abecedario español completo)
    return "".join(c if ord(c) < 256 else " " for c in texto)


class ReporteBiomecanicoPDF(FPDF):
    """
    Clase personalizada de FPDF2 para generar informes clínicos formales
    con membrete institucional sobrio y pie de página con numeración continua.
    """
    def __init__(self, paciente_id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.paciente_id = paciente_id

    def header(self):
        # Franja institucional superior
        self.set_fill_color(15, 23, 42)  # Slate 900
        self.rect(0, 0, 210, 6, "F")
        
        # Título del informe
        self.set_y(10)
        self.set_font("Helvetica", "B", 13)
        self.set_text_color(15, 23, 42)
        self.cell(0, 6, "INFORME DE EVALUACIÓN BIOMECÁNICA PÉLVICA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_font("Helvetica", "", 8.5)
        self.set_text_color(100, 116, 139)
        self.cell(0, 4, "SERVICIO DE BIOMECÁNICA CLÍNICA Y CRITERIOS QUIROPRÁCTICOS - BIOPELVIS PRO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(148, 163, 184)
        self.line(15, 282, 195, 282)
        self.cell(0, 8, f"Paciente: {sanitizar_para_pdf(self.paciente_id)} | Página {self.page_no()} de {{nb}} | Documento Clínico Confidencial", align="C")


def generar_reporte_pdf(
    paciente: DatosPaciente,
    banderas: BanderasRojas,
    cluster: ClusterLaslett,
    palpacion: ExamenPalpatorio,
    diag: DiagnosticoBiomecanico
) -> bytes:
    """
    Genera y compila el informe clínico formal en formato PDF utilizando fpdf2.
    Retorna el contenido en bytes listo para descarga inmediata.
    """
    pdf = ReporteBiomecanicoPDF(paciente_id=paciente.identificador)
    pdf.set_margins(15, 15, 15)
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    now_str = datetime.now().strftime("%d/%m/%Y %H:%M hrs")
    sacrotuberoso_str = "TENSIÓN AUMENTADA IPSILATERAL (Positivo)" if palpacion.ligamento_sacrotuberoso_tenso else "Tensión fisiológica normal"
    interpretacion_laslett, detalle_laslett, _ = cluster.interpretacion

    # --------------------------------------------------------------------------
    # ENCABEZADO INSTITUCIONAL: DATOS DEL PACIENTE Y METADATOS
    # --------------------------------------------------------------------------
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(15, pdf.get_y(), 180, 22, "FD")

    pdf.set_y(pdf.get_y() + 2)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(90, 4.2, sanitizar_para_pdf(f"  PACIENTE / FICHA: {paciente.identificador.upper()}"), new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 4.2, sanitizar_para_pdf(f"FECHA DE EMISIÓN: {now_str}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(90, 4.2, sanitizar_para_pdf(f"  Edad: {paciente.edad} años | Sexo: {paciente.sexo} | Lateralidad: {paciente.lateralidad}"), new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 4.2, sanitizar_para_pdf(f"Ocupación/Deporte: {paciente.ocupacion_deporte}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.cell(90, 4.2, sanitizar_para_pdf(f"  Tiempo de Evolución: {paciente.tiempo_evolucion.value}"), new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 4.2, sanitizar_para_pdf(f"Mecanismo de Inicio: {paciente.mecanismo_inicio.value}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

    # --------------------------------------------------------------------------
    # SECCIÓN 1: SEGURIDAD (BANDERAS ROJAS) Y CLÚSTER DE LASLETT
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(180, 5.5, " 1. SEGURIDAD Y BATERÍA DE PROVOCACIÓN ARTICULAR (LASLETT)", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Banner de Banderas Rojas
    if banderas.hay_bandera_roja:
        pdf.set_fill_color(254, 226, 226)
        pdf.set_draw_color(239, 68, 68)
        pdf.set_text_color(185, 28, 28)
        pdf.set_font("Helvetica", "B", 8)
        pdf.rect(15, pdf.get_y(), 180, 10, "FD")
        pdf.set_y(pdf.get_y() + 1.5)
        pdf.cell(180, 3.8, sanitizar_para_pdf(" [ALERTA CRÍTICA] Banderas rojas identificadas. MANIPULACIÓN HVLA CONTRAINDICADA."), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 7.5)
        for al in banderas.obtener_alertas_activas():
            pdf.cell(180, 3.4, sanitizar_para_pdf(f"   * {al}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)
    else:
        pdf.set_fill_color(220, 252, 231)
        pdf.set_draw_color(34, 197, 94)
        pdf.set_text_color(21, 128, 61)
        pdf.set_font("Helvetica", "B", 8)
        pdf.rect(15, pdf.get_y(), 180, 6, "FD")
        pdf.set_y(pdf.get_y() + 1)
        pdf.cell(180, 4, sanitizar_para_pdf(" [SEGURO] Criterios de exclusión negativos. Tratamiento biomecánico manual habilitado."), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(3)

    # Tabla de Pruebas de Provocación Articular
    pruebas_laslett = [
        ("Test de Distracción Anterior (Gapping test)", "POSITIVO" if cluster.distraccion else "Negativo"),
        ("Test de Compresión Ilíaca (Compression test)", "POSITIVO" if cluster.compresion else "Negativo"),
        ("Test de Thigh Thrust (Empuje Femoral / Cizallamiento posterior)", "POSITIVO" if cluster.thigh_thrust else "Negativo"),
        ("Test de FABER / Patrick (Flexión, Abducción, Rotación Externa)", "POSITIVO" if cluster.faber else "Negativo"),
        ("Test de Gaenslen (Torsión pelviana dinámica)", "POSITIVO" if cluster.gaenslen else "Negativo")
    ]

    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(15, 23, 42)
    pdf.set_draw_color(226, 232, 240)

    for desc, res in pruebas_laslett:
        pdf.cell(130, 4, sanitizar_para_pdf(f"  - {desc}"), border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        if res == "POSITIVO":
            pdf.set_font("Helvetica", "B", 7.5)
            pdf.set_text_color(185, 28, 28)
        else:
            pdf.set_font("Helvetica", "", 7.5)
            pdf.set_text_color(100, 116, 139)
        pdf.cell(50, 4, sanitizar_para_pdf(res), border="B", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "", 7.5)

    pdf.ln(2)
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(15, pdf.get_y(), 180, 6, "F")
    pdf.set_y(pdf.get_y() + 1)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(90, 4, sanitizar_para_pdf(f" Total Pruebas Positivas: {cluster.total_positivos} / 5"), new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 4, sanitizar_para_pdf(f"Nivel: {interpretacion_laslett}"), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: PROTOCOLO PALPATORIO DETALLADO
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(180, 5.5, " 2. PROTOCOLO PALPATORIO Y DINÁMICA ARTICULAR", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    col1_items = [
        ("Lado de Restricción:", palpacion.lado_restriccion.value),
        ("Cresta Ilíaca:", palpacion.cresta_iliaca.value),
        ("Tuberosidad Isquiática:", palpacion.tuberosidad_isquiatica.value),
        ("Espina Ilíaca Ántero-Sup (EIAS):", palpacion.eias.value),
        ("Espina Ilíaca Póstero-Sup (EIPS):", palpacion.eips.value),
        ("Sínfisis Púbica:", palpacion.escalon_pubis.value)
    ]
    col2_items = [
        ("Maléolo Medial (Supino):", palpacion.maleolo_supino.value),
        ("Long-Sitting Test (Inversión):", palpacion.long_sitting.value),
        ("Surco Sacro Homolateral:", palpacion.surco_sacro.value),
        ("Ángulo Inferolateral (AIL):", palpacion.ail.value),
        ("Músculo Piramidal:", palpacion.piramidal.value),
        ("Ligamento Sacrotuberoso:", sacrotuberoso_str)
    ]

    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(15, 23, 42)

    for i in range(len(col1_items)):
        # Columna Izquierda
        pdf.cell(48, 4.2, sanitizar_para_pdf(f" {col1_items[i][0]}"), border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(39, 4.2, sanitizar_para_pdf(col1_items[i][1]), border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "", 7.5)
        
        # Espaciador central
        pdf.cell(6, 4.2, "", new_x=XPos.RIGHT, new_y=YPos.TOP)
        
        # Columna Derecha
        pdf.cell(48, 4.2, sanitizar_para_pdf(f"{col2_items[i][0]}"), border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.cell(39, 4.2, sanitizar_para_pdf(col2_items[i][1]), border="B", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 7.5)

    pdf.ln(4)

    # --------------------------------------------------------------------------
    # SECCIÓN 3: JUICIO BIOMECÁNICO Y PRESCRIPCIÓN TERAPÉUTICA
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.cell(180, 5.5, " 3. JUICIO BIOMECÁNICO Y PRESCRIPCIÓN TERAPÉUTICA", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Caja de Diagnóstico Principal
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(2, 132, 199)
    pdf.rect(15, pdf.get_y(), 180, 16, "FD")
    pdf.set_y(pdf.get_y() + 1.5)
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(2, 132, 199)
    pdf.cell(180, 4.5, sanitizar_para_pdf(f"  DIAGNÓSTICO: {diag.titulo}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "I", 7.5)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(180, 3.8, sanitizar_para_pdf(f"  Subtipo: {diag.subtitulo}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(180, 3.8, sanitizar_para_pdf(f"  Categoría: {diag.clasificacion_tipo} | Concordancia: {diag.nivel_concordancia.split('(')[0].strip()}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(4)

    # Criterios y Justificación Clínica
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(180, 4, "Criterios y Correlaciones Clínicas Identificadas:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.5)
    for just in diag.justificacion_clinica:
        pdf.cell(180, 3.8, sanitizar_para_pdf(f"  * {just}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # Prescripción y Plan Terapéutico
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(180, 4, "Plan Terapéutico y Prescripción Biomecánica:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # 1. Ajuste Articular Biomecánico
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(180, 3.8, "  1. Ajuste Articular Biomecánico (Vector y Posicionamiento):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(diag.vector_ajuste))
    pdf.ln(1.5)

    # 2. Técnica de Energía Muscular (MET)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(180, 3.8, "  2. Técnica de Energía Muscular (MET - Fred Mitchell Sr.):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(diag.tecnica_met))
    pdf.ln(1.5)

    # 3. Inhibición Miofascial
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(180, 3.8, "  3. Protocolo de Inhibición Miofascial de Cadenas Acortadas:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    texto_mio = ", ".join(diag.inhibicion_miofascial)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(texto_mio))
    pdf.ln(6)

    # --------------------------------------------------------------------------
    # SECCIÓN DE FIRMA PROFESIONAL
    # --------------------------------------------------------------------------
    pdf.ln(3)
    pdf.set_draw_color(148, 163, 184)
    pdf.line(25, pdf.get_y(), 85, pdf.get_y())
    pdf.line(125, pdf.get_y(), 185, pdf.get_y())
    pdf.set_font("Helvetica", "", 7.5)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(90, 4, "Firma del Profesional Evaluador", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 4, "N° de Registro / Colegiatura", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())


# ==============================================================================
# ENCABEZADO Y HEADER CLÍNICO DE STREAMLIT
# ==============================================================================

st.markdown("""
<div class="clinical-header">
    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
        <div>
            <h1 style="margin:0; font-size:1.8rem; font-weight:700; letter-spacing:-0.02em;">
                ⚖️ BioPelvis Pro | Suite de Diagnóstico Sacroilíaco y Pelviano
            </h1>
            <p style="margin:4px 0 0 0; color:#94a3b8; font-size:0.95rem;">
                Inferencia Biomecánica Sagital y Vertical (Downslip/Upslip), Gonstead PI, Clúster de Laslett y Reportes Clínicos en PDF
            </p>
        </div>
        <div>
            <span class="badge badge-info" style="font-size:0.8rem; padding:6px 14px;">
                v2.2 • PDF MÉDICO
            </span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# PESTAÑAS PRINCIPALES DEL SISTEMA (WORKFLOW CRONOLÓGICO)
# ==============================================================================

tab_anamnesis, tab_exploracion, tab_visualizador, tab_juicio = st.tabs([
    "1. 📋 Anamnesis y Banderas Rojas",
    "2. 🔍 Provocación y Palpación",
    "3. 🦴 Visualización y Cinemática",
    "4. ⚖️ Juicio Clínico y Exportación"
])


# ------------------------------------------------------------------------------
# TAB 1: ANAMNESIS Y CRITERIOS DE EXCLUSIÓN (RED FLAGS)
# ------------------------------------------------------------------------------
with tab_anamnesis:
    st.markdown("### 👤 Datos Demográficos y Cronología del Dolor")
    
    col_dem1, col_dem2, col_dem3 = st.columns([2, 1, 1])
    with col_dem1:
        nombre_ficha = st.text_input(
            "Identificador del Paciente / Ficha Clínica:",
            value="PAC-2026-001",
            help="Ingrese el nombre completo o código alfanumérico para el informe."
        )
        ocupacion_deporte = st.text_input(
            "Ocupación laboral / Actividad deportiva predominante:",
            value="Trabajo de oficina (sedente 8h) / Corredor aficionado",
            help="Factores biomecánicos posturales o patrones de sobrecarga."
        )
    with col_dem2:
        edad = st.number_input("Edad:", min_value=12, max_value=105, value=38)
        lateralidad = st.selectbox("Lateralidad Dominante:", ["Diestro", "Zurdo", "Ambidiestro"])
    with col_dem3:
        sexo = st.selectbox("Sexo Biológico:", ["Masculino", "Femenino", "Otro"])

    col_cron1, col_cron2 = st.columns(2)
    with col_cron1:
        tiempo_evolucion_sel = st.selectbox(
            "Tiempo de Evolución de los Síntomas:",
            options=list(TiempoEvolucion),
            format_func=lambda x: x.value
        )
    with col_cron2:
        mecanismo_inicio_sel = st.selectbox(
            "Mecanismo Lesional o Desencadenante:",
            options=list(MecanismoInicio),
            format_func=lambda x: x.value
        )

    st.markdown("---")
    st.markdown("### 🛑 Protocolo de Banderas Rojas (Criterios de Exclusión de HVLA)")
    st.caption("Marque cualquier criterio positivo. La presencia de al menos una bandera roja contraindica absolutamente maniobras HVLA.")

    col_rf1, col_rf2 = st.columns(2)
    with col_rf1:
        rf_nocturno = st.checkbox(
            "🌙 **Dolor nocturno no mecánico** que despierta al paciente y no cede con el reposo.",
            help="Posible sospecha de patología oncológica o infección activa."
        )
        rf_esfinteres = st.checkbox(
            "⚡ **Pérdida de control de esfínteres / parestesia en 'silla de montar'**.",
            help="Urgencia neuroquirúrgica: Síndrome de Cauda Equina."
        )
    with col_rf2:
        rf_constitucional = st.checkbox(
            "📉 **Fiebre inexplicada, diaforesis nocturna, pérdida ponderal involuntaria o antecedente oncológico**.",
            help="Proceso infeccioso lumbopélvico o metástasis ósea."
        )
        rf_axial = st.checkbox(
            "🌅 **Rigidez matutina axial severa > 45 minutos** que mejora con la actividad en < 45 años.",
            help="Posible espondiloartritis axial / sacroileítis inflamatoria autoinmune (HLA-B27)."
        )

    banderas_rojas_inst = BanderasRojas(
        dolor_nocturno=rf_nocturno,
        compromiso_esfinteres=rf_esfinteres,
        sintomas_constitucionales=rf_constitucional,
        rigidez_axial_juvenil=rf_axial
    )

    if banderas_rojas_inst.hay_bandera_roja:
        st.error("""
        ### ⚠️ ADVERTENCIA CRÍTICA: CONTRAINDICACIÓN ABSOLUTA DE MANIPULACIÓN HVLA
        Se han marcado signos de alarma que sugieren compromiso sistémico, infeccioso, inflamatorio o neurológico grave.
        - **Acción Inmediata:** Descartar de inmediato técnicas de empuje de alta velocidad (HVLA) o descompresión forzada.
        - **Conducta Mandatoria:** Derivación urgente a especialista médico (Reumatología, Neurología o Traumatología) con solicitud de RMN pélvica/lumbosacra con secuencia STIR o analítica sanguínea (PCR, VSG, HLA-B27).
        """)
    else:
        st.success("✅ **Criterios de seguridad aprobados:** No se registran banderas rojas que contraindiquen la evaluación biomecánica manual.")

    paciente_inst = DatosPaciente(
        identificador=nombre_ficha,
        edad=edad,
        sexo=sexo,
        lateralidad=lateralidad,
        ocupacion_deporte=ocupacion_deporte,
        tiempo_evolucion=tiempo_evolucion_sel,
        mecanismo_inicio=mecanismo_inicio_sel
    )


# ------------------------------------------------------------------------------
# TAB 2: EXPLORACIÓN FÍSICA Y CLÚSTER DE PROVOCACIÓN
# ------------------------------------------------------------------------------
with tab_exploracion:
    st.markdown("### 🎯 Batería de Dolor Articular (Clúster de Laslett)")
    st.caption("Gold Standard clínico para descartar o confirmar compromiso intraarticular sacroilíaco.")

    col_las1, col_las2, col_las3 = st.columns([1.2, 1.2, 1.6])
    with col_las1:
        t_distraccion = st.checkbox("1. Test de Distracción Anterior (Gapping)", value=True)
        t_compresion = st.checkbox("2. Test de Compresión Ilíaca", value=True)
        t_thigh = st.checkbox("3. Test de Thigh Thrust (Empuje Femoral)", value=True)
    with col_las2:
        t_faber = st.checkbox("4. Test de FABER / Patrick", value=False)
        t_gaenslen = st.checkbox("5. Test de Gaenslen (Torsión pelviana)", value=False)

    cluster_inst = ClusterLaslett(
        distraccion=t_distraccion,
        compresion=t_compresion,
        thigh_thrust=t_thigh,
        faber=t_faber,
        gaenslen=t_gaenslen
    )

    interpretacion_laslett, detalle_laslett, badge_laslett = cluster_inst.interpretacion

    with col_las3:
        st.markdown(f"""
        <div class="metric-container">
            <div style="font-size:0.85rem; color:#64748b; font-weight:600;">PRUEBAS POSITIVAS</div>
            <div style="font-size:2.2rem; font-weight:700; color:#0f172a;">{cluster_inst.total_positivos} / 5</div>
            <div style="margin-top:4px;"><span class="badge {badge_laslett}">{interpretacion_laslett}</span></div>
        </div>
        """, unsafe_allow_html=True)
        st.info(f"**Nota clínica:** {detalle_laslett}")

    with st.expander("📖 Protocolo de Realización de las Pruebas de Laslett"):
        st.markdown("""
        - **Distracción Anterior:** Paciente en decúbito supino. Brazos cruzados del evaluador aplicando presión posterolateral sobre ambas EIAS. Tensa los ligamentos sacroilíacos anteriores.
        - **Compresión Ilíaca:** Paciente en decúbito lateral. Presión directa hacia abajo en la cresta ilíaca superior. Tensa los ligamentos sacroilíacos posteriores.
        - **Thigh Thrust:** Paciente en decúbito supino con flexión de cadera a 90°. Fuerza de cizallamiento posterior a lo largo del fémur estabilizando el sacro por detrás.
        - **FABER (Patrick):** Flexión, Abducción y Rotación Externa de cadera con maléolo sobre la rodilla opuesta. Dolor sacroilíaco posterior indica positividad.
        - **Gaenslen:** Una cadera en flexión máxima hacia el tórax y la opuesta en hiperextensión forzada al borde de la camilla.
        """)

    st.markdown("---")
    st.markdown("### 📐 Protocolo Palpatorio y de Movilidad Dinámica")
    
    lado_restriccion_sel = st.radio(
        "Lado con mayor restricción o dolor articular predominante:",
        options=list(LadoRestriccion),
        format_func=lambda x: x.value,
        horizontal=True
    )

    col_pal1, col_pal2, col_pal3 = st.columns(3)

    with col_pal1:
        st.markdown("##### 🦴 Hitos Óseos Ilíacos y Verticales")
        cresta_sel = st.selectbox(
            f"Cresta Ilíaca ({lado_restriccion_sel.value}):",
            options=list(PosicionNivel),
            format_func=lambda x: x.value,
            index=1  # Default: Nivelada
        )
        tuberosidad_sel = st.selectbox(
            f"Tuberosidad Isquiática ({lado_restriccion_sel.value}):",
            options=list(PosicionNivel),
            format_func=lambda x: x.value,
            index=1  # Default: Nivelada
        )
        eias_sel = st.selectbox(
            f"EIAS ({lado_restriccion_sel.value}):",
            options=list(HitoOseoPosicion),
            format_func=lambda x: x.value,
            index=1  # Default: Alta
        )
        eips_sel = st.selectbox(
            f"EIPS ({lado_restriccion_sel.value}):",
            options=list(HitoOseoPosicion),
            format_func=lambda x: x.value,
            index=2  # Default: Baja
        )
        escalon_pubis_sel = st.selectbox(
            f"Sínfisis Púbica ({lado_restriccion_sel.value}):",
            options=list(EscalonPubico),
            format_func=lambda x: x.value,
            index=0  # Default: Neutro
        )

    with col_pal2:
        st.markdown("##### 📏 Longitud de Extremidad y Dinámica")
        maleolo_sel = st.selectbox(
            f"Maléolo en Decúbito Supino ({lado_restriccion_sel.value}):",
            options=list(MaleoloSupino),
            format_func=lambda x: x.value,
            index=1  # Default: Corto funcional
        )
        long_sitting_sel = st.selectbox(
            "Long-Sitting Test (Inversión Supino a Sedente):",
            options=list(LongSittingTest),
            format_func=lambda x: x.value,
            index=1  # Default: Corto se alarga
        )
        st.caption("Prueba de Deerfield / Long-Sitting: evalúa la palanca iliofemoral sobre la dismetría aparente.")

    with col_pal3:
        st.markdown("##### 🧬 Sacro y Cadenas Miofasciales")
        surco_sacro_sel = st.selectbox(
            f"Surco Sacro ({lado_restriccion_sel.value}):",
            options=list(SurcoSacro),
            format_func=lambda x: x.value,
            index=0
        )
        ail_sel = st.selectbox(
            f"Ángulo Inferolateral - AIL ({lado_restriccion_sel.value}):",
            options=list(AnguloInferolateral),
            format_func=lambda x: x.value,
            index=0
        )
        piramidal_sel = st.selectbox(
            f"Tono Músculo Piramidal ({lado_restriccion_sel.value}):",
            options=list(EstadoTejidoBlando),
            format_func=lambda x: x.value,
            index=1  # Default: Hipertónico
        )
        sacrotuberoso_tenso_check = st.checkbox(
            "⚡ Tensión aumentada ipsilateral en Ligamento Sacrotuberoso",
            value=True,
            help="Signo cardinal de tracción caudal o rotación posterior del isquion."
        )

    palpacion_inst = ExamenPalpatorio(
        lado_restriccion=lado_restriccion_sel,
        cresta_iliaca=cresta_sel,
        tuberosidad_isquiatica=tuberosidad_sel,
        eias=eias_sel,
        eips=eips_sel,
        escalon_pubis=escalon_pubis_sel,
        maleolo_supino=maleolo_sel,
        long_sitting=long_sitting_sel,
        surco_sacro=surco_sacro_sel,
        ail=ail_sel,
        piramidal=piramidal_sel,
        ligamento_sacrotuberoso_tenso=sacrotuberoso_tenso_check
    )


# ------------------------------------------------------------------------------
# INFERENCIA BIOMECÁNICA (EJECUCIÓN DETERMINISTA)
# ------------------------------------------------------------------------------
diagnostico_actual = inferir_diagnostico(
    palpacion=palpacion_inst,
    banderas_rojas=banderas_rojas_inst,
    cluster=cluster_inst
)


# ------------------------------------------------------------------------------
# TAB 3: VISUALIZACIÓN DINÁMICA DE CINEMÁTICA PELVIANA
# ------------------------------------------------------------------------------
with tab_visualizador:
    st.markdown("### 🦴 Simulación Vectorial de Cinemática Pelviana y Vectores de Corrección")
    st.caption("El visor esquemático sincroniza automáticamente las rotaciones sagitales, traslaciones verticales (Downslip/Upslip) o combinadas (Gonstead PI).")

    col_view_info, col_view_canvas = st.columns([1, 2.5])

    with col_view_info:
        st.markdown(f"""
        <div class="clinical-card" style="background:#f1f5f9; border-left:4px solid #0284c7;">
            <div style="font-size:0.8rem; color:#64748b; font-weight:700;">ESTADO SINCRONIZADO</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0f172a; margin:4px 0;">{diagnostico_actual.titulo}</div>
            <div style="font-size:0.85rem; color:#475569;">{diagnostico_actual.subtitulo}</div>
            <hr style="margin:10px 0; border:0; border-top:1px solid #cbd5e1;" />
            <div style="font-size:0.8rem; color:#334155;">
                <strong>Cinemática observable:</strong>
                <ul style="padding-left:16px; margin-top:4px;">
                    <li>Desplazamiento vertical en bloque (Downslip / Upslip).</li>
                    <li>Rotación sagital pura o combinada (Ilíaco Postero-Inferior).</li>
                    <li>Asimetría de cresta, tuberosidad isquiática y sínfisis púbica.</li>
                    <li>Línea de conducción de ajuste articular (Vector Verde/Azul).</li>
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("##### 🎮 Modos del Visor:")
        st.markdown("""
        - **Auto-Clínico:** Carga automáticamente la disfunción inferida en la exploración.
        - **Ilíaco PI (Gonstead):** Rotación posterior combinada con descenso caudal.
        - **Downslip (-Y):** Cizallamiento o traslación inferior en bloque.
        - **Upslip (+Y):** Traslación craneal en bloque.
        - **Ilíaco Posterior / Anterior:** Rotaciones sagitales puras.
        - **Animar (▶):** Modulación oscilatoria dinámica.
        """)

    with col_view_canvas:
        canvas_html = generar_componente_cinematica(
            lado=palpacion_inst.lado_restriccion.value,
            disfuncion_clave=diagnostico_actual.titulo
        )
        components.html(canvas_html, height=520, scrolling=False)


# ------------------------------------------------------------------------------
# TAB 4: JUICIO CLÍNICO, PRESCRIPCIÓN Y EXPORTACIÓN EN PDF
# ------------------------------------------------------------------------------
with tab_juicio:
    st.markdown("### ⚖️ Juicio Diagnóstico Biomecánico y Prescripción Terapéutica")

    if banderas_rojas_inst.hay_bandera_roja:
        st.markdown(f"""
        <div style="background:#fee2e2; border:2px solid #ef4444; border-radius:8px; padding:16px; margin-bottom:16px;">
            <div style="color:#b91c1c; font-weight:700; font-size:1.05rem;">
                🛑 TRATAMIENTO MANUAL CONTRAINDICADO POR BANDERAS ROJAS ACTIVAS
            </div>
            <div style="color:#7f1d1d; font-size:0.9rem; margin-top:4px;">
                No aplicar empuje HVLA ni descompresión axial forzada. Se requiere derivación prioritaria.
            </div>
        </div>
        """, unsafe_allow_html=True)

    col_diag_main, col_diag_metrics = st.columns([2.2, 1])

    with col_diag_main:
        st.markdown(f"""
        <div class="clinical-card" style="border-left: 6px solid #0284c7;">
            <div style="font-size:0.8rem; color:#64748b; font-weight:700; text-transform:uppercase;">
                {diagnostico_actual.clasificacion_tipo}
            </div>
            <h2 style="margin:6px 0; color:#0f172a; font-size:1.6rem; font-weight:700;">
                {diagnostico_actual.titulo}
            </h2>
            <p style="color:#475569; font-size:0.95rem; margin-bottom:12px;">
                {diagnostico_actual.subtitulo}
            </p>
            <div style="background:#f8fafc; border-radius:6px; padding:12px; border:1px solid #e2e8f0;">
                <div style="font-weight:600; font-size:0.85rem; color:#334155; margin-bottom:6px;">
                    Criterios y Correlaciones Identificadas:
                </div>
                <ul style="margin:0; padding-left:20px; font-size:0.85rem; color:#475569;">
                    {''.join([f"<li>{just}</li>" for just in diagnostico_actual.justificacion_clinica])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_diag_metrics:
        st.markdown(f"""
        <div class="metric-container" style="margin-bottom:12px;">
            <div style="font-size:0.8rem; color:#64748b; font-weight:600;">CONCORDANCIA BIOMECÁNICA</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0369a1; margin:6px 0;">
                {diagnostico_actual.nivel_concordancia.split('(')[0]}
            </div>
            <div style="font-size:0.75rem; color:#64748b;">
                Correlación ósea, vertical y dinámica
            </div>
        </div>
        <div class="metric-container">
            <div style="font-size:0.8rem; color:#64748b; font-weight:600;">SENSIBILIDAD CLÚSTER LASLETT</div>
            <div style="font-size:1.1rem; font-weight:700; color:#0f172a; margin:6px 0;">
                {cluster_inst.total_positivos} de 5 positivos
            </div>
            <div>
                <span class="badge {badge_laslett}">{interpretacion_laslett.split('(')[0]}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 💊 Prescripción Biomecánica y Terapéutica")

    col_tx1, col_tx2, col_tx3 = st.columns(3)

    with col_tx1:
        st.markdown("##### 🔄 Ajuste Articular Biomecánico")
        if diagnostico_actual.contraindicacion_hvla:
            st.error("⛔ **Manipulación HVLA Bloqueada:** Presencia de banderas rojas en la anamnesis.")
        else:
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b;">
                <strong>Vector y Posicionamiento:</strong><br>
                {diagnostico_actual.vector_ajuste}
            </div>
            """, unsafe_allow_html=True)

    with col_tx2:
        st.markdown("##### ⚡ Técnica de Energía Muscular (MET)")
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b;">
            <strong>Protocolo de Fred Mitchell:</strong><br>
            {diagnostico_actual.tecnica_met}
        </div>
        """, unsafe_allow_html=True)

    with col_tx3:
        st.markdown("##### 🧘 Inhibición Miofascial de Cadenas Acortadas")
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b;">
            <strong>Músculos y Tejidos Diana:</strong>
            <ul style="padding-left:16px; margin-top:6px;">
        """ + "".join([f"<li>{m}</li>" for m in diagnostico_actual.inhibicion_miofascial]) + """
            </ul>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 📄 Generación y Descarga del Informe Clínico Oficial en PDF")

    # Generación del PDF con fpdf2
    pdf_bytes = generar_reporte_pdf(
        paciente=paciente_inst,
        banderas=banderas_rojas_inst,
        cluster=cluster_inst,
        palpacion=palpacion_inst,
        diag=diagnostico_actual
    )

    with st.expander("👁️ Resumen de Contenidos del Informe PDF para Ficha Médica"):
        st.markdown(f"""
        - **Paciente:** `{paciente_inst.identificador}` | **Fecha:** `{datetime.now().strftime('%d/%m/%Y %H:%M hrs')}`
        - **Diagnóstico:** **{diagnostico_actual.titulo}**
        - **Subtipo:** {diagnostico_actual.subtitulo}
        - **Seguridad Clínica:** `{'CRÍTICO - Banderas Rojas Activas' if banderas_rojas_inst.hay_bandera_roja else 'SEGURO - Sin Banderas Rojas'}`
        - **Clúster de Laslett:** `{cluster_inst.total_positivos} de 5 positivos` ({interpretacion_laslett})
        - **Lado Afectado:** `{palpacion_inst.lado_restriccion.value}` (Cresta: {palpacion_inst.cresta_iliaca.value}, Isquion: {palpacion_inst.tuberosidad_isquiatica.value}, EIAS: {palpacion_inst.eias.value}, EIPS: {palpacion_inst.eips.value})
        """)
        st.caption("El documento PDF generado incluye encabezado institucional, tablas palpatorias estructuradas, plan terapéutico con vectores y líneas para firma profesional.")

    nombre_archivo_pdf = f"informe_biomecanico_{paciente_inst.identificador.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    col_down1, col_down2 = st.columns([1.2, 2])
    with col_down1:
        st.download_button(
            label="📥 Descargar Informe Clínico (PDF)",
            data=pdf_bytes,
            file_name=nombre_archivo_pdf,
            mime="application/pdf",
            type="primary",
            use_container_width=True
        )
    with col_down2:
        st.caption("Documento formal en formato PDF (generado con fpdf2) listo para imprimir, enviar por correo o adjuntar a la historia clínica electrónica con validez médica legal.")