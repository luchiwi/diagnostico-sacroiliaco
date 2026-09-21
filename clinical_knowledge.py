"""
clinical_knowledge.py - Base de conocimiento biomecánico y prescripción clínica
"""

CLINICAL_KNOWLEDGE_BASE = {
    "ILIACO_POSTERIOR": {
        "nombre_clinico": "Ilíaco Posterior (PI / Postero-Inferior)",
        "categoria": "Disfunción Iliosacra Rotacional Sagital",
        "eje_movimiento": "Eje Transverso S3 (Transverso inferior del sacro)",
        "criterios_diagnosticos": {
            "eias": "Alta y lateralizada",
            "eips": "Baja y medializada",
            "cresta": "Baja",
            "isquion": "Bajo y anterior",
            "sinfisis": "Antero-superior (alta y anterior)",
            "maleolo_supino": "Corto funcional",
            "long_sitting": "Pierna corta en supino se alarga al pasar a sedente",
            "tejidos_blandos": "Tensión en ligamento sacrotuberoso; piramidal en tensión excéntrica reactiva"
        },
        "ajuste_articular": {
            "tecnica": "Side-Posture Gonstead PI / Drop Pelviano",
            "posicion_paciente": "Decúbito lateral con hemipelvis afectada hacia arriba, tronco y extremidades estabilizadas.",
            "pcc": "Pisiforme / eminencia hipotenar de la mano caudal.",
            "pcp": "Aspecto postero-inferior de la EIPS homolateral.",
            "linea_correccion": "Posterior a Anterior (P-A) con línea de conducción ántero-inferior / caudal (hacia eje S3).",
            "advertencia": "Evitar empuje cefálico/craneal; bloquea el brazo de palanca e induce cizallamiento."
        },
        "tecnica_met": {
            "nombre": "MET de Fred Mitchell Sr. para Ilíaco Posterior",
            "posicion": "Decúbito prono con rodilla flexionada 90° o supino con extremidad en borde estabilizando pelvis contralateral.",
            "musculo_motor": "Recto femoral y Psoas ilíaco.",
            "accion": "Contracción isométrica resistida de flexores de cadera al 20-25% por 7-10 s.",
            "fase_post": "En relajación, avanzar cadera a mayor extensión guiando la báscula anterior (3 a 5 ciclos)."
        },
        "manejo_miofascial": {
            "inhibir": ["Isquiotibiales proximales", "Ligamento sacrotuberoso"],
            "precaucion_piramidal": "Priorizar técnicas por posición (Strain-Counterstrain); evitar compresión isquémica agresiva si existe elongación reactiva.",
            "activar": ["Glúteo mayor en cadena cinética cerrada", "Glúteo medio", "Core lumbo-pélvico"]
        }
    },
    "ILIACO_ANTERIOR": {
        "nombre_clinico": "Ilíaco Anterior (AS / Antero-Superior)",
        "categoria": "Disfunción Iliosacra Rotacional Sagital",
        "eje_movimiento": "Eje Transverso S3 (Transverso inferior del sacro)",
        "criterios_diagnosticos": {
            "eias": "Baja y medializada",
            "eips": "Alta y lateralizada",
            "cresta": "Alta",
            "isquion": "Alto y posterior",
            "sinfisis": "Postero-inferior (baja y posterior)",
            "maleolo_supino": "Largo funcional",
            "long_sitting": "Pierna larga en supino se acorta al pasar a sedente",
            "tejidos_blandos": "Tensión en psoas-ilíaco y recto anterior; ligamento sacrotuberoso distendido o laxo"
        },
        "ajuste_articular": {
            "tecnica": "Side-Posture Gonstead AS / Drop Pelviano",
            "posicion_paciente": "Decúbito lateral con hemipelvis afectada superior, cadera y rodilla en mayor flexión.",
            "pcc": "Eminencia tenar o antebrazo según técnica de palanca corta/larga.",
            "pcp": "Aspecto antero-superior de la cresta ilíaca / EIAS hacia posterior, o cara posterior del isquion hacia anterior.",
            "linea_correccion": "Anterior a Posterior (A-P) o vector sobre isquion de Postero-Inferior a Antero-Superior.",
            "advertencia": "No forzar hiperextensión de cadera en presencia de patología facetaria L5-S1."
        },
        "tecnica_met": {
            "nombre": "MET de Fred Mitchell Sr. para Ilíaco Anterior",
            "posicion": "Decúbito supino, flexión máxima de cadera y rodilla homolateral contra el tronco.",
            "musculo_motor": "Isquiotibiales y Glúteo mayor.",
            "accion": "Contracción isométrica resistida de extensores de cadera (empuje hacia la camilla) al 20-25% por 7-10 s.",
            "fase_post": "En relajación, ganar mayor flexión de cadera induciendo rotación posterior (3 a 5 ciclos)."
        },
        "manejo_miofascial": {
            "inhibir": ["Psoas-Ilíaco", "Recto Femoral", "Tensor de la fascia lata"],
            "precaucion_piramidal": "Evaluar tono; suele encontrarse acortado en compensación rotatoria externa.",
            "activar": ["Isquiotibiales", "Glúteo mayor en rango de flexión", "Recto abdominal homolateral"]
        }
    }
}