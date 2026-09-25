import base64
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import os
from typing import Dict, List, Optional, Tuple
from PIL import Image
import streamlit as st
import streamlit.components.v1 as components

# 1. Configuración de página (SIEMPRE la primera llamada de Streamlit)
try:
    icono = Image.open("assets/favicon.png")
except Exception:
    icono = "🦴"

st.set_page_config(
    page_title="Evaluación Sacroilíaca y Biomecánica 3D",
    page_icon=icono,
    layout="wide",
    initial_sidebar_state="collapsed",
)
from auth import render_auth_screen, render_user_badge, cerrar_sesion

if not render_auth_screen():
    st.stop()
# 2. Resto de importaciones del proyecto
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from clinical_knowledge import CLINICAL_KNOWLEDGE_BASE, get_disfuncion_info

# ==============================================================================
# SUITE CLÍNICA DE DIAGNÓSTICO BIOMECÁNICO SACROILÍACO E ILIOSACRO
# ==============================================================================

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

    /* Main Navigation Bar Styling (st.radio horizontal) */
    div[data-testid="stRadio"] > div[role="radiogroup"] {
        gap: 8px;
        padding: 6px 8px;
        background: #f1f5f9;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
        margin-bottom: 20px;
        display: flex;
        flex-wrap: wrap;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {
        background: #ffffff;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 0.90rem;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
        cursor: pointer;
        transition: all 0.2s ease;
    }
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {
        border-color: #0284c7;
        color: #0284c7;
        background: #f0f9ff;
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
    SUPERFICIAL = "Superficial (Base posteriorizada)"
    PLANO = "Plano / Superficial (Base posteriorizada)"


class AnguloInferolateral(str, Enum):
    SIMETRICO = "Neutro / Simétrico"
    SUPERFICIAL = "Superficial (Posterior)"
    PROFUNDO = "Profundo (Anterior)"
    MAS_BAJO = "Más bajo (Descendido / Caudal)"
    MAS_CRANEAL = "Más craneal (Ascendido / Cefálico)"
    POSTERIOR_INFERIOR = "Posterior e Inferior (Descendido)"
    ANTERIOR_SUPERIOR = "Anterior y Superior (Ascendido)"


class EstadoTejidoBlando(str, Enum):
    NORMOTONICO = "Normotónico / Eutónico (Normal)"
    HIPERTONICO = "Hipertonía / Tenso (Banda tensa activa)"
    NORMAL = "Normal / Eutónico"


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
    diametro_transverso: str = "Neutro / Simétrico"
    es_torsion_sacra: bool = False
    spring_test_positivo: bool = True


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
    clave_conocimiento: str = ""  # Llave que conecta con clinical_knowledge.py
    ejercicio_terapeutico: Dict[str, str] = field(default_factory=dict)


# ==============================================================================
# MOTOR DE DECISIÓN BIOMECÁNICA (LÓGICA PURA Y REGLAS CLÍNICAS)
# ==============================================================================
def _txt(val) -> str:
    if val is None:
        return ""
    if hasattr(val, "value"):
        return str(val.value).lower().strip()
    return str(val).lower().strip()


def _es_alto(val) -> bool:
    t = _txt(val)
    return "alt" in t or "superior" in t or "ascendid" in t


def _es_bajo(val) -> bool:
    t = _txt(val)
    return "baj" in t or "inferior" in t or "descendid" in t


def obtener_ejercicios_activos(clave: str, subtipo: str = "") -> Dict[str, str]:
    """
    Retorna la prescripción de ejercicio terapéutico y control sensorio-motor (Fase Activa)
    adaptada específicamente a la disfunción biomecánica diagnosticada.
    """
    if clave == "ILIACO_POSTERIOR":
        if "Downslip" in subtipo or "Cizallamiento" in subtipo:
            return {
                "Activación de Inhibidores Recíprocos y Tractores Craneales": (
                    "Fortalecimiento y reclutamiento analítico de flexores de cadera (psoas mayor, recto femoral) "
                    "en rangos finales junto a activación concéntrica del cuadrado lumbar homolateral para revertir el doble componente rotacional y de descenso."
                ),
                "Control Lumbopélvico y Estabilización Central": (
                    "Ejercicios de disociación lumbopélvica (Deadbug y Bird-dog) enfatizando el neutro pelviano, "
                    "evitando compensaciones en hiperlordosis o retroversión y manteniendo niveladas las crestas ilíacas."
                ),
                "Reeducación Funcional en Carga": (
                    "Pautas específicas para la marcha y apoyo monopodal (zancadas controladas / split squats y step-ups) "
                    "para transferir el ajuste a la dinámica funcional sin drop ni caída caudal de la hemipelvis."
                )
            }
        return {
            "Activación de Inhibidores Recíprocos": (
                "Fortalecimiento y reclutamiento analítico de flexores de cadera (psoas mayor, recto femoral) "
                "en rangos finales para fijar la basculación anterior."
            ),
            "Control Lumbopélvico y Estabilización Central": (
                "Ejercicios de disociación lumbopélvica (ej. Deadbug, Bird-dog o puentes bipodales a unipodales) "
                "enfatizando el neutro pelviano y evitando compensaciones en hiperlordosis o retroversión."
            ),
            "Reeducación Funcional en Carga": (
                "Pautas específicas para la marcha/apoyo monopodal (ej. zancadas controladas / split squats) "
                "para transferir el ajuste a la dinámica funcional."
            )
        }
    elif clave == "ILIACO_ANTERIOR":
        if "Upslip" in subtipo or "Cizallamiento" in subtipo:
            return {
                "Activación de Inhibidores Recíprocos y Depresores Pélvicos": (
                    "Reclutamiento analítico de extensores de cadera (isquiotibiales proximales y glúteo mayor) "
                    "junto a descompresión activa del cuadrado lumbar para revertir la anteversión y el ascenso en bloque."
                ),
                "Control Lumbopélvico y Estabilización Central": (
                    "Activación de pared abdominal anterior y oblicuos (Deadbug con presión lumbar) "
                    "para neutralizar la lordosis compensatoria y fijar la pelvis."
                ),
                "Reeducación Funcional en Carga": (
                    "Sentadillas bipodales controladas con retroversión activa final y trabajo de empuje de cadera (Hip Thrust) en neutro."
                )
            }
        return {
            "Activación de Inhibidores Recíprocos": (
                "Reclutamiento analítico de extensores de cadera (isquiotibiales proximales y glúteo mayor) "
                "en rangos funcionales para favorecer la retroversión coxal."
            ),
            "Control Lumbopélvico y Estabilización Central": (
                "Activación de la pared abdominal anterior y oblicuos (Deadbug con aplanamiento lumbar activo) "
                "para frenar la anteversión excesiva y el estrés lumbosacro L5-S1."
            ),
            "Reeducación Funcional en Carga": (
                "Sentadilla bipodal controlada con retroversión activa final y puentes de cadera (Hip Thrust) "
                "con fijación lumbopélvica en plano neutro."
            )
        }
    elif clave == "ILIACO_DOWNSLIP":
        return {
            "Activación de Tracción Craneal Ipsilateral": (
                "Reclutamiento concéntrico de cuadrado lumbar, dorsal ancho y oblicuos homolaterales "
                "en descarga lateral para inducir elevación pélvica."
            ),
            "Control Lumbopélvico y Estabilización Central": (
                "Planchas laterales con elevación pélvica homolateral activa (Pelvic Hike) "
                "manteniendo el alineamiento neutro de la cintura escapular y pélvica."
            ),
            "Reeducación Funcional en Carga": (
                "Ejercicios de Step-up con foco en nivelación horizontal de crestas en el apoyo unipodal "
                "y marcha rítmica evitando la caída caudal de la hemipelvis en fase de balanceo."
            )
        }
    elif clave == "ILIACO_UPSLIP":
        return {
            "Descompresión y Elongación Neuromuscular": (
                "Inhibición recíproca y tracción isométrica excéntrica de cuadrado lumbar homolateral; "
                "activación analítica de glúteo medio contralateral en apoyo."
            ),
            "Control Lumbopélvico y Estabilización Central": (
                "Disociación en descarga con auto-tracción axial lumbo-pélvica y respiración diafragmática "
                "enfocada en expandir la concavidad lumbar ipsilateral."
            ),
            "Reeducación Funcional en Carga": (
                "Reeducación simétrica de la descarga de peso en bipedestación con feedback en báscula bipodal "
                "y marcha cadenciosa con extensión completa de cadera en apoyo terminal."
            )
        }
    elif clave == "ILIACO_INFLARE":
        return {
            "Activación de Abductores y Rotadores Externos": (
                "Fortalecimiento analítico de rotadores externos y abductores de cadera (glúteo medio, piramidal, "
                "obturadores) mediante Clamshells resistidos con minicinta elástica."
            ),
            "Control Lumbopélvico y Estabilización Transversal": (
                "Puente glúteo bipodal con abducción sostenida contra resistencia elástica "
                "para promover la desrotación externa y apertura de la hemipelvis."
            ),
            "Reeducación Funcional en Carga": (
                "Desplazamientos laterales resistidos (Monster Walks) con énfasis en la estabilidad rotacional "
                "y control de la rodilla en el plano frontal."
            )
        }
    elif clave == "ILIACO_OUTFLARE":
        return {
            "Activación de Aductores y Rotadores Internos": (
                "Fortalecimiento analítico del compartimento aductor y tensor de la fascia lata "
                "(compresión isométrica de balón entre rodillas en sedente y supino)."
            ),
            "Control Lumbopélvico y Estabilización Transversal": (
                "Deadbug con aducción pélvica activa sostenida para cerrar el ángulo interespinal "
                "y centrar la articulación sacroilíaca."
            ),
            "Reeducación Funcional en Carga": (
                "Sentadillas sumo controladas y marcha en línea recta con zancada estrecha "
                "evitando la rotación externa patológica del pie y del coxal."
            )
        }
    elif "TORSION_SACRA" in clave:
        return {
            "Activación Neuromuscular Lumbosacra": (
                "Reclutamiento de multífidos lumbares en el cuadrante contralateral "
                "para favorecer la desrotación del bloque sacro sobre el eje oblicuo."
            ),
            "Control Lumbopélvico y Estabilización Segmentaria": (
                "Bird-dog unilateral enfocado en extensión pura de cadera sin rotación toracolumbar "
                "y control pélvico en decúbito prono."
            ),
            "Reeducación Funcional en Carga": (
                "Transferencias de sedente a bipedestación con alineación simétrica de la cuña sacra "
                "y pautas de descarga de peso en fases tempranas del apoyo."
            )
        }
    elif "SACRO_FLEXION" in clave:
        return {
            "Activación Antilordótica y Desnutación": (
                "Reclutamiento analítico del transverso abdominal y flexores profundos de tronco "
                "en decúbito supino (Deadbug con aplanamiento lumbar activo) para neutralizar la nutación sacra."
            ),
            "Control Sensorio-Motor y Descompresión Lumbosacra": (
                "Posición cuadrúpeda con respiración diafragmática y retroversión pélvica activa en espiración, "
                "guiando la base sacra hacia la extensión."
            ),
            "Reeducación Funcional en Carga": (
                "Sentadillas controladas en rango medio evitando la hiperextensión lumbosacra terminal "
                "con activación bilateral de glúteos mayores."
            )
        }
    elif "SACRO_EXTENSION" in clave:
        return {
            "Recuperación de la Nutación Fisiológica": (
                "Activación de multífidos lumbosacros bajos y erectores espinales en decúbito prono "
                "(Bird-dog con preservación lordótica fisiológica y extensión pura de cadera)."
            ),
            "Control Sensorio-Motor Lumbopélvico": (
                "Puente pélvico (Glute Bridge) con anteversión pélvica suave en el inicio del movimiento "
                "para dinamizar la charnela lumbosacra en nutación."
            ),
            "Reeducación Funcional en Carga": (
                "Bisagra de cadera (Hip Hinge) con pica manteniendo las curvaturas fisiológicas "
                "y evitando la rectificación lumbar rígida."
            )
        }
    elif "SACRO_ANTERO_INFERIOR" in clave:
        return {
            "Desrotación y Descarga del Piramidal": (
                "Inhibición activa y elongación neuromuscular del piramidal homolateral tenso "
                "mediante puente glúteo unilateral y rotaciones en descarga asistida."
            ),
            "Control Lumbopélvico en Cadena Cerrada": (
                "Split Squat búlgaro con feedback propioceptivo en crestas ilíacas "
                "manteniendo la pelvis perpendicular al plano de avance."
            ),
            "Reeducación de la Marcha y Apoyo Monopodal": (
                "Step-ups lentos y controlados con descarga uniforme del talón "
                "evitando la anteversión compensatoria de la hemipelvis afectada."
            )
        }
    elif "SACRO_POSTERO_SUPERIOR" in clave:
        return {
            "Reclutamiento Extensor y Anteriorización Sacra": (
                "Fortalecimiento analítico del glúteo mayor y multífidos ipsilaterales "
                "en decúbito prono con resistencia elástica ligera en el tobillo."
            ),
            "Control Sensorio-Motor y Descompresión": (
                "Descompresión en decúbito supino con tracción longitudinal auto-inducida "
                "y activación alternada de flexores/extensores coxofemorales."
            ),
            "Reeducación Funcional en Carga": (
                "Peso muerto rumano unilateral (Single-Leg RDL) controlado "
                "con fijación de la cuña sacra en plano neutro."
            )
        }
    else:
        return {
            "Reeducación Global Lumbopélvica": (
                "Movilizaciones pélvicas suaves en rango neutro (Cat-Camel), puentes bipodales neutros "
                "y activación del core profundo sin inducir dolor."
            ),
            "Control Sensorio-Motor Central": (
                "Respiración diafragmática coordinada con co-contracción suave de transverso del abdomen "
                "y suelo pélvico para estabilización global."
            ),
            "Reeducación Funcional en Carga": (
                "Pautas ergonómicas de marcha y sedestación simétrica con pausas activas regulares "
                "previas a la reevaluación biomecánica articular."
            )
        }


def _crear_diagnostico_desde_kb(
    clave: str,
    lado: str,
    concordancia: str,
    justificaciones: List[str],
    contraindicacion: bool,
    titulo_custom: Optional[str] = None,
    subtitulo_custom: Optional[str] = None,
    ejercicios_custom: Optional[Dict[str, str]] = None
) -> DiagnosticoBiomecanico:
    info = get_disfuncion_info(clave)
    titulo_final = titulo_custom or (f"{info.get('nombre_clinico', clave)} {lado}" if info else f"Disfunción ({clave}) {lado}")
    subtitulo_final = subtitulo_custom or (info.get("categoria", "") if info else "")
    categoria_final = info.get("categoria", "") if info else "Disfunción Pélvica"

    if not info:
        return DiagnosticoBiomecanico(
            titulo=titulo_final,
            subtitulo=subtitulo_final,
            clasificacion_tipo=categoria_final,
            nivel_concordancia=concordancia,
            justificacion_clinica=justificaciones,
            vector_ajuste="",
            tecnica_met="",
            inhibicion_miofascial=[],
            contraindicacion_hvla=contraindicacion,
            clave_conocimiento=clave,
            ejercicio_terapeutico=ejercicios_custom or obtener_ejercicios_activos(clave, subtitulo_final)
        )
    ajuste = info.get("ajuste_articular", {})
    met = info.get("tecnica_met", {})
    mio = info.get("abordaje_miofascial", {})

    txt_ajuste = (
        "CONTRAINDICADO por Banderas Rojas" if contraindicacion else
        f"{ajuste.get('tecnica', '')} | Vector: {ajuste.get('linea_correccion', '')} (PCC: {ajuste.get('pcc', '')} en PCP: {ajuste.get('pcp', '')}) | Advertencia: {ajuste.get('advertencia', '')}"
    )
    txt_met = f"{met.get('nombre', '')} ({met.get('musculo_motor', '')}): {met.get('accion', '')} | Fase post: {met.get('fase_post', '')}"
    lista_mio = list(mio.get("inhibir", []))
    if mio.get("precaucion_reactiva"):
        lista_mio.append(f"Precaución: {mio['precaucion_reactiva']}")

    ejercicios_final = ejercicios_custom or obtener_ejercicios_activos(clave, subtitulo_final)

    return DiagnosticoBiomecanico(
        titulo=titulo_final,
        subtitulo=subtitulo_final,
        clasificacion_tipo=categoria_final,
        nivel_concordancia=concordancia,
        justificacion_clinica=justificaciones,
        vector_ajuste=txt_ajuste,
        tecnica_met=txt_met,
        inhibicion_miofascial=lista_mio,
        contraindicacion_hvla=contraindicacion,
        clave_conocimiento=clave,
        ejercicio_terapeutico=ejercicios_final
    )


def inferir_diagnostico(
    palpacion: ExamenPalpatorio,
    banderas_rojas: BanderasRojas,
    cluster: ClusterLaslett
) -> DiagnosticoBiomecanico:
    """
    Función de inferencia biomecánica pélvica basada en signos cardinales prioritarios,
    puntuación de concordancia y normalización de inputs tolerante a variaciones.
    Desambigua rigurosamente la nomenclatura rotacional Gonstead de los cizallamientos verticales osteopáticos (Downslip/Upslip)
    y prescribe las cuatro fases terapéuticas (Ajuste, MET, Miofascial y Ejercicio Activo).
    """
    lado = palpacion.lado_restriccion.value if hasattr(palpacion.lado_restriccion, "value") else str(palpacion.lado_restriccion)
    contraindicacion = banderas_rojas.hay_bandera_roja

    # 1. Normalización completamente tolerante
    cresta_alta = _es_alto(palpacion.cresta_iliaca)
    cresta_baja = _es_bajo(palpacion.cresta_iliaca)

    isquion_alto = _es_alto(palpacion.tuberosidad_isquiatica)
    isquion_bajo = _es_bajo(palpacion.tuberosidad_isquiatica)

    eias_alta = _es_alto(palpacion.eias)
    eias_baja = _es_bajo(palpacion.eias)

    eips_alta = _es_alto(palpacion.eips)
    eips_baja = _es_bajo(palpacion.eips)

    mal_txt = _txt(palpacion.maleolo_supino)
    maleolo_corto = "cort" in mal_txt
    maleolo_largo = "larg" in mal_txt

    sit_txt = _txt(palpacion.long_sitting)
    sitting_alarga = "alarga" in sit_txt
    sitting_acorta = "acorta" in sit_txt
    sitting_fijo = "mantiene" in sit_txt or "fijo" in sit_txt or "constante" in sit_txt

    pub_txt = _txt(palpacion.escalon_pubis)
    pubis_alto = "superior" in pub_txt or "alto" in pub_txt or "ascendid" in pub_txt
    pubis_bajo = "inferior" in pub_txt or "bajo" in pub_txt or "descendid" in pub_txt

    sacrotub_val = palpacion.ligamento_sacrotuberoso_tenso
    if isinstance(sacrotub_val, bool):
        sacrotuberoso_tenso = sacrotub_val
    else:
        st_txt = _txt(sacrotub_val)
        sacrotuberoso_tenso = "tens" in st_txt or "hiper" in st_txt or "aumentad" in st_txt or "positiv" in st_txt or st_txt == "true"

    pir_txt = _txt(palpacion.piramidal)
    piramidal_tenso = "hiper" in pir_txt or "tens" in pir_txt
    piramidal_normotonico = "normo" in pir_txt or "euton" in pir_txt or "normal" in pir_txt or not piramidal_tenso

    # Normalización Sacra Específica
    surco_txt = _txt(palpacion.surco_sacro)
    sulcus_profundo = "profund" in surco_txt
    sulcus_superficial = "superfic" in surco_txt or "plan" in surco_txt
    sulcus_neutro = "neutr" in surco_txt or "simetric" in surco_txt

    ail_txt = _txt(palpacion.ail)
    ila_superficial = "superfic" in ail_txt or "posterior" in ail_txt
    ila_profundo = "profund" in ail_txt or "anterior" in ail_txt
    ila_bajo = "bajo" in ail_txt or "descendid" in ail_txt or "caudal" in ail_txt
    ila_craneal = "craneal" in ail_txt or "ascendid" in ail_txt or "cefálic" in ail_txt or "cefalic" in ail_txt or "alto" in ail_txt
    ila_neutro = "neutr" in ail_txt or "simetric" in ail_txt

    maleolo_simetrico = "simetr" in mal_txt or (not maleolo_corto and not maleolo_largo)

    # Transverso (Inflare / Outflare)
    dt_txt = _txt(getattr(palpacion, "diametro_transverso", None))
    eias_medial = getattr(palpacion, "eias_medializada", False) or "eias medial" in dt_txt
    eips_lateral = getattr(palpacion, "eips_lateralizada", False) or "eips lateral" in dt_txt
    eias_lateral = getattr(palpacion, "eias_lateralizada", False) or "eias lateral" in dt_txt
    eips_medial = getattr(palpacion, "eips_medializada", False) or "eips medial" in dt_txt

    is_inflare = "inflare" in dt_txt or (eias_medial and eips_lateral)
    is_outflare = "outflare" in dt_txt or (eias_lateral and eips_medial)

    # Torsiones
    es_torsion = getattr(palpacion, "es_torsion_sacra", False)
    spring_positivo = getattr(palpacion, "spring_test_positivo", True)

    # 2. EVALUACIÓN Y PUNTUACIÓN DE CONCORDANCIA BIOMECÁNICA
    candidatos = {}

    # A. UPSLIP PURO (Cizallamiento Craneal en Bloque)
    # Cardinal: EIAS alta + EIPS alta simultáneas (ambas elevadas sin divergencia rotacional)
    score_upslip = 0
    just_upslip = []
    if eias_alta and eips_alta:
        score_upslip += 4
        just_upslip.append(f"Ascenso simultáneo en bloque de ambos hitos ilíacos: EIAS Alta y EIPS Alta en {lado}.")
        if cresta_alta:
            score_upslip += 2
            just_upslip.append("Cresta ilíaca alta ipsilateral en el plano frontal.")
        if isquion_alto:
            score_upslip += 2
            just_upslip.append("Tuberosidad isquiática ascendida en concordancia con traslación craneal.")
        if maleolo_corto:
            score_upslip += 2
            just_upslip.append("Maléolo medial funcionalmente corto constante.")
        if sitting_fijo:
            score_upslip += 1
            just_upslip.append("Long-Sitting Test: pierna corta se mantiene corta al sentarse (dismetría fija).")
        if pubis_alto:
            score_upslip += 1
            just_upslip.append("Escalón superior ipsilateral en sínfisis púbica.")
        if score_upslip >= 6:
            candidatos["ILIACO_UPSLIP"] = (score_upslip, just_upslip)

    # B. DOWNSLIP PURO (Cizallamiento Caudal en Bloque)
    # Cardinal: EIAS baja + EIPS baja simultáneas (ambas descendidas sin divergencia rotacional)
    score_downslip = 0
    just_downslip = []
    if eias_baja and eips_baja:
        score_downslip += 4
        just_downslip.append(f"Descenso simultáneo en bloque de ambos hitos ilíacos: EIAS Baja y EIPS Baja en {lado}.")
        if cresta_baja:
            score_downslip += 2
            just_downslip.append("Cresta ilíaca baja ipsilateral en el plano frontal.")
        if isquion_bajo:
            score_downslip += 2
            just_downslip.append("Tuberosidad isquiática descendida por cizallamiento caudal.")
        if maleolo_largo:
            score_downslip += 2
            just_downslip.append("Maléolo medial funcionalmente largo constante por traslación inferior acetabular.")
        if sacrotuberoso_tenso:
            score_downslip += 1
            just_downslip.append("Tensión reactiva aumentada en ligamento sacrotuberoso por distensión inferior del isquion.")
        if pubis_bajo:
            score_downslip += 1
            just_downslip.append("Escalón inferior ipsilateral en sínfisis púbica.")
        if score_downslip >= 6:
            candidatos["ILIACO_DOWNSLIP"] = (score_downslip, just_downslip)

    # C. ILÍACO ANTERIOR / COMBINADO ANTERO-SUPERIOR (Rotación Sagital Anterior)
    # Cardinal prioritario: EIAS baja + EIPS alta (opuestas)
    score_anterior = 0
    just_anterior = []
    if eias_baja and eips_alta:
        score_anterior += 5
        just_anterior.append(f"Signo cardinal rotacional anterior: EIAS Baja combinada con EIPS Alta homolateral en {lado}.")
        if maleolo_largo:
            score_anterior += 2
            just_anterior.append("Maléolo medial funcionalmente largo en decúbito supino por proyección anteroinferior acetabular.")
        if sitting_acorta or sitting_alarga:
            score_anterior += 2
            just_anterior.append("Prueba de Long-Sitting: variación dinámica concordante con basculación ilíaca.")
        if pubis_bajo:
            score_anterior += 1
            just_anterior.append("Escalón púbico inferior homolateral.")
        if cresta_alta and isquion_alto:
            score_anterior += 2
            just_anterior.append("Coexistencia de Cresta Ilíaca Alta e Isquion Alto, confirmando cizallamiento craneal vertical (Upslip) superpuesto.")
        elif not cresta_alta and not isquion_alto:
            just_anterior.append("Cresta ilíaca y tuberosidad isquiática niveladas en plano frontal, descartando cizallamiento craneal (Upslip osteopático).")
        candidatos["ILIACO_ANTERIOR"] = (score_anterior, just_anterior)

    # D. ILÍACO POSTERIOR / COMBINADO POSTERO-INFERIOR (Rotación Sagital Posterior / Gonstead PI)
    # Cardinal prioritario: EIAS alta + EIPS baja (opuestas)
    score_posterior = 0
    just_posterior = []
    if eias_alta and eips_baja:
        score_posterior += 5
        just_posterior.append(f"Signo cardinal rotacional posterior: EIAS Alta combinada con EIPS Baja homolateral en {lado}.")
        if sacrotuberoso_tenso:
            score_posterior += 2
            just_posterior.append("Tensión aumentada en el ligamento sacrotuberoso por retroversión del isquion.")
        if maleolo_corto:
            score_posterior += 2
            just_posterior.append("Maléolo medial funcionalmente corto en decúbito supino por posteriorización acetabular.")
        if sitting_alarga:
            score_posterior += 2
            just_posterior.append("Long-Sitting Test clásico: pierna corta funcional se alarga al pasar a sedente.")
        if piramidal_tenso:
            score_posterior += 1
            just_posterior.append("Músculo piramidal tenso / hipertonía reactiva homolateral.")
        if cresta_baja and isquion_bajo:
            score_posterior += 2
            just_posterior.append("Coexistencia de Cresta Ilíaca Baja e Isquion Bajo en el lado afectado, confirmando cizallamiento caudal vertical (Downslip) superpuesto.")
        elif not cresta_baja and not isquion_bajo:
            just_posterior.append("Cresta ilíaca y tuberosidad isquiática niveladas en plano frontal, descartando cizallamiento vertical caudal (Downslip osteopático).")
        candidatos["ILIACO_POSTERIOR"] = (score_posterior, just_posterior)

    # E. INFLARE / OUTFLARE (Plano Transverso)
    if is_inflare:
        candidatos["ILIACO_INFLARE"] = (6, [
            f"Diámetro transverso en Inflare: EIAS medializada y EIPS lateralizada en {lado}.",
            "Disminución de la distancia entre la EIAS y el ombligo en el plano horizontal."
        ])
    elif is_outflare:
        candidatos["ILIACO_OUTFLARE"] = (6, [
            f"Diámetro transverso en Outflare: EIAS lateralizada y EIPS medializada en {lado}.",
            "Aumento de la distancia entre la EIAS y la línea media umbilical."
        ])

    # F. TORSIONES SACRAS
    if es_torsion:
        if spring_positivo:
            candidatos["TORSION_SACRA_ANTERIOR"] = (7, [
                "Torsión sacra anterior fisiológica: surco profundo contralateral con AIL posterior.",
                "Spring Test positivo conservando elasticidad lumbosacra."
            ])
        else:
            candidatos["TORSION_SACRA_POSTERIOR"] = (7, [
                "Torsión sacra posterior no fisiológica: base sacra posteriorizada / rígida.",
                "Spring Test negativo indicando rigidez lumbosacra franca."
            ])

    # G. DISFUNCIONES SACRAS BIOMECÁNICAS ESPECÍFICAS
    # 1. Sacro Antero-Inferior (Sulcus profundo + ILA contralateral superficial + piramidal tenso)
    if sulcus_profundo and (ila_superficial or ila_craneal) and piramidal_tenso:
        score_sai = 12
        just_sai = [
            f"Relación articular sacra cardinal: Sulcus {lado.lower()} profundo con ILA contralateral superficial.",
            f"Músculo piramidal {lado.lower()} tenso (hipertonía marcada homolateral a la base profunda).",
            "Punto de contacto: ILA contralateral (ALI) | Vector: PA + LM (codo pegado al cuerpo)."
        ]
        if maleolo_largo:
            score_sai += 2
            just_sai.append(f"Pierna funcionalmente larga {lado.lower()} en concordancia con anterioridad sacra homolateral.")
        clave_sai = "SACRO_ANTERO_INFERIOR_D" if lado == "Derecho" else "SACRO_ANTERO_INFERIOR_I"
        candidatos[clave_sai] = (score_sai, just_sai)

    # 2. Sacro Postero-Superior (Base superficial + ILA contralateral profundo + maléolo alto)
    if sulcus_superficial and (ila_profundo or ila_bajo):
        score_sps = 11
        just_sps = [
            f"Relación articular sacra cardinal: Base sacra {lado.lower()} superficial (sulcus plano) con ILA contralateral profundo.",
            "Contacto: Medial a EIPS homolateral por encima del eje de flexión | Vector: PA + ML + de craneal a caudal."
        ]
        if maleolo_corto:
            score_sps += 2
            just_sps.append(f"Maléolo {lado.lower()} más alto en supino concordante con posterioridad sacra homolateral.")
        clave_sps = "SACRO_POSTERO_SUPERIOR_I" if lado == "Izquierdo" else "SACRO_POSTERO_SUPERIOR_D"
        candidatos[clave_sps] = (score_sps, just_sps)

    # 3. Sacro en Flexión Unilateral (Inclinado) (Base profunda e ILA más bajo del lado hipomóvil, sin bandas tensas)
    if sulcus_profundo and ila_bajo and piramidal_normotonico:
        score_sfu = 12
        just_sfu = [
            f"Signos cardinales de flexión sacra unilateral: Base sacra profunda e ILA más bajo en {lado}.",
            "Ausencia de bandas tensas en el piramidal (normotónico), descartando componente torsional puro.",
            "Contacto: S1-S2 / ILA en decúbito prono | Vector: Lateral a medial con torque hacia arriba / ILA de abajo hacia arriba."
        ]
        candidatos["SACRO_FLEXION_UNILATERAL"] = (score_sfu, just_sfu)

    # 4. Sacro en Extensión Unilateral (Base más posterior e ILA más craneal del lado hipomóvil, sin bandas tensas)
    if sulcus_superficial and ila_craneal and piramidal_normotonico:
        score_seu = 12
        just_seu = [
            f"Signos cardinales de extensión sacra unilateral: Base sacra más posterior e ILA más craneal en {lado}.",
            "Ausencia de bandas tensas en piramidal (normotónico).",
            "Contacto: Lateral al ILA (ALI) | Vector: Lateral a medial (LM), descendiendo el ILA."
        ]
        candidatos["SACRO_EXTENSION_UNILATERAL"] = (score_seu, just_seu)

    # 5. Sacro en Flexión Bilateral (Base profunda bilateralmente, sulcus bilateral profundo, maléolos sin cambios)
    if sulcus_profundo and (ila_superficial or ila_craneal) and maleolo_simetrico and not piramidal_tenso:
        score_sfb = 12
        just_sfb = [
            "Signos cardinales de flexión sacra bilateral: Base sacra anterior y profunda bilateralmente.",
            "Ápex postero-superior con sulcus bilateral profundo y maléolos sin cambios (simétricos).",
            "Contacto: Base sacra (técnica pull) o ápex por debajo de línea de EIPS (push) | Vector: PA + SI hacia extensión."
        ]
        candidatos["SACRO_FLEXION"] = (score_sfb, just_sfb)

    # 6. Sacro en Extensión Bilateral (Base postero-superior, sulcus superficial bilateral, maléolos sin cambios)
    if sulcus_superficial and (ila_profundo or ila_bajo) and maleolo_simetrico and not piramidal_tenso:
        score_seb = 12
        just_seb = [
            "Signos cardinales de extensión sacra bilateral: Base postero-superior con sulcus superficial bilateral.",
            "Ápex antero-inferior con maléolos sin cambios funcionales.",
            "Contacto: Base sacra sobre nivel de espinas en línea media | Vector: PA puro, sin lateralidad."
        ]
        candidatos["SACRO_EXTENSION"] = (score_seb, just_seb)

    # 3. SELECCIÓN DE LA MEJOR DISFUNCIÓN SEGÚN SCORE
    if candidatos:
        mejor_clave = max(candidatos, key=lambda k: candidatos[k][0])
        mejor_score, mejores_just = candidatos[mejor_clave]

        if mejor_score >= 5:
            if mejor_score >= 8:
                concordancia = "Alta (Concordancia biomecánica total con signos cardinales y confirmación funcional)"
            elif mejor_score >= 6:
                concordancia = "Moderada a Alta (Signos cardinales claros y pruebas de apoyo presentes)"
            else:
                concordancia = "Moderada (Presencia de signos cardinales prioritarios)"

            # Desambiguación de títulos según modelos Gonstead vs. Osteopático
            if mejor_clave == "ILIACO_POSTERIOR":
                if cresta_baja and isquion_bajo:
                    titulo_final = f"Disfunción Combinada: Rotación Posterior con Cizallamiento Inferior (Downslip) {lado}"
                    subtitulo_final = "Disfunción Multiaxial: Rotación Sagital Posterior (Gonstead PI) + Cizallamiento Caudal (Downslip Osteopático)"
                else:
                    titulo_final = f"Ilíaco Posterior {lado}"
                    subtitulo_final = "Listado Quiropráctico Gonstead: PI ilium (rotación posterior pura sin traslación vertical)"
            elif mejor_clave == "ILIACO_DOWNSLIP":
                titulo_final = f"Ilíaco Inferior / Downslip Puro {lado}"
                subtitulo_final = "Cizallamiento Vertical Caudal Puro (sin componente rotacional sagital)"
            elif mejor_clave == "ILIACO_ANTERIOR":
                if cresta_alta and isquion_alto:
                    titulo_final = f"Disfunción Combinada: Rotación Anterior con Cizallamiento Superior (Upslip) {lado}"
                    subtitulo_final = "Disfunción Multiaxial: Rotación Sagital Anterior (Gonstead AS) + Cizallamiento Craneal (Upslip Osteopático)"
                else:
                    titulo_final = f"Ilíaco Anterior {lado}"
                    subtitulo_final = "Listado Quiropráctico Gonstead: AS ilium (rotación anterior pura sin traslación vertical)"
            elif mejor_clave == "ILIACO_UPSLIP":
                titulo_final = f"Ilíaco Superior / Upslip Puro {lado}"
                subtitulo_final = "Cizallamiento Vertical Craneal Puro (sin componente rotacional sagital)"
            elif mejor_clave == "SACRO_ANTERO_INFERIOR_D":
                titulo_final = "Sacro Antero-Inferior Derecho"
                subtitulo_final = "Disfunción Sacra Unilateral Asimétrica (Sulcus derecho profundo + ILA contralateral superficial + Piramidal tenso)"
            elif mejor_clave == "SACRO_ANTERO_INFERIOR_I":
                titulo_final = "Sacro Antero-Inferior Izquierdo"
                subtitulo_final = "Disfunción Sacra Unilateral Asimétrica (Sulcus izquierdo profundo + ILA contralateral superficial + Piramidal tenso)"
            elif mejor_clave == "SACRO_POSTERO_SUPERIOR_I":
                titulo_final = "Sacro Postero-Superior Izquierdo"
                subtitulo_final = "Disfunción Sacra Unilateral Asimétrica (Base izquierda superficial + ILA contralateral profundo + Maléolo alto)"
            elif mejor_clave == "SACRO_POSTERO_SUPERIOR_D":
                titulo_final = "Sacro Postero-Superior Derecho"
                subtitulo_final = "Disfunción Sacra Unilateral Asimétrica (Base derecha superficial + ILA contralateral profundo + Maléolo alto)"
            elif mejor_clave == "SACRO_FLEXION_UNILATERAL":
                titulo_final = f"Sacro en Flexión Unilateral {lado}"
                subtitulo_final = "Disfunción Sacra Sagital Unilateral Inclinada (Base profunda e ILA más bajo, sin bandas tensas)"
            elif mejor_clave == "SACRO_EXTENSION_UNILATERAL":
                titulo_final = f"Sacro en Extensión Unilateral {lado}"
                subtitulo_final = "Disfunción Sacra Sagital Unilateral (Base más posterior e ILA más craneal, sin bandas tensas)"
            elif mejor_clave == "SACRO_FLEXION":
                titulo_final = "Sacro en Flexión Bilateral"
                subtitulo_final = "Nutación Bilateral Sacra (Base anterior y profunda bilateralmente + Sulcus bilateral profundo)"
            elif mejor_clave == "SACRO_EXTENSION":
                titulo_final = "Sacro en Extensión Bilateral"
                subtitulo_final = "Contranutación Bilateral Sacra (Base postero-superior + Sulcus superficial bilateral)"
            else:
                titulo_final = None
                subtitulo_final = None

            return _crear_diagnostico_desde_kb(
                clave=mejor_clave,
                lado=lado,
                concordancia=concordancia,
                justificaciones=mejores_just,
                contraindicacion=contraindicacion,
                titulo_custom=titulo_final,
                subtitulo_custom=subtitulo_final
            )

    # 3.5 EVALUACIÓN DETERMINISTA DE REGLAS SACRAS BIOMECÁNICAS ANTES DEL FALLBACK
    # Regla 1: Sulcus profundo + ILA contralateral superficial + piramidal tenso -> Sacro Antero-Inferior
    if sulcus_profundo and (ila_superficial or ila_craneal) and piramidal_tenso:
        clave_sai = "SACRO_ANTERO_INFERIOR_D" if lado == "Derecho" else "SACRO_ANTERO_INFERIOR_I"
        return _crear_diagnostico_desde_kb(
            clave=clave_sai,
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                f"Sulcus {lado.lower()} profundo con ILA contralateral superficial.",
                f"Hipertonía reactiva marcada del músculo piramidal {lado.lower()}.",
                "Contacto en ILA contralateral (ALI) con vector PA + LM (codo pegado al cuerpo)."
            ],
            contraindicacion=contraindicacion,
            titulo_custom=f"Sacro Antero-Inferior {lado}",
            subtitulo_custom="Disfunción Sacra Asimétrica: Sulcus profundo + ILA contralateral superficial + Piramidal tenso"
        )

    # Regla 2: Base sacra superficial + ILA profundo + Maléolo alto -> Sacro Postero-Superior
    if sulcus_superficial and (ila_profundo or ila_bajo) and maleolo_corto:
        clave_sps = "SACRO_POSTERO_SUPERIOR_I" if lado == "Izquierdo" else "SACRO_POSTERO_SUPERIOR_D"
        return _crear_diagnostico_desde_kb(
            clave=clave_sps,
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                f"Base sacra {lado.lower()} superficial (sulcus plano) con ILA contralateral profundo.",
                f"Maléolo {lado.lower()} más alto en supino concordante con posterioridad sacra.",
                "Contacto medial a EIPS con vector PA + ML + de craneal a caudal."
            ],
            contraindicacion=contraindicacion,
            titulo_custom=f"Sacro Postero-Superior {lado}",
            subtitulo_custom="Disfunción Sacra Asimétrica: Base superficial + ILA contralateral profundo + Maléolo alto"
        )

    # Regla 3: Base profunda e ILA más bajo del lado hipomóvil, sin bandas tensas -> Sacro en Flexión Unilateral
    if sulcus_profundo and ila_bajo and piramidal_normotonico:
        return _crear_diagnostico_desde_kb(
            clave="SACRO_FLEXION_UNILATERAL",
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                f"Base sacra profunda e ILA más bajo del lado hipomóvil ({lado.lower()}).",
                "Ausencia de bandas tensas en piramidal (normotónico).",
                "Contacto en S1-S2 / ILA con vector LM con torque hacia arriba / ILA abajo hacia arriba."
            ],
            contraindicacion=contraindicacion,
            titulo_custom=f"Sacro en Flexión Unilateral {lado}",
            subtitulo_custom="Disfunción Sacra Sagital Unilateral Inclinada: Base profunda e ILA más bajo, sin bandas tensas"
        )

    # Regla 4: Base más posterior e ILA más craneal del lado hipomóvil, sin bandas tensas -> Sacro en Extensión Unilateral
    if sulcus_superficial and ila_craneal and piramidal_normotonico:
        return _crear_diagnostico_desde_kb(
            clave="SACRO_EXTENSION_UNILATERAL",
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                f"Base sacra más posterior e ILA más craneal del lado hipomóvil ({lado.lower()}).",
                "Ausencia de bandas tensas en el piramidal (normotónico).",
                "Contacto lateral al ILA (ALI) con vector lateral a medial descendiendo el ILA."
            ],
            contraindicacion=contraindicacion,
            titulo_custom=f"Sacro en Extensión Unilateral {lado}",
            subtitulo_custom="Disfunción Sacra Sagital Unilateral: Base más posterior e ILA más craneal, sin bandas tensas"
        )

    # Regla 5: Sulcus bilateral profundo + maléolos sin cambios -> Sacro en Flexión Bilateral
    if sulcus_profundo and (ila_superficial or ila_craneal) and maleolo_simetrico:
        return _crear_diagnostico_desde_kb(
            clave="SACRO_FLEXION",
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                "Base anterior y profunda bilateralmente con sulcus bilateral profundo.",
                "Ápex postero-superior con maléolos simétricos sin dismetría.",
                "Contacto en base sacra (pull) o ápex por debajo de EIPS (push) con vector PA + SI hacia extensión."
            ],
            contraindicacion=contraindicacion,
            titulo_custom="Sacro en Flexión Bilateral",
            subtitulo_custom="Nutación Bilateral Sacra: Base anterior y profunda bilateralmente + Sulcus bilateral profundo"
        )

    # Regla 6: Sulcus bilateral superficial + maléolos sin cambios -> Sacro en Extensión Bilateral
    if sulcus_superficial and (ila_profundo or ila_bajo) and maleolo_simetrico:
        return _crear_diagnostico_desde_kb(
            clave="SACRO_EXTENSION",
            lado=lado,
            concordancia="Alta (Regla biomecánica articular sacra exacta)",
            justificaciones=[
                "Base postero-superior con sulcus superficial bilateral.",
                "Ápex antero-inferior con maléolos simétricos.",
                "Contacto en base sacra sobre nivel de espinas en línea media con vector PA puro sin lateralidad."
            ],
            contraindicacion=contraindicacion,
            titulo_custom="Sacro en Extensión Bilateral",
            subtitulo_custom="Contranutación Bilateral Sacra: Base postero-superior + Sulcus superficial bilateral"
        )

    # 4. FALLBACK VERDADERO: PATRÓN MIXTO / NO CONCLUYENTE (SIN FORZAR ILÍACO POSTERIOR)
    return DiagnosticoBiomecanico(
        titulo=f"Patrón Mixto / No Concluyente ({lado})",
        subtitulo="Signos palpatorios cruzados o fijaciones adaptativas lumbopélvicas múltiples",
        clasificacion_tipo="Patrón Mixto / No Concluyente",
        nivel_concordancia="Baja / Indeterminada",
        justificacion_clinica=[
            "Los hallazgos palpatorios no alcanzan el umbral de concordancia para una disfunción rotacional o de cizallamiento unívoca.",
            "Posible coexistencia de fijaciones fasciales múltiples o asimetría adaptativa secundaria.",
            "Se sugiere realizar descarga miofascial diagnóstica de pelvitrocantéreos y reevaluar la movilidad dinámica articular."
        ],
        vector_ajuste="No se recomienda manipulación forzada HVLA inmediata sin barrera motriz clara. Priorizar movilización suave grado I-II.",
        tecnica_met="Sin protocolo MET específico asignado. Reevaluar tras normalización de tejidos blandos.",
        inhibicion_miofascial=[
            "Descarga neuromuscular completa de Piramidal, Cuadrado Lumbar y Psoas-Ilíaco bilateral",
            "Liberación miofascial del diafragma pélvico y ligamentos sacrotuberosos"
        ],
        contraindicacion_hvla=contraindicacion,
        clave_conocimiento="",
        ejercicio_terapeutico=obtener_ejercicios_activos("", "Patrón Mixto")
    )


