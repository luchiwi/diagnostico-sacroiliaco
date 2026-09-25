"""
clinical_knowledge.py
Base de conocimiento biomecánico, semiológico y prescripción clínica integral.
Basado en criterios quiroprácticos (Gonstead/Side-Posture), MET (Fred Mitchell Sr.)
y control motor lumbo-pélvico en cadena cinética cerrada.
"""

from typing import Dict, Any

CLINICAL_KNOWLEDGE_BASE: Dict[str, Any] = {
    # =========================================================================
    # 1. DISFUNCIONES ILIOSACRAS - PLANO SAGITAL
    # =========================================================================
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
            "surco_sacro": "Neutro / Simétrico",
            "ail": "Simétrico",
            "maleolo_supino": "Corto funcional",
            "long_sitting": "Pierna corta en supino se alarga al sentarse",
            "pierna_supino_prono": "Pierna corta constante en supino y prono",
            "spring_test": "Neutro",
            "tejidos_blandos": "Tensión aumentada en ligamento sacrotuberoso; piramidal en tensión excéntrica reactiva"
        },
        "ajuste_articular": {
            "tecnica": "Side-Posture Gonstead PI / Drop Pelviano",
            "posicion_paciente": "Decúbito lateral con hemipelvis afectada hacia arriba, rodilla y cadera flexionadas para puesta en tensión.",
            "pcc": "Pisiforme / eminencia hipotenar de la mano caudal.",
            "pcp": "Aspecto postero-inferior de la EIPS homolateral.",
            "linea_correccion": "Posterior a Anterior (P-A) con línea de conducción ántero-inferior / caudal (hacia eje S3). Ángulo aproximado de 45° caudal.",
            "advertencia": "Prohibido empuje cefálico/superior; acentúa el brazo de palanca posterior o genera cizallamiento vertical."
        },
        "tecnica_met": {
            "nombre": "MET de Fred Mitchell Sr. para Ilíaco Posterior",
            "posicion": "Decúbito prono con rodilla en 90° o supino con extremidad en borde de camilla estabilizando pelvis contralateral.",
            "musculo_motor": "Recto femoral y Psoas ilíaco.",
            "accion": "Contracción isométrica resistida de flexores de cadera al 20-25% por 7-10 s contra la resistencia fija del clínico.",
            "fase_post": "En periodo de relajación, guiar cadera a mayor extensión pasiva induciendo la basculación anterior del hueso coxal (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Isquiotibiales proximales (Bíceps femoral y Semitendinoso)",
                "Ligamento sacrotuberoso homolateral (presión sostenida o fricción transversal profunda)",
                "Glúteo mayor (fibras inferiores)"
            ],
            "precaucion_reactiva": "Músculo Piramidal bajo tensión excéntrica reactiva por posteriorización coxal. Priorizar técnicas posicionales (Strain-Counterstrain); evitar compresión isquémica agresiva para prevenir neuropraxia ciática.",
            "activar": [
                "Glúteo mayor en cadena cinética cerrada (puente unipodal con control pélvico)",
                "Glúteo medio (estabilidad en plano frontal)",
                "Core lumbo-pélvico (disociación Dead Bug)"
            ],
            "criterios_retorno": "Simetría en hitos palpatorios pélvicos, Laslett negativo y adecuada disociación lumbo-pélvica previa al retorno al running o sobrecarga."
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
            "surco_sacro": "Neutro / Simétrico",
            "ail": "Simétrico",
            "maleolo_supino": "Largo funcional",
            "long_sitting": "Pierna larga en supino se acorta al sentarse",
            "pierna_supino_prono": "Pierna larga constante en supino y prono",
            "spring_test": "Neutro",
            "tejidos_blandos": "Tensión en psoas-ilíaco y recto femoral; ligamento sacrotuberoso distendido o laxo"
        },
        "ajuste_articular": {
            "tecnica": "Side-Posture Gonstead AS / Drop Pelviano",
            "posicion_paciente": "Decúbito lateral con hemipelvis afectada hacia arriba, cadera y rodilla en mayor flexión que en PI.",
            "pcc": "Eminencia tenar/hipotenar o antebrazo según técnica de palanca corta/larga.",
            "pcp": "Aspecto antero-superior de la cresta ilíaca / EIAS hacia posterior, o cara posterior del isquion hacia anterior.",
            "linea_correccion": "Anterior a Posterior (A-P) sobre cresta, o Postero-Inferior a Antero-Superior sobre tuberosidad isquiática.",
            "advertencia": "Evitar hiperextensión lumbar forzada durante la maniobra, especialmente en pacientes con hiperlordosis o patología facetaria L5-S1."
        },
        "tecnica_met": {
            "nombre": "MET de Fred Mitchell Sr. para Ilíaco Anterior",
            "posicion": "Decúbito supino, flexión máxima de cadera y rodilla homolateral contra el tronco del paciente.",
            "musculo_motor": "Isquiotibiales y Glúteo mayor.",
            "accion": "Contracción isométrica resistida de extensores de cadera (empuje hacia la camilla) al 20-25% por 7-10 s.",
            "fase_post": "En la relajación, ganar mayor flexión de cadera induciendo la rotación posterior del hueso coxal (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Psoas-Ilíaco",
                "Recto Femoral",
                "Tensor de la fascia lata"
            ],
            "precaucion_reactiva": "Evaluar tono de rotadores externos y piramidal por compensación rotatoria en apoyo unipodal.",
            "activar": [
                "Isquiotibiales en rango funcional",
                "Glúteo mayor en flexión inicial",
                "Recto abdominal homolateral"
            ],
            "criterios_retorno": "Nivelación de EIAS/EIPS en bipedestación y ausencia de anteversión forzada durante la marcha."
        }
    },

    # =========================================================================
    # 2. DISFUNCIONES ILIOSACRAS - CIZALLAMIENTOS VERTICALES
    # =========================================================================
    "ILIACO_UPSLIP": {
        "nombre_clinico": "Ilíaco Ascendido (Upslip / Cizallamiento Craneal)",
        "categoria": "Disfunción Iliosacra de Cizallamiento Vertical",
        "eje_movimiento": "Traslación lineal vertical pura sin rotación primaria",
        "criterios_diagnosticos": {
            "eias": "Alta",
            "eips": "Alta",
            "cresta": "Alta",
            "isquion": "Alto",
            "sinfisis": "Alta (escalón superior ipsilateral)",
            "surco_sacro": "Profundo aparente por horizontalización sacra compensatoria",
            "ail": "Alto",
            "maleolo_supino": "Corto constante (Regla de 3 Puntos Altos)",
            "long_sitting": "Pierna corta se mantiene corta al sentarse (sin cambio relativo)",
            "pierna_supino_prono": "Pierna corta constante en supino y prono",
            "spring_test": "Rígido / Positivo localizado",
            "tejidos_blandos": "Espasmo severo del cuadrado lumbar; ligamentos sacrotuberoso y sacroespinoso bajo alta tracción"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste por Tracción Caudal Rápida (Pull en Supino)",
            "posicion_paciente": "Decúbito supino; terapeuta de pie a los pies de la camilla.",
            "pcc": "Cruce de manos por sobre los maléolos tibial y fibular de la extremidad a tratar.",
            "pcp": "Tercio distal de la pierna (soporte supra-maleolar).",
            "linea_correccion": "Flexión de cadera de 15-20°, leve aducción y ligera rotación interna. Tracción axial pura y rápida caudal combinada con tos fuerte del paciente.",
            "advertencia": "Descartar inestabilidad ligamentosa de rodilla o patología coxofemoral previa al impulso axial traccional."
        },
        "tecnica_met": {
            "nombre": "MET para Ilíaco Ascendido (Fred Mitchell Sr.)",
            "posicion": "Decúbito supino. Terapeuta a los pies toma la pierna por encima de los maléolos y tracciona caudalmente hasta la barrera.",
            "musculo_motor": "Cuadrado lumbar e iliocostal ipsilaterales.",
            "accion": "El paciente intenta subir la cadera hacia la axila (hip hike) al 20-30% de fuerza isométrica por 7-10 s contra resistencia inamovible.",
            "fase_post": "Tras 3 s de relajación completa, traccionar caudalmente hacia la nueva barrera de longitud pélvica (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Cuadrado lumbar ipsilateral (técnica neuromuscular y compresión isquémica)",
                "Masa común de erectores espinales lumbares",
                "Ligamento iliolumbar y ligamentos sacroilíacos interóseos"
            ],
            "precaucion_reactiva": "Ligamentos sacrotuberoso y sacroespinoso distendidos por cizallamiento vertical pasivo. Evitar compresión profunda en inserciones isquiáticas para no aumentar irritación.",
            "activar": [
                "Sentadilla unipodal asistida en escalón (Step-Down controlado con descenso excéntrico pélvico)",
                "Dead Bug con presión isométrica contra pared para co-activar transverso del abdomen",
                "Estabilización frontal lumbo-pélvica"
            ],
            "criterios_retorno": "Carga bipodal simétrica sin dolor ligamentoso y corrección de la asimetría en el Test de Flexión de Pie (Vorlauf)."
        }
    },

    "ILIACO_DOWNSLIP": {
        "nombre_clinico": "Ilíaco Descendido (Downslip / Cizallamiento Caudal)",
        "categoria": "Disfunción Iliosacra de Cizallamiento Vertical",
        "eje_movimiento": "Traslación lineal vertical caudal sin componente rotacional primario",
        "criterios_diagnosticos": {
            "eias": "Baja",
            "eips": "Baja",
            "cresta": "Baja",
            "isquion": "Bajo",
            "sinfisis": "Baja (escalón inferior ipsilateral)",
            "surco_sacro": "Superficial aparente",
            "ail": "Bajo",
            "maleolo_supino": "Largo constante (Regla de 3 Puntos Bajos)",
            "long_sitting": "Pierna larga se mantiene larga al sentarse (sin cambio relativo)",
            "pierna_supino_prono": "Pierna larga constante en supino y prono",
            "spring_test": "Neutro / Alivio con marcha y descarga",
            "tejidos_blandos": "Tensión reactiva en vientre de aductores y tensor de la fascia lata"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo Isquiático Cefálico (Push en Prono)",
            "posicion_paciente": "Decúbito prono; clínico de pie al lado homolateral a nivel de los muslos.",
            "pcc": "Talón de la mano caudal reforzada en muñeca con mano contralateral (toma en brazalete).",
            "pcp": "Borde inferior de la tuberosidad isquiática ipsilateral.",
            "linea_correccion": "Vector de Inferior a Superior (I-S) paralelo al fémur, aplicado en fase de espiración completa.",
            "advertencia": "Evitar presionar estructuras del nervio ciático en la fosa poplítea o medial al isquion."
        },
        "tecnica_met": {
            "nombre": "MET para Ilíaco Descendido (Fred Mitchell Sr.)",
            "posicion": "Decúbito supino con leve flexión de cadera y rodilla. Contacto del terapeuta sobre cara posterior de muslo/isquion.",
            "musculo_motor": "Recto anterior del abdomen, oblicuo interno y aductores.",
            "accion": "El paciente intenta traccionar la pierna hacia su cabeza (flexión pélvica activa) al 20-30% por 7-10 s contra la toma fija.",
            "fase_post": "En relajación, guiar el ilíaco hacia un mayor ascenso axial cefálico (3 a 5 repeticiones)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Aductor mayor, aductor largo y pectíneo",
                "Tensor de la fascia lata",
                "Membrana obturatriz e interósea"
            ],
            "precaucion_reactiva": "Ligamento iliolumbar y fibras superiores del ligamento sacroilíaco posterior sufren tracción excéntrica reactiva; enfocar la descarga en vientres musculares y no en ligamentos lumbosacros.",
            "activar": [
                "Marcha con carga unilateral (Farmer Carry asimétrico contralateral para inducir ascenso reactivo)",
                "Glute Bridge con banda elástica sobre rodillas manteniendo alineación de EIAS",
                "Isometría de flexores de tronco"
            ],
            "criterios_retorno": "Tolerancia a la carga monopodal con impacto en talón sin dolor púbico ni sensación de inestabilidad."
        }
    },

    # =========================================================================
    # 3. DISFUNCIONES ILIOSACRAS - PLANO HORIZONTAL (IN/EX)
    # =========================================================================
    "ILIACO_INFLARE": {
        "nombre_clinico": "Ilíaco en Inflare (Rotación Interna / IN)",
        "categoria": "Disfunción Iliosacra en Plano Transverso",
        "eje_movimiento": "Rotación sobre eje vertical que pasa por la sínfisis púbica y la SI",
        "criterios_diagnosticos": {
            "eias": "Medializada (aproximada a la línea media, misma altura sagital)",
            "eips": "Lateralizada (alejada de la línea media)",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro / Tensión ligamentosa local",
            "surco_sacro": "Más ancho",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico (sin alteración en supino ni prono)",
            "long_sitting": "Sin cambio relativo en longitud de miembros",
            "pierna_supino_prono": "Simetría constante",
            "spring_test": "Conservado",
            "tejidos_blandos": "Tensión en músculo ilíaco en fosa ilíaca interna, pectíneo y ligamento sacroilíaco anterior"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Pull en Decúbito Lateral para Inflare",
            "posicion_paciente": "Decúbito lateral con hemipelvis disfuncional hacia arriba. Terapeuta en postura de esgrimista.",
            "pcc": "Pulpejos y eminencia hipotenar de la mano de contacto.",
            "pcp": "Borde medial de la EIPS superior.",
            "linea_correccion": "Medial a Lateral (M-L) con el antebrazo paralelo a la parrilla costal del paciente.",
            "advertencia": "No introducir vectores rotacionales sagitales durante el impulso transversal."
        },
        "tecnica_met": {
            "nombre": "MET para Ilíaco en Inflare (Fred Mitchell Sr.)",
            "posicion": "Decúbito supino, cadera y rodilla flectadas a 90°. Pie por fuera de rodilla contralateral. Rodilla guiada a abducción/rotación externa hasta la barrera.",
            "musculo_motor": "Músculo ilíaco, pectíneo y aductor corto.",
            "accion": "El paciente intenta aducir la rodilla hacia la línea media contra resistencia isométrica al 20-30% por 7-10 s.",
            "fase_post": "En relajación, profundizar la abducción/rotación externa abriendo la EIAS hacia lateral (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Músculo ilíaco (abordaje suave en fosa ilíaca interna)",
                "Fascia pectínea y aductor corto",
                "Ligamento sacroilíaco anterior"
            ],
            "precaucion_reactiva": "Rotadores externos profundos (obturador interno) y glúteo medio posterior bajo distensión excéntrica; no masajear agresivamente el aspecto posterior de la EIPS.",
            "activar": [
                "Split Squat búlgaro con banda elástica resistiendo el valgo dinámico",
                "Clamshell lateral con banda co-activando el transverso abdominal",
                "Abductores en bipedestación"
            ],
            "criterios_retorno": "Control del valgo de rodilla en saltos monopodales sin compensación rotatoria pélvica."
        }
    },

    "ILIACO_OUTFLARE": {
        "nombre_clinico": "Ilíaco en Outflare (Rotación Externa / EX)",
        "categoria": "Disfunción Iliosacra en Plano Transverso",
        "eje_movimiento": "Rotación sobre eje vertical que pasa por la sínfisis púbica y la SI",
        "criterios_diagnosticos": {
            "eias": "Lateralizada (alejada de la línea media, misma altura sagital)",
            "eips": "Medializada (aproximada a la línea media)",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Estrecho y profundo",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico (sin alteración en supino ni prono)",
            "long_sitting": "Sin cambio relativo en longitud de miembros",
            "pierna_supino_prono": "Simetría constante",
            "spring_test": "Conservado",
            "tejidos_blandos": "Tensión en tensor de la fascia lata, banda iliotibial y vientre de glúteo medio/menor"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Indirecto en Decúbito Lateral (Push en Sulcus)",
            "posicion_paciente": "Decúbito lateral con el ilíaco disfuncional apoyado abajo sobre la camilla para fijarlo.",
            "pcc": "Borde ulnar / eminencia hipotenar.",
            "pcp": "Base sacra (sulcus) del lado inferior, inmediatamente por medial a la EIPS.",
            "linea_correccion": "Posterior a Anterior (P-A) y Medial a Lateral (M-L) para anteriorizar el sacro y abrir el coxal.",
            "advertencia": "Evitar presión excesiva sobre el sacro si existe sospecha de espondilolistesis activa."
        },
        "tecnica_met": {
            "nombre": "MET para Ilíaco en Outflare (Fred Mitchell Sr.)",
            "posicion": "Decúbito supino con flexión de cadera y rodilla. Pie sobre rodilla opuesta (posición en 4). Estabilizar EIAS contralateral.",
            "musculo_motor": "Glúteo medio (fibras anteriores), glúteo menor y tensor de la fascia lata.",
            "accion": "El paciente empuja la rodilla hacia afuera en abducción al 20-30% por 7-10 s contra resistencia fija.",
            "fase_post": "En relajación, aproximar la rodilla hacia la línea media en aducción para cerrar la EIAS hacia la neutralidad (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Tensor de la fascia lata y cintilla iliotibial",
                "Glúteo medio y menor (fibras laterales)",
                "Fascia glútea profunda"
            ],
            "precaucion_reactiva": "Ligamento sacroilíaco anterior e iliopsoas distendidos mecánicamente; focalizar la liberación en la banda iliotibial y zona lateral.",
            "activar": [
                "Single-Leg RDL (peso muerto rumano unipodal) manteniendo pelvis paralela al suelo",
                "Pallof Press antirrotacional con elástico o polea",
                "Aductores en cadena cinética cerrada"
            ],
            "criterios_retorno": "Signo de Trendelenburg dinámico negativo durante apoyo unipodal sostenido."
        }
    },

    # =========================================================================
    # 4. DISFUNCIONES SACROILÍACAS - TORSIONES SOBRE EJES OBLICUOS
    # =========================================================================
    "TORSION_SACRA_ANTERIOR": {
        "nombre_clinico": "Torsión Sacra Anterior Fisiológica (D/D o I/I)",
        "categoria": "Disfunción Sacroilíaca sobre Eje Oblicuo",
        "eje_movimiento": "Eje Oblicuo correspondiente (Eje Derecho para D/D; Eje Izquierdo para I/I)",
        "criterios_diagnosticos": {
            "eias": "Incongruente con la longitud del maléolo en supino",
            "eips": "Nivelada relativamente",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Profundo en el lado opuesto al eje oblicuo",
            "ail": "Posterior e inferior en el lado contralateral al surco profundo",
            "maleolo_supino": "Pierna larga aparente en supino",
            "long_sitting": "Inversión maleolar",
            "pierna_supino_prono": "INVERSIÓN: Larga en supino pasa a ser Corta en prono",
            "spring_test": "POSITIVO (Conserva elasticidad fisiológica; columna lumbar en lordosis)",
            "tejidos_blandos": "Banda tensa e hipertónica en músculo piramidal del lado del eje oblicuo"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Body Drop / Push en Decúbito Lateral",
            "posicion_paciente": "Decúbito lateral con la base sacra profunda apoyada ABAJO contra la camilla. Flexión de cadera > 90°.",
            "pcc": "Pisiforme / eminencia hipotenar con codo alineado al cuerpo del terapeuta.",
            "pcp": "Ángulo Inferolateral del Sacro (AIL) posteriorizado (el que queda arriba).",
            "linea_correccion": "Posterior a Anterior (P-A) y Lateral a Medial (L-M) para inducir rotación correctora del sacro.",
            "advertencia": "Verificar ángulo de flexión de cadera para bloquear la charnela lumbosacra antes del impulso."
        },
        "tecnica_met": {
            "nombre": "MET para Torsión Sacra Anterior (Fred Mitchell Sr.)",
            "posicion": "Posición de Sims (semi-prono) sobre el lado del eje. Tronco rotado hacia camilla; piernas flectadas colgando fuera del borde.",
            "musculo_motor": "Músculo piramidal homolateral al eje oblicuo.",
            "accion": "El paciente intenta elevar ambos tobillos hacia el techo contra la resistencia caudal del terapeuta al 20-30% por 7-10 s.",
            "fase_post": "En relajación, empujar los tobillos más hacia el suelo para inducir rotación posterior del sacro a la neutralidad (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Músculo piramidal del lado del eje (hipertónico primario; compresión isquémica previa al MET)",
                "Ligamento sacrotuberoso homolateral al eje",
                "Rotadores externos profundos"
            ],
            "precaucion_reactiva": "Multífidos lumbares contralaterales sometidos a tracción torsional continua.",
            "activar": [
                "Reverse Lunges (zancadas dorsales) con rotación de tronco hacia la extremidad anterior",
                "Bird-Dog manteniendo extensión pura sin hiperextensión lumbosacra",
                "Core rotacional funcional"
            ],
            "criterios_retorno": "Extensión lumbar activa indolora y resolución de la asimetría en el Spring Test."
        }
    },

    "TORSION_SACRA_POSTERIOR": {
        "nombre_clinico": "Torsión Sacra Posterior No Fisiológica (D/I o I/D)",
        "categoria": "Disfunción Sacroilíaca sobre Eje Oblicuo",
        "eje_movimiento": "Eje Oblicuo contralateral a la rotación (Eje Izquierdo para D/I; Eje Derecho para I/D)",
        "criterios_diagnosticos": {
            "eias": "Descendida en supino con maléolo alto (incongruencia marcada)",
            "eips": "Nivelada relativamente",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Menos profundo / Plano / Posteriorizado en el lado de la base rígida",
            "ail": "Anterior y superior contralateral a la base posteriorizada",
            "maleolo_supino": "Pierna corta/alta aparente en supino",
            "long_sitting": "Inversión maleolar",
            "pierna_supino_prono": "INVERSIÓN: Corta en supino pasa a ser Larga en prono",
            "spring_test": "NEGATIVO (Rigidez lumbosacra franca / columna lumbar rectificada)",
            "tejidos_blandos": "Espasmo marcado del piramidal en lado del eje y multífidos lumbosacros"
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Body Drop / Push en Decúbito Lateral para Base Sacra",
            "posicion_paciente": "Decúbito lateral con la base sacra posteriorizada hacia ARRIBA. Marcada flexión de cadera (> 90°).",
            "pcc": "Eminencia hipotenar / pisiforme de la mano de contacto.",
            "pcp": "Directamente en el sulcus / base sacra posteriorizada (por medial a la EIPS).",
            "linea_correccion": "Posterior a Anterior (P-A) con leve vector Medial a Lateral (M-L) para anteriorizar la base fija.",
            "advertencia": "Maniobra contraindicada si existe patología discal L5-S1 extruida sintomática."
        },
        "tecnica_met": {
            "nombre": "MET para Torsión Sacra Posterior (Fred Mitchell Sr.)",
            "posicion": "Decúbito lateral sobre el lado opuesto al eje (tronco inclinado hacia atrás). Pierna superior extendida y colgando por detrás de la camilla.",
            "musculo_motor": "Multífidos lumbares bajos (L5-S1) y glúteo mayor contralateral.",
            "accion": "El paciente intenta elevar la pierna extendida hacia el techo contra la resistencia del terapeuta al 20-30% por 7-10 s.",
            "fase_post": "En relajación, permitir mayor descenso en extensión de la extremidad para anteriorizar la base sacra posteriorizada (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Multífidos lumbares bajos del lado posteriorizado",
                "Fascia toracolumbar profunda",
                "Ligamento iliolumbar posterior y piramidal del lado del eje"
            ],
            "precaucion_reactiva": "Ligamento sacroespinoso del lado de la base profunda bajo tensión; focalizar la descarga en erectores del lado posteriorizado.",
            "activar": [
                "Goblet Squat profundo con control de presión intraabdominal (PIA)",
                "Side Plank asistida con abducción controlada de cadera superior",
                "Control motor lumbo-pélvico en flexión/extensión coordinada"
            ],
            "criterios_retorno": "Recuperación del juego articular en el Spring Test y flexión de tronco indolora bajo carga progresiva."
        }
    },

    # =========================================================================
    # 5. DISFUNCIONES SACRAS SAGITALES Y UNILATERALES
    # =========================================================================
    "SACRO_FLEXION": {
        "nombre_clinico": "Sacro en Flexión Bilateral (Nutación Bilateral Sacra)",
        "categoria": "Disfunción Sacra Sagital Bilateral",
        "eje_movimiento": "Eje Transverso Medio (S2) / Respiratorio Axial",
        "criterios_diagnosticos": {
            "eias": "Nivelada / Simétrica",
            "eips": "Nivelada / Simétrica",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Bilateral profundo (Base anterior y profunda bilateralmente)",
            "ail": "Ápex postero-superior bilateral / Superficial bilateral",
            "maleolo_supino": "Simétrico (Maléolos sin cambios)",
            "long_sitting": "Sin dismetría dinámica significativa",
            "pierna_supino_prono": "Maléolos sin cambios en supino ni prono",
            "spring_test": "Rígido a la extensión lumbosacra",
            "tejidos_blandos": "Tensión bilateral en ligamentos sacrotuberosos; hiperlordosis lumbosacra",
            "hallazgos": "Base anterior y profunda bilateralmente, ápex postero-superior, sulcus bilateral profundo, maléolos sin cambios."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste de Desnutación Sacra Bilateral (Pull o Push)",
            "posicion_paciente": "Decúbito prono con paciente en posición neutra o sobre antebrazos (esfinge).",
            "pcc": "Base de la mano / pisiforme o eminencia hipotenar bilateral.",
            "pcp": "Base sacra con técnica pull, o ápex por debajo de la línea de EIPS con push.",
            "linea_correccion": "PA + SI (orientado a llevarlo a extensión / desnutación).",
            "advertencia": "Evitar hiperextensión lumbar forzada en pacientes con estenosis canalicular o espondilolistesis."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro en Flexión Bilateral (Fred Mitchell Sr.)",
            "posicion": "Decúbito prono en posición de esfinge apoyado en antebrazos.",
            "musculo_motor": "Erectores espinales lumbosacros y multífidos.",
            "accion": "El paciente realiza una inhalación profunda y contracción isométrica extensora resistida al 20% por 7-10 s.",
            "fase_post": "En exhalación completa, profundizar el empuje en ápex sacro hacia anterior (PA) para llevar la base a extensión (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Ligamentos sacrotuberosos bilaterales",
                "Multífidos lumbares bajos",
                "Masa erectora lumbar baja"
            ],
            "precaucion_reactiva": "Respetar la hiperlordosis reactiva; no forzar empujes directos sobre bases sacras profundas sin descompresión.",
            "activar": [
                "Transverso del abdomen en decúbito prono",
                "Glúteo mayor bilateral con retroversión activa",
                "Core antilordótico funcional"
            ],
            "criterios_retorno": "Simetría en sulcus bilaterales y recuperación de movilidad lumbosacra indolora en flexión/extensión."
        }
    },

    "SACRO_EXTENSION": {
        "nombre_clinico": "Sacro en Extensión Bilateral (Contranutación Bilateral Sacra)",
        "categoria": "Disfunción Sacra Sagital Bilateral",
        "eje_movimiento": "Eje Transverso Medio (S2)",
        "criterios_diagnosticos": {
            "eias": "Nivelada / Simétrica",
            "eips": "Nivelada / Simétrica",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Bilateral superficial (Base postero-superior)",
            "ail": "Ápex antero-inferior bilateral / Profundo bilateral",
            "maleolo_supino": "Simétrico (Maléolos sin cambios)",
            "long_sitting": "Sin dismetría dinámica",
            "pierna_supino_prono": "Simétrico en supino y prono",
            "spring_test": "Positivo franco (Bloqueo rígido en tabla de madera / rectificación lumbar)",
            "tejidos_blandos": "Tensión en ligamentos sacroilíacos dorsales y rectificación lumbosacra",
            "hallazgos": "Base postero-superior, ápex antero-inferior, sulcus superficial bilateral."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo de Nutación en Prono",
            "posicion_paciente": "Decúbito prono con cojín pélvico para posicionar la columna lumbosacra en neutro.",
            "pcc": "Talón de la mano o eminencia tenar/hipotenar reforzada.",
            "pcp": "Base sacra, sobre el nivel de las espinas en la línea media.",
            "linea_correccion": "PA puro, sin lateralidad.",
            "advertencia": "Mantener el vector estrictamente en la línea media sagital sin desvío lateral para no inducir torsión sacra."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro en Extensión Bilateral (Fred Mitchell Sr.)",
            "posicion": "Decúbito prono o posición cuadrúpeda neutra con retroversión controlada.",
            "musculo_motor": "Diafragma y musculatura espiratoria accesoria profunda.",
            "accion": "Espiración forzada del paciente mientras se mantiene compresión firme sobre base sacra al 20% por 7-10 s.",
            "fase_post": "En la siguiente inspiración, acompañar la nutación sacra hacia anterior e inferior (PA puro) (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Erectores espinales lumbares hiperreactivos",
                "Fascia toracolumbar lumbosacra",
                "Ligamento sacroilíaco dorsal"
            ],
            "precaucion_reactiva": "Descartar hernia discal posterior extruida sensible a la flexión lumbosacra sostenida.",
            "activar": [
                "Erectores lumbares profundos en neutro",
                "Puente pélvico con anteversión suave coordinada",
                "Reeducación del ritmo lumbopélvico"
            ],
            "criterios_retorno": "Restauración de la lordosis fisiológica lumbar y Spring Test elástico normal."
        }
    },

    "SACRO_ANTERO_INFERIOR_D": {
        "nombre_clinico": "Sacro Antero-Inferior Derecho (Flexión Unilateral / Anterioridad Derecha)",
        "categoria": "Disfunción Sacra Unilateral Asimétrica",
        "eje_movimiento": "Eje Oblicuo o Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Sulcus derecho profundo",
            "ail": "ILA izquierdo superficial",
            "maleolo_supino": "Pierna funcionalmente larga derecha",
            "long_sitting": "Pierna larga derecha que modula sin inversión torsional pura",
            "pierna_supino_prono": "Pierna funcionalmente larga derecha en supino",
            "spring_test": "Conserva elasticidad relativa con asimetría local",
            "tejidos_blandos": "Piramidal derecho tenso (hipertonía marcada homolateral a la base profunda)",
            "hallazgos": "Sulcus derecho profundo, ILA izquierdo superficial, pierna funcionalmente larga derecha, piramidal derecho tenso."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo sobre ILA Contralateral",
            "posicion_paciente": "Decúbito prono; pierna derecha en ligera abducción y rotación externa.",
            "pcc": "Pisiforme / eminencia hipotenar con mano caudal.",
            "pcp": "ILA izquierdo (ALI).",
            "linea_correccion": "PA + LM (lateral a medial), con codo pegado al cuerpo.",
            "advertencia": "Mantener el codo pegado al cuerpo para asegurar la dirección exacta de lateral a medial y evitar torsión indebida."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro Antero-Inferior Derecho",
            "posicion": "Decúbito prono con extremidad derecha en abducción moderada.",
            "musculo_motor": "Músculo piramidal derecho y rotadores externos de cadera.",
            "accion": "El paciente intenta aducir suavemente la pierna derecha al 20% por 7-10 s contra la resistencia manual fija del terapeuta.",
            "fase_post": "En relajación, empuje PA sostenido sobre ILA izquierdo para reequilibrar el sacro a la neutralidad (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Músculo piramidal derecho (compresión isquémica y liberación neuromuscular)",
                "Ligamento sacrotuberoso derecho",
                "Pelvitrocantéreos homolaterales"
            ],
            "precaucion_reactiva": "Evitar compresión profunda sobre el foramen infrapiriforme para proteger el nervio ciático derecho.",
            "activar": [
                "Piramidal y rotadores externos contralaterales (izquierdos)",
                "Glúteo medio derecho en apoyo monopodal",
                "Estabilizadores lumbopélvicos en plano frontal"
            ],
            "criterios_retorno": "Nivelación de surcos sacros, AIL simétrico en decúbito prono y tono piramidal normalizado."
        }
    },

    "SACRO_ANTERO_INFERIOR_I": {
        "nombre_clinico": "Sacro Antero-Inferior Izquierdo (Flexión Unilateral / Anterioridad Izquierda)",
        "categoria": "Disfunción Sacra Unilateral Asimétrica",
        "eje_movimiento": "Eje Oblicuo o Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Sulcus izquierdo profundo",
            "ail": "ILA derecho superficial",
            "maleolo_supino": "Pierna funcionalmente larga izquierda",
            "long_sitting": "Pierna larga izquierda con modulación sin inversión patológica",
            "pierna_supino_prono": "Pierna funcionalmente larga izquierda en supino",
            "spring_test": "Conserva elasticidad relativa con asimetría local",
            "tejidos_blandos": "Piramidal izquierdo tenso (hipertonía homolateral a la base profunda)",
            "hallazgos": "Sulcus izquierdo profundo, ILA derecho superficial, pierna funcionalmente larga izquierda, piramidal izquierdo tenso."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo sobre ILA Contralateral",
            "posicion_paciente": "Decúbito prono; pierna izquierda en ligera abducción y rotación externa.",
            "pcc": "Pisiforme / eminencia hipotenar con mano caudal.",
            "pcp": "ILA derecho (ALI).",
            "linea_correccion": "PA + LM (lateral a medial), con codo pegado al cuerpo.",
            "advertencia": "Mantener el codo pegado al cuerpo para asegurar la dirección exacta de lateral a medial y evitar torsión indebida."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro Antero-Inferior Izquierdo",
            "posicion": "Decúbito prono con extremidad izquierda en abducción moderada.",
            "musculo_motor": "Músculo piramidal izquierdo y rotadores externos de cadera.",
            "accion": "El paciente intenta aducir suavemente la pierna izquierda al 20% por 7-10 s contra la resistencia manual del examinador.",
            "fase_post": "En relajación, empuje PA sostenido sobre ILA derecho para reequilibrar el sacro a la neutralidad (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Músculo piramidal izquierdo (técnicas de presión neuromuscular)",
                "Ligamento sacrotuberoso izquierdo",
                "Pelvitrocantéreos homolaterales"
            ],
            "precaucion_reactiva": "Proteger el nervio ciático izquierdo de presiones focales profundas en escotadura ciática.",
            "activar": [
                "Piramidal y rotadores externos derechos",
                "Glúteo medio izquierdo",
                "Core lumbo-pélvico en cadena cerrada"
            ],
            "criterios_retorno": "Nivelación de surcos sacros, AIL simétrico en decúbito prono y tono piramidal normalizado."
        }
    },

    "SACRO_POSTERO_SUPERIOR_I": {
        "nombre_clinico": "Sacro Postero-Superior Izquierdo (Extensión Unilateral / Posterioridad Izquierda)",
        "categoria": "Disfunción Sacra Unilateral Asimétrica",
        "eje_movimiento": "Eje Oblicuo o Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Base sacra izquierda superficial / Sulcus plano",
            "ail": "ILA derecho profundo",
            "maleolo_supino": "Maléolo izquierdo más alto en supino (pierna corta funcional)",
            "long_sitting": "Asimetría maleolar concordante",
            "pierna_supino_prono": "Maléolo izquierdo más alto en supino",
            "spring_test": "Rígido en la base izquierda (resistencia aumentada)",
            "tejidos_blandos": "Tensión y espasmo reactivo en multífidos izquierdos L5-S1",
            "hallazgos": "Base sacra izquierda superficial, ILA derecho profundo, maléolo izquierdo más alto en supino."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo sobre Base Sacra en Prono",
            "posicion_paciente": "Decúbito prono; ligera rotación interna del fémur izquierdo para abrir la articulación sacroilíaca posterior.",
            "pcc": "Pisiforme / talón de la mano del clínico.",
            "pcp": "Medial a la EIPS izquierda, por encima del eje de flexión.",
            "linea_correccion": "PA + ML + de craneal a caudal (arriba hacia abajo).",
            "advertencia": "Asegurar el vector cráneo-caudal para anteriorizar y descender la base sacra fijada en superioridad."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro Postero-Superior Izquierdo",
            "posicion": "Decúbito prono o lateral derecho con extremidad inferior izquierda colgando en ligera extensión.",
            "musculo_motor": "Multífidos izquierdos y glúteo mayor.",
            "accion": "Contracción isométrica suave contra resistencia por 7-10 s al 20% de fuerza.",
            "fase_post": "En relajación, empuje mantenido PA + caudal sobre la base sacra izquierda para anteriorizarla (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Multífidos izquierdos L5-S1",
                "Ligamento sacroilíaco posterior izquierdo",
                "Fascia toracolumbar ipsilateral"
            ],
            "precaucion_reactiva": "Descartar radiculopatía compresiva L5-S1 homolateral antes de realizar empujes cráneo-caudales.",
            "activar": [
                "Extensores contralaterales",
                "Glúteo mayor izquierdo en cadena cinética cerrada",
                "Core antirotacional"
            ],
            "criterios_retorno": "Surco sacro izquierdo profundo simétrico y prueba del resorte positiva elástica."
        }
    },

    "SACRO_POSTERO_SUPERIOR_D": {
        "nombre_clinico": "Sacro Postero-Superior Derecho (Extensión Unilateral / Posterioridad Derecha)",
        "categoria": "Disfunción Sacra Unilateral Asimétrica",
        "eje_movimiento": "Eje Oblicuo o Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Base sacra derecha superficial / Sulcus plano",
            "ail": "ILA izquierdo profundo",
            "maleolo_supino": "Maléolo derecho más alto en supino (pierna corta funcional)",
            "long_sitting": "Asimetría maleolar concordante",
            "pierna_supino_prono": "Maléolo derecho más alto en supino",
            "spring_test": "Rígido en la base derecha (resistencia aumentada)",
            "tejidos_blandos": "Tensión y espasmo reactivo en multífidos derechos L5-S1",
            "hallazgos": "Base sacra derecha superficial, ILA izquierdo profundo, maléolo derecho más alto en supino."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo sobre Base Sacra en Prono",
            "posicion_paciente": "Decúbito prono; ligera rotación interna del fémur derecho para abrir la articulación sacroilíaca posterior.",
            "pcc": "Pisiforme / talón de la mano del clínico.",
            "pcp": "Medial a la EIPS derecha, por encima del eje de flexión.",
            "linea_correccion": "PA + ML + de craneal a caudal (arriba hacia abajo).",
            "advertencia": "Asegurar el vector cráneo-caudal para anteriorizar y descender la base sacra fijada en superioridad."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro Postero-Superior Derecho",
            "posicion": "Decúbito prono o lateral izquierdo con extremidad inferior derecha en ligera extensión.",
            "musculo_motor": "Multífidos derechos y glúteo mayor.",
            "accion": "Contracción isométrica suave contra resistencia por 7-10 s al 20% de fuerza.",
            "fase_post": "En relajación, empuje mantenido PA + caudal sobre la base sacra derecha para anteriorizarla (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Multífidos derechos L5-S1",
                "Ligamento sacroilíaco posterior derecho",
                "Fascia toracolumbar ipsilateral"
            ],
            "precaucion_reactiva": "Descartar radiculopatía compresiva L5-S1 homolateral antes de realizar empujes cráneo-caudales.",
            "activar": [
                "Extensores contralaterales",
                "Glúteo mayor derecho en cadena cinética cerrada",
                "Core antirotacional"
            ],
            "criterios_retorno": "Surco sacro derecho profundo simétrico y prueba del resorte positiva elástica."
        }
    },

    "SACRO_FLEXION_UNILATERAL": {
        "nombre_clinico": "Sacro en Flexión Unilateral (Sacro Inclinado / Unilateral Flexed Sacrum)",
        "categoria": "Disfunción Sacra Unilateral Sagital",
        "eje_movimiento": "Eje Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Base profunda del lado hipomóvil",
            "ail": "ILA más bajo del lado hipomóvil",
            "maleolo_supino": "Sin dismetría primaria significativa o discreto alargamiento homolateral",
            "long_sitting": "Sin inversión rotacional patológica",
            "pierna_supino_prono": "Simetría maleolar relativa",
            "spring_test": "Resistencia local en la base homolateral, elástico en contralateral",
            "tejidos_blandos": "Sin bandas tensas (piramidal normotónico, sin espasmo característico de torsión)",
            "hallazgos": "Base profunda e ILA más bajo del lado hipomóvil, sin bandas tensas."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo Unilateral en Prono (S1-S2 o ILA)",
            "posicion_paciente": "Decúbito prono con extremidades inferiores alineadas y relajadas.",
            "pcc": "Eminencia hipotenar de la mano de contacto.",
            "pcp": "S1-S2 con eminencia hipotenar, o ILA en decúbito prono.",
            "linea_correccion": "Lateral a medial con torque hacia arriba / ILA de abajo hacia arriba.",
            "advertencia": "Evitar palancas de torsión lumbar durante el impulso axial; focalizar el contacto en S1-S2 o ILA."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro en Flexión Unilateral",
            "posicion": "Decúbito prono con abducción de la extremidad del lado afecto.",
            "musculo_motor": "Músculos del diafragma pélvico y coccígeo.",
            "accion": "Contracción isométrica suave en fase espiratoria por 7-10 s al 20%.",
            "fase_post": "En la inspiración profunda, guiar el ILA cranealmente para desnutar el segmento fijo (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Ligamento sacroilíaco anterior homolateral",
                "Fascia perisacra homolateral",
                "Ligamento sacrotuberoso inferior"
            ],
            "precaucion_reactiva": "Confirmar ausencia de bandas tensas en el músculo piramidal para descartar torsión sacra verdadera.",
            "activar": [
                "Multífidos segmentarios lumbosacros",
                "Transverso del abdomen",
                "Glúteo medio homolateral"
            ],
            "criterios_retorno": "Nivelación de altura del ILA y equiparación de profundidad de la base sacra."
        }
    },

    "SACRO_EXTENSION_UNILATERAL": {
        "nombre_clinico": "Sacro en Extensión Unilateral (Sacro Posteriorizado Unilateral / Unilateral Extended Sacrum)",
        "categoria": "Disfunción Sacra Unilateral Sagital",
        "eje_movimiento": "Eje Transverso Unilateral",
        "criterios_diagnosticos": {
            "eias": "Nivelada",
            "eips": "Nivelada",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Neutro",
            "surco_sacro": "Base más posterior del lado hipomóvil / Sulcus superficial",
            "ail": "ILA más craneal del lado hipomóvil",
            "maleolo_supino": "Sin dismetría primaria o discreto acortamiento homolateral",
            "long_sitting": "Sin inversión rotacional patológica",
            "pierna_supino_prono": "Simetría maleolar relativa",
            "spring_test": "Negativo / Rígido localizado en la base sacra afectada",
            "tejidos_blandos": "Sin bandas tensas (piramidal normotónico, sin contractura espasmódica de torsión)",
            "hallazgos": "Base más posterior e ILA más craneal del lado hipomóvil, sin bandas tensas."
        },
        "ajuste_articular": {
            "tecnica": "Ajuste Directo sobre ILA / ALI en Prono",
            "posicion_paciente": "Decúbito prono con ligera abducción y rotación externa femoral homolateral.",
            "pcc": "Eminencia tenar o hipotenar de la mano caudal.",
            "pcp": "Lateral al ILA (ALI).",
            "linea_correccion": "Lateral a medial (LM), descendiendo el ILA.",
            "advertencia": "Evitar contacto directo sobre el cóccix o el hiato sacro; el contacto debe ser estrictamente en el ILA lateral."
        },
        "tecnica_met": {
            "nombre": "MET para Sacro en Extensión Unilateral",
            "posicion": "Decúbito lateral sobre el lado hipomóvil con cadera flexionada >90° para abrir la articulación posterior.",
            "musculo_motor": "Multífidos y glúteo mayor.",
            "accion": "Contracción isométrica resistida de extensión al 20% por 7-10 s.",
            "fase_post": "En relajación, empuje continuo PA sobre la base sacra posteriorizada para llevarla a neutro (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Ligamento sacroilíaco posterior del lado afecto",
                "Fascia lumbosacra ipsilateral",
                "Fibras profundas de multífidos lumbosacros"
            ],
            "precaucion_reactiva": "Proteger las ramas cutáneas dorsales sacras de presiones excesivas directas sobre el ILA.",
            "activar": [
                "Estabilizadores lumbopélvicos en cadena cerrada",
                "Core rotacional funcional",
                "Glúteo mayor en rango funcional completo"
            ],
            "criterios_retorno": "Simetría palpatoria de ambos ILA en prono y bipedestación con resolución de la rigidez en base sacra."
        }
    }
}


def get_disfuncion_info(clave_disfuncion: str) -> Dict[str, Any]:
    """Retorna la ficha clínica biomecánica estandarizada para una disfunción dada."""
    return CLINICAL_KNOWLEDGE_BASE.get(clave_disfuncion, {})