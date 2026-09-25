import json
import os
import sys

# Add project root to path
sys.path.insert(0, r"c:\Users\luisp\OneDrive\Desktop\APP-SACROILIACO")

from clinical_knowledge import CLINICAL_KNOWLEDGE_BASE, get_disfuncion_info

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
    "sacro_ai_i": "SACRO_ANTERO_INFERIOR_I",
    "sacro_ps_d": "SACRO_POSTERO_SUPERIOR_D",
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
    "sacro_ai_i": {
        "listing": "Osteopatía: Sacro Anterior Izquierdo (Antero-Inferior I)",
        "mecanismo": "Microtrauma repetitivo en rotación pélvica izquierda con carga asimétrica, hipertonía del piramidal izquierdo.",
        "cinematica_resumen": "La hemibase sacra izquierda se profundiza en nutación hacia antero-inferior, el ILA derecho se hace prominente/superficial hacia posterior, piramidal tenso ipsilateral y falsa pierna larga izquierda.",
    },
    "sacro_ps_d": {
        "listing": "Osteopatía: Sacro Posterior Derecho (Postero-Superior D)",
        "mecanismo": "Impacto axial asimétrico en flexión o atrapamiento articular en contranutación unilateral derecha.",
        "cinematica_resumen": "La hemibase sacra derecha se fija en contranutación postero-superior quedando superficial y dolorosa en el sulcus; el ILA izquierdo se profundiza. Maléolo alto homolateral y Spring test rígido sobre base derecha.",
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

def generar_payload():
    payload = {}
    for preset_k, ck_k in PRESET_TO_CK_KEY.items():
        info = get_disfuncion_info(ck_k)
        meta = ATLAS_PRESET_METADATA.get(preset_k, {})
        payload[preset_k] = {
            "nombre_clinico": info.get("nombre_clinico", preset_k),
            "categoria": info.get("categoria", "Disfunción Pélvica"),
            "eje_movimiento": info.get("eje_movimiento", "Sacroilíaco"),
            "listing": meta.get("listing", "N/D"),
            "mecanismo": meta.get("mecanismo", "Sobrecarga biomecánica o traumatismo."),
            "cinematica_resumen": meta.get("cinematica_resumen", "Movimiento tridimensional acoplado."),
            "crit": info.get("criterios_diagnosticos", {}),
            "miofascial": info.get("abordaje_miofascial", {}),
            "ajuste": info.get("ajuste_articular", {}),
            "met": info.get("tecnica_met", {})
        }
    return payload

p = generar_payload()
print(f"Total presets generated: {len(p)}")
s = json.dumps(p, ensure_ascii=False)
print(f"JSON length: {len(s)} bytes")
assert len(p) == 18, f"Expected 18 presets, got {len(p)}"
for k in PRESET_TO_CK_KEY:
    assert k in p, f"Missing preset {k}"
    assert "nombre_clinico" in p[k], f"Missing nombre_clinico in {k}"
    assert "crit" in p[k], f"Missing crit in {k}"
    assert "ajuste" in p[k], f"Missing ajuste in {k}"
    assert "met" in p[k], f"Missing met in {k}"
print("All 18 presets validated successfully!")