# ==============================================================================
# COMPONENTES DE VISUALIZACIÓN DINÁMICA Y CINEMÁTICA PELVIANA (MÓDULOS A Y B)
# ==============================================================================

def _obtener_glb_pelvis_base64() -> str:
    """Retorna el modelo pelvis_anatomica.glb o pelvis.glb codificado en base64 para incrustación directa sin CORS."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    rutas_candidatas = [
        os.path.join(base_dir, "models", "pelvis_anatomica.glb"),
        os.path.join(base_dir, "assets", "pelvis.glb"),
        os.path.join("models", "pelvis_anatomica.glb"),
        os.path.join("assets", "pelvis.glb"),
    ]
    for ruta in rutas_candidatas:
        if os.path.exists(ruta) and os.path.getsize(ruta) > 1000:
            try:
                with open(ruta, "rb") as f:
                    return base64.b64encode(f.read()).decode("utf-8")
            except Exception:
                continue
    return ""


PRESET_TO_CK_KEY = {
    "pi": "ILIACO_POSTERIOR",
    "as": "ILIACO_ANTERIOR",
    "up": "ILIACO_UPSLIP",
    "down": "ILIACO_DOWNSLIP",
    "outflare": "ILIACO_OUTFLARE",
    "inflare": "ILIACO_INFLARE",
    "torsion_ant": "TORSION_SACRA_ANTERIOR",
    "torsion_post": "TORSION_SACRA_POSTERIOR",
    "sacro_flexion": "SACRO_FLEXION",
    "sacro_extension": "SACRO_EXTENSION",
    "sacro_ai_d": "SACRO_ANTERO_INFERIOR_D",
    "sacro_ps_i": "SACRO_POSTERO_SUPERIOR_I",
    "sacro_flex_uni": "SACRO_FLEXION_UNILATERAL",
    "sacro_ext_uni": "SACRO_EXTENSION_UNILATERAL",
    "pubis_up": "ILIACO_UPSLIP",
    "pubis_down": "ILIACO_DOWNSLIP",
}

ATLAS_PRESET_METADATA = {
    "pi": {
        "listing": "Gonstead: PI | Mitchell: Rotación Posterior | Osteopatía: Retroversión coxal",
        "mecanismo": "Caída sentada sobre isquion, frenada brusca con rodilla en extensión, o flexión lumbar forzada con piernas estiradas.",
        "cinematica_resumen": "Retroversión pura del coxal sobre la carilla auricular sacra S3. La EIAS se desplaza hacia póstero-superior, la EIPS desciende hacia póstero-inferior aproximándose al sacro, y la rama púbica asciende y se retrae hacia posterior.",
    },
    "as": {
        "listing": "Gonstead: AS | Mitchell: Rotación Anterior | Osteopatía: Anteversión coxal",
        "mecanismo": "Pisar en falso (escalón o bache), patada en vacío, extensión forzada de cadera en carrera o sobrecarga en fútbol/golf.",
        "cinematica_resumen": "Anteversión pura del coxal sobre eje S3. La EIAS desciende y se proyecta hacia antero-inferior, la EIPS asciende y se lateraliza, y la sínfisis púbica desciende quedando prominente hacia anterior.",
    },
    "up": {
        "listing": "Mitchell: Cizallamiento Craneal / Upslip | Gonstead: Subluxación Vertical Superior",
        "mecanismo": "Impacto axial con rodilla en extensión rígida (caída de altura sobre talón, frenazo automovilístico con pie en freno, choque frontal).",
        "cinematica_resumen": "Traslación cefálica en bloque de la hemipelvis completa sobre la superficie articular sacroilíaca. Cresta, EIAS, EIPS, isquion y pubis ascienden en igual magnitud. Pierna corta constante.",
    },
    "down": {
        "listing": "Mitchell: Cizallamiento Caudal / Downslip | Gonstead: Subluxación Vertical Inferior",
        "mecanismo": "Tracción brusca caudal del miembro inferior (pie atascado mientras el cuerpo avanza) o caída violenta con pierna colgando.",
        "cinematica_resumen": "Traslación caudal en bloque de la hemipelvis completa. Cresta, EIAS, EIPS, isquion y pubis descienden en igual magnitud. Pierna larga constante.",
    },
    "outflare": {
        "listing": "Mitchell: Outflare | Gonstead: EX (External) | Osteopatía: Apertura Ilíaca Externa",
        "mecanismo": "Aducción forzada con rotación externa femoral, sobrecarga de abductores en ciclistas/patinadores o hipertonía de TFL/glúteo medio.",
        "cinematica_resumen": "Rotación externa del ilíaco en el plano transverso sobre un eje vertical sacroilíaco. La EIAS se lateraliza (mayor distancia a la sínfisis/ombligo) y la EIPS se medializa comprimiendo el surco sacro.",
    },
    "inflare": {
        "listing": "Mitchell: Inflare | Gonstead: IN (Internal) | Osteopatía: Cierre Ilíaco Interno",
        "mecanismo": "Caída con cadera en abducción y rotación externa extrema, sobrecarga repetitiva en flexión/aducción.",
        "cinematica_resumen": "Rotación interna del ilíaco en el plano transverso. La EIAS se medializa (menor distancia a la sínfisis/ombligo) y la EIPS se lateraliza alejándose del surco sacro.",
    },
    "torsion_ant": {
        "listing": "Mitchell: Torsión Anterior (Derecha/Derecha o Izquierda/Izquierda) - Fisiológica",
        "mecanismo": "Sobrecarga en flexión con rotación lumbar sincronizada durante la marcha o levantamiento asimétrico en bipedestación.",
        "cinematica_resumen": "Nutación sacra unilateral sobre el eje oblicuo dinámico. La base sacra opuesta al eje se anterioriza profundamente en el surco, mientras el AIL contralateral se posterioriza e inferioriza. Elasticidad normal conservada.",
    },
    "torsion_post": {
        "listing": "Mitchell: Torsión Posterior (Derecha/Izquierda o Izquierda/Derecha) - No Fisiológica",
        "mecanismo": "Flexión brusca de tronco con carga excéntrica inesperada o traumatismo en caída que atrapa el sacro en contra-nutación fija.",
        "cinematica_resumen": "Contra-nutación sacra posterior sobre el eje oblicuo. La base sacra se posterioriza prominentemente hacia atrás, quedando plana, rígida y dolorosa. Spring test francamente positivo (bloqueo rígido en tabla).",
    },
    "sacro_flexion": {
        "listing": "Mitchell / Osteopatía: Sacro en Flexión Bilateral (Nutación Bilateral)",
        "mecanismo": "Sobrecarga en flexión lumbar prolongada, esfuerzo de carga en inclinación anterior forzada o traumatismo posterior.",
        "cinematica_resumen": "Nutación bilateral del sacro sobre eje transverso S2. Ambas bases sacras se hunden profundamente en el surco, el ápex se desplaza hacia póstero-superior y los AIL se anteriorizan.",
    },
    "sacro_extension": {
        "listing": "Mitchell / Osteopatía: Sacro en Extensión Bilateral (Contranutación Bilateral)",
        "mecanismo": "Caída en sedestación directa sobre el sacro/cóccix, hiperextensión lumbar violenta o desbalance pélvico en bipedestación.",
        "cinematica_resumen": "Contranutación bilateral del sacro sobre eje transverso S2. Ambas bases sacras se posteriorizan haciéndose superficiales y prominentes, el ápex se anterioriza e inferioriza, bloqueo rígido en Spring test.",
    },
    "sacro_ai_d": {
        "listing": "Osteopatía: Sacro Antero-Inferior Derecho (Falsa pierna corta / Torsión unilateral)",
        "mecanismo": "Microtrauma repetitivo en rotación pélvica con carga asimétrica, espasmo protector del músculo piramidal derecho.",
        "cinematica_resumen": "La hemibase sacra derecha se desplaza en nutación hacia antero-inferior, el ILA izquierdo se hace prominente/superficial hacia posterior, piramidal tenso ipsilateral y falsa pierna larga derecha.",
    },
    "sacro_ps_i": {
        "listing": "Osteopatía: Sacro Postero-Superior Izquierdo",
        "mecanismo": "Impacto axial asimétrico en flexión o atrapamiento articular en contranutación unilateral izquierda.",
        "cinematica_resumen": "La hemibase sacra izquierda se fija en contranutación postero-superior quedando superficial y dolorosa en el sulcus; el ILA derecho se profundiza. Maléolo alto homolateral y Spring test rígido sobre base izquierda.",
    },
    "sacro_flex_uni": {
        "listing": "Mitchell / Greenman: Sacro en Flexión Unilateral (Inclinado)",
        "mecanismo": "Fuerza asimétrica de cizallamiento con tronco flexionado y rotado.",
        "cinematica_resumen": "Hemibase sacra homolateral en nutación profunda sin torsión contralateral compensatoria completa. ILA homolateral inferiorizado y posteriorizado.",
    },
    "sacro_ext_uni": {
        "listing": "Mitchell / Greenman: Sacro en Extensión Unilateral",
        "mecanismo": "Carga repentina con tronco en extensión o caída sobre una sola tuberosidad isquiática/hemipelvis.",
        "cinematica_resumen": "Hemibase sacra homolateral posteriorizada y rígida en contranutación fija; ILA homolateral asciende y se anterioriza. Spring test localmente positivo rígido.",
    },
    "pubis_up": {
        "listing": "Cizallamiento Púbico Superior / Pubis Ascendido",
        "mecanismo": "Sobrecarga de rectos abdominales o tracción asimétrica por traumatismo pélvico frontal.",
        "cinematica_resumen": "Escalón superior en sínfisis púbica con ascenso de la rama púbica homolateral, tensión dolorosa a la palpación.",
    },
    "pubis_down": {
        "listing": "Cizallamiento Púbico Inferior / Pubis Descendido",
        "mecanismo": "Tracción violenta de aductores (deportistas de impacto, fútbol) o caída a horcajadas.",
        "cinematica_resumen": "Escalón inferior en sínfisis púbica con descenso de la rama púbica homolateral y severo espasmo de aductores.",
    },
}


def generar_visor_3d_pelvis(
    palpacion: Optional[ExamenPalpatorio] = None,
    diagnostico: Optional[DiagnosticoBiomecanico] = None,
    preset_inicial: Optional[str] = None,
    lado_inicial: Optional[str] = None,
    mostrar_ficha_didactica: bool = False,
    es_modo_atlas: Optional[bool] = None,
    altura_canvas: Optional[int] = None
) -> str:
    """
    Genera el Visor Anatómico 3D Pélvico Interactivo en 360° con Three.js y OrbitControls.
    Permite cargar modelos .glb / .gltf con mallas separadas ('sacro', 'iliaco_izquierdo', 'iliaco_derecho'),
    rotación 360°, zoom, paneo, botones de cámara rápida y cinemática reactiva con lerp/tweening.
    Soporta presets biomecánicos del Atlas (PI, AS, Upslip, Downslip, Inflare, Outflare, Torsiones Sacras)
    y tarjeta didáctica flotante (listing, mecanismo, semiología, corrección).
    """
    if es_modo_atlas is None:
        es_modo_atlas = (diagnostico is None or (preset_inicial is not None and preset_inicial not in ["dysfunction", "neutral"]))
    if altura_canvas is None:
        altura_canvas = 850

    if palpacion is not None:
        lado = lado_inicial or palpacion.lado_restriccion.value
        eias_str = str(palpacion.eias.value).lower()
        eips_str = str(palpacion.eips.value).lower()
        cresta_str = str(palpacion.cresta_iliaca.value).lower()
        isquion_str = str(palpacion.tuberosidad_isquiatica.value).lower()
    else:
        lado = lado_inicial or "Derecho"
        eias_str = ""
        eips_str = ""
        cresta_str = ""
        isquion_str = ""

    is_right = (lado == "Derecho")

    # Rotación sagital en radianes (eje X en Three.js)
    target_rot_rad = 0.0
    target_trans_y = 0.0

    if diagnostico is not None:
        titulo_diag = diagnostico.titulo.replace('"', '&quot;')
        subtitulo_diag = diagnostico.subtitulo.replace('"', '&quot;')
        if ("alt" in eias_str and "baj" in eips_str) or "posterior" in diagnostico.titulo.lower():
            target_rot_rad = -0.07
        elif ("baj" in eias_str and "alt" in eips_str) or "anterior" in diagnostico.titulo.lower():
            target_rot_rad = 0.07

        if ("baj" in cresta_str and "baj" in isquion_str) or "downslip" in diagnostico.titulo.lower() or "inferior" in diagnostico.titulo.lower():
            target_trans_y = -0.07
        elif ("alt" in cresta_str and "alt" in isquion_str) or "upslip" in diagnostico.titulo.lower() or "superior" in diagnostico.titulo.lower():
            target_trans_y = 0.07
    else:
        titulo_diag = "Atlas Biomecánico y Galería 3D"
        subtitulo_diag = "Simulador Articular Interactivo"
        if preset_inicial == "pi":
            target_rot_rad = -0.07
        elif preset_inicial == "as":
            target_rot_rad = 0.07
        elif preset_inicial == "up":
            target_trans_y = 0.07
        elif preset_inicial == "down":
            target_trans_y = -0.07

    preset_init = preset_inicial or ("dysfunction" if diagnostico is not None else "pi")
    glb_b64 = _obtener_glb_pelvis_base64()

    if es_modo_atlas:
        bar_title_html = "<span>🦴 ATLAS Y VISOR 3D BIOMECÁNICO</span>"
        status_badge_html = '<span id="status-badge" class="badge-status badge-dysfunction">🔴 SIMULACIÓN 3D</span>'
        selectors_html = ""
        subtoolbar_html = ""
        btn_paciente_html = ""
        if mostrar_ficha_didactica:
            btn_ficha_html = '<button id="btn-toggle-didactic" class="v3d-btn active" onclick="toggleDidacticCardVisibility()">📖 Ficha</button>'
            didactic_card_html = """
                <!-- Tarjeta Didáctica Flotante de Biomecánica y Prescripción -->
                <div id="didacticCard" class="didactic-card-overlay">
                    <div class="didactic-card-header" onclick="toggleDidacticCard()">
                        <div class="didactic-card-title">
                            <span>📚 FICHA DIDÁCTICA</span>
                            <span id="didacticPresetBadge" class="didactic-badge">ILÍACO POSTERIOR (PI)</span>
                        </div>
                        <div class="didactic-card-actions">
                            <button id="didacticToggleBtn" class="didactic-toggle-btn" title="Minimizar / Expandir">—</button>
                        </div>
                    </div>
                    <div id="didacticCardBody" class="didactic-card-body">
                        <div class="didactic-section">
                            <span class="didactic-sec-title">🏷️ DENOMINACIÓN & LISTING:</span>
                            <p id="didacticListing" class="didactic-sec-content"></p>
                        </div>
                        <div class="didactic-section">
                            <span class="didactic-sec-title">💥 MECANISMO LESIONAL:</span>
                            <p id="didacticMechanism" class="didactic-sec-content"></p>
                        </div>
                        <div class="didactic-section">
                            <span class="didactic-sec-title">🔍 HALLAZGOS PALPATORIOS & TESTS:</span>
                            <p id="didacticPalpation" class="didactic-sec-content"></p>
                        </div>
                        <div class="didactic-section">
                            <span class="didactic-sec-title">🎯 VECTOR DE CORRECCIÓN (LOD / MET):</span>
                            <p id="didacticCorrection" class="didactic-sec-content"></p>
                        </div>
                    </div>
                </div>"""
        else:
            btn_ficha_html = ""
            didactic_card_html = ""
    else:
        bar_title_html = "<span>🦴 VISOR 3D ANATÓMICO (PRE-AJUSTE)</span>"
        status_badge_html = '<span id="status-badge" class="badge-status badge-dysfunction">🔴 CASO PACIENTE</span>'
        selectors_html = ""
        btn_ficha_html = ""
        subtoolbar_html = ""
        didactic_card_html = ""
        active_cls = "active" if preset_init == "dysfunction" else ""
        btn_paciente_html = f'<button id="btn-dysfunction" class="v3d-btn {active_cls}" onclick="applyAtlasPreset(\'dysfunction\')">⚡ Paciente</button>'

    html = f"""
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
            html, body {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100%;
                overflow: hidden;
                background-color: #0b1329 !important;
                color: #e2e8f0;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            }}
            .viewer-container {{
                background-color: #0b1329 !important;
                border: 1px solid #1e293b;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
                width: 100%;
                height: 100%;
                max-width: 100%;
                display: flex;
                flex-direction: column;
                position: relative;
                overflow: hidden;
            }}
            .top-toolbar {{
                width: 100%;
                padding: 9px 14px;
                background: #111e38;
                border-bottom: 1px solid #1e293b;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: center;
                gap: 6px;
                border-radius: 12px 12px 0 0;
                z-index: 10;
            }}
            .title-badge-group {{
                display: flex;
                align-items: center;
                gap: 8px;
            }}
            .title-text {{
                font-size: 12px;
                font-weight: 700;
                color: #38bdf8;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .badge-status {{
                padding: 3px 9px;
                border-radius: 9999px;
                font-size: 10px;
                font-weight: 600;
                letter-spacing: 0.03em;
            }}
            .badge-dysfunction {{
                background: #fef2f2;
                color: #ef4444;
                border: 1px solid #fca5a5;
            }}
            .badge-neutral {{
                background: #ecfdf5;
                color: #10b981;
                border: 1px solid #6ee7b7;
            }}
            .btn-group {{
                display: flex;
                flex-wrap: wrap;
                gap: 4px;
                align-items: center;
            }}
            button.v3d-btn {{
                background: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                padding: 5px 9px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 4px;
            }}
            button.v3d-btn:hover {{
                background: #334155;
                border-color: #64748b;
            }}
            button.v3d-btn.active {{
                background: #0284c7;
                border-color: #38bdf8;
                box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
            }}
            button.v3d-btn-cam {{
                background: #111e38;
                color: #94a3b8;
                border: 1px solid #1e293b;
                padding: 4px 8px;
                font-size: 10.5px;
            }}
            button.v3d-btn-cam:hover {{
                background: #1e293b;
                color: #f8fafc;
            }}
            /* Sub-barra de Presets Categorizados del Atlas */
            .preset-subtoolbar {{
                width: 100%;
                padding: 5px 10px;
                background: #0d172e;
                border-bottom: 1px solid #1e293b;
                display: flex;
                flex-wrap: wrap;
                align-items: center;
                gap: 6px;
                font-size: 10.5px;
                z-index: 9;
            }}
            .preset-category-group {{
                display: inline-flex;
                align-items: center;
                gap: 3px;
                padding: 2px 5px;
                background: rgba(15, 23, 42, 0.7);
                border: 1px solid #1e293b;
                border-radius: 6px;
            }}
            .preset-cat-label {{
                font-size: 9px;
                font-weight: 700;
                color: #94a3b8;
                margin-right: 2px;
                text-transform: uppercase;
                letter-spacing: 0.02em;
            }}
            .v3d-btn-preset {{
                background: #1e293b;
                color: #cbd5e1;
                border: 1px solid #334155;
                padding: 3px 7px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.15s ease;
                display: inline-flex;
                align-items: center;
                gap: 3px;
            }}
            .v3d-btn-preset:hover {{
                background: #334155;
                color: #ffffff;
                border-color: #64748b;
            }}
            .v3d-btn-preset.active {{
                background: #0284c7;
                color: #ffffff;
                border-color: #38bdf8;
                box-shadow: 0 0 8px rgba(56, 189, 248, 0.4);
            }}
            /* Controles superiores del Atlas (Categoría, Disfunción y Lado) */
            .toolbar-selectors-group {{
                display: inline-flex;
                align-items: center;
                gap: 5px;
                flex-wrap: wrap;
            }}
            .toolbar-control-group {{
                display: inline-flex;
                align-items: center;
                gap: 4px;
                background: #0b1329;
                padding: 2px 6px;
                border-radius: 6px;
                border: 1px solid #334155;
            }}
            .toolbar-control-label {{
                font-size: 9px;
                font-weight: 700;
                color: #94a3b8;
                text-transform: uppercase;
                letter-spacing: 0.02em;
                white-space: nowrap;
            }}
            .v3d-select {{
                background: #1e293b;
                color: #f8fafc;
                border: 1px solid #334155;
                padding: 2px 5px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 600;
                cursor: pointer;
                outline: none;
                transition: all 0.15s ease;
                max-width: 175px;
            }}
            .v3d-select:hover {{
                border-color: #38bdf8;
                background: #273549;
            }}
            .v3d-select:focus {{
                border-color: #38bdf8;
                box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.25);
            }}
            /* Selector de Lado (Hemipelvis) */
            .side-selector-group {{
                display: inline-flex;
                align-items: center;
                gap: 2px;
                background: #0b1329;
                padding: 2px 4px;
                border-radius: 6px;
                border: 1px solid #334155;
            }}
            .side-btn {{
                background: #1e293b;
                color: #94a3b8;
                border: none;
                padding: 3px 7px;
                border-radius: 4px;
                font-size: 10px;
                font-weight: 700;
                cursor: pointer;
                transition: all 0.15s ease;
            }}
            .side-btn:hover {{
                color: #f8fafc;
            }}
            .side-btn.active {{
                background: #0284c7;
                color: #ffffff;
                box-shadow: 0 0 6px rgba(56, 189, 248, 0.4);
            }}
            /* Tarjeta Didáctica Flotante (Glassmorphism HUD Lateral) */
            .didactic-card-overlay {{
                position: absolute;
                top: 12px;
                right: 14px;
                width: 340px;
                max-width: calc(100% - 28px);
                max-height: calc(100% - 24px);
                background: rgba(11, 19, 41, 0.92);
                backdrop-filter: blur(12px);
                -webkit-backdrop-filter: blur(12px);
                border: 1px solid rgba(56, 189, 248, 0.4);
                border-radius: 10px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.7);
                display: flex;
                flex-direction: column;
                z-index: 15;
                font-size: 11px;
                color: #e2e8f0;
                transition: all 0.3s ease;
                overflow: hidden;
            }}
            .didactic-card-overlay.minimized {{
                max-height: 38px;
            }}
            .didactic-card-header {{
                padding: 7px 10px;
                background: rgba(17, 30, 56, 0.95);
                border-bottom: 1px solid rgba(56, 189, 248, 0.25);
                display: flex;
                justify-content: space-between;
                align-items: center;
                cursor: pointer;
                user-select: none;
            }}
            .didactic-card-title {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-weight: 700;
                font-size: 10.5px;
                color: #38bdf8;
                letter-spacing: 0.03em;
            }}
            .didactic-badge {{
                background: #0284c7;
                color: #ffffff;
                padding: 1px 6px;
                border-radius: 4px;
                font-size: 9.5px;
                font-weight: 700;
            }}
            .didactic-toggle-btn {{
                background: transparent;
                border: none;
                color: #94a3b8;
                font-weight: 700;
                cursor: pointer;
                font-size: 13px;
                line-height: 1;
                padding: 2px 5px;
                border-radius: 4px;
            }}
            .didactic-toggle-btn:hover {{
                color: #f8fafc;
                background: rgba(255, 255, 255, 0.1);
            }}
            .didactic-card-body {{
                padding: 8px 10px;
                overflow-y: auto;
                display: flex;
                flex-direction: column;
                gap: 7px;
                max-height: calc(100% - 44px);
            }}
            .didactic-card-body::-webkit-scrollbar {{
                width: 4px;
            }}
            .didactic-card-body::-webkit-scrollbar-thumb {{
                background: #334155;
                border-radius: 4px;
            }}
            .didactic-section {{
                background: rgba(15, 23, 42, 0.6);
                border: 1px solid rgba(51, 65, 85, 0.6);
                border-radius: 6px;
                padding: 6px 8px;
            }}
            .didactic-sec-title {{
                font-size: 9.5px;
                font-weight: 700;
                color: #38bdf8;
                display: block;
                margin-bottom: 3px;
                text-transform: uppercase;
                letter-spacing: 0.03em;
            }}
            .didactic-sec-content {{
                font-size: 10.5px;
                line-height: 1.35;
                color: #cbd5e1;
                margin: 0;
                white-space: pre-line;
            }}
            #canvas-container {{
                width: 100%;
                height: 850px; /* Que coincida con la altura de components.html */
                position: relative;
                background-color: #0b1329 !important;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: grab;
                overflow: hidden;
            }}
            #canvas-container:active {{
                cursor: grabbing;
            }}
            .canvas-area {{
                position: relative;
                width: 100%;
                height: 850px;
                background-color: #0b1329 !important;
                display: flex;
                justify-content: center;
                align-items: center;
                cursor: grab;
                overflow: hidden;
            }}
            .canvas-area:active {{
                cursor: grabbing;
            }}
            #webglCanvas {{
                position: relative;
                width: 100%;
                height: 850px;
                display: block;
                background-color: #0b1329 !important;
                overflow: hidden;
            }}
            /* Overlay de controles flotantes de cámara */
            .cam-preset-overlay {{
                position: absolute;
                top: 10px;
                left: 12px;
                background: rgba(11, 19, 41, 0.88);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(56, 189, 248, 0.3);
                border-radius: 8px;
                padding: 6px 10px;
                display: flex;
                flex-direction: column;
                gap: 5px;
                z-index: 5;
                box-shadow: 0 4px 12px rgba(0,0,0,0.5);
            }}
            .cam-title {{
                font-size: 9.5px;
                font-weight: 700;
                color: #38bdf8;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            .cam-buttons-row {{
                display: flex;
                gap: 4px;
            }}
            /* Badge flotante de desnivel e inclinación angular */
            .tilt-badge-overlay {{
                position: absolute;
                top: 76px;
                left: 12px;
                background: rgba(11, 19, 41, 0.92);
                backdrop-filter: blur(10px);
                border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 8px;
                padding: 6px 12px;
                display: flex;
                flex-direction: column;
                gap: 3px;
                z-index: 6;
                box-shadow: 0 4px 14px rgba(0, 0, 0, 0.5);
                transition: all 0.3s ease;
                min-width: 180px;
            }}
            .tilt-badge-overlay.tilt-alert {{
                border-color: rgba(244, 63, 94, 0.65);
                box-shadow: 0 0 14px rgba(244, 63, 94, 0.3);
            }}
            .tilt-badge-overlay.tilt-neutral {{
                border-color: rgba(16, 185, 129, 0.4);
            }}
            .tilt-badge-header {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 9.5px;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-transform: uppercase;
                color: #f8fafc;
            }}
            .tilt-dot {{
                width: 7px;
                height: 7px;
                border-radius: 50%;
                display: inline-block;
            }}
            .dot-alert {{
                background: #f43f5e;
                box-shadow: 0 0 6px #f43f5e;
            }}
            .dot-neutral {{
                background: #10b981;
                box-shadow: 0 0 6px #10b981;
            }}
            .tilt-metrics {{
                display: flex;
                align-items: center;
                gap: 6px;
                font-size: 11px;
                font-weight: 600;
                color: #38bdf8;
            }}
            .tilt-alert .tilt-metrics {{
                color: #fda4af;
            }}
            .tilt-sep {{
                color: #475569;
            }}
            /* HUD Panel Inferior */
            .hud-footer {{
                width: 100%;
                padding: 7px 14px;
                background: #0b1329;
                border-top: 1px solid #1e293b;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 11px;
                color: #94a3b8;
                border-radius: 0 0 12px 12px;
                min-height: 36px;
                z-index: 10;
            }}
            .hud-info {{
                display: flex;
                align-items: center;
                gap: 8px;
                color: #e2e8f0;
            }}
            .hud-info strong {{
                color: #38bdf8;
            }}
            /* Drag & Drop Indicator */
            .drag-overlay {{
                position: absolute;
                top: 0; left: 0; right: 0; bottom: 0;
                background: rgba(2, 132, 199, 0.4);
                border: 2px dashed #38bdf8;
                border-radius: 12px;
                display: none;
                align-items: center;
                justify-content: center;
                color: #ffffff;
                font-size: 16px;
                font-weight: 700;
                z-index: 20;
                pointer-events: none;
            }}
            /* Etiquetas Anatómicas Vectoriales Nítidas (CSS2DRenderer) */
            .v3d-label {{
                display: inline-flex;
                align-items: center;
                gap: 6px;
                padding: 3px 8px;
                border-radius: 6px;
                background: rgba(11, 19, 41, 0.90);
                backdrop-filter: blur(8px);
                -webkit-backdrop-filter: blur(8px);
                border: 1.5px solid rgba(255, 255, 255, 0.25);
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.6), 0 0 6px rgba(0, 0, 0, 0.4);
                color: #f8fafc;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                font-size: 11px;
                font-weight: 600;
                line-height: 1.2;
                white-space: nowrap;
                user-select: none;
                pointer-events: none;
                transition: opacity 0.2s ease;
                letter-spacing: 0.2px;
            }}
            .v3d-label-dot {{
                width: 7px;
                height: 7px;
                border-radius: 50%;
                flex-shrink: 0;
            }}
        </style>
        <!-- Scripts Three.js, OrbitControls, GLTFLoader y CSS2DRenderer -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/renderers/CSS2DRenderer.js"></script>
    </head>
    <body>
        <div class="viewer-container" id="viewerContainer">
            <!-- Barra Superior Principal -->
            <div class="top-toolbar">
                <div class="title-badge-group">
                    <div class="title-text">
                        {bar_title_html}
                    </div>
                    {selectors_html}
                    {status_badge_html}
                </div>
                <div class="btn-group">
                    {btn_paciente_html}
                    <button id="btn-neutral" class="v3d-btn {'active' if preset_init == 'neutral' else ''}" onclick="toggleNeutral()">📐 Neutro</button>
                    <button id="btn-gait" class="v3d-btn" onclick="toggleGait()">▶ Marcha</button>
                    <button id="btn-toggle-landmarks" class="v3d-btn active" onclick="toggleLandmarks()">📍 Hitos</button>
                    <button id="btn-toggle-lines" class="v3d-btn active" onclick="toggleReferenceLines()">📏 Planos</button>
                    {btn_ficha_html}
                    <label class="v3d-btn" style="cursor:pointer; margin:0;">
                        📁 GLB
                        <input type="file" id="glbFileInput" accept=".glb,.gltf" style="display:none;" onchange="handleFileSelect(event)">
                    </label>
                </div>
            </div>

            {subtoolbar_html}

            <div class="canvas-area" id="canvas-container">
                <div id="dragOverlay" class="drag-overlay">📂 Soltar archivo .GLB / .GLTF anatómico aquí</div>
                <!-- Overlay de vistas de cámara rápida -->
                <div class="cam-preset-overlay">
                    <span class="cam-title">Vistas 360°</span>
                    <div class="cam-buttons-row">
                        <button class="v3d-btn v3d-btn-cam" onclick="setCameraView('anterior')">👁️ Anterior</button>
                        <button class="v3d-btn v3d-btn-cam" onclick="setCameraView('posterior')">👁️ Posterior</button>
                        <button class="v3d-btn v3d-btn-cam" onclick="setCameraView('sagital')">👁️ Sagital</button>
                        <button class="v3d-btn v3d-btn-cam" onclick="setCameraView('axial')">👁️ Axial</button>
                        <button class="v3d-btn v3d-btn-cam" onclick="resetCamera()">↺ Reset</button>
                    </div>
                </div>

                <!-- Badge flotante de desnivel e inclinación angular -->
                <div id="tiltBadge" class="tilt-badge-overlay tilt-neutral">
                    <div class="tilt-badge-header">
                        <span id="tiltStatusDot" class="tilt-dot dot-neutral"></span>
                        <span id="tiltTitle">ALINEACIÓN SIMÉTRICA</span>
                    </div>
                    <div class="tilt-metrics">
                        <span id="tiltAngle">Inclinación: 0.0°</span>
                        <span class="tilt-sep">|</span>
                        <span id="tiltDeltaY">Desnivel: 0.0 mm</span>
                    </div>
                </div>

                {didactic_card_html}

                <div id="webglCanvas"></div>
            </div>

            <div class="hud-footer">
                <div id="hud-info" class="hud-info">
                    <span>💡 <strong>Navegación 3D:</strong> Clic izquierdo: rotar 360° | Rueda: zoom | Clic derecho: paneo.</span>
                </div>
                <div id="model-status" style="font-size: 10.5px; color: #38bdf8;">
                    Modelo: Pelvis Anatómica CT (Sacrum, Hip_L, Hip_R)
                </div>
            </div>
        </div>

        <script>
            // Evitar múltiples render loops concurrentes y parpadeos
            if (window.__biopelvis_anim_frame) {{
                cancelAnimationFrame(window.__biopelvis_anim_frame);
                window.__biopelvis_anim_frame = null;
            }}

            // Definición de seguridad offline para CSS2DRenderer y CSS2DObject
            if (typeof THREE.CSS2DRenderer === 'undefined') {{
                (function() {{
                    class CSS2DObject extends THREE.Object3D {{
                        constructor(element) {{
                            super();
                            this.element = element || document.createElement('div');
                            this.element.style.position = 'absolute';
                            this.addEventListener('removed', function() {{
                                this.traverse(function(object) {{
                                    if (object.element instanceof Element && object.element.parentNode !== null) {{
                                        object.element.parentNode.removeChild(object.element);
                                    }}
                                }});
                            }});
                        }}
                        copy(source, recursive) {{
                            super.copy(source, recursive);
                            this.element = source.element.cloneNode(true);
                            return this;
                        }}
                    }}
                    CSS2DObject.prototype.isCSS2DObject = true;

                    const _vec = new THREE.Vector3();
                    const _vMat = new THREE.Matrix4();
                    const _vpMat = new THREE.Matrix4();
                    const _posA = new THREE.Vector3();
                    const _posB = new THREE.Vector3();

                    class CSS2DRenderer {{
                        constructor() {{
                            const _this = this;
                            let _w, _h, _wHalf, _hHalf;
                            const cache = {{ objects: new WeakMap() }};
                            const domElement = document.createElement('div');
                            domElement.style.overflow = 'hidden';
                            this.domElement = domElement;

                            this.getSize = function() {{ return {{ width: _w, height: _h }}; }};

                            this.render = function(scene, camera) {{
                                if (scene.autoUpdate === true) scene.updateMatrixWorld();
                                if (camera.parent === null) camera.updateMatrixWorld();
                                _vMat.copy(camera.matrixWorldInverse);
                                _vpMat.multiplyMatrices(camera.projectionMatrix, _vMat);
                                renderObject(scene, scene, camera);
                                zOrder(scene);
                            }};

                            this.setSize = function(width, height) {{
                                _w = width; _h = height;
                                _wHalf = _w / 2; _hHalf = _h / 2;
                                domElement.style.width = width + 'px';
                                domElement.style.height = height + 'px';
                            }};

                            function renderObject(object, scene, camera) {{
                                if (object.isCSS2DObject) {{
                                    if (typeof object.onBeforeRender === 'function') object.onBeforeRender(_this, scene, camera);
                                    _vec.setFromMatrixPosition(object.matrixWorld);
                                    _vec.applyMatrix4(_vpMat);
                                    const element = object.element;
                                    element.style.transform = 'translate(-50%,-50%) translate(' + (_vec.x * _wHalf + _wHalf) + 'px,' + (-_vec.y * _hHalf + _hHalf) + 'px)';

                                    let isVisible = object.visible;
                                    let p = object.parent;
                                    while (p && isVisible) {{
                                        if (!p.visible) isVisible = false;
                                        p = p.parent;
                                    }}
                                    element.style.display = isVisible && _vec.z >= -1 && _vec.z <= 1 ? '' : 'none';
                                    const objectData = {{ distanceToCameraSquared: getDistSq(camera, object) }};
                                    cache.objects.set(object, objectData);
                                    if (element.parentNode !== domElement) domElement.appendChild(element);
                                    if (typeof object.onAfterRender === 'function') object.onAfterRender(_this, scene, camera);
                                }}
                                for (let i = 0, l = object.children.length; i < l; i++) {{
                                    renderObject(object.children[i], scene, camera);
                                }}
                            }}

                            function getDistSq(camera, object) {{
                                _posA.setFromMatrixPosition(object.matrixWorld);
                                _posB.setFromMatrixPosition(camera.matrixWorld);
                                return _posA.distanceToSquared(_posB);
                            }}

                            function filterAndFlatten(scene) {{
                                const res = [];
                                scene.traverse(function(obj) {{ if (obj.isCSS2DObject) res.push(obj); }});
                                return res;
                            }}

                            function zOrder(scene) {{
                                const sorted = filterAndFlatten(scene).sort(function(a, b) {{
                                    return (cache.objects.get(a)?.distanceToCameraSquared || 0) - (cache.objects.get(b)?.distanceToCameraSquared || 0);
                                }});
                                const zMax = sorted.length;
                                for (let i = 0, l = sorted.length; i < l; i++) {{
                                    sorted[i].element.style.zIndex = zMax - i;
                                }}
                            }}
                        }}
                    }}
                    THREE.CSS2DObject = CSS2DObject;
                    THREE.CSS2DRenderer = CSS2DRenderer;
                }})();
            }}

            // Parámetros clínicos inyectados
            let currentPatientSide = "{lado}";
            let isRight = (currentPatientSide === "Derecho");
            const clinicalTargetRotX = {target_rot_rad};
            const clinicalTargetTransY = {target_trans_y};
            const diagTitle = "{titulo_diag}";
            let currentActivePreset = "{preset_init}";
            const baseActivePreset = "{preset_init}";
            let showDidacticCard = { 'true' if mostrar_ficha_didactica else 'true' };
            const defaultGlbBase64 = "data:model/gltf-binary;base64,{glb_b64}";
            const REMOTE_GLB_URL = "https://raw.githubusercontent.com/I-STAR/PelvisAtlas/main/models/pelvis_anatomica.glb";

            // Variables de escena Three.js
            let scene, camera, renderer, labelRenderer, controls;
            let container = document.getElementById('canvas-container') || document.getElementById('webglCanvas');
            let statusBadge = document.getElementById('status-badge');
            let hudInfo = document.getElementById('hud-info');
            let modelStatus = document.getElementById('model-status');

            // Nodos anatómicos segmentados
            let sacroMesh = null;
            let iliacoIzqMesh = null;
            let iliacoDerMesh = null;

            // Grupo raíz pélvico calibrado y nivelado
            let pelvisGroup = new THREE.Group();
            pelvisGroup.name = "pelvisGroup";

            // Calibración tomográfica basal para nivelación frontal (roll) y centrado de plomada
            const BASE_CALIBRATION_ROT_Z = -0.082058; // -4.7016° para nivelar simétricamente ambas crestas
            const BASE_CALIBRATION_POS_X = -0.010488; // Centrado bilateral de la plomada en X = 0
            const BASE_CALIBRATION_POS_Y = 0.0;

            // Pivotes de articulación sacroilíaca (carillas auriculares tomográficas S2/S3 exactas)
            let pivotIzq = new THREE.Group();
            let pivotDer = new THREE.Group();

            const SIJ_LEFT_POS = new THREE.Vector3(0.305, 0.201, -0.187);
            const SIJ_RIGHT_POS = new THREE.Vector3(-0.368, 0.171, -0.152);

            // Marcadores anatómicos (Puntos de Reparo 3D)
            let markerCrestL, markerCrestR;
            let markerEiasL, markerEiasR;
            let markerEipsL, markerEipsR;
            let markerIschL, markerIschR;
            let markerPubisL, markerPubisR;
            let showLandmarks = true;

            // Planos y líneas de nivel de referencia
            let lineCrests, refLineCrests;
            let lineEIAS, refLineEIAS;
            let refLinesGroup = new THREE.Group();
            let showReferenceLines = true;

            // Cinemática y animación
            let currentMode = "{preset_init}";
            let isGaitActive = false;
            let gaitTime = 0;

            // Variables de interpolación (lerp) con acoplamiento 3D
            let targetRotLeft = 0.0, currentRotLeft = 0.0;
            let targetRotYLeft = 0.0, currentRotYLeft = 0.0;
            let targetTransYLeft = 0.0, currentTransYLeft = 0.0;
            let targetTransZLeft = 0.0, currentTransZLeft = 0.0;

            let targetRotRight = 0.0, currentRotRight = 0.0;
            let targetRotYRight = 0.0, currentRotYRight = 0.0;
            let targetTransYRight = 0.0, currentTransYRight = 0.0;
            let targetTransZRight = 0.0, currentTransZRight = 0.0;

            // Interpolación para el nodo Sacro (Torsiones sobre eje oblicuo)
            let targetSacrumRotY = 0.0, currentSacrumRotY = 0.0;
            let targetSacrumRotZ = 0.0, currentSacrumRotZ = 0.0;
            let targetSacrumPosZ = 0.0, currentSacrumPosZ = 0.0;

            const DEFAULT_CAM_DISTANCE = 2.3;
            let neutralCrestY = 0.6212;
            let neutralEiasY = 0.0655;

            // Interpolación de cámara
            let targetCamPos = new THREE.Vector3(0, 0, DEFAULT_CAM_DISTANCE);
            let targetLookAt = new THREE.Vector3(0, 0, 0);
            let isCameraAnimating = false;

            // 1. MATERIAL ÓSEO REALISTA TIPO ATLAS MÉDICO
            const boneMaterial = new THREE.MeshStandardMaterial({{
                color: 0xd5cca8,
                roughness: 0.75,
                metalness: 0.05,
                flatShading: false,
                side: THREE.DoubleSide
            }});

            // 2. INICIALIZACIÓN DE THREE.JS Y PIPELINE DE RENDER
            function initScene() {{
                while (container.firstChild) {{
                    container.removeChild(container.firstChild);
                }}

                const width = container.clientWidth || 940;
                const height = 850;

                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x0b1329);

                camera = new THREE.PerspectiveCamera(45, (container.clientWidth || 940) / 850, 0.05, 100);
                camera.position.set(0, 0, DEFAULT_CAM_DISTANCE);

                // Renderer 3D con antialiasing, soporte retina (pixelRatio) y tone mapping cinematográfico
                renderer = new THREE.WebGLRenderer({{ antialias: true, alpha: true, powerPreference: "high-performance" }});
                renderer.setClearColor(0x0b1329, 1.0);
                renderer.setSize(container.clientWidth, 850);
                camera.aspect = container.clientWidth / 850;
                camera.updateProjectionMatrix();
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                renderer.outputEncoding = THREE.sRGBEncoding;
                renderer.toneMapping = THREE.ACESFilmicToneMapping;
                renderer.toneMappingExposure = 1.0;
                container.appendChild(renderer.domElement);

                // Renderer 2D de etiquetas anatómicas vectoriales nítidas (CSS2DRenderer)
                if (typeof THREE.CSS2DRenderer !== 'undefined') {{
                    labelRenderer = new THREE.CSS2DRenderer();
                    labelRenderer.setSize(container.clientWidth, 850);
                    labelRenderer.domElement.style.position = 'absolute';
                    labelRenderer.domElement.style.top = '0px';
                    labelRenderer.domElement.style.left = '0px';
                    labelRenderer.domElement.style.width = '100%';
                    labelRenderer.domElement.style.height = '850px';
                    labelRenderer.domElement.style.pointerEvents = 'none';
                    labelRenderer.domElement.style.overflow = 'hidden';
                    container.appendChild(labelRenderer.domElement);
                }}

                // OrbitControls con amortiguación y rango de zoom amplio sin pixelación
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.06;
                controls.screenSpacePanning = true;
                controls.minDistance = 0.3;
                controls.maxDistance = 10.0;
                controls.target.set(0, 0, 0);

                // Restauración de cámara persistente desde sessionStorage (evita cualquier reset forzado)
                let cameraRestored = false;
                try {{
                    const savedPos = sessionStorage.getItem('biopelvis_cam_pos');
                    const savedTarget = sessionStorage.getItem('biopelvis_cam_target');
                    const savedZoom = sessionStorage.getItem('biopelvis_cam_zoom');
                    if (savedPos && savedTarget) {{
                        const p = JSON.parse(savedPos);
                        const t = JSON.parse(savedTarget);
                        const dist = Math.sqrt(p.x * p.x + p.y * p.y + p.z * p.z);
                        if (dist > 2.8) {{
                            sessionStorage.removeItem('biopelvis_cam_pos');
                            sessionStorage.removeItem('biopelvis_cam_target');
                            sessionStorage.removeItem('biopelvis_cam_zoom');
                        }} else if (typeof p.x === 'number' && typeof t.x === 'number') {{
                            camera.position.set(p.x, p.y, p.z);
                            controls.target.set(t.x, t.y, t.z);
                            if (savedZoom) camera.zoom = parseFloat(savedZoom);
                            camera.updateProjectionMatrix();
                            controls.update();
                            cameraRestored = true;
                        }}
                    }}
                }} catch(e) {{}}

                if (!cameraRestored) {{
                    camera.position.set(0, 0, DEFAULT_CAM_DISTANCE);
                    controls.target.set(0, 0, 0);
                }}

                // Persistir posición orbital 360° en cada interacción del usuario
                controls.addEventListener('change', function() {{
                    if (!isCameraAnimating && camera && controls) {{
                        try {{
                            sessionStorage.setItem('biopelvis_cam_pos', JSON.stringify({{
                                x: camera.position.x,
                                y: camera.position.y,
                                z: camera.position.z
                            }}));
                            sessionStorage.setItem('biopelvis_cam_target', JSON.stringify({{
                                x: controls.target.x,
                                y: controls.target.y,
                                z: controls.target.z
                            }}));
                            sessionStorage.setItem('biopelvis_cam_zoom', String(camera.zoom));
                        }} catch(e) {{}}
                    }}
                }});

                // 3. ESQUEMA DE ILUMINACIÓN CON OCLUSIÓN Y SOMBRAS (ATLAS MÉDICO)
                // Luz ambiental tenue para conservar oclusión y relieve en cavidades internas
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.35);
                scene.add(ambientLight);

                // Luz principal clave (Key Light): superior-anterolateral para sombras en fosa ilíaca y foramen obturador
                const keyLight = new THREE.DirectionalLight(0xfff5ea, 1.4);
                keyLight.position.set(5, 10, 7);
                scene.add(keyLight);

                // Luz de relleno suave (Fill Light): ángulo opuesto inferior para contraste tenue sin zonas negras
                const fillLight = new THREE.DirectionalLight(0x90b0d0, 0.4);
                fillLight.position.set(-5, -4, -5);
                scene.add(fillLight);

                // Luz de contorno (Rim/Backlight): posterior para recortar la silueta contra el fondo oscuro
                const rimLight = new THREE.DirectionalLight(0xffffff, 0.5);
                rimLight.position.set(0, 2, -8);
                scene.add(rimLight);

                // Configurar grupo raíz pélvico calibrado y pivotes en el árbol de escena
                pelvisGroup.rotation.z = BASE_CALIBRATION_ROT_Z;
                pelvisGroup.position.set(BASE_CALIBRATION_POS_X, BASE_CALIBRATION_POS_Y, 0);
                scene.add(pelvisGroup);

                pivotIzq.position.copy(SIJ_LEFT_POS);
                pivotDer.position.copy(SIJ_RIGHT_POS);
                pelvisGroup.add(pivotIzq);
                pelvisGroup.add(pivotDer);

                // Incorporar grupo de líneas guía
                scene.add(refLinesGroup);
                setupReferenceLines();

                // Cargar modelo predeterminado
                loadDefaultModel();

                // Sincronizar selectores del Atlas al iniciar
                syncCategoryAndDysfunctionSelectors(currentActivePreset);

                // Listeners de Resize y Drag & Drop
                window.addEventListener('resize', onWindowResize);
                setTimeout(onWindowResize, 80);
                setupDragAndDrop();

                // Loop de animación seguro
                animate();
            }}

            function onWindowResize() {{
                if (!container || !renderer || !camera) return;
                const w = container.clientWidth || 940;
                camera.aspect = w / 850;
                camera.updateProjectionMatrix();
                renderer.setSize(w, 850);
                if (labelRenderer) {{
                    labelRenderer.setSize(w, 850);
                }}
            }}

            // 4. CREACIÓN DE ETIQUETAS Y MARCADORES 3D (VECTORIAL CSS2D + FALLBACK SPRITE HD)
            function createTextSprite(text, colorHex) {{
                const canvas = document.createElement('canvas');
                canvas.width = 1024;
                canvas.height = 256;
                const ctx = canvas.getContext('2d');
                ctx.imageSmoothingEnabled = true;
                ctx.imageSmoothingQuality = 'high';

                ctx.fillStyle = "rgba(11, 19, 41, 0.94)";
                ctx.strokeStyle = colorHex;
                ctx.lineWidth = 10;
                ctx.beginPath();
                ctx.roundRect(16, 16, 992, 224, 40);
                ctx.fill();
                ctx.stroke();

                ctx.fillStyle = colorHex;
                ctx.beginPath();
                ctx.arc(100, 128, 28, 0, Math.PI * 2);
                ctx.fill();

                ctx.font = "bold 72px -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif";
                ctx.fillStyle = "#ffffff";
                ctx.textAlign = "left";
                ctx.textBaseline = "middle";
                ctx.fillText(text, 160, 128);

                const texture = new THREE.CanvasTexture(canvas);
                texture.minFilter = THREE.LinearMipmapLinearFilter;
                texture.magFilter = THREE.LinearFilter;
                texture.generateMipmaps = true;
                const spriteMat = new THREE.SpriteMaterial({{
                    map: texture,
                    depthTest: false,
                    depthWrite: false
                }});
                const sprite = new THREE.Sprite(spriteMat);
                sprite.scale.set(0.38, 0.095, 1);
                sprite.renderOrder = 999;
                return sprite;
            }}

            function createLandmarkMarker(label, colorHex) {{
                const group = new THREE.Group();

                // Esfera luminosa 3D sobre la superficie ósea
                const sphereGeom = new THREE.SphereGeometry(0.028, 16, 16);
                const sphereMat = new THREE.MeshStandardMaterial({{
                    color: colorHex,
                    emissive: colorHex,
                    emissiveIntensity: 0.75,
                    roughness: 0.2,
                    metalness: 0.1
                }});
                const sphere = new THREE.Mesh(sphereGeom, sphereMat);
                group.add(sphere);

                // Anillo de referencia horizontal
                const ringGeom = new THREE.RingGeometry(0.035, 0.048, 24);
                const ringMat = new THREE.MeshBasicMaterial({{
                    color: colorHex,
                    side: THREE.DoubleSide,
                    transparent: true,
                    opacity: 0.75
                }});
                const ring = new THREE.Mesh(ringGeom, ringMat);
                ring.rotation.x = Math.PI / 2;
                group.add(ring);

                // Etiqueta flotante 3D vectorial nítida con CSS2DObject
                let label2d = null;
                let sprite = null;

                if (typeof THREE.CSS2DObject !== 'undefined') {{
                    const labelDiv = document.createElement('div');
                    labelDiv.className = 'v3d-label';
                    labelDiv.style.borderColor = colorHex;

                    const dot = document.createElement('span');
                    dot.className = 'v3d-label-dot';
                    dot.style.backgroundColor = colorHex;
                    dot.style.boxShadow = '0 0 6px ' + colorHex;
                    labelDiv.appendChild(dot);

                    const textSpan = document.createElement('span');
                    textSpan.textContent = label;
                    labelDiv.appendChild(textSpan);

                    label2d = new THREE.CSS2DObject(labelDiv);
                    label2d.position.set(0, 0.075, 0.02);
                    group.add(label2d);
                }} else {{
                    sprite = createTextSprite(label, colorHex);
                    sprite.position.set(0, 0.08, 0.03);
                    group.add(sprite);
                }}

                return {{ group, sphere, ring, label2d, sprite }};
            }}

            // Vincular los marcadores como hijos solidarios de sus respectivos huesos
            function attachLandmarksToBones() {{
                if (iliacoIzqMesh) {{
                    markerCrestL = createLandmarkMarker("Cresta Ilíaca (I)", "#f59e0b");
                    markerCrestL.group.position.set(0.480511, 0.662772, -0.047074);
                    iliacoIzqMesh.add(markerCrestL.group);

                    markerEiasL = createLandmarkMarker("EIAS (I)", "#38bdf8");
                    markerEiasL.group.position.set(0.8979, 0.1392, 0.5072);
                    iliacoIzqMesh.add(markerEiasL.group);

                    markerEipsL = createLandmarkMarker("EIPS (I)", "#a855f7");
                    markerEipsL.group.position.set(0.2659, 0.3039, -0.4277);
                    iliacoIzqMesh.add(markerEipsL.group);

                    markerIschL = createLandmarkMarker("Isquion (I)", "#10b981");
                    markerIschL.group.position.set(0.3997, -0.8825, -0.1151);
                    iliacoIzqMesh.add(markerIschL.group);

                    markerPubisL = createLandmarkMarker("Pubis (I)", "#ec4899");
                    markerPubisL.group.position.set(0.1453, -0.5425, 0.5210);
                    iliacoIzqMesh.add(markerPubisL.group);
                }}

                if (iliacoDerMesh) {{
                    markerCrestR = createLandmarkMarker("Cresta Ilíaca (D)", "#f59e0b");
                    markerCrestR.group.position.set(-0.561433, 0.577079, 0.015238);
                    iliacoDerMesh.add(markerCrestR.group);

                    markerEiasR = createLandmarkMarker("EIAS (D)", "#38bdf8");
                    markerEiasR.group.position.set(-0.8038, 0.0000, 0.6864);
                    iliacoDerMesh.add(markerEiasR.group);

                    markerEipsR = createLandmarkMarker("EIPS (D)", "#a855f7");
                    markerEipsR.group.position.set(-0.3933, 0.2722, -0.3676);
                    iliacoDerMesh.add(markerEipsR.group);

                    markerIschR = createLandmarkMarker("Isquion (D)", "#10b981");
                    markerIschR.group.position.set(-0.2403, -0.9367, -0.0094);
                    iliacoDerMesh.add(markerIschR.group);

                    markerPubisR = createLandmarkMarker("Pubis (D)", "#ec4899");
                    markerPubisR.group.position.set(-0.0605, -0.5996, 0.5557);
                    iliacoDerMesh.add(markerPubisR.group);
                }}
            }}

            // 5. LÍNEAS GUÍA HORIZONTALES Y PLANOS DE REFERENCIA
            function setupReferenceLines() {{
                while (refLinesGroup.children.length > 0) {{
                    refLinesGroup.remove(refLinesGroup.children[0]);
                }}

                // Línea dinámica entre ambas crestas
                const crestGeom = new THREE.BufferGeometry().setFromPoints([
                    new THREE.Vector3(0.52, neutralCrestY, 0),
                    new THREE.Vector3(-0.52, neutralCrestY, 0)
                ]);
                const crestMat = new THREE.LineBasicMaterial({{
                    color: 0xf59e0b,
                    linewidth: 2,
                    transparent: true,
                    opacity: 0.85
                }});
                lineCrests = new THREE.Line(crestGeom, crestMat);
                refLinesGroup.add(lineCrests);

                // Plano horizontal nivelado neutro para crestas
                const refCrestGeom = new THREE.BufferGeometry().setFromPoints([
                    new THREE.Vector3(-1.15, neutralCrestY, 0),
                    new THREE.Vector3(1.15, neutralCrestY, 0)
                ]);
                const refCrestMat = new THREE.LineDashedMaterial({{
                    color: 0x94a3b8,
                    dashSize: 0.05,
                    gapSize: 0.03,
                    transparent: true,
                    opacity: 0.55
                }});
                refLineCrests = new THREE.Line(refCrestGeom, refCrestMat);
                refLineCrests.computeLineDistances();
                refLinesGroup.add(refLineCrests);

                // Línea dinámica entre ambas EIAS
                const eiasGeom = new THREE.BufferGeometry().setFromPoints([
                    new THREE.Vector3(0.90, neutralEiasY, 0.5),
                    new THREE.Vector3(-0.90, neutralEiasY, 0.5)
                ]);
                const eiasMat = new THREE.LineBasicMaterial({{
                    color: 0x38bdf8,
                    linewidth: 2,
                    transparent: true,
                    opacity: 0.85
                }});
                lineEIAS = new THREE.Line(eiasGeom, eiasMat);
                refLinesGroup.add(lineEIAS);

                // Plano horizontal nivelado neutro para EIAS
                const refEiasGeom = new THREE.BufferGeometry().setFromPoints([
                    new THREE.Vector3(-1.15, neutralEiasY, 0.5),
                    new THREE.Vector3(1.15, neutralEiasY, 0.5)
                ]);
                const refEiasMat = new THREE.LineDashedMaterial({{
                    color: 0x94a3b8,
                    dashSize: 0.05,
                    gapSize: 0.03,
                    transparent: true,
                    opacity: 0.55
                }});
                refLineEIAS = new THREE.Line(refEiasGeom, refEiasMat);
                refLineEIAS.computeLineDistances();
                refLinesGroup.add(refLineEIAS);

                // Plomada central vertical perpendicular en X = 0
                const plumbGeom = new THREE.BufferGeometry().setFromPoints([
                    new THREE.Vector3(0, 1.0, 0),
                    new THREE.Vector3(0, -1.0, 0)
                ]);
                const plumbMat = new THREE.LineDashedMaterial({{
                    color: 0x64748b,
                    dashSize: 0.04,
                    gapSize: 0.03,
                    transparent: true,
                    opacity: 0.40
                }});
                const plumbLine = new THREE.Line(plumbGeom, plumbMat);
                plumbLine.computeLineDistances();
                refLinesGroup.add(plumbLine);
            }}

            // 6. CARGA DE MODELO GLTF/GLB
            function loadDefaultModel() {{
                const loader = new THREE.GLTFLoader();

                if (defaultGlbBase64 && defaultGlbBase64.length > 5000) {{
                    loader.load(
                        defaultGlbBase64,
                        function (gltf) {{
                            setupModelHierarchy(gltf.scene);
                            modelStatus.textContent = "Modelo: Pelvis Anatómica CT (.GLB)";
                            applyAtlasPreset(currentActivePreset);
                        }},
                        undefined,
                        function (err) {{
                            console.warn("Fallo carga Base64, intentando ruta local:", err);
                            loadFromPathCascade();
                        }}
                    );
                }} else {{
                    loadFromPathCascade();
                }}

                function loadFromPathCascade() {{
                    loader.load(
                        "models/pelvis_anatomica.glb",
                        function (gltf) {{
                            setupModelHierarchy(gltf.scene);
                            modelStatus.textContent = "Modelo: models/pelvis_anatomica.glb";
                            applyAtlasPreset(currentActivePreset);
                        }},
                        undefined,
                        function (err1) {{
                            loader.load(
                                "assets/pelvis.glb",
                                function (gltf) {{
                                    setupModelHierarchy(gltf.scene);
                                    modelStatus.textContent = "Modelo: assets/pelvis.glb";
                                    applyAtlasPreset(currentActivePreset);
                                }},
                                undefined,
                                function (err2) {{
                                    loader.load(
                                        REMOTE_GLB_URL,
                                        function (gltf) {{
                                            setupModelHierarchy(gltf.scene);
                                            modelStatus.textContent = "Modelo: PelvisAtlas Remoto";
                                            applyAtlasPreset(currentActivePreset);
                                        }},
                                        undefined,
                                        function (err3) {{
                                            buildProceduralFallback();
                                            modelStatus.textContent = "Modelo: Estructura Base";
                                            applyAtlasPreset(currentActivePreset);
                                        }}
                                    );
                                }}
                            );
                        }}
                    );
                }}
            }}

            function splitCombinedPelvisMesh(combinedMesh, baseMat) {{
                const geom = combinedMesh.geometry;
                geom.computeBoundingBox();
                const bbox = geom.boundingBox;
                const center = bbox.getCenter(new THREE.Vector3());
                const size = bbox.getSize(new THREE.Vector3());

                const posAttr = geom.attributes.position;
                const indAttr = geom.index;
                const numTris = indAttr ? (indAttr.count / 3) : (posAttr.count / 3);

                const trisSacrum = [], trisL = [], trisR = [];

                for (let t = 0; t < numTris; t++) {{
                    const i0 = indAttr ? indAttr.getX(t * 3) : t * 3;
                    const i1 = indAttr ? indAttr.getX(t * 3 + 1) : t * 3 + 1;
                    const i2 = indAttr ? indAttr.getX(t * 3 + 2) : t * 3 + 2;

                    const cx = (posAttr.getX(i0) + posAttr.getX(i1) + posAttr.getX(i2)) / 3;
                    const cz = (posAttr.getZ(i0) + posAttr.getZ(i1) + posAttr.getZ(i2)) / 3;

                    const relX = (cx - center.x) / size.x;
                    const relZ = (cz - center.z) / size.z;

                    if (Math.abs(relX) < 0.16 && relZ < 0.05) {{
                        trisSacrum.push(i0, i1, i2);
                    }} else if (relX >= 0) {{
                        trisL.push(i0, i1, i2);
                    }} else {{
                        trisR.push(i0, i1, i2);
                    }}
                }}

                function makeSubMesh(triangleIndices, name) {{
                    const subGeom = new THREE.BufferGeometry();
                    const newPositions = [];
                    const remap = new Map();
                    const newIndices = [];

                    for (let idx of triangleIndices) {{
                        if (!remap.has(idx)) {{
                            remap.set(idx, newPositions.length / 3);
                            newPositions.push(posAttr.getX(idx), posAttr.getY(idx), posAttr.getZ(idx));
                        }}
                        newIndices.push(remap.get(idx));
                    }}

                    subGeom.setAttribute('position', new THREE.Float32BufferAttribute(newPositions, 3));
                    subGeom.setIndex(newIndices);
                    subGeom.computeVertexNormals();

                    const mesh = new THREE.Mesh(subGeom, baseMat.clone());
                    mesh.name = name;
                    return mesh;
                }}

                return {{
                    sacrum: makeSubMesh(trisSacrum, "Sacrum"),
                    hipL: makeSubMesh(trisL, "Hip_L"),
                    hipR: makeSubMesh(trisR, "Hip_R")
                }};
            }}

            function setupModelHierarchy(modelRoot) {{
                while(pivotIzq.children.length > 0) pivotIzq.remove(pivotIzq.children[0]);
                while(pivotDer.children.length > 0) pivotDer.remove(pivotDer.children[0]);
                if (sacroMesh && sacroMesh.parent) sacroMesh.parent.remove(sacroMesh);

                sacroMesh = null;
                iliacoIzqMesh = null;
                iliacoDerMesh = null;

                let detectedMeshes = [];
                modelRoot.traverse(function (child) {{
                    if (child.isMesh) {{
                        detectedMeshes.push(child);
                        // Asegurar normales suaves para evitar caras negras o invertidas
                        if (child.geometry) {{
                            child.geometry.computeVertexNormals();
                        }}
                        const name = (child.name || "").toLowerCase();

                        if (name === 'sacrum' || name === 'sacro' || name.includes('sacr')) {{
                            sacroMesh = child;
                        }} else if (name === 'hip_l' || name === 'ilium_l' || name === 'iliaco_izquierdo' ||
                                 name.includes('hip_l') || name.includes('ilium_l') || name.includes('left') || 
                                 name.includes('izq') || name.includes('_l')) {{
                            iliacoIzqMesh = child;
                        }} else if (name === 'hip_r' || name === 'ilium_r' || name === 'iliaco_derecho' ||
                                 name.includes('hip_r') || name.includes('ilium_r') || name.includes('right') || 
                                 name.includes('der') || name.includes('_r')) {{
                            iliacoDerMesh = child;
                        }}
                    }}
                }});

                if (detectedMeshes.length === 1 && (!sacroMesh || !iliacoIzqMesh || !iliacoDerMesh)) {{
                    const splitResult = splitCombinedPelvisMesh(detectedMeshes[0], boneMaterial);
                    sacroMesh = splitResult.sacrum;
                    iliacoIzqMesh = splitResult.hipL;
                    iliacoDerMesh = splitResult.hipR;
                }}

                if (!sacroMesh || !iliacoIzqMesh || !iliacoDerMesh) {{
                    detectedMeshes.forEach(mesh => {{
                        mesh.geometry.computeBoundingBox();
                        const center = mesh.geometry.boundingBox.getCenter(new THREE.Vector3());
                        if (Math.abs(center.x) < 0.15 && !sacroMesh) {{
                            sacroMesh = mesh;
                        }} else if (center.x > 0.10 && !iliacoIzqMesh) {{
                            iliacoIzqMesh = mesh;
                        }} else if (center.x < -0.10 && !iliacoDerMesh) {{
                            iliacoDerMesh = mesh;
                        }}
                    }});
                }}

                // Asignar el material óseo uniforme visible a todas las mallas
                if (sacroMesh) {{
                    sacroMesh.material = boneMaterial.clone();
                    pelvisGroup.add(sacroMesh);
                }}

                if (iliacoIzqMesh) {{
                    iliacoIzqMesh.material = boneMaterial.clone();
                    iliacoIzqMesh.position.sub(SIJ_LEFT_POS);
                    pivotIzq.add(iliacoIzqMesh);
                }}

                if (iliacoDerMesh) {{
                    iliacoDerMesh.material = boneMaterial.clone();
                    iliacoDerMesh.position.sub(SIJ_RIGHT_POS);
                    pivotDer.add(iliacoDerMesh);
                }}

                if (!sacroMesh && !iliacoIzqMesh && !iliacoDerMesh) {{
                    buildProceduralFallback();
                }}

                // Anclar hitos anatómicos vinculados solidariamente a los huesos
                attachLandmarksToBones();

                // Centrado automático tridimensional de la pelvis (THREE.Box3) sobre el origen (0, 0, 0)
                centerPelvisModel();
            }}

            function buildProceduralFallback() {{
                const sacroGeom = new THREE.CylinderGeometry(0.35, 0.15, 1.2, 16);
                sacroGeom.rotateX(Math.PI);
                sacroMesh = new THREE.Mesh(sacroGeom, boneMaterial.clone());
                sacroMesh.position.set(0, 0.1, -0.1);
                pelvisGroup.add(sacroMesh);

                const iliacoGeom = new THREE.TorusGeometry(0.65, 0.16, 16, 32, Math.PI * 1.3);
                iliacoIzqMesh = new THREE.Mesh(iliacoGeom, boneMaterial.clone());
                iliacoIzqMesh.position.set(-0.25, 0.05, 0);
                pivotIzq.add(iliacoIzqMesh);

                iliacoDerMesh = new THREE.Mesh(iliacoGeom.clone(), boneMaterial.clone());
                iliacoDerMesh.scale.set(-1, 1, 1);
                iliacoDerMesh.position.set(0.25, 0.05, 0);
                pivotDer.add(iliacoDerMesh);

                attachLandmarksToBones();
                centerPelvisModel();
            }}

            // 6.1 CENTRADO AUTOMÁTICO BASADO EN BOUNDING BOX (THREE.Box3)
            function centerPelvisModel() {{
                if (!sacroMesh && !iliacoIzqMesh && !iliacoDerMesh) return;

                pelvisGroup.updateMatrixWorld(true);
                const bbox = new THREE.Box3().setFromObject(pelvisGroup);
                const center = bbox.getCenter(new THREE.Vector3());

                // Desplazar pelvisGroup para que el centro geométrico de la pelvis coincida exactamente con (0, 0, 0)
                pelvisGroup.position.y += -center.y;
                pelvisGroup.position.z += -center.z;
                pelvisGroup.position.x += -center.x + BASE_CALIBRATION_POS_X;

                pelvisGroup.updateMatrixWorld(true);

                // Calibrar las alturas horizontales neutras de Crestas y EIAS
                if (markerCrestL && markerCrestR) {{
                    const pL = new THREE.Vector3();
                    const pR = new THREE.Vector3();
                    markerCrestL.group.getWorldPosition(pL);
                    markerCrestR.group.getWorldPosition(pR);
                    neutralCrestY = (pL.y + pR.y) / 2;
                }}
                if (markerEiasL && markerEiasR) {{
                    const eL = new THREE.Vector3();
                    const eR = new THREE.Vector3();
                    markerEiasL.group.getWorldPosition(eL);
                    markerEiasR.group.getWorldPosition(eR);
                    neutralEiasY = (eL.y + eR.y) / 2;
                }}

                setupReferenceLines();
            }}

            // 7. CONTROL DE CINEMÁTICA Y LERP DEL ATLAS BIOMECÁNICO
            const ATLAS_PRESETS_INFO = {{
                "pi": {{
                    title: "Ilíaco Posterior (PI)",
                    category: "Disfunción Iliosacra Rotacional Sagital",
                    listing: "Gonstead: PI | Mitchell: Rotación Posterior | Osteopatía: Retroversión coxal",
                    mechanism: "Caída sentada sobre isquion, frenada brusca con rodilla en extensión, o flexión lumbar forzada con piernas estiradas.",
                    palpation: "• EIAS: Alta y lateralizada\\n• EIPS: Baja y medializada hacia el sacro\\n• Cresta: Baja\\n• Pubis: Ascendido y hundido (retraído posterior)\\n• Isquion: Bajo\\n• Long-Sitting: Pierna corta en supino se alarga al sentarse\\n• Ligamento sacrotuberoso: Tensión aumentada\\n• Músculo Piramidal: Tensión excéntrica reactiva",
                    correction: "• Ajuste HVLA (Side-Posture Gonstead): Decúbito lateral con hemipelvis afectada arriba. PCP: Borde postero-inferior de EIPS. PCC: Pisiforme/eminencia hipotenar. LOD: P-A y de cefálico a caudal (~45° hacia carilla S3). Empuje cefálico contraindicado.\\n• MET (Mitchell): Contracción isométrica resistida de flexores de cadera (Psoas/Recto femoral) al 20-25% por 7-10s. Relajación y extensión pasiva."
                }},
                "as": {{
                    title: "Ilíaco Anterior (AS)",
                    category: "Disfunción Iliosacra Rotacional Sagital",
                    listing: "Gonstead: AS | Mitchell: Rotación Anterior | Osteopatía: Anteversión coxal",
                    mechanism: "Pisar en falso (escalón o bache), patada en vacío, extensión forzada de cadera en carrera o sobrecarga en golf/fútbol.",
                    palpation: "• EIAS: Baja y medializada\\n• EIPS: Alta y lateralizada\\n• Cresta: Alta\\n• Pubis: Descendido y prominente hacia anterior\\n• Isquion: Alto y posterior\\n• Long-Sitting: Pierna larga en supino se acorta al sentarse\\n• Ligamento sacrotuberoso: Distendido o laxo\\n• Músculo Psoas-Ilíaco: Espasmo hipertónico",
                    correction: "• Ajuste HVLA (Side-Posture Gonstead): Decúbito lateral con hemipelvis afectada arriba y cadera en flexión. PCP: Borde antero-superior de la cresta ilíaca (A-P) o tuberosidad isquiática hacia anterior. LOD: A-P sobre cresta para desrotar hacia posterior.\\n• MET (Mitchell): Contracción isométrica de extensores de cadera (Isquiotibiales/Glúteo mayor) al 20-25% por 7-10s. Ganar flexión pasiva de cadera."
                }},
                "up": {{
                    title: "Ilíaco Ascendido (Upslip)",
                    category: "Disfunción Iliosacra de Cizallamiento Vertical",
                    listing: "Mitchell: Cizallamiento Craneal / Upslip | Gonstead: Subluxación Vertical Superior",
                    mechanism: "Impacto axial con rodilla rígida extendida (ej. caída desde altura, frenazo automovilístico con pie en freno, choque frontal).",
                    palpation: "• Regla de los 3 Puntos Altos: Cresta, EIAS y EIPS altas simultáneamente\\n• Isquion: Alto\\n• Sínfisis Púbica: Escalón superior homolateral\\n• Long-Sitting: Pierna corta constante (se mantiene corta en supino y sentado)\\n• Tejidos blandos: Severo espasmo y dolor en Cuadrado Lumbar homolateral\\n• Ligamentos sacrotuberoso y sacroespinoso: Alta tracción",
                    correction: "• Ajuste HVLA (Supine Leg Pull): Paciente en supino. Toma supramaleolar con 15-20° de flexión de cadera, leve aducción y rotación interna. Tracción axial pura caudal enérgica y rápida sincronizada con tos fuerte.\\n• MET (Mitchell): Decúbito supino. Resistencia a elevación de cadera hacia la axila (hip hike) al 25% por 7-10s. Relajación y elongación caudal."
                }},
                "down": {{
                    title: "Ilíaco Descendido (Downslip)",
                    category: "Disfunción Iliosacra de Cizallamiento Vertical",
                    listing: "Mitchell: Cizallamiento Caudal / Downslip | Gonstead: Subluxación Vertical Inferior",
                    mechanism: "Tracción brusca de la pierna (pie atascado mientras el cuerpo avanza) o caída violenta con pierna colgando.",
                    palpation: "• Regla de los 3 Puntos Bajos: Cresta, EIAS y EIPS bajas simultáneamente\\n• Isquion: Bajo\\n• Sínfisis Púbica: Escalón inferior homolateral\\n• Long-Sitting: Pierna larga constante (se mantiene larga en supino y sentado)\\n• Tejidos blandos: Tensión reactiva en vientre de aductores y tensor de la fascia lata",
                    correction: "• Ajuste HVLA (Prone Ischial Push): Paciente en decúbito prono. PCP: Borde inferior de tuberosidad isquiática. PCC: Talón de mano caudal reforzado con mano contralateral. LOD: Inferior a Superior (I-S) paralelo al fémur en espiración.\\n• MET (Mitchell): Contracción isométrica de flexores de tronco y recto abdominal contra resistencia fija en fémur distal."
                }},
                "outflare": {{
                    title: "Ilíaco en Outflare (Rotación Externa)",
                    category: "Disfunción Iliosacra en Plano Transverso",
                    listing: "Mitchell: Outflare | Gonstead: EX (External) | Osteopatía: Apertura Ilíaca Externa",
                    mechanism: "Aducción forzada con rotación externa de fémur, microtraumas en ciclistas o patinadores, hipertonía del glúteo medio/TFL.",
                    palpation: "• EIAS: Lateralizada (distancia EIAS-ombligo aumentada)\\n• EIPS: Medializada (aproximada al surco sacro)\\n• Surco Sacro: Estrecho y comprimido en lado afecto\\n• Cresta e Isquion: Alturas niveladas simétricas\\n• Long-Sitting: Sin alteración de longitud funcional\\n• Banda iliotibial y TFL: Tensión e hipertonía notable",
                    correction: "• Ajuste HVLA: Decúbito lateral sobre el lado afecto abajo para fijarlo. PCP: Base sacra ipsilateral (sulcus). LOD: Posterior a Anterior (P-A) y Medial a Lateral (M-L) para anteriorizar el sacro y abrir el coxal.\\n• MET (Mitchell): Pierna 'en 4'. Contracción isométrica de abductores al 20-25% por 7-10s contra resistencia. Aducir progresivamente hacia línea media."
                }},
                "inflare": {{
                    title: "Ilíaco en Inflare (Rotación Interna)",
                    category: "Disfunción Iliosacra en Plano Transverso",
                    listing: "Mitchell: Inflare | Gonstead: IN (Internal) | Osteopatía: Cierre Ilíaco Interno",
                    mechanism: "Caída con cadera en abducción y rotación externa extrema, sobrecarga repetitiva en flexión/aducción.",
                    palpation: "• EIAS: Medializada (distancia EIAS-ombligo disminuida)\\n• EIPS: Lateralizada (alejada del surco sacro)\\n• Surco Sacro: Aparentemente más amplio\\n• Alturas verticales: Niveladas\\n• Fosa ilíaca: Dolorosa a la palpación del músculo ilíaco y ligamento sacroilíaco anterior",
                    correction: "• Ajuste HVLA: Decúbito lateral con hemipelvis afectada arriba. PCP: Cara medial de EIPS superior. LOD: Medial a Lateral (M-L) con antebrazo perpendicular para abrir la espina hacia lateral.\\n• MET (Mitchell): Cadera flectada a 90°. Contracción isométrica de aductores hacia línea media al 20-25% por 7-10s. Relajación y abducción pasiva hacia la barrera."
                }},
                "torsion_ant": {{
                    title: "Torsión Sacra Anterior (D/D o I/I)",
                    category: "Disfunción Sacroilíaca sobre Eje Oblicuo (Fisiológica)",
                    listing: "Mitchell: Torsión Anterior (Derecha/Derecha o Izquierda/Izquierda)",
                    mechanism: "Sobrecarga en flexión con rotación lumbar sincronizada durante la marcha o levantamiento asimétrico en bipedestación.",
                    palpation: "• Surco Sacro: Profundo en el lado opuesto al eje oblicuo dinámico\\n• Ángulo Inferolateral (AIL): Posterior e inferior contralateral al surco profundo\\n• Spring Test: NEGATIVO (retiene elasticidad normal y lordosis fisiológica)\\n• Test Supino/Prono: Inversión (pierna que parece larga en supino pasa a ser corta en prono)\\n• Piramidal: Espasmo e hipertonía notable del lado del eje oblicuo",
                    correction: "• Ajuste HVLA: Paciente en decúbito lateral sobre el lado de la base profunda (abajo). Flexión de cadera >90° para fijar L5-S1. PCP: Pisiforme sobre AIL posteriorizado arriba. LOD: P-A rápido para desrotar el sacro.\\n• MET (Mitchell): Posición de Sims (semi-prono) sobre el lado del eje oblicuo. El paciente intenta elevar ambos tobillos hacia el techo al 25% por 7-10s contra resistencia fija."
                }},
                "torsion_post": {{
                    title: "Torsión Sacra Posterior (D/I o I/D)",
                    category: "Disfunción Sacroilíaca sobre Eje Oblicuo (No Fisiológica)",
                    listing: "Mitchell: Torsión Posterior (Derecha/Izquierda o Izquierda/Derecha)",
                    mechanism: "Flexión de tronco brusca con carga excéntrica inesperada o traumatismo en caída que atrapa el sacro en retroversión no fisiológica.",
                    palpation: "• Surco Sacro: Plano, superficial y doloroso (base sacra posteriorizada hacia atrás)\\n• Ángulo Inferolateral (AIL): Anterior y superior contralateral a la base posteriorizada\\n• Spring Test: POSITIVO FRANCO (bloqueo rígido en tabla de madera, sin juego elástico, rectificación lumbar)\\n• Test Supino/Prono: Inversión (pierna corta en supino pasa a ser larga en prono)\\n• Tensión miofascial: Severa hipertonía de multífidos L5-S1 y piramidal",
                    correction: "• Ajuste HVLA: Decúbito lateral con la base sacra posteriorizada arriba. Cadera flexionada >90°. PCP: Eminencia hipotenar directamente en el sulcus/base sacra rígida. LOD: P-A con ligero vector M-L para intruir la base fija hacia anterior.\\n• MET (Mitchell): Decúbito lateral sobre el lado opuesto al eje oblicuo (tronco rotado hacia atrás). Pierna superior extendida colgando detrás de la camilla. Contracción isométrica de extensión de cadera al 25% por 7-10s."
                }}
            }};

            const ATLAS_CATEGORIES = {{
                "sagital": {{
                    name: "Rotacionales Sagitales",
                    presets: [
                        {{ key: "pi", name: "Ilíaco Posterior (PI) - Retroversión" }},
                        {{ key: "as", name: "Ilíaco Anterior (AS) - Anteversión" }}
                    ]
                }},
                "vertical": {{
                    name: "Cizallamientos Verticales",
                    presets: [
                        {{ key: "up", name: "Ilíaco Ascendido (Upslip) - Craneal" }},
                        {{ key: "down", name: "Ilíaco Descendido (Downslip) - Caudal" }}
                    ]
                }},
                "transversal": {{
                    name: "Transversales (Flares)",
                    presets: [
                        {{ key: "outflare", name: "Ilíaco Outflare (EX) - Rot. Externa" }},
                        {{ key: "inflare", name: "Ilíaco Inflare (IN) - Rot. Interna" }}
                    ]
                }},
                "sacro": {{
                    name: "Torsiones Sacras",
                    presets: [
                        {{ key: "torsion_ant", name: "Torsión Sacra Anterior (D/D, I/I)" }},
                        {{ key: "torsion_post", name: "Torsión Sacra Posterior (D/I, I/D)" }}
                    ]
                }}
            }};

            function onCategorySelectChange(catKey) {{
                const disfSelect = document.getElementById('atlas-dysfunction-select');
                if (!disfSelect) return;
                disfSelect.innerHTML = '';
                const cat = ATLAS_CATEGORIES[catKey];
                if (!cat) return;
                cat.presets.forEach(p => {{
                    const opt = document.createElement('option');
                    opt.value = p.key;
                    opt.textContent = p.name;
                    disfSelect.appendChild(opt);
                }});
                if (cat.presets.length > 0) {{
                    applyAtlasPreset(cat.presets[0].key);
                }}
            }}

            function syncCategoryAndDysfunctionSelectors(presetKey) {{
                let foundCat = 'sagital';
                for (const [ck, cdata] of Object.entries(ATLAS_CATEGORIES)) {{
                    if (cdata.presets.some(p => p.key === presetKey)) {{
                        foundCat = ck;
                        break;
                    }}
                }}
                const catSelect = document.getElementById('atlas-category-select');
                const disfSelect = document.getElementById('atlas-dysfunction-select');
                if (catSelect && catSelect.value !== foundCat) {{
                    catSelect.value = foundCat;
                }}
                if (disfSelect) {{
                    disfSelect.innerHTML = '';
                    ATLAS_CATEGORIES[foundCat].presets.forEach(p => {{
                        const opt = document.createElement('option');
                        opt.value = p.key;
                        opt.textContent = p.name;
                        if (p.key === presetKey) opt.selected = true;
                        disfSelect.appendChild(opt);
                    }});
                    if (presetKey !== 'neutral' && presetKey !== 'dysfunction') {{
                        disfSelect.value = presetKey;
                    }}
                }}
            }}

            function setAtlasSide(side) {{
                currentPatientSide = side;
                isRight = (side === "Derecho");
                const btnD = document.getElementById('side-btn-d');
                const btnI = document.getElementById('side-btn-i');
                if (btnD) btnD.classList.toggle('active', isRight);
                if (btnI) btnI.classList.toggle('active', !isRight);

                applyAtlasPreset(currentActivePreset);
            }}

            function applyAtlasPreset(presetKey) {{
                if (isGaitActive) toggleGait();
                currentActivePreset = presetKey;
                currentMode = presetKey;

                syncCategoryAndDysfunctionSelectors(presetKey);

                // Actualizar resaltado de botones
                document.querySelectorAll('.preset-subtoolbar button, .top-toolbar button').forEach(b => {{
                    if (b.id && (b.id.startsWith('btn-preset-') || b.id === 'btn-dysfunction' || b.id === 'btn-neutral')) {{
                        b.classList.remove('active');
                    }}
                }});

                const activeBtn = document.getElementById('btn-preset-' + presetKey) || document.getElementById('btn-' + presetKey);
                if (activeBtn) activeBtn.classList.add('active');

                const btnL = document.getElementById('btn-toggle-landmarks');
                if (btnL) btnL.classList.toggle('active', showLandmarks);
                const btnR = document.getElementById('btn-toggle-lines');
                if (btnR) btnR.classList.toggle('active', showReferenceLines);
                const btnCard = document.getElementById('btn-toggle-didactic');
                if (btnCard) btnCard.classList.toggle('active', showDidacticCard);

                // Reset de objetivos de transformación
                targetRotLeft = 0.0; targetRotYLeft = 0.0; targetTransYLeft = 0.0; targetTransZLeft = 0.0;
                targetRotRight = 0.0; targetRotYRight = 0.0; targetTransYRight = 0.0; targetTransZRight = 0.0;
                targetSacrumRotY = 0.0; targetSacrumRotZ = 0.0; targetSacrumPosZ = 0.0;

                if (presetKey === 'neutral') {{
                    statusBadge.className = 'badge-status badge-neutral';
                    statusBadge.textContent = '🟢 ESTADO NEUTRO (ALINEACIÓN SIMÉTRICA)';
                    hudInfo.innerHTML = '<span>📐 <strong>Estado Neutro:</strong> Pelvis nivelada, sin torsión ni cizallamiento. Planos de referencia paralelos.</span>';
                    updateDidacticCard('neutral');
                    return;
                }}

                statusBadge.className = 'badge-status badge-dysfunction';

                if (presetKey === 'dysfunction') {{
                    statusBadge.textContent = '🔴 DISFUNCIÓN ACTIVA: ' + diagTitle;
                    let coupledTransZ = 0.0;
                    if (clinicalTargetRotX < -0.01) coupledTransZ = -0.075;
                    else if (clinicalTargetRotX > 0.01) coupledTransZ = 0.075;

                    if (isRight) {{
                        targetRotRight = clinicalTargetRotX;
                        targetTransYRight = clinicalTargetTransY;
                        targetTransZRight = coupledTransZ;
                    }} else {{
                        targetRotLeft = clinicalTargetRotX;
                        targetTransYLeft = clinicalTargetTransY;
                        targetTransZLeft = coupledTransZ;
                    }}
                    const rotDeg = (Math.abs(clinicalTargetRotX) * (180 / Math.PI)).toFixed(1);
                    const rotDesc = clinicalTargetRotX < -0.01 ? "Retroversión (PI)" : (clinicalTargetRotX > 0.01 ? "Anteversión (AS)" : "Sin rotación");
                    hudInfo.innerHTML = `<span>⚡ <strong>Disfunción del Paciente:</strong> ${{rotDesc}} [${{rotDeg}}°] | Cizallamiento ${{clinicalTargetTransY.toFixed(2)}} u sobre el lado <strong>${{currentPatientSide}}</strong>.</span>`;

                    if (clinicalTargetRotX < -0.01) updateDidacticCard('pi');
                    else if (clinicalTargetRotX > 0.01) updateDidacticCard('as');
                    else if (clinicalTargetTransY > 0.01) updateDidacticCard('up');
                    else if (clinicalTargetTransY < -0.01) updateDidacticCard('down');
                    else updateDidacticCard('pi');
                    return;
                }}

                if (presetKey === 'pi') {{
                    statusBadge.textContent = `⚡ Ilíaco Posterior (PI) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetRotRight = -0.07;
                        targetTransZRight = -0.075;
                    }} else {{
                        targetRotLeft = -0.07;
                        targetTransZLeft = -0.075;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Ilíaco Posterior (PI) [${{currentPatientSide}}]:</strong> Retroversión (-4.0°). EIAS alta/posterior, EIPS baja, Pubis retraído posterior/superior.</span>`;
                }} else if (presetKey === 'as') {{
                    statusBadge.textContent = `⚡ Ilíaco Anterior (AS) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetRotRight = 0.07;
                        targetTransZRight = 0.075;
                    }} else {{
                        targetRotLeft = 0.07;
                        targetTransZLeft = 0.075;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Ilíaco Anterior (AS) [${{currentPatientSide}}]:</strong> Anteversión (+4.0°). EIAS baja/anterior, EIPS alta, Pubis adelantado anterior/inferior.</span>`;
                }} else if (presetKey === 'up') {{
                    statusBadge.textContent = `⚡ Ilíaco Ascendido (Upslip) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetTransYRight = 0.07;
                    }} else {{
                        targetTransYLeft = 0.07;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Ilíaco Ascendido (Upslip) [${{currentPatientSide}}]:</strong> Cizallamiento craneal (+0.07 u). Cresta, EIAS, EIPS y pubis elevados en bloque.</span>`;
                }} else if (presetKey === 'down') {{
                    statusBadge.textContent = `⚡ Ilíaco Descendido (Downslip) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetTransYRight = -0.07;
                    }} else {{
                        targetTransYLeft = -0.07;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Ilíaco Descendido (Downslip) [${{currentPatientSide}}]:</strong> Cizallamiento caudal (-0.07 u). Todos los hitos pélvicos descendidos en bloque.</span>`;
                }} else if (presetKey === 'outflare') {{
                    statusBadge.textContent = `⚡ Ilíaco Outflare (EX) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetRotYRight = -0.06;
                    }} else {{
                        targetRotYLeft = 0.06;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Outflare (Rotación Externa) [${{currentPatientSide}}]:</strong> EIAS lateralizada y abierta (distancia al ombligo aumentada), EIPS medializada.</span>`;
                }} else if (presetKey === 'inflare') {{
                    statusBadge.textContent = `⚡ Ilíaco Inflare (IN) - ${{currentPatientSide}}`;
                    if (isRight) {{
                        targetRotYRight = 0.06;
                    }} else {{
                        targetRotYLeft = -0.06;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Inflare (Rotación Interna) [${{currentPatientSide}}]:</strong> EIAS medializada y cerrada (distancia al ombligo disminuida), EIPS lateralizada.</span>`;
                }} else if (presetKey === 'torsion_ant') {{
                    statusBadge.textContent = `⚡ Torsión Sacra Anterior (${{isRight ? 'Der/Der' : 'Izq/Izq'}})`;
                    if (isRight) {{
                        targetSacrumRotY = 0.045;
                        targetSacrumRotZ = -0.025;
                        targetSacrumPosZ = -0.015;
                    }} else {{
                        targetSacrumRotY = -0.045;
                        targetSacrumRotZ = 0.025;
                        targetSacrumPosZ = -0.015;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Torsión Sacra Anterior (${{isRight ? 'D/D' : 'I/I'}}):</strong> Sulcus profundo en lado dinámico, AIL posterior contralateral, Spring test negativo (elástico).</span>`;
                }} else if (presetKey === 'torsion_post') {{
                    statusBadge.textContent = `⚡ Torsión Sacra Posterior (${{isRight ? 'Der/Izq' : 'Izq/Der'}})`;
                    if (isRight) {{
                        targetSacrumRotY = -0.045;
                        targetSacrumRotZ = 0.025;
                        targetSacrumPosZ = 0.015;
                    }} else {{
                        targetSacrumRotY = 0.045;
                        targetSacrumRotZ = -0.025;
                        targetSacrumPosZ = 0.015;
                    }}
                    hudInfo.innerHTML = `<span>⚡ <strong>Torsión Sacra Posterior (${{isRight ? 'D/I' : 'I/D'}}):</strong> Base sacra posteriorizada (sulcus plano/rígido), Spring test positivo franco (bloqueo duro).</span>`;
                }}

                updateDidacticCard(presetKey);
            }}

            function toggleNeutral() {{
                if (currentMode === 'neutral') {{
                    applyAtlasPreset(baseActivePreset);
                }} else {{
                    applyAtlasPreset('neutral');
                }}
            }}

            // Compatibilidad con llamadas heredadas
            function setMode(mode) {{
                applyAtlasPreset(mode);
            }}

            function applyPreset(preset) {{
                applyAtlasPreset(preset);
            }}

            function updateDidacticCard(presetKey) {{
                const card = document.getElementById('didacticCard');
                if (!card) return;
                const badge = document.getElementById('didacticPresetBadge');
                const listElem = document.getElementById('didacticListing');
                const mechElem = document.getElementById('didacticMechanism');
                const palpElem = document.getElementById('didacticPalpation');
                const corrElem = document.getElementById('didacticCorrection');

                if (presetKey === 'neutral') {{
                    if (badge) badge.textContent = 'ESTADO NEUTRO';
                    if (listElem) listElem.textContent = 'Alineación anatómica normal / Eje simétrico en 3 planos';
                    if (mechElem) mechElem.textContent = 'Equilibrio estático y dinámico simétrico sin restricción articular ni dolor.';
                    if (palpElem) palpElem.textContent = '• Alturas de EIAS, EIPS, Crestas e Isquion niveladas bilateralmente\\n• Sínfisis púbica alineada sin escalón\\n• Spring Test: Normal elástico\\n• Long-Sitting: Sin alteración de longitud funcional';
                    if (corrElem) corrElem.textContent = 'No requiere corrección ni manipulación articular. Mantener movilidad fisiológica y estabilidad funcional.';
                    return;
                }}

                const info = ATLAS_PRESETS_INFO[presetKey];
                if (!info) return;

                if (badge) badge.textContent = info.title.toUpperCase() + ' (' + currentPatientSide + ')';
                if (listElem) listElem.textContent = info.listing;
                if (mechElem) mechElem.textContent = info.mechanism;
                if (palpElem) palpElem.textContent = info.palpation;
                if (corrElem) corrElem.textContent = info.correction;
            }}

            function toggleDidacticCard() {{
                const card = document.getElementById('didacticCard');
                const btn = document.getElementById('didacticToggleBtn');
                if (card) {{
                    card.classList.toggle('minimized');
                    if (btn) btn.textContent = card.classList.contains('minimized') ? '+' : '—';
                }}
            }}

            function toggleDidacticCardVisibility() {{
                showDidacticCard = !showDidacticCard;
                const card = document.getElementById('didacticCard');
                const btn = document.getElementById('btn-toggle-didactic');
                if (card) {{
                    card.style.display = showDidacticCard ? 'flex' : 'none';
                }}
                if (btn) {{
                    btn.classList.toggle('active', showDidacticCard);
                }}
            }}

            function toggleGait() {{
                isGaitActive = !isGaitActive;
                const btn = document.getElementById('btn-gait');
                if (isGaitActive) {{
                    btn.textContent = '⏸ Pausar Marcha';
                    btn.classList.add('active');
                    statusBadge.className = 'badge-status badge-neutral';
                    statusBadge.textContent = '🔄 SIMULACIÓN DE DINÁMICA DE MARCHA (3D)';
                }} else {{
                    btn.textContent = '▶ Marcha Dinámica';
                    btn.classList.remove('active');
                    setMode(currentMode);
                }}
            }}

            function toggleLandmarks() {{
                showLandmarks = !showLandmarks;
                const btn = document.getElementById('btn-toggle-landmarks');
                if (btn) btn.classList.toggle('active', showLandmarks);
                const allMarkers = [markerCrestL, markerCrestR, markerEiasL, markerEiasR, markerEipsL, markerEipsR, markerIschL, markerIschR, markerPubisL, markerPubisR];
                allMarkers.forEach(m => {{
                    if (m && m.group) {{
                        m.group.visible = showLandmarks;
                        if (m.label2d) m.label2d.visible = showLandmarks;
                    }}
                }});
                if (labelRenderer && labelRenderer.domElement) {{
                    labelRenderer.domElement.style.display = showLandmarks ? 'block' : 'none';
                }}
            }}

            function toggleReferenceLines() {{
                showReferenceLines = !showReferenceLines;
                const btn = document.getElementById('btn-toggle-lines');
                if (btn) btn.classList.toggle('active', showReferenceLines);
                if (refLinesGroup) refLinesGroup.visible = showReferenceLines;
                const tiltBadge = document.getElementById('tiltBadge');
                if (tiltBadge) tiltBadge.style.display = showReferenceLines ? 'flex' : 'none';
            }}

            // 8. CONTROL DE VISTAS RÁPIDAS DE CÁMARA
            function setCameraView(view) {{
                isCameraAnimating = true;
                targetLookAt.set(0, 0, 0);

                if (view === 'anterior') {{
                    targetCamPos.set(0, 0, DEFAULT_CAM_DISTANCE);
                    camera.up.set(0, 1, 0);
                }} else if (view === 'posterior') {{
                    targetCamPos.set(0, 0, -DEFAULT_CAM_DISTANCE);
                    camera.up.set(0, 1, 0);
                }} else if (view === 'sagital') {{
                    const camX = isRight ? -DEFAULT_CAM_DISTANCE : DEFAULT_CAM_DISTANCE;
                    targetCamPos.set(camX, 0, 0);
                    camera.up.set(0, 1, 0);
                }} else if (view === 'axial') {{
                    targetCamPos.set(0, DEFAULT_CAM_DISTANCE, 0.01);
                    camera.up.set(0, 0, -1);
                }}
            }}

            function resetCamera() {{
                try {{
                    sessionStorage.removeItem('biopelvis_cam_pos');
                    sessionStorage.removeItem('biopelvis_cam_target');
                    sessionStorage.removeItem('biopelvis_cam_zoom');
                }} catch(e) {{}}
                camera.up.set(0, 1, 0);
                if (controls) controls.target.set(0, 0, 0);
                setCameraView('anterior');
            }}

            // 9. CARGA DE ARCHIVO EXTERNO (DRAG & DROP / BOTÓN)
            function setupDragAndDrop() {{
                const zone = document.getElementById('canvas-container') || document.getElementById('dropZone');
                const overlay = document.getElementById('dragOverlay');
                if (!zone || !overlay) return;

                zone.addEventListener('dragover', (e) => {{
                    e.preventDefault();
                    overlay.style.display = 'flex';
                }});

                zone.addEventListener('dragleave', () => {{
                    overlay.style.display = 'none';
                }});

                zone.addEventListener('drop', (e) => {{
                    e.preventDefault();
                    overlay.style.display = 'none';
                    if (e.dataTransfer.files.length > 0) {{
                        loadGlbFromFile(e.dataTransfer.files[0]);
                    }}
                }});
            }}

            function handleFileSelect(event) {{
                if (event.target.files.length > 0) {{
                    loadGlbFromFile(event.target.files[0]);
                }}
            }}

            function loadGlbFromFile(file) {{
                const reader = new FileReader();
                reader.onload = function(e) {{
                    const contents = e.target.result;
                    const loader = new THREE.GLTFLoader();
                    loader.parse(contents, '', function(gltf) {{
                        setupModelHierarchy(gltf.scene);
                        modelStatus.textContent = "Modelo: " + file.name;
                        hudInfo.innerHTML = `<span>✅ <strong>Modelo anatómico cargado:</strong> ${{file.name}} con articulación y marcadores óseos activos.</span>`;
                    }}, function(err) {{
                        alert("Error al procesar el archivo 3D: " + err);
                    }});
                }};
                reader.readAsArrayBuffer(file);
            }}

            // 10. BUCLE DE RENDERIZADO Y ACTUALIZACIÓN DINÁMICA
            function animate() {{
                window.__biopelvis_anim_frame = requestAnimationFrame(animate);

                // Cinemática de marcha dinámica fisiológica calibrada
                if (isGaitActive) {{
                    gaitTime += 0.05;
                    const waveL = Math.sin(gaitTime);
                    const waveR = Math.sin(gaitTime + Math.PI);
                    targetRotLeft = waveL * 0.06;
                    targetTransYLeft = waveL * 0.02;
                    targetRotRight = waveR * 0.06;
                    targetTransYRight = waveR * 0.02;
                }}

                // Interpolación fluida (lerp) para el ilíaco izquierdo
                currentRotLeft += (targetRotLeft - currentRotLeft) * 0.08;
                currentRotYLeft += (targetRotYLeft - currentRotYLeft) * 0.08;
                currentTransYLeft += (targetTransYLeft - currentTransYLeft) * 0.08;
                currentTransZLeft += (targetTransZLeft - currentTransZLeft) * 0.08;
                pivotIzq.rotation.x = currentRotLeft;
                pivotIzq.rotation.y = currentRotYLeft;
                pivotIzq.position.y = SIJ_LEFT_POS.y + currentTransYLeft;
                pivotIzq.position.z = SIJ_LEFT_POS.z + currentTransZLeft;

                // Interpolación fluida (lerp) para el ilíaco derecho
                currentRotRight += (targetRotRight - currentRotRight) * 0.08;
                currentRotYRight += (targetRotYRight - currentRotYRight) * 0.08;
                currentTransYRight += (targetTransYRight - currentTransYRight) * 0.08;
                currentTransZRight += (targetTransZRight - currentTransZRight) * 0.08;
                pivotDer.rotation.x = currentRotRight;
                pivotDer.rotation.y = currentRotYRight;
                pivotDer.position.y = SIJ_RIGHT_POS.y + currentTransYRight;
                pivotDer.position.z = SIJ_RIGHT_POS.z + currentTransZRight;

                // Interpolación fluida (lerp) para el nodo Sacro (Torsiones sobre eje oblicuo)
                currentSacrumRotY += (targetSacrumRotY - currentSacrumRotY) * 0.08;
                currentSacrumRotZ += (targetSacrumRotZ - currentSacrumRotZ) * 0.08;
                currentSacrumPosZ += (targetSacrumPosZ - currentSacrumPosZ) * 0.08;
                if (sacroMesh) {{
                    sacroMesh.rotation.y = currentSacrumRotY;
                    sacroMesh.rotation.z = currentSacrumRotZ;
                    sacroMesh.position.z = currentSacrumPosZ;
                }}

                // Actualizar planos y líneas de nivel de referencia en tiempo real
                if (showReferenceLines) {{
                    let maxDeltaY = 0;
                    let tiltAngleDeg = 0;

                    if (lineCrests && refLineCrests && markerCrestL && markerCrestR) {{
                        const posCL = new THREE.Vector3();
                        const posCR = new THREE.Vector3();
                        markerCrestL.group.getWorldPosition(posCL);
                        markerCrestR.group.getWorldPosition(posCR);

                        lineCrests.geometry.setFromPoints([posCL, posCR]);

                        // Plano horizontal neutro FIJO en el nivel calibrado
                        const avgZ_c = (posCL.z + posCR.z) / 2;
                        refLineCrests.geometry.setFromPoints([
                            new THREE.Vector3(-1.15, neutralCrestY, avgZ_c),
                            new THREE.Vector3(1.15, neutralCrestY, avgZ_c)
                        ]);
                        refLineCrests.computeLineDistances();

                        const deltaY_c = posCL.y - posCR.y;
                        const deltaX_c = posCL.x - posCR.x;
                        const angleCrest = Math.atan(Math.abs(deltaY_c) / Math.abs(deltaX_c)) * (180 / Math.PI);
                        if (Math.abs(deltaY_c) > maxDeltaY) {{
                            maxDeltaY = Math.abs(deltaY_c);
                            tiltAngleDeg = angleCrest;
                        }}
                    }}

                    if (lineEIAS && refLineEIAS && markerEiasL && markerEiasR) {{
                        const posEL = new THREE.Vector3();
                        const posER = new THREE.Vector3();
                        markerEiasL.group.getWorldPosition(posEL);
                        markerEiasR.group.getWorldPosition(posER);

                        lineEIAS.geometry.setFromPoints([posEL, posER]);

                        // Plano horizontal neutro FIJO en el nivel calibrado
                        const avgZ_e = (posEL.z + posER.z) / 2;
                        refLineEIAS.geometry.setFromPoints([
                            new THREE.Vector3(-1.15, neutralEiasY, avgZ_e),
                            new THREE.Vector3(1.15, neutralEiasY, avgZ_e)
                        ]);
                        refLineEIAS.computeLineDistances();

                        const deltaY_e = posEL.y - posER.y;
                        const deltaX_e = posEL.x - posER.x;
                        const angleEias = Math.atan(Math.abs(deltaY_e) / Math.abs(deltaX_e)) * (180 / Math.PI);
                        if (Math.abs(deltaY_e) > maxDeltaY) {{
                            maxDeltaY = Math.abs(deltaY_e);
                            tiltAngleDeg = angleEias;
                        }}
                    }}

                    // En Estado Neutro, forzar lectura estricta 0.0° y 0.0 mm
                    const isNeutralState = (currentActivePreset === 'neutral') ||
                        (Math.abs(currentRotLeft) < 0.002 && Math.abs(currentRotRight) < 0.002 &&
                         Math.abs(currentRotYLeft) < 0.002 && Math.abs(currentRotYRight) < 0.002 &&
                         Math.abs(currentTransYLeft) < 0.002 && Math.abs(currentTransYRight) < 0.002 &&
                         Math.abs(currentSacrumRotY) < 0.002 && Math.abs(currentSacrumRotZ) < 0.002 && !isGaitActive);

                    const hasTilt = !isNeutralState && (maxDeltaY > 0.005);
                    const alertColorCrest = hasTilt ? 0xf43f5e : 0x10b981;
                    const alertColorEias = hasTilt ? 0xf43f5e : 0x38bdf8;
                    if (lineCrests) lineCrests.material.color.setHex(alertColorCrest);
                    if (lineEIAS) lineEIAS.material.color.setHex(alertColorEias);

                    // Actualizar badge flotante con ángulo y desnivel relativo
                    const tiltBadge = document.getElementById('tiltBadge');
                    const tiltDot = document.getElementById('tiltStatusDot');
                    const tiltTitle = document.getElementById('tiltTitle');
                    const tiltAngle = document.getElementById('tiltAngle');
                    const tiltDeltaY = document.getElementById('tiltDeltaY');

                    if (tiltBadge) {{
                        if (isNeutralState || !hasTilt) {{
                            tiltBadge.className = 'tilt-badge-overlay tilt-neutral';
                            if (tiltDot) tiltDot.className = 'tilt-dot dot-neutral';
                            if (tiltTitle) tiltTitle.textContent = 'ALINEACIÓN SIMÉTRICA';
                            if (tiltAngle) tiltAngle.textContent = 'Inclinación: 0.0°';
                            if (tiltDeltaY) tiltDeltaY.textContent = 'Desnivel: 0.0 mm';
                        }} else {{
                            tiltBadge.className = 'tilt-badge-overlay tilt-alert';
                            if (tiltDot) tiltDot.className = 'tilt-dot dot-alert';
                            if (tiltTitle) tiltTitle.textContent = 'ASIMETRÍA PÉLVICA DETECTADA';
                            const mmDisp = (maxDeltaY * 100).toFixed(1);
                            if (tiltAngle) tiltAngle.textContent = `Inclinación: ${{tiltAngleDeg.toFixed(1)}}°`;
                            if (tiltDeltaY) tiltDeltaY.textContent = `Desnivel: ${{mmDisp}} mm`;
                        }}
                    }}
                }}

                // Interpolación suave de cámara en cambios de vista
                if (isCameraAnimating) {{
                    camera.position.lerp(targetCamPos, 0.08);
                    controls.target.lerp(targetLookAt, 0.08);
                    if (targetCamPos.z !== 0.01) {{
                        camera.up.set(0, 1, 0);
                    }}
                    camera.lookAt(controls.target);
                    if (camera.position.distanceTo(targetCamPos) < 0.01) {{
                        camera.position.copy(targetCamPos);
                        controls.target.copy(targetLookAt);
                        if (targetCamPos.z !== 0.01) {{
                            camera.up.set(0, 1, 0);
                        }}
                        camera.lookAt(controls.target);
                        isCameraAnimating = false;
                    }}
                }}

                controls.update();
                renderer.render(scene, camera);
                if (labelRenderer) {{
                    labelRenderer.render(scene, camera);
                }}
            }}

            window.onload = initScene;
        </script>
    </body>
    </html>
    """
    return html


# Alias de compatibilidad histórica
generar_simulador_dinamico_svg = generar_visor_3d_pelvis


def generar_diagrama_vectorial_ajuste(
    lado: str,
    diagnostico: DiagnosticoBiomecanico,
    palpacion: Optional[ExamenPalpatorio] = None
) -> str:
    """
    Genera el Módulo B: Diagrama Vectorial de Ajuste y Puntos de Contacto (Post-Evaluación).
    Presenta un esquema anatómico focalizado en la hemipelvis y articulación sacroilíaca a tratar,
    con el Punto de Contacto del Paciente (PCP) pulsante, el Vector de Fuerza (LOD) de alta visibilidad,
    y una leyenda técnica flotante con diseño Glassmorphism HUD.
    """
    info = get_disfuncion_info(diagnostico.clave_conocimiento) if diagnostico.clave_conocimiento else {}
    ajuste = info.get("ajuste_articular", {}) if info else {}
    is_right = (lado == "Derecho")

    # Valores por defecto sobrios si no está en la base de datos o patrón mixto
    tecnica = ajuste.get("tecnica", "Técnica de Movilización Articular / MET Funcional")
    pcc = ajuste.get("pcc", "Pisiforme / Eminencia hipotenar de la mano caudal")
    pcp = ajuste.get("pcp", "Aspecto postero-inferior de la EIPS homolateral")
    linea_correccion = ajuste.get("linea_correccion", "Vector de corrección biomecánica específico")
    posicion_paciente = ajuste.get("posicion_paciente", "Decúbito lateral con hemipelvis en restricción hacia arriba")
    advertencia = ajuste.get("advertencia", "Verificar ausencia de banderas rojas y respetar la barrera motriz patológica.")

    # Calcular coordenadas anatómicas específicas para PCP y LOD
    clave = (diagnostico.clave_conocimiento or "").upper()
    titulo_diag = diagnostico.titulo.lower()

    # Center schematic around (340, 260) for left or flipped for right
    cx = 320 if not is_right else 360
    
    vector_text = "Vector LOD"
    vector_angle_label = "45° Caudal"
    arrow_color = "#10b981"
    
    # Defaults for Gonstead PI
    pcp_x = cx + 65
    pcp_y = 155
    lod_from_x = pcp_x + 90
    lod_from_y = pcp_y - 75
    lod_to_x = pcp_x - 30
    lod_to_y = pcp_y + 40
    vector_angle_label = "45° Caudal hacia Eje S3"
    vector_text = "LOD: P-A 45° Caudal (Eje S3)"

    if "sacro_antero_inferior" in clave.lower() or "antero-inferior" in titulo_diag:
        # Contacto: ILA contralateral (ALI) | Vector: PA + LM con codo pegado al cuerpo
        pcp_x = cx + (35 if is_right else -35)
        pcp_y = 350
        lod_from_x = pcp_x + (60 if is_right else -60)
        lod_from_y = pcp_y - 30
        lod_to_x = pcp_x - (25 if is_right else -25)
        lod_to_y = pcp_y + 10
        vector_angle_label = "PA + LM (Codo al cuerpo)"
        vector_text = "LOD: PA + LM sobre ILA contralateral"
        arrow_color = "#f59e0b"
    elif "sacro_postero_superior" in clave.lower() or "postero-superior" in titulo_diag:
        # Contacto: Medial a la EIPS, por encima del eje | Vector: PA + ML + de craneal a caudal
        pcp_x = cx + (-25 if is_right else 25)
        pcp_y = 190
        lod_from_x = pcp_x - (40 if is_right else -40)
        lod_from_y = pcp_y - 60
        lod_to_x = pcp_x + (20 if is_right else -20)
        lod_to_y = pcp_y + 40
        vector_angle_label = "PA + ML + Cráneo-Caudal"
        vector_text = "LOD: PA + ML + Caudal sobre Base"
        arrow_color = "#ec4899"
    elif "sacro_flexion_unilateral" in clave.lower() or "flexión unilateral" in titulo_diag:
        # Contacto: S1-S2 / ILA | Vector: LM torque arriba / ILA abajo a arriba
        pcp_x = cx + (20 if is_right else -20)
        pcp_y = 280
        lod_from_x = pcp_x + (45 if is_right else -45)
        lod_from_y = pcp_y + 45
        lod_to_x = pcp_x - (15 if is_right else -15)
        lod_to_y = pcp_y - 35
        vector_angle_label = "LM + Torque hacia arriba"
        vector_text = "LOD: LM con torque ascendente"
        arrow_color = "#8b5cf6"
    elif "sacro_extension_unilateral" in clave.lower() or "extensión unilateral" in titulo_diag:
        # Contacto: Lateral al ILA (ALI) | Vector: LM descendiendo el ILA
        pcp_x = cx + (30 if is_right else -30)
        pcp_y = 355
        lod_from_x = pcp_x + (50 if is_right else -50)
        lod_from_y = pcp_y - 40
        lod_to_x = pcp_x - (20 if is_right else -20)
        lod_to_y = pcp_y + 35
        vector_angle_label = "LM descendiendo ILA"
        vector_text = "LOD: Lateral a Medial Descendente"
        arrow_color = "#06b6d4"
    elif "sacro_flexion" in clave.lower() or "flexión bilateral" in titulo_diag:
        # Contacto: Base sacra / ápex | Vector: PA + SI hacia extensión
        pcp_x = cx
        pcp_y = 220
        lod_from_x = pcp_x
        lod_from_y = pcp_y - 60
        lod_to_x = pcp_x
        lod_to_y = pcp_y + 40
        vector_angle_label = "PA + SI (Hacia Extensión)"
        vector_text = "LOD: PA + SI hacia Extensión"
        arrow_color = "#10b981"
    elif "sacro_extension" in clave.lower() or "extensión bilateral" in titulo_diag:
        # Contacto: Base sacra en línea media | Vector: PA puro
        pcp_x = cx
        pcp_y = 200
        lod_from_x = pcp_x
        lod_from_y = pcp_y - 70
        lod_to_x = pcp_x
        lod_to_y = pcp_y + 30
        vector_angle_label = "PA puro (Sin Lateralidad)"
        vector_text = "LOD: PA puro en línea media"
        arrow_color = "#0284c7"
    elif "downslip" in clave or "downslip" in titulo_diag or "inferior" in titulo_diag:
        # Downslip: Ischium contact, upward push
        pcp_x = cx - 20
        pcp_y = 425
        lod_from_x = pcp_x
        lod_from_y = pcp_y + 80
        lod_to_x = pcp_x
        lod_to_y = pcp_y - 45
        vector_angle_label = "90° Vertical Caudo-Craneal (+Y)"
        vector_text = "LOD: Caudo-Craneal Vertical Directo"
        arrow_color = "#38bdf8"
    elif "upslip" in clave or "upslip" in titulo_diag or "superior" in titulo_diag:
        # Upslip: Supramalleolar traction, downward pull
        pcp_x = cx - 40
        pcp_y = 440
        lod_from_x = pcp_x
        lod_from_y = pcp_y - 70
        lod_to_x = pcp_x
        lod_to_y = pcp_y + 65
        vector_angle_label = "90° Axial Longitudinal Caudal (-Y)"
        vector_text = "LOD: Tracción Axial Caudal"
        arrow_color = "#f59e0b"
    elif "anterior" in clave or "anterior" in titulo_diag:
        # AS Gonstead: ASIS / crest contact
        pcp_x = cx - 110
        pcp_y = 175
        lod_from_x = pcp_x - 85
        lod_from_y = pcp_y - 50
        lod_to_x = pcp_x + 35
        lod_to_y = pcp_y + 25
        vector_angle_label = "Anterior a Posterior (A-P)"
        vector_text = "LOD: A-P hacia Posterior sobre Cresta"
        arrow_color = "#38bdf8"
    elif "torsion" in clave or "torsion" in titulo_diag:
        # Sacral Torsion
        pcp_x = cx + 85
        pcp_y = 290
        lod_from_x = pcp_x + 70
        lod_from_y = pcp_y - 40
        lod_to_x = pcp_x - 35
        lod_to_y = pcp_y + 15
        vector_angle_label = "P-A y L-M Rotacional"
        vector_text = "LOD: P-A y Lateral a Medial"
        arrow_color = "#a855f7"

    # Sanitizar textos
    titulo_sanitizado = diagnostico.titulo.replace('"', '&quot;')
    subtitulo_sanitizado = diagnostico.subtitulo.replace('"', '&quot;')

    html = f"""
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
                justify-content: flex-start;
                padding: 10px;
                overflow: hidden;
            }}
            .module-container {{
                background: radial-gradient(circle at 35% 50%, #1e293b 0%, #090e17 100%);
                border: 1px solid #334155;
                border-radius: 12px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                width: 100%;
                max-width: 980px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .header-bar {{
                width: 100%;
                padding: 10px 16px;
                background: #1e293b;
                border-bottom: 1px solid #334155;
                display: flex;
                flex-wrap: wrap;
                justify-content: space-between;
                align-items: center;
                gap: 8px;
                border-radius: 12px 12px 0 0;
            }}
            .header-title {{
                font-size: 12px;
                font-weight: 700;
                color: #38bdf8;
                display: flex;
                align-items: center;
                gap: 6px;
            }}
            .badge-action {{
                padding: 3px 8px;
                border-radius: 9999px;
                font-size: 10px;
                font-weight: 600;
                background: #0284c7;
                color: #ffffff;
                box-shadow: 0 0 8px rgba(2, 132, 199, 0.4);
            }}
            .btn-thrust {{
                background: linear-gradient(135deg, #059669 0%, #10b981 100%);
                color: #ffffff;
                border: 1px solid #34d399;
                padding: 5px 12px;
                border-radius: 6px;
                font-size: 11px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.2s ease;
                display: inline-flex;
                align-items: center;
                gap: 5px;
            }}
            .btn-thrust:hover {{
                background: linear-gradient(135deg, #10b981 0%, #34d399 100%);
                box-shadow: 0 0 12px rgba(16, 185, 129, 0.5);
            }}
            .canvas-area {{
                position: relative;
                width: 100%;
                height: 450px;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            svg.vector-svg {{
                width: 100%;
                height: 100%;
                max-height: 450px;
            }}
            /* Animación de pulso PCP */
            .pulse-ring-anim {{
                animation: pulseRingKey 2s cubic-bezier(0.215, 0.61, 0.355, 1) infinite;
                transform-origin: center;
            }}
            .pulse-core-anim {{
                animation: pulseCoreKey 2s ease-in-out infinite;
                transform-origin: center;
            }}
            @keyframes pulseRingKey {{
                0% {{ r: 8px; opacity: 0.9; }}
                50% {{ opacity: 0.5; }}
                100% {{ r: 28px; opacity: 0; }}
            }}
            @keyframes pulseCoreKey {{
                0%, 100% {{ r: 6px; }}
                50% {{ r: 8.5px; }}
            }}
            /* Animación del vector de empuje al pulsar simular */
            .thrust-active {{
                animation: thrustImpulse 0.4s ease-out;
            }}
            @keyframes thrustImpulse {{
                0% {{ transform: translate(0, 0); }}
                50% {{ transform: translate(-8px, 6px); filter: drop-shadow(0 0 18px #34d399); }}
                100% {{ transform: translate(0, 0); }}
            }}
            /* Glassmorphism HUD */
            .glass-hud {{
                position: absolute;
                top: 18px;
                right: 20px;
                width: 370px;
                background: rgba(15, 23, 42, 0.88);
                backdrop-filter: blur(14px);
                border: 1px solid rgba(56, 189, 248, 0.35);
                border-radius: 12px;
                padding: 16px;
                box-shadow: 0 12px 30px rgba(0, 0, 0, 0.55);
                display: flex;
                flex-direction: column;
                gap: 10px;
                pointer-events: auto;
            }}
            .hud-header {{
                border-bottom: 1px solid rgba(51, 65, 85, 0.8);
                padding-bottom: 8px;
            }}
            .hud-title {{
                font-size: 11px;
                font-weight: 700;
                color: #38bdf8;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }}
            .hud-diag {{
                font-size: 13px;
                font-weight: 700;
                color: #f8fafc;
                margin-top: 2px;
            }}
            .hud-grid {{
                display: grid;
                grid-template-columns: 1fr;
                gap: 7px;
                font-size: 11px;
            }}
            .hud-row {{
                display: flex;
                flex-direction: column;
                background: rgba(30, 41, 59, 0.5);
                padding: 5px 8px;
                border-radius: 6px;
                border-left: 2px solid #38bdf8;
            }}
            .hud-label {{
                font-size: 9px;
                font-weight: 700;
                color: #94a3b8;
                text-transform: uppercase;
            }}
            .hud-val {{
                color: #f1f5f9;
                font-weight: 500;
                margin-top: 2px;
                line-height: 1.25;
            }}
            .hud-warning {{
                background: rgba(127, 29, 29, 0.25);
                border-left: 2px solid #ef4444;
                padding: 6px 8px;
                border-radius: 6px;
                font-size: 10px;
                color: #fca5a5;
                line-height: 1.3;
            }}
            .footer-strip {{
                width: 100%;
                padding: 8px 16px;
                background: #111827;
                border-top: 1px solid #1f2937;
                display: flex;
                justify-content: space-between;
                align-items: center;
                font-size: 11px;
                color: #94a3b8;
                border-radius: 0 0 12px 12px;
            }}
        </style>
    </head>
    <body>
        <div class="module-container">
            <div class="header-bar">
                <div class="header-title">
                    <span>🔵 MÓDULO B: DIAGRAMA VECTORIAL DE AJUSTE Y PUNTOS DE CONTACTO</span>
                    <span style="color:#64748b;">| Lado: <strong style="color:#ffffff;">{lado}</strong></span>
                </div>
                <div style="display:flex; align-items:center; gap:8px;">
                    <span class="badge-action">POST-EVALUACIÓN</span>
                    <button class="btn-thrust" onclick="triggerThrustImpulse()">⚡ Simular Impulso HVLA</button>
                </div>
            </div>

            <div class="canvas-area">
                <svg id="vectorSvg" class="vector-svg" viewBox="0 0 940 480" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <!-- Gradiente Vector LOD -->
                        <linearGradient id="vectorGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                            <stop offset="0%" stop-color="#10b981" />
                            <stop offset="50%" stop-color="#38bdf8" />
                            <stop offset="100%" stop-color="#6366f1" />
                        </linearGradient>

                        <!-- Marcador de Flecha Vectorial -->
                        <marker id="arrowLOD" markerWidth="14" markerHeight="14" refX="10" refY="7" orient="auto">
                            <path d="M 0 1 L 12 7 L 0 13 L 3 7 Z" fill="{arrow_color}" />
                        </marker>

                        <filter id="vectorGlow" x="-50%" y="-50%" width="200%" height="200%">
                            <feGaussianBlur in="SourceGraphic" stdDeviation="4" result="blur" />
                            <feMerge>
                                <feMergeNode in="blur" />
                                <feMergeNode in="SourceGraphic" />
                            </feMerge>
                        </filter>
                    </defs>

                    <!-- ESQUEMA ANATÓMICO FOCALIZADO DEL COXAL Y SACRO IPSILATERAL -->
                    <g id="anatomicalTargetGroup" opacity="0.85">
                        <!-- Sacro homolateral -->
                        <path d="M 370 120 Q 405 112 430 118 L 415 250 Q 395 300 375 340 L 360 320 Z"
                              fill="#78350f" stroke="#f59e0b" stroke-width="1.8" />
                        
                        <!-- Eje S3 Transverso Sacro (Línea de Referencia) -->
                        <line x1="310" y1="235" x2="450" y2="235" stroke="#38bdf8" stroke-width="1.2" stroke-dasharray="4 3" opacity="0.7" />
                        <text x="455" y="239" font-size="9.5" fill="#38bdf8" font-weight="600">Eje S3 Transverso</text>

                        <!-- Contorno Hemipelvis Enfocada -->
                        <path d="M 368 122
                                 C 350 100 310 70 210 68
                                 C 145 68 95 110 110 165
                                 C 120 195 140 220 150 245
                                 C 162 270 175 290 185 315
                                 C 155 330 115 345 98 358
                                 C 92 364 95 380 105 385
                                 C 125 385 155 365 188 348
                                 C 200 380 220 445 250 468
                                 C 290 480 335 445 375 420
                                 L 400 415 L 400 395
                                 C 345 365 305 315 288 270
                                 C 270 215 335 160 368 122 Z"
                              fill="#1e293b" stroke="#38bdf8" stroke-width="2.5" />

                        <!-- Cavidad Acetabular -->
                        <circle cx="190" cy="320" r="25" fill="#090e17" stroke="#38bdf8" stroke-width="1.8" />
                        <circle cx="190" cy="320" r="16" fill="#0284c7" opacity="0.3" />

                        <!-- Articulación SI en Foco -->
                        <path d="M 368 124 Q 380 190 382 250" stroke="#34d399" stroke-width="3.5" stroke-dasharray="5 3" fill="none" />
                        <text x="390" y="195" font-size="9.5" font-weight="600" fill="#34d399">Art. Sacroilíaca</text>
                    </g>

                    <!-- VECTOR DE FUERZA DIRECCIONAL (LINE OF DRIVE - LOD) -->
                    <g id="lodVectorGroup">
                        <!-- Línea Guía de Trayectoria Vectorial -->
                        <line x1="{lod_from_x + (lod_from_x - lod_to_x)*0.3}" y1="{lod_from_y + (lod_from_y - lod_to_y)*0.3}"
                              x2="{lod_to_x}" y2="{lod_to_y}"
                              stroke="#64748b" stroke-width="1" stroke-dasharray="3 3" opacity="0.5" />

                        <!-- Flecha Principal de Conducción con Gradiente -->
                        <line id="vectorArrowLine" x1="{lod_from_x}" y1="{lod_from_y}" x2="{lod_to_x}" y2="{lod_to_y}"
                              stroke="{arrow_color}" stroke-width="5" stroke-linecap="round"
                              marker-end="url(#arrowLOD)" filter="url(#vectorGlow)" />

                        <!-- Etiqueta Flotante sobre el Vector -->
                        <rect x="{(lod_from_x + lod_to_x)/2 - 95}" y="{(lod_from_y + lod_to_y)/2 - 28}"
                              width="190" height="22" rx="5" fill="rgba(15, 23, 42, 0.9)" stroke="{arrow_color}" stroke-width="1" />
                        <text x="{(lod_from_x + lod_to_x)/2}" y="{(lod_from_y + lod_to_y)/2 - 13}"
                              text-anchor="middle" font-size="10" font-weight="700" fill="#f8fafc">
                            {vector_text}
                        </text>

                        <!-- Indicador de Ángulo -->
                        <text x="{(lod_from_x + lod_to_x)/2}" y="{(lod_from_y + lod_to_y)/2 + 8}"
                              text-anchor="middle" font-size="8.5" font-weight="600" fill="#94a3b8">
                            Ángulo: {vector_angle_label}
                        </text>
                    </g>

                    <!-- PUNTO DE CONTACTO DEL PACIENTE (PCP) ANIMADO -->
                    <g id="pcpMarkerGroup">
                        <!-- Anillo de Pulso Expansivo -->
                        <circle cx="{pcp_x}" cy="{pcp_y}" r="8" class="pulse-ring-anim" stroke="{arrow_color}" stroke-width="2.5" fill="none" />
                        <circle cx="{pcp_x}" cy="{pcp_y}" r="16" class="pulse-ring-anim" stroke="{arrow_color}" stroke-width="1.5" fill="none" style="animation-delay: 0.8s;" />
                        
                        <!-- Núcleo Central de Contacto -->
                        <circle cx="{pcp_x}" cy="{pcp_y}" r="7" class="pulse-core-anim" fill="{arrow_color}" stroke="#ffffff" stroke-width="2" />
                        
                        <!-- Mirilla / Retícula Cruzada -->
                        <line x1="{pcp_x - 14}" y1="{pcp_y}" x2="{pcp_x + 14}" y2="{pcp_y}" stroke="#ffffff" stroke-width="1.2" opacity="0.85" />
                        <line x1="{pcp_x}" y1="{pcp_y - 14}" x2="{pcp_x}" y2="{pcp_y + 14}" stroke="#ffffff" stroke-width="1.2" opacity="0.85" />

                        <!-- Badge de Identificación PCP -->
                        <rect x="{pcp_x + 18}" y="{pcp_y - 12}" width="150" height="24" rx="4" fill="rgba(15, 23, 42, 0.92)" stroke="{arrow_color}" stroke-width="1" />
                        <text x="{pcp_x + 24}" y="{pcp_y + 4}" font-size="9.5" font-weight="700" fill="#ffffff">🎯 PCP: {pcp[:20]}</text>
                    </g>
                </svg>

                <!-- GLASSMORPHISM HUD (TARJETA TÉCNICA FLOTANTE) -->
                <div class="glass-hud">
                    <div class="hud-header">
                        <div class="hud-title">📋 ESPECIFICACIÓN DEL AJUSTE ARTICULAR</div>
                        <div class="hud-diag">{titulo_sanitizado}</div>
                    </div>

                    <div class="hud-grid">
                        <div class="hud-row">
                            <span class="hud-label">Técnica Recomendada</span>
                            <span class="hud-val">{tecnica}</span>
                        </div>

                        <div class="hud-row">
                            <span class="hud-label">🖐️ Punto de Contacto Clínico (PCC)</span>
                            <span class="hud-val">{pcc}</span>
                        </div>

                        <div class="hud-row">
                            <span class="hud-label">🎯 Punto de Contacto Paciente (PCP)</span>
                            <span class="hud-val" style="color: {arrow_color}; font-weight: 700;">{pcp}</span>
                        </div>

                        <div class="hud-row">
                            <span class="hud-label">↗️ Línea de Conducción (LOD) / Vector</span>
                            <span class="hud-val">{linea_correccion}</span>
                        </div>

                        <div class="hud-row">
                            <span class="hud-label">👤 Posición del Paciente</span>
                            <span class="hud-val">{posicion_paciente}</span>
                        </div>
                    </div>

                    <div class="hud-warning">
                        <strong>⚠️ Precaución Biomecánica:</strong> {advertencia}
                    </div>
                </div>
            </div>

            <div class="footer-strip">
                <div>
                    <span>Vector: <strong>{vector_angle_label}</strong></span>
                    <span style="margin: 0 8px; color: #475569;">|</span>
                    <span>Modo: <strong>HVLA al final del rango pasivo</strong></span>
                </div>
                <div style="font-size: 10px; color: #64748b;">
                    Protocolo Clínico Gonstead &amp; Biomecánica Sacroilíaca
                </div>
            </div>
        </div>

        <script>
            function triggerThrustImpulse() {{
                const group = document.getElementById('lodVectorGroup');
                group.classList.remove('thrust-active');
                void group.offsetWidth; // Trigger reflow
                group.classList.add('thrust-active');
            }}
        </script>
    </body>
    </html>
    """
    return html


def generar_componente_cinematica(
    lado: str,
    disfuncion_clave: str
) -> str:
    """Función de compatibilidad histórica que redirige a los nuevos módulos vectoriales."""
    from app import DiagnosticoBiomecanico
    diag_dummy = DiagnosticoBiomecanico(
        titulo=disfuncion_clave,
        subtitulo="Simulación Cinemática Pelviana",
        clasificacion_tipo="Disfunción Pélvica",
        nivel_concordancia="Alta",
        justificacion_clinica=[],
        vector_ajuste="",
        tecnica_met="",
        inhibicion_miofascial=[],
        clave_conocimiento="ILIACO_POSTERIOR" if "posterior" in disfuncion_clave.lower() else "ILIACO_ANTERIOR"
    )
    return generar_diagrama_vectorial_ajuste(lado=lado, diagnostico=diag_dummy)


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
        "•": "\u00b7", "·": "\u00b7", "≥": ">=", "≤": "<="
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
        self.rect(0, 0, 210, 5, "F")
        
        # Título del informe
        self.set_y(7)
        self.set_font("Helvetica", "B", 12)
        self.set_text_color(15, 23, 42)
        self.cell(0, 5, "INFORME DE EVALUACIÓN BIOMECÁNICA PÉLVICA", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        self.set_font("Helvetica", "", 8)
        self.set_text_color(100, 116, 139)
        self.cell(0, 3.5, "SERVICIO DE BIOMECÁNICA CLÍNICA Y CRITERIOS QUIROPRÁCTICOS - BIOPELVIS PRO", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(148, 163, 184)
        self.line(15, 285, 195, 285)
        self.cell(0, 6, f"Paciente: {sanitizar_para_pdf(self.paciente_id)} | Página {self.page_no()} de {{nb}} | Documento Clínico Confidencial", align="C")


def generar_reporte_pdf(
    paciente: DatosPaciente,
    banderas: BanderasRojas,
    cluster: ClusterLaslett,
    palpacion: ExamenPalpatorio,
    diag: DiagnosticoBiomecanico
) -> bytes:
    """
    Genera y compila el informe clínico formal en formato PDF utilizando fpdf2.
    Incluye las cuatro fases terapéuticas (Ajuste, MET, Miofascial y Ejercicio Activo).
    Retorna el contenido en bytes listo para descarga inmediata.
    """
    pdf = ReporteBiomecanicoPDF(paciente_id=paciente.identificador)
    pdf.set_margins(15, 11, 15)
    pdf.set_auto_page_break(auto=True, margin=13)
    pdf.add_page()

    now_str = datetime.now().strftime("%d/%m/%Y %H:%M hrs")
    sacrotuberoso_str = "TENSIÓN AUMENTADA IPSILATERAL (Positivo)" if palpacion.ligamento_sacrotuberoso_tenso else "Tensión fisiológica normal"
    interpretacion_laslett, detalle_laslett, _ = cluster.interpretacion

    # --------------------------------------------------------------------------
    # ENCABEZADO INSTITUCIONAL: DATOS DEL PACIENTE Y METADATOS
    # --------------------------------------------------------------------------
    box_y = pdf.get_y()
    box_w = 180
    box_h = 19.5
    pdf.set_fill_color(248, 250, 252)
    pdf.set_draw_color(203, 213, 225)
    pdf.rect(15, box_y, box_w, box_h, "FD")

    # Columna Izquierda (x=17, w=86)
    pdf.set_xy(17, box_y + 1.6)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(86, 3.6, sanitizar_para_pdf(f"PACIENTE / FICHA: {paciente.identificador.upper()}"))

    pdf.set_xy(17, box_y + 5.6)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(86, 3.4, sanitizar_para_pdf(f"Edad: {paciente.edad} años | Sexo: {paciente.sexo} | Lateralidad: {paciente.lateralidad}"))

    pdf.set_xy(17, box_y + 9.4)
    pdf.cell(86, 3.4, sanitizar_para_pdf(f"Ocupación/Deporte: {paciente.ocupacion_deporte}"))

    pdf.set_xy(17, box_y + 13.2)
    pdf.cell(86, 3.4, sanitizar_para_pdf(f"Tiempo de Evolución: {paciente.tiempo_evolucion.value}"))

    # Columna Derecha (x=105, w=86 - margen derecho restringido a 191mm < 195mm)
    pdf.set_xy(105, box_y + 1.6)
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(86, 3.6, sanitizar_para_pdf(f"FECHA DE EMISIÓN: {now_str}"))

    pdf.set_xy(105, box_y + 5.6)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.set_text_color(51, 65, 85)
    txt_mecanismo = sanitizar_para_pdf(f"Mecanismo de Inicio: {paciente.mecanismo_inicio.value}")
    pdf.multi_cell(86, 3.4, txt_mecanismo)

    pdf.set_y(box_y + box_h + 2.5)

    # --------------------------------------------------------------------------
    # SECCIÓN 1: SEGURIDAD (BANDERAS ROJAS) Y CLÚSTER DE LASLETT
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(180, 5, " 1. SEGURIDAD Y BATERÍA DE PROVOCACIÓN ARTICULAR (LASLETT)", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)

    # Banner de Banderas Rojas
    if banderas.hay_bandera_roja:
        pdf.set_fill_color(254, 226, 226)
        pdf.set_draw_color(239, 68, 68)
        pdf.set_text_color(185, 28, 28)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.rect(15, pdf.get_y(), 180, 9, "FD")
        pdf.set_y(pdf.get_y() + 1.2)
        pdf.cell(180, 3.4, sanitizar_para_pdf(" [ALERTA CRÍTICA] Banderas rojas identificadas. MANIPULACIÓN HVLA CONTRAINDICADA."), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_font("Helvetica", "", 7)
        for al in banderas.obtener_alertas_activas():
            pdf.cell(180, 3.0, sanitizar_para_pdf(f"   * {al}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2.5)
    else:
        pdf.set_fill_color(220, 252, 231)
        pdf.set_draw_color(34, 197, 94)
        pdf.set_text_color(21, 128, 61)
        pdf.set_font("Helvetica", "B", 7.5)
        pdf.rect(15, pdf.get_y(), 180, 5, "FD")
        pdf.set_y(pdf.get_y() + 0.8)
        pdf.cell(180, 3.4, sanitizar_para_pdf(" [SEGURO] Criterios de exclusión negativos. Tratamiento biomecánico manual habilitado."), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(2.5)

    # Tabla de Pruebas de Provocación Articular
    pruebas_laslett = [
        ("Test de Distracción Anterior (Gapping test)", "POSITIVO" if cluster.distraccion else "Negativo"),
        ("Test de Compresión Ilíaca (Compression test)", "POSITIVO" if cluster.compresion else "Negativo"),
        ("Test de Thigh Thrust (Empuje Femoral / Cizallamiento posterior)", "POSITIVO" if cluster.thigh_thrust else "Negativo"),
        ("Test de FABER / Patrick (Flexión, Abducción, Rotación Externa)", "POSITIVO" if cluster.faber else "Negativo"),
        ("Test de Gaenslen (Torsión pelviana dinámica)", "POSITIVO" if cluster.gaenslen else "Negativo")
    ]

    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(15, 23, 42)
    pdf.set_draw_color(226, 232, 240)

    for desc, res in pruebas_laslett:
        pdf.cell(130, 3.4, sanitizar_para_pdf(f"  - {desc}"), border="B", new_x=XPos.RIGHT, new_y=YPos.TOP)
        if res == "POSITIVO":
            pdf.set_font("Helvetica", "B", 7)
            pdf.set_text_color(185, 28, 28)
        else:
            pdf.set_font("Helvetica", "", 7)
            pdf.set_text_color(100, 116, 139)
        pdf.cell(50, 3.4, sanitizar_para_pdf(res), border="B", align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.set_text_color(15, 23, 42)
        pdf.set_font("Helvetica", "", 7)

    pdf.ln(1.5)
    pdf.set_fill_color(241, 245, 249)
    pdf.rect(15, pdf.get_y(), 180, 5, "F")
    pdf.set_y(pdf.get_y() + 0.8)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.cell(90, 3.4, sanitizar_para_pdf(f" Total Pruebas Positivas: {cluster.total_positivos} / 5"), new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 3.4, sanitizar_para_pdf(f"Nivel: {interpretacion_laslett}"), align="R", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(3)

    # --------------------------------------------------------------------------
    # SECCIÓN 2: PROTOCOLO PALPATORIO DETALLADO (CUADRÍCULA SIMÉTRICA 50% / 50%)
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(180, 4.5, " 2. PROTOCOLO PALPATORIO Y DINÁMICA ARTICULAR", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)

    col1_items = [
        ("Lado de Restricción", palpacion.lado_restriccion.value),
        ("Cresta Ilíaca", palpacion.cresta_iliaca.value),
        ("Tuberosidad Isquiática", palpacion.tuberosidad_isquiatica.value),
        ("Espina Ilíaca Ántero-Sup (EIAS)", palpacion.eias.value),
        ("Espina Ilíaca Póstero-Sup (EIPS)", palpacion.eips.value),
        ("Sínfisis Púbica", palpacion.escalon_pubis.value)
    ]
    # Abreviación concisa de tests dinámicos para evitar saltos innecesarios
    long_sitting_str = palpacion.long_sitting.value
    if "alarga" in long_sitting_str:
        long_sitting_disp = "Corta en supino se alarga al sentarse"
    elif "acorta" in long_sitting_str:
        long_sitting_disp = "Larga en supino se acorta al sentarse"
    elif "mantiene" in long_sitting_str:
        long_sitting_disp = "Pierna corta se mantiene corta"
    else:
        long_sitting_disp = "Neutro / Sin cambio evidente"

    sacrotuberoso_disp = "Tensión aumentada ipsilateral (+)" if palpacion.ligamento_sacrotuberoso_tenso else "Tensión normal fisiológica"

    col1_items = [
        ("Lado de Restricción", palpacion.lado_restriccion.value),
        ("Cresta Ilíaca", palpacion.cresta_iliaca.value),
        ("Tuberosidad Isquiática", palpacion.tuberosidad_isquiatica.value),
        ("Espina Ilíaca Ántero-Sup (EIAS)", palpacion.eias.value),
        ("Espina Ilíaca Póstero-Sup (EIPS)", palpacion.eips.value),
        ("Sínfisis Púbica", palpacion.escalon_pubis.value)
    ]
    col2_items = [
        ("Maléolo Medial (Supino)", palpacion.maleolo_supino.value),
        ("Long-Sitting Test", long_sitting_disp),
        ("Surco Sacro Homolateral", palpacion.surco_sacro.value),
        ("Ángulo Inferolateral (AIL)", palpacion.ail.value),
        ("Músculo Piramidal", palpacion.piramidal.value),
        ("Ligamento Sacrotuberoso", sacrotuberoso_disp)
    ]

    y_curr = pdf.get_y()
    col1_w = 86
    col2_w = 90
    gap = 4
    pad_v = 1.0  # padding-top y padding-bottom de 1mm (~4px)
    line_h = 3.4

    pdf.set_draw_color(226, 232, 240)
    pdf.set_text_color(26, 26, 26)  # Color oscuro explícito (#1a1a1a) para visibilidad total

    for i in range(len(col1_items)):
        y_top = y_curr + pad_v
        pdf.set_font("Helvetica", size=7.2)
        pdf.set_text_color(26, 26, 26)

        # Columna Izquierda: Hito óseo -> Valor (ancho: 86mm, x=15)
        pdf.set_xy(15, y_top)
        txt_l = sanitizar_para_pdf(f"**{col1_items[i][0]}:**  {col1_items[i][1]}")
        pdf.multi_cell(col1_w, line_h, txt_l, markdown=True)
        y_left = pdf.get_y()

        # Columna Derecha: Test/Hallazgo dinámico -> Valor (ancho ampliado: 90mm, x=105)
        pdf.set_xy(15 + col1_w + gap, y_top)
        txt_r = sanitizar_para_pdf(f"**{col2_items[i][0]}:**  {col2_items[i][1]}")
        pdf.multi_cell(col2_w, line_h, txt_r, markdown=True)
        y_right = pdf.get_y()

        # Altura dinámica automática: la fila se expande según la celda más alta + padding
        row_bottom = max(y_left, y_right) + pad_v
        pdf.line(15, row_bottom, 195, row_bottom)
        y_curr = row_bottom

    pdf.set_y(y_curr + 3)

    # --------------------------------------------------------------------------
    # SECCIÓN 3: JUICIO BIOMECÁNICO Y PRESCRIPCIÓN TERAPÉUTICA
    # --------------------------------------------------------------------------
    pdf.set_fill_color(30, 41, 59)
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 8)
    pdf.cell(180, 4.5, " 3. JUICIO BIOMECÁNICO Y PRESCRIPCIÓN TERAPÉUTICA", fill=True, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)

    # Caja de Diagnóstico Principal
    pdf.set_fill_color(241, 245, 249)
    pdf.set_draw_color(2, 132, 199)
    diag_y = pdf.get_y()
    pdf.rect(15, diag_y, 180, 12, "FD")
    pdf.set_y(diag_y + 0.8)
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(2, 132, 199)
    pdf.cell(180, 3.5, sanitizar_para_pdf(f"  DIAGNÓSTICO: {diag.titulo}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "I", 7)
    pdf.set_text_color(51, 65, 85)
    pdf.cell(180, 3.0, sanitizar_para_pdf(f"  Subtipo: {diag.subtitulo}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(180, 3.0, sanitizar_para_pdf(f"  Categoría: {diag.clasificacion_tipo} | Concordancia: {diag.nivel_concordancia.split('(')[0].strip()}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(2)

    # Criterios y Justificación Clínica
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(180, 3.4, "Criterios y Correlaciones Clínicas Identificadas:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7)
    for just in diag.justificacion_clinica:
        pdf.cell(180, 3.0, sanitizar_para_pdf(f"  \u00b7 {just}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(1.5)

    # Prescripción y Plan Terapéutico (Interlineado y respiración visual)
    pdf.set_font("Helvetica", "B", 7.5)
    pdf.set_text_color(15, 23, 42)
    pdf.cell(180, 3.4, "Plan Terapéutico y Prescripción Biomecánica Integral:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    # 1. Ajuste Articular Biomecánico
    pdf.set_font("Helvetica", "B", 7.2)
    pdf.cell(180, 3.0, "  1. Ajuste Articular Biomecánico (Vector y Posicionamiento):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(f"     {diag.vector_ajuste}"))
    pdf.ln(1)

    # 2. Técnica de Energía Muscular (MET)
    pdf.set_font("Helvetica", "B", 7.2)
    pdf.cell(180, 3.0, "  2. Técnica de Energía Muscular (MET - Fred Mitchell Sr.):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(f"     {diag.tecnica_met}"))
    pdf.ln(1)

    # 3. Inhibición Miofascial
    pdf.set_font("Helvetica", "B", 7.2)
    pdf.cell(180, 3.0, "  3. Protocolo de Inhibición Miofascial de Cadenas Acortadas:", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 7.2)
    texto_mio = ", ".join(diag.inhibicion_miofascial)
    pdf.multi_cell(180, 3.4, sanitizar_para_pdf(f"     {texto_mio}"))
    pdf.ln(1)

    # 4. Ejercicio Terapéutico y Control Sensorio-Motor (Fase Activa - Bloque fluido en una sola línea)
    pdf.set_font("Helvetica", "B", 7.2)
    pdf.cell(180, 3.0, "  4. Ejercicio Terapéutico y Control Sensorio-Motor (Fase Activa):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    if diag.ejercicio_terapeutico:
        for sub_ej, desc_ej in diag.ejercicio_terapeutico.items():
            pdf.set_font("Helvetica", "", 7.2)
            texto_ej = sanitizar_para_pdf(f"     \u00b7 **{sub_ej.strip()}:** {desc_ej.strip()}")
            pdf.multi_cell(180, 3.4, texto_ej, markdown=True)
            pdf.ln(0.6)

    # Margen de separación limpio previo a firmas (margin-top: 12px ~ 6mm)
    pdf.ln(6)

    # --------------------------------------------------------------------------
    # SECCIÓN DE FIRMA PROFESIONAL
    # --------------------------------------------------------------------------
    pdf.set_draw_color(148, 163, 184)
    y_sig = pdf.get_y() + 4
    pdf.line(25, y_sig, 85, y_sig)
    pdf.line(125, y_sig, 185, y_sig)
    pdf.set_y(y_sig + 1.8)
    pdf.set_font("Helvetica", "", 7.2)
    pdf.set_text_color(71, 85, 105)
    pdf.cell(90, 3.5, "Firma del Profesional Evaluador", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(90, 3.5, "N° de Registro / Colegiatura", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    return bytes(pdf.output())


# ==============================================================================
# ENCABEZADO Y HEADER CLÍNICO DE STREAMLIT
# ==============================================================================

col_hdr_main, col_hdr_user = st.columns([3.3, 1.7])
with col_hdr_main:
    st.markdown("""
    <div class="clinical-header" style="margin-bottom:12px; padding:18px 24px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:16px;">
            <div>
                <h1 style="margin:0; font-size:1.65rem; font-weight:700; letter-spacing:-0.02em;">
                    ⚖️ BioPelvis Pro | Suite de Diagnóstico Sacroilíaco y Pelviano
                </h1>
                <p style="margin:4px 0 0 0; color:#94a3b8; font-size:0.90rem;">
                    Inferencia Biomecánica Sagital y Vertical (Downslip/Upslip), Gonstead PI, Clúster de Laslett y Reportes Clínicos en PDF
                </p>
            </div>
            <div>
                <span class="badge badge-info" style="font-size:0.75rem; padding:5px 12px;">
                    v2.2 • PDF MÉDICO
                </span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
with col_hdr_user:
    st.markdown("<div style='height:12px;'></div>", unsafe_allow_html=True)
    render_user_badge()


# ==============================================================================
# MENÚ DE NAVEGACIÓN PRINCIPAL DEL SISTEMA (PERSISTENCIA ESTRICTA CON URL)
# ==============================================================================

OPCIONES_MENU_PRINCIPAL = [
    "1. 📋 Anamnesis y Banderas Rojas",
    "2. 🔍 Provocación y Palpación",
    "3. 🦴 Visualización y Cinemática",
    "4. ⚖️ Juicio Clínico y Exportación"
]

# 1. Al inicio de la app, lee el parámetro st.query_params.get("tab") o "modulo"
tab_url = st.query_params.get("tab") or st.query_params.get("modulo") or ""

# 2. Si ese parámetro existe en la URL y coincide con alguna de las opciones del menú de navegación,
# calcula su índice dinámicamente (index = opciones.index(tab_url)) para pasárselo al st.radio o selector principal.
# Si no existe, usa 0.
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
else:
    index = 0

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

# ==============================================================================
# ESTADO CLÍNICO GLOBAL PERSISTENTE (ACCESIBLE EN TODAS LAS PÁGINAS)
# ==============================================================================
if "paciente_inst" not in st.session_state:
    st.session_state["paciente_inst"] = DatosPaciente(
        identificador="PAC-2026-001",
        edad=38,
        sexo="Masculino",
        lateralidad="Diestro",
        ocupacion_deporte="Trabajo de oficina (sedente 8h) / Corredor aficionado",
        tiempo_evolucion=TiempoEvolucion.SUBAGUDO,
        mecanismo_inicio=MecanismoInicio.INSIDIOSO
    )

if "banderas_rojas_inst" not in st.session_state:
    st.session_state["banderas_rojas_inst"] = BanderasRojas(
        dolor_nocturno=False,
        compromiso_esfinteres=False,
        sintomas_constitucionales=False,
        rigidez_axial_juvenil=False
    )

if "cluster_inst" not in st.session_state:
    st.session_state["cluster_inst"] = ClusterLaslett(
        distraccion=True,
        compresion=True,
        thigh_thrust=True,
        faber=False,
        gaenslen=False
    )

if "palpacion_inst" not in st.session_state:
    st.session_state["palpacion_inst"] = ExamenPalpatorio(
        lado_restriccion=LadoRestriccion.DERECHO,
        cresta_iliaca=PosicionNivel.NIVELADA,
        tuberosidad_isquiatica=PosicionNivel.NIVELADA,
        eias=HitoOseoPosicion.ALTA,
        eips=HitoOseoPosicion.BAJA,
        escalon_pubis=EscalonPubico.NEUTRO,
        maleolo_supino=MaleoloSupino.CORTO,
        long_sitting=LongSittingTest.CORTO_A_LARGO,
        surco_sacro=SurcoSacro.NEUTRO,
        ail=AnguloInferolateral.SIMETRICO,
        piramidal=EstadoTejidoBlando.NORMOTONICO,
        ligamento_sacrotuberoso_tenso=True,
        diametro_transverso="Neutro / Simétrico",
        es_torsion_sacra=False,
        spring_test_positivo=True
    )

if "diagnostico_actual" not in st.session_state:
    st.session_state["diagnostico_actual"] = inferir_diagnostico(
        palpacion=st.session_state["palpacion_inst"],
        banderas_rojas=st.session_state["banderas_rojas_inst"],
        cluster=st.session_state["cluster_inst"]
    )

paciente_inst = st.session_state["paciente_inst"]
banderas_rojas_inst = st.session_state["banderas_rojas_inst"]
cluster_inst = st.session_state["cluster_inst"]
interpretacion_laslett, detalle_laslett, badge_laslett = cluster_inst.interpretacion
palpacion_inst = st.session_state["palpacion_inst"]
diagnostico_actual = st.session_state["diagnostico_actual"]


# ------------------------------------------------------------------------------
# PÁGINA 1: ANAMNESIS Y CRITERIOS DE EXCLUSIÓN (RED FLAGS)
# ------------------------------------------------------------------------------
if nav_activa == OPCIONES_MENU_PRINCIPAL[0]:
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
    st.session_state["paciente_inst"] = paciente_inst
    st.session_state["banderas_rojas_inst"] = banderas_rojas_inst
    st.session_state["diagnostico_actual"] = inferir_diagnostico(
        palpacion=st.session_state["palpacion_inst"],
        banderas_rojas=banderas_rojas_inst,
        cluster=st.session_state["cluster_inst"]
    )
    diagnostico_actual = st.session_state["diagnostico_actual"]


# ------------------------------------------------------------------------------
# PÁGINA 2: EXPLORACIÓN FÍSICA Y CLÚSTER DE PROVOCACIÓN
# ------------------------------------------------------------------------------
elif nav_activa == OPCIONES_MENU_PRINCIPAL[1]:
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

        diametro_transverso_sel = st.selectbox(
            "Diámetro Transverso / Flare Ilíaco:",
            options=[
                "Neutro / Simétrico",
                "Inflare: EIAS medializada / EIPS lateralizada",
                "Outflare: EIAS lateralizada / EIPS medializada"
            ],
            index=0,
            help="Evalúa la rotación del hueso coxal en el plano transverso horizontal."
        )

    with col_pal3:
        st.markdown("##### 🧬 Sacro y Cadenas Miofasciales")
        surco_sacro_sel = st.selectbox(
            f"Surco Sacro / Sulcus ({lado_restriccion_sel.value}):",
            options=[
                SurcoSacro.NEUTRO,
                SurcoSacro.PROFUNDO,
                SurcoSacro.SUPERFICIAL,
            ],
            format_func=lambda x: x.value,
            index=0
        )
        ail_sel = st.selectbox(
            f"Ángulo Inferolateral - AIL / ILA ({lado_restriccion_sel.value}):",
            options=[
                AnguloInferolateral.SIMETRICO,
                AnguloInferolateral.SUPERFICIAL,
                AnguloInferolateral.PROFUNDO,
                AnguloInferolateral.MAS_BAJO,
                AnguloInferolateral.MAS_CRANEAL,
            ],
            format_func=lambda x: x.value,
            index=0
        )
        piramidal_sel = st.selectbox(
            f"Tono Músculo Piramidal ({lado_restriccion_sel.value}):",
            options=[
                EstadoTejidoBlando.NORMOTONICO,
                EstadoTejidoBlando.HIPERTONICO,
            ],
            format_func=lambda x: x.value,
            index=0
        )
        sacrotuberoso_tenso_check = st.checkbox(
            "⚡ Tensión aumentada ipsilateral en Ligamento Sacrotuberoso",
            value=True,
            help="Signo cardinal de tracción caudal o rotación posterior del isquion."
        )
        spring_test_check = st.checkbox(
            "Spring Test Positivo (Elasticidad lumbosacra presente)",
            value=True,
            help="Desmarcar si hay rigidez franca lumbosacra / hipomovilidad en extensión."
        )

    es_torsion_eval = (surco_sacro_sel != SurcoSacro.NEUTRO or ail_sel != AnguloInferolateral.SIMETRICO)

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
        ligamento_sacrotuberoso_tenso=sacrotuberoso_tenso_check,
        diametro_transverso=diametro_transverso_sel,
        es_torsion_sacra=es_torsion_eval,
        spring_test_positivo=spring_test_check
    )
    st.session_state["cluster_inst"] = cluster_inst
    st.session_state["palpacion_inst"] = palpacion_inst
    st.session_state["diagnostico_actual"] = inferir_diagnostico(
        palpacion=palpacion_inst,
        banderas_rojas=st.session_state["banderas_rojas_inst"],
        cluster=cluster_inst
    )
    diagnostico_actual = st.session_state["diagnostico_actual"]


# ------------------------------------------------------------------------------
# PÁGINA 3: VISUALIZACIÓN DINÁMICA DE CINEMÁTICA PELVIANA
# ------------------------------------------------------------------------------
elif nav_activa == OPCIONES_MENU_PRINCIPAL[2]:
    st.markdown("### 🦴 Representación Visual Pélvica Interactiva y Vectorial")
    st.caption("Simulador anatómico dinámico pre-ajuste y cálculo vectorial de alta visibilidad para el protocolo quiropráctico post-evaluación.")

    OPCIONES_MODULO_VIS = [
        "🟢 Módulo A: Visor 3D Anatómico Interactivo 360° (Pre-Ajuste)",
        "🔵 Módulo B: Diagrama Vectorial de Ajuste y Puntos de Contacto (Post-Evaluación)",
        "🟣 Módulo C: Atlas Biomecánico Interactivo y Galería de Disfunciones 3D"
    ]
    MAPA_MODULOS = {
        # Módulo A
        "a": 0,
        "modulo_a": 0,
        "modulo-a": 0,
        "modulo a": 0,
        "0": 0,
        OPCIONES_MODULO_VIS[0].lower(): 0,
        # Módulo B
        "b": 1,
        "modulo_b": 1,
        "modulo-b": 1,
        "modulo b": 1,
        "1": 1,
        OPCIONES_MODULO_VIS[1].lower(): 1,
        # Módulo C
        "c": 2,
        "modulo_c": 2,
        "modulo-c": 2,
        "modulo c": 2,
        "atlas": 2,
        "2": 2,
        OPCIONES_MODULO_VIS[2].lower(): 2,
    }

    # 1. Leer st.query_params.get('tab') (con fallback a modulo)
    raw_tab = str(st.query_params.get("tab") or st.query_params.get("modulo") or "").strip().lower()

    # 2. Mapear ese valor de la URL al índice exacto del selector
    idx_encontrado = 0
    if raw_tab in MAPA_MODULOS:
        idx_encontrado = MAPA_MODULOS[raw_tab]
    elif "módulo c" in raw_tab or "modulo c" in raw_tab or "atlas" in raw_tab or "galería" in raw_tab:
        idx_encontrado = 2
    elif "módulo b" in raw_tab or "modulo b" in raw_tab or "vectorial" in raw_tab:
        idx_encontrado = 1
    elif "módulo a" in raw_tab or "modulo a" in raw_tab or "3d" in raw_tab:
        idx_encontrado = 0

    KEY_MODULO = "selector_modulo_cinematica"

    # 3. Inicializar st.session_state con esa opción si no existe o si la URL difiere
    if KEY_MODULO not in st.session_state:
        st.session_state[KEY_MODULO] = OPCIONES_MODULO_VIS[idx_encontrado]
    elif raw_tab in MAPA_MODULOS and st.session_state.get(KEY_MODULO) != OPCIONES_MODULO_VIS[idx_encontrado]:
        st.session_state[KEY_MODULO] = OPCIONES_MODULO_VIS[idx_encontrado]

    # 4. Callback on_change para actualizar st.query_params['tab'] y ['modulo'] de forma síncrona
    def _sync_modulo_tab():
        sel = st.session_state.get(KEY_MODULO, "")
        if "Módulo A" in sel:
            val = "a"
        elif "Módulo B" in sel:
            val = "b"
        elif "Módulo C" in sel:
            val = "c"
        else:
            val = "a"
        st.query_params["tab"] = val
        st.query_params["modulo"] = val

    # 5. Selector st.radio sincronizado
    sel_modulo_vis = st.radio(
        "Perspectiva de Visualización Biomecánica:",
        options=OPCIONES_MODULO_VIS,
        key=KEY_MODULO,
        horizontal=True,
        on_change=_sync_modulo_tab
    )

    if "Módulo A" in sel_modulo_vis:
        col_view_info, col_view_canvas = st.columns([1, 2.5])
        with col_view_info:
            st.markdown(f"""
            <div class="clinical-card" style="background:#f8fafc; border-left:4px solid #0284c7;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700;">ESTADO SINCRONIZADO PRE-AJUSTE</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0;">{diagnostico_actual.titulo}</div>
                <div style="font-size:0.82rem; color:#475569;">{diagnostico_actual.subtitulo}</div>
                <hr style="margin:10px 0; border:0; border-top:1px solid #cbd5e1;" />
                <div style="font-size:0.8rem; color:#334155;">
                    <strong>Semiología Palpatoria ({palpacion_inst.lado_restriccion.value}):</strong>
                    <ul style="padding-left:16px; margin-top:4px;">
                        <li><strong>Cresta Ilíaca:</strong> {palpacion_inst.cresta_iliaca.value}</li>
                        <li><strong>EIAS:</strong> {palpacion_inst.eias.value}</li>
                        <li><strong>EIPS:</strong> {palpacion_inst.eips.value}</li>
                        <li><strong>Isquion:</strong> {palpacion_inst.tuberosidad_isquiatica.value}</li>
                        <li><strong>Sínfisis Púbica:</strong> {palpacion_inst.escalon_pubis.value}</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🎮 Controles e Interacción 3D:")
            st.markdown("""
            - **🖱️ Orbitación 360°:** Arrastre con clic izquierdo para rotación esférica libre en 3 planos. Clic derecho para paneo y rueda para zoom.
            - **🎥 Cámaras Rápidas:** Acceda a vistas ortogonales (Anterior, Posterior, Sagital Lateral, Axial Superior) con transición suave.
            - **⚡ Cinemática Reactiva:** Alterne entre **Disfunción Actual** (rotación/cizallamiento real) y **Estado Neutro**.
            - **▶ Marcha Dinámica:** Simulación de contrarrotación pélvica cíclica en apoyo monopodal alterno.
            - **📂 Carga Personalizada GLB:** Arrastre o seleccione un archivo `.glb` pélvico segmentado (`sacro`, `iliaco_izquierdo`, `iliaco_derecho`).
            """)

        with col_view_canvas:
            sim_html = generar_visor_3d_pelvis(
                palpacion=palpacion_inst,
                diagnostico=diagnostico_actual,
                es_modo_atlas=False,
                altura_canvas=850
            )
            components.html(sim_html, height=850, scrolling=False)

    elif "Módulo B" in sel_modulo_vis:
        col_view_info, col_view_canvas = st.columns([1, 2.5])
        with col_view_info:
            lod_resumen = diagnostico_actual.vector_ajuste.split('|')[1].strip() if '|' in diagnostico_actual.vector_ajuste else 'Vector específico de corrección'
            st.markdown(f"""
            <div class="clinical-card" style="background:#f8fafc; border-left:4px solid #10b981;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700;">PRESCRIPCIÓN POST-EVALUACIÓN</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0;">{diagnostico_actual.titulo}</div>
                <div style="font-size:0.82rem; color:#475569;">{diagnostico_actual.clasificacion_tipo}</div>
                <hr style="margin:10px 0; border:0; border-top:1px solid #cbd5e1;" />
                <div style="font-size:0.8rem; color:#334155;">
                    <strong>Parámetros Clave de Ajuste:</strong>
                    <ul style="padding-left:16px; margin-top:4px;">
                        <li><strong>LOD:</strong> {lod_resumen}</li>
                        <li><strong>Modo:</strong> HVLA Palanca Corta</li>
                        <li><strong>Concordancia:</strong> {diagnostico_actual.nivel_concordancia.split('(')[0]}</li>
                    </ul>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("##### 🎯 Protocolo Vectorial:")
            st.markdown("""
            - **PCP Pulsante:** Marcador animado en el punto anatómico exacto de contacto.
            - **Flecha LOD:** Vector de fuerza direccional con gradiente y ángulo de corrección.
            - **HUD Flotante:** Parámetros técnicos del impulso (PCC, PCP, LOD, Precauciones).
            - **⚡ Simular Impulso:** Presione el botón en el visor para visualizar la dirección y amplitud del empuje.
            """)

        with col_view_canvas:
            vector_html = generar_diagrama_vectorial_ajuste(
                lado=palpacion_inst.lado_restriccion.value,
                diagnostico=diagnostico_actual,
                palpacion=palpacion_inst
            )
            components.html(vector_html, height=550, scrolling=False)

    else:
        # Módulo C: Atlas Biomecánico Interactivo y Galería de Disfunciones 3D
        st.markdown("#### 📚 Atlas Biomecánico Interactivo y Galería de Disfunciones 3D")
        st.caption("Estación clínica 3D interactiva en tiempo real. Seleccione categoría, disfunción específica y hemipelvis afectada. La pelvis 3D y la ficha didáctica inferior se actualizarán instantáneamente con los parámetros anatomo-patológicos y vectores de ajuste.")

        # 1. SELECTOR DEL MÓDULO C
        st.markdown("##### 🎛️ Selectores Biomecánicos de Simulación:")
        col_cat, col_disf, col_lado = st.columns([1.6, 2.2, 1.2])

        CATEGORIAS_ATLAS = {
            "Disfunciones Sagitales (Rotacionales)": [
                ("pi", "Ilíaco Posterior (PI / Retroversión)"),
                ("as", "Ilíaco Anterior (AS / Anteversión)"),
            ],
            "Disfunciones Verticales (Cizallamientos / Slips)": [
                ("up", "Ilíaco Ascendido (Upslip Craneal)"),
                ("down", "Ilíaco Descendido (Downslip Caudal)"),
            ],
            "Disfunciones Transversales (Flares)": [
                ("outflare", "Outflare (Rotación Externa / EX)"),
                ("inflare", "Inflare (Rotación Interna / IN)"),
            ],
            "Disfunciones Púbicas": [
                ("pubis_up", "Pubis Ascendido (Cizallamiento Superior)"),
                ("pubis_down", "Pubis Descendido (Cizallamiento Inferior)"),
            ],
            "Disfunciones Sacras": [
                ("sacro_flexion", "Sacro en Flexión Bilateral"),
                ("sacro_extension", "Sacro en Extensión Bilateral"),
                ("sacro_ai_d", "Sacro Antero-Inferior Derecho"),
                ("sacro_ps_i", "Sacro Postero-Superior Izquierdo"),
                ("sacro_flex_uni", "Sacro en Flexión Unilateral (Inclinado)"),
                ("sacro_ext_uni", "Sacro en Extensión Unilateral"),
                ("torsion_ant", "Torsión Sacra Anterior (Fisiológica R/R o L/L)"),
                ("torsion_post", "Torsión Sacra Posterior (No Fisiológica R/L o L/R)"),
            ]
        }

        with col_cat:
            cat_seleccionada = st.selectbox(
                "📂 Categoría:",
                options=list(CATEGORIAS_ATLAS.keys()),
                index=0,
                key="modulo_c_cat_sel"
            )

        opciones_disf = CATEGORIAS_ATLAS[cat_seleccionada]
        nombres_disf = [opt[1] for opt in opciones_disf]

        # Reset seguro de la disfunción si se cambia de categoría
        disf_index = 0
        if "modulo_c_disf_sel" in st.session_state and st.session_state.modulo_c_disf_sel in nombres_disf:
            disf_index = nombres_disf.index(st.session_state.modulo_c_disf_sel)
        elif "modulo_c_disf_sel" in st.session_state:
            st.session_state.modulo_c_disf_sel = nombres_disf[0]

        with col_disf:
            disf_nombre_sel = st.selectbox(
                "🎯 Disfunción Específica:",
                options=nombres_disf,
                index=disf_index,
                key="modulo_c_disf_sel"
            )

        preset_actual = next(opt[0] for opt in opciones_disf if opt[1] == disf_nombre_sel)

        with col_lado:
            lado_actual = st.radio(
                "🦵 Hemipelvis Afectada:",
                options=["Derecho", "Izquierdo"],
                index=0,
                horizontal=True,
                key="modulo_c_lado_sel"
            )

        # 2. VISOR 3D ANATÓMICO (Sin paneles superpuestos, 100% visibilidad pélvica)
        atlas_html = generar_visor_3d_pelvis(
            palpacion=palpacion_inst,
            diagnostico=diagnostico_actual,
            preset_inicial=preset_actual,
            lado_inicial=lado_actual,
            mostrar_ficha_didactica=False,
            es_modo_atlas=True,
            altura_canvas=850
        )
        components.html(atlas_html, height=850, scrolling=False)

        # 3. FICHA BIOMECÁNICA Y DIDÁCTICA REUBICADA FUERA DEL CANVAS 3D
        ck_key = PRESET_TO_CK_KEY.get(preset_actual, "SACRO_FLEXION")
        info_clinica = get_disfuncion_info(ck_key)
        meta_preset = ATLAS_PRESET_METADATA.get(preset_actual, {})
        crit = info_clinica.get("criterios_diagnosticos", {})
        ajuste = info_clinica.get("ajuste_articular", {})
        met = info_clinica.get("tecnica_met", {})
        miofascial = info_clinica.get("abordaje_miofascial", {})

        # Banner informativo de la ficha
        st.markdown(f"""
        <div class="clinical-card" style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); border-left: 5px solid #0284c7; padding: 18px 24px; margin-top: 18px; margin-bottom: 20px; color: #f8fafc; border-radius: 12px; box-shadow: 0 4px 14px rgba(0,0,0,0.2);">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:12px;">
                <div>
                    <span class="badge" style="background:#0284c7; color:#fff; font-weight:700; font-size:0.75rem; letter-spacing:0.05em; padding:3px 10px; border-radius:999px;">📋 FICHA BIOMECÁNICA DIDÁCTICA</span>
                    <h3 style="margin:6px 0 2px 0; color:#38bdf8; font-size:1.4rem; font-weight:700;">{info_clinica.get('nombre_clinico', disf_nombre_sel)} — Hemipelvis {lado_actual}</h3>
                    <div style="color:#94a3b8; font-size:0.86rem; margin-top:3px;">
                        <strong>🏷️ Listings:</strong> {meta_preset.get('listing', 'N/D')}
                    </div>
                </div>
                <div style="background:rgba(2, 132, 199, 0.15); border:1px solid rgba(56, 189, 248, 0.4); border-radius:8px; padding:10px 16px; text-align:right;">
                    <div style="font-size:0.72rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.05em;">Eje Articular / Clasificación</div>
                    <div style="font-size:0.95rem; font-weight:700; color:#38bdf8;">{info_clinica.get('eje_movimiento', 'Sacroilíaco')}</div>
                    <div style="font-size:0.8rem; color:#cbd5e1;">{info_clinica.get('categoria', cat_seleccionada)}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 4 Columnas informativas organizadas
        col_c1, col_c2, col_c3, col_c4 = st.columns(4)

        with col_c1:
            st.markdown(f"""
            <div class="clinical-card" style="height:100%; border-top: 3px solid #38bdf8;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">PALPACIÓN CLÍNICA</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0 10px 0;">📍 Reparos Anatómicos</div>
                <ul style="padding-left:16px; font-size:0.83rem; color:#334155; line-height:1.6; margin:0;">
                    <li><strong>EIAS:</strong> {crit.get('eias', 'N/A')}</li>
                    <li><strong>EIPS:</strong> {crit.get('eips', 'N/A')}</li>
                    <li><strong>Cresta Ilíaca:</strong> {crit.get('cresta', 'N/A')}</li>
                    <li><strong>Tub. Isquiática:</strong> {crit.get('isquion', 'N/A')}</li>
                    <li><strong>Sínfisis Púbica:</strong> {crit.get('sinfisis', 'N/A')}</li>
                    <li><strong>Surco Sacro / AIL:</strong> {crit.get('surco_sacro', 'Simétrico')} / {crit.get('ail', 'Simétrico')}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        with col_c2:
            st.markdown(f"""
            <div class="clinical-card" style="height:100%; border-top: 3px solid #f59e0b;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">DINÁMICA ARTICULAR</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0 10px 0;">💥 Cinemática & Causa</div>
                <div style="font-size:0.83rem; color:#334155; line-height:1.5;">
                    <div style="margin-bottom:8px;">
                        <strong>Eje de Movimiento:</strong><br>
                        <span style="color:#0284c7; font-weight:600;">{info_clinica.get('eje_movimiento', 'Articulación SI')}</span>
                    </div>
                    <div style="margin-bottom:8px;">
                        <strong>Cinemática Articular:</strong><br>
                        <span>{meta_preset.get('cinematica_resumen', 'Movimiento tridimensional acoplado.')}</span>
                    </div>
                    <div>
                        <strong>Mecanismo Lesional:</strong><br>
                        <span style="color:#475569;">{meta_preset.get('mecanismo', 'Sobrecarga biomecánica o traumatismo.')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_c3:
            inhibir_str = ", ".join(miofascial.get("inhibir", [])) if miofascial.get("inhibir") else "Evaluación específica"
            activar_str = ", ".join(miofascial.get("activar", [])) if miofascial.get("activar") else "Estabilizadores pélvicos"
            alerta_str = miofascial.get("precaucion_reactiva", "Monitorear tono muscular.")
            st.markdown(f"""
            <div class="clinical-card" style="height:100%; border-top: 3px solid #ec4899;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">ESTADO TISULAR</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0 10px 0;">🧬 Tensión Ligamentosa</div>
                <div style="font-size:0.83rem; color:#334155; line-height:1.5;">
                    <div style="margin-bottom:8px;">
                        <strong>Tensión Ligamentosa:</strong><br>
                        <span style="color:#be185d; font-weight:600;">{crit.get('tejidos_blandos', 'Normal')}</span>
                    </div>
                    <div style="margin-bottom:8px;">
                        <strong>Músculos a Inhibir / Liberar:</strong><br>
                        <span style="color:#475569;">{inhibir_str}</span>
                    </div>
                    <div style="margin-bottom:8px;">
                        <strong>Alerta Reactiva:</strong><br>
                        <span style="color:#b45309; font-size:0.8rem;">{alerta_str}</span>
                    </div>
                    <div>
                        <strong>Activar / Fortalecer:</strong><br>
                        <span style="color:#047857; font-weight:600;">{activar_str}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_c4:
            st.markdown(f"""
            <div class="clinical-card" style="height:100%; border-top: 3px solid #10b981;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">EVALUACIÓN FUNCIONAL</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0 10px 0;">⚡ Pruebas Funcionales</div>
                <div style="font-size:0.83rem; color:#334155; line-height:1.5;">
                    <div style="margin-bottom:8px;">
                        <strong>Long-Sitting Test:</strong><br>
                        <span style="color:#047857; font-weight:600;">{crit.get('long_sitting', 'Neutro')}</span>
                    </div>
                    <div style="margin-bottom:8px;">
                        <strong>Maléolo en Supino:</strong><br>
                        <span>{crit.get('maleolo_supino', 'Simétrico')}</span>
                    </div>
                    <div style="margin-bottom:8px;">
                        <strong>Supino vs Prono:</strong><br>
                        <span>{crit.get('pierna_supino_prono', 'Sin alteración relativa')}</span>
                    </div>
                    <div>
                        <strong>Spring Test Sacro:</strong><br>
                        <span style="font-weight:600;">{crit.get('spring_test', 'Negativo')}</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # 2 Columnas para Protocolo de Tratamiento & Corrección Manual
        st.markdown("##### 🎯 Protocolo de Tratamiento & Corrección Manual:")
        col_adj1, col_adj2 = st.columns(2)

        with col_adj1:
            st.markdown(f"""
            <div class="clinical-card" style="border-left:4px solid #0284c7;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">MANIPULACIÓN ARTICULAR</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0;">🔨 Ajuste HVLA: {ajuste.get('tecnica', 'Side-Posture')}</div>
                <hr style="margin:8px 0; border:0; border-top:1px solid #e2e8f0;" />
                <div style="font-size:0.83rem; color:#334155; line-height:1.6;">
                    <p style="margin-bottom:6px;"><strong>Posición del Paciente:</strong> {ajuste.get('posicion_paciente', 'Decúbito lateral')}</p>
                    <p style="margin-bottom:6px;"><strong>PCP (Punto de Contacto Paciente):</strong> <span style="color:#0284c7; font-weight:600;">{ajuste.get('pcp', 'EIPS')}</span></p>
                    <p style="margin-bottom:6px;"><strong>PCC (Punto de Contacto Clínico):</strong> {ajuste.get('pcc', 'Pisiforme / Hipotenar')}</p>
                    <p style="margin-bottom:6px;"><strong>LOD (Línea de Conducción / Vector):</strong> <span style="color:#047857; font-weight:600;">{ajuste.get('linea_correccion', 'P-A')}</span></p>
                    <p style="margin-bottom:0; background:#fef2f2; border:1px solid #fecaca; border-radius:6px; padding:6px 10px; color:#b91c1c; font-size:0.8rem;">
                        <strong>⚠️ Precaución Técnica:</strong> {ajuste.get('advertencia', 'Respetar barrera motriz sin rebote.')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        with col_adj2:
            st.markdown(f"""
            <div class="clinical-card" style="border-left:4px solid #10b981;">
                <div style="font-size:0.75rem; color:#64748b; font-weight:700; text-transform:uppercase;">REEDUCACIÓN NEUROMUSCULAR</div>
                <div style="font-size:1.05rem; font-weight:700; color:#0f172a; margin:4px 0;">🧘 Técnica MET: {met.get('nombre', 'MET de Fred Mitchell Sr.')}</div>
                <hr style="margin:8px 0; border:0; border-top:1px solid #e2e8f0;" />
                <div style="font-size:0.83rem; color:#334155; line-height:1.6;">
                    <p style="margin-bottom:6px;"><strong>Posición:</strong> {met.get('posicion', 'Decúbito supino/prono')}</p>
                    <p style="margin-bottom:6px;"><strong>Músculo Motor Clave:</strong> <span style="color:#047857; font-weight:600;">{met.get('musculo_motor', 'Flexores/Extensores')}</span></p>
                    <p style="margin-bottom:6px;"><strong>Acción Isométrica:</strong> {met.get('accion', 'Contracción resistida al 20-25% por 7-10s.')}</p>
                    <p style="margin-bottom:0; background:#ecfdf5; border:1px solid #a7f3d0; border-radius:6px; padding:6px 10px; color:#065f46; font-size:0.8rem;">
                        <strong>Fase Post-Isométrica (Relajación):</strong> {met.get('fase_post', 'Ganancia pasiva hacia nueva barrera motriz.')}
                    </p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Matriz Comparativa General de Consulta Rápida
        st.markdown("---")
        st.markdown("### 📊 Matriz Comparativa de Diagnóstico Diferencial Pélvico")
        st.caption("Resumen anatomo-clínico de referencia rápida según criterios osteopáticos y quiroprácticos (Gonstead & Mitchell).")

        tabla_comparativa_html = """
        <div style="overflow-x:auto; border-radius:8px; border:1px solid #e2e8f0; box-shadow:0 1px 3px rgba(0,0,0,0.05); margin-bottom:20px;">
            <table style="width:100%; border-collapse:collapse; font-size:0.82rem; text-align:left; background:#ffffff;">
                <thead>
                    <tr style="background:#0f172a; color:#f8fafc;">
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Disfunción</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Eje / Plano</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">EIAS</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">EIPS</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Pubis</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Long-Sitting</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Spring Test</th>
                        <th style="padding:10px 12px; border-bottom:2px solid #334155;">Ajuste HVLA / LOD</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco Posterior (PI)</td>
                        <td style="padding:9px 12px;">Transverso S3 (Sagital)</td>
                        <td style="padding:9px 12px; color:#0284c7;">Alta / Posterior</td>
                        <td style="padding:9px 12px; color:#7c3aed;">Baja / Medial</td>
                        <td style="padding:9px 12px;">Alto y hundido</td>
                        <td style="padding:9px 12px;">Corta a Larga</td>
                        <td style="padding:9px 12px; color:#10b981;">Neutro</td>
                        <td style="padding:9px 12px;">Side-Posture EIPS P-A caudal</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco Anterior (AS)</td>
                        <td style="padding:9px 12px;">Transverso S3 (Sagital)</td>
                        <td style="padding:9px 12px; color:#0284c7;">Baja / Anterior</td>
                        <td style="padding:9px 12px; color:#7c3aed;">Alta / Lateral</td>
                        <td style="padding:9px 12px;">Bajo y prominente</td>
                        <td style="padding:9px 12px;">Larga a Corta</td>
                        <td style="padding:9px 12px; color:#10b981;">Neutro</td>
                        <td style="padding:9px 12px;">Cresta ilíaca A-P / Isquion P-A</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco Ascendido (Upslip)</td>
                        <td style="padding:9px 12px;">Translación Y (Cizallamiento)</td>
                        <td style="padding:9px 12px; color:#ef4444;">Alta</td>
                        <td style="padding:9px 12px; color:#ef4444;">Alta</td>
                        <td style="padding:9px 12px; color:#ef4444;">Escalón superior</td>
                        <td style="padding:9px 12px; color:#ef4444;">Corta fija</td>
                        <td style="padding:9px 12px; color:#f59e0b;">Rígido local</td>
                        <td style="padding:9px 12px;">Leg Pull traccional caudal axial</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco Descendido (Downslip)</td>
                        <td style="padding:9px 12px;">Translación Y (Cizallamiento)</td>
                        <td style="padding:9px 12px; color:#10b981;">Baja</td>
                        <td style="padding:9px 12px; color:#10b981;">Baja</td>
                        <td style="padding:9px 12px; color:#10b981;">Escalón inferior</td>
                        <td style="padding:9px 12px; color:#10b981;">Larga fija</td>
                        <td style="padding:9px 12px; color:#10b981;">Alivio en descarga</td>
                        <td style="padding:9px 12px;">Ischial Push en prono I-S</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco en Outflare (EX)</td>
                        <td style="padding:9px 12px;">Vertical Carilla SI (Transverso)</td>
                        <td style="padding:9px 12px;">Lateralizada</td>
                        <td style="padding:9px 12px;">Medializada</td>
                        <td style="padding:9px 12px;">Nivelado</td>
                        <td style="padding:9px 12px;">Sin cambio</td>
                        <td style="padding:9px 12px;">Conservado</td>
                        <td style="padding:9px 12px;">Push en sulcus sacro P-A y M-L</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Ilíaco en Inflare (IN)</td>
                        <td style="padding:9px 12px;">Vertical Carilla SI (Transverso)</td>
                        <td style="padding:9px 12px;">Medializada</td>
                        <td style="padding:9px 12px;">Lateralizada</td>
                        <td style="padding:9px 12px;">Nivelado</td>
                        <td style="padding:9px 12px;">Sin cambio</td>
                        <td style="padding:9px 12px;">Conservado</td>
                        <td style="padding:9px 12px;">Pull cara medial EIPS M-L</td>
                    </tr>
                    <tr style="border-bottom:1px solid #e2e8f0; background:#f8fafc;">
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Torsión Sacra Anterior</td>
                        <td style="padding:9px 12px;">Oblicuo homolateral (D/D, I/I)</td>
                        <td style="padding:9px 12px;">Nivelada</td>
                        <td style="padding:9px 12px;">Nivelada</td>
                        <td style="padding:9px 12px;">Nivelado</td>
                        <td style="padding:9px 12px;">Inversión supino/prono</td>
                        <td style="padding:9px 12px; color:#10b981;">NEGATIVO (elástico)</td>
                        <td style="padding:9px 12px;">Pisiforme en AIL posterior P-A</td>
                    </tr>
                    <tr>
                        <td style="padding:9px 12px; font-weight:700; color:#0f172a;">Torsión Sacra Posterior</td>
                        <td style="padding:9px 12px;">Oblicuo contralateral (D/I, I/D)</td>
                        <td style="padding:9px 12px;">Nivelada</td>
                        <td style="padding:9px 12px;">Nivelada</td>
                        <td style="padding:9px 12px;">Nivelado</td>
                        <td style="padding:9px 12px;">Inversión supino/prono</td>
                        <td style="padding:9px 12px; color:#ef4444; font-weight:700;">POSITIVO FRANCO (rígido)</td>
                        <td style="padding:9px 12px;">Base sacra rígida P-A intruir</td>
                    </tr>
                </tbody>
            </table>
        </div>
        """
        st.markdown(tabla_comparativa_html, unsafe_allow_html=True)


# ------------------------------------------------------------------------------
# PÁGINA 4: JUICIO CLÍNICO, PRESCRIPCIÓN Y EXPORTACIÓN EN PDF
# ------------------------------------------------------------------------------
elif nav_activa == OPCIONES_MENU_PRINCIPAL[3]:
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
    st.markdown("### 💊 Prescripción Biomecánica y Terapéutica Integral (4 Pilares Clínicos)")

    col_tx1, col_tx2 = st.columns(2)

    with col_tx1:
        st.markdown("##### 🔄 1. Ajuste Articular Biomecánico")
        if diagnostico_actual.contraindicacion_hvla:
            st.error("⛔ **Manipulación HVLA Bloqueada:** Presencia de banderas rojas en la anamnesis.")
        else:
            st.markdown(f"""
            <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b; min-height:125px;">
                <strong>Vector y Posicionamiento:</strong><br>
                {diagnostico_actual.vector_ajuste}
            </div>
            """, unsafe_allow_html=True)

    with col_tx2:
        st.markdown("##### ⚡ 2. Técnica de Energía Muscular (MET)")
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b; min-height:125px;">
            <strong>Protocolo de Fred Mitchell Sr.:</strong><br>
            {diagnostico_actual.tecnica_met}
        </div>
        """, unsafe_allow_html=True)

    col_tx3, col_tx4 = st.columns(2)

    with col_tx3:
        st.markdown("##### 🧘 3. Inhibición Miofascial de Cadenas Acortadas")
        st.markdown("""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b; min-height:150px;">
            <strong>Músculos y Tejidos Diana:</strong>
            <ul style="padding-left:16px; margin-top:6px;">
        """ + "".join([f"<li>{m}</li>" for m in diagnostico_actual.inhibicion_miofascial]) + """
            </ul>
        </div>
        """, unsafe_allow_html=True)

    with col_tx4:
        st.markdown("##### 🏋️ 4. Ejercicio Terapéutico y Control Sensorio-Motor")
        items_html = "".join([
            f"<li style='margin-bottom:6px;'><strong>{sub}:</strong> {desc}</li>"
            for sub, desc in diagnostico_actual.ejercicio_terapeutico.items()
        ])
        st.markdown(f"""
        <div style="background:#f8fafc; border:1px solid #cbd5e1; border-radius:8px; padding:14px; font-size:0.88rem; color:#1e293b; min-height:150px;">
            <ul style="padding-left:16px; margin:0;">
                {items_html}
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # MÓDULO EXPANDIBLE DE CONOCIMIENTO CLÍNICO E INTEGRACIÓN TERAPÉUTICA
    if getattr(diagnostico_actual, "clave_conocimiento", None):
        kb_info = get_disfuncion_info(diagnostico_actual.clave_conocimiento)
        if kb_info:
            with st.expander("📖 Protocolo Terapéutico Detallado y Evidencia Biomecánica (Base de Conocimiento)", expanded=True):
                col_kb1, col_kb2 = st.columns(2)

                with col_kb1:
                    st.markdown("#### 🎯 Técnica de Energía Muscular (MET - Fred Mitchell)")
                    met_data = kb_info.get("tecnica_met") or kb_info.get("met", {})
                    st.markdown(f"- **Técnica:** {met_data.get('nombre', 'N/A')}")
                    st.markdown(f"- **Músculo Motor:** {met_data.get('musculo_motor', 'N/A')}")
                    st.markdown(f"- **Posicionamiento y Acción:** {met_data.get('accion', 'N/A')}")
                    st.markdown(f"- **Fase Post-Isométrica:** {met_data.get('fase_post', 'N/A')}")

                    st.markdown("#### 🛡️ Abordaje Miofascial y Criterios")
                    mio_data = kb_info.get("abordaje_miofascial") or kb_info.get("miofascial", {})
                    if mio_data.get("inhibir"):
                        st.markdown(f"- **Tejidos a Inhibir:** {', '.join(mio_data['inhibir'])}")
                    if mio_data.get("activar"):
                        st.markdown(f"- **Tejidos a Activar (Reeducación):** {', '.join(mio_data['activar'])}")
                    if mio_data.get("precaucion_reactiva"):
                        st.warning(f"⚠️ **Precaución Reactiva:** {mio_data['precaucion_reactiva']}")
                    if mio_data.get("criterios_retorno"):
                        st.info(f"🏁 **Criterios de Alta / Retorno:** {mio_data['criterios_retorno']}")

                with col_kb2:
                    st.markdown("#### 🔄 Ajuste Articular Biomecánico")
                    ajuste_data = kb_info.get("ajuste_articular", {})
                    st.markdown(f"- **Técnica:** {ajuste_data.get('tecnica', 'N/A')}")
                    st.markdown(f"- **Punto Contacto Clínico (PCC):** {ajuste_data.get('pcc', 'N/A')}")
                    st.markdown(f"- **Punto Contacto Paciente (PCP):** {ajuste_data.get('pcp', 'N/A')}")
                    st.markdown(f"- **Línea de Corrección (LOD):** {ajuste_data.get('linea_correccion', 'N/A')}")
                    if ajuste_data.get("advertencia"):
                        st.warning(f"⚠️ **Advertencia:** {ajuste_data['advertencia']}")

                    st.markdown("#### 🏋️ Ejercicio Terapéutico y Control Activo")
                    for sub_ej, desc_ej in diagnostico_actual.ejercicio_terapeutico.items():
                        st.markdown(f"- **{sub_ej}:** {desc_ej}")
    else:
        st.info("ℹ️ **Patrón Mixto en Evaluación:** Los hallazgos palpatorios no corresponden a un patrón biomecánico puro predefinido. Se aconseja normalización manual general y reevaluación articular.")
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