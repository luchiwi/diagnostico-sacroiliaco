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
        }    },

    # =========================================================================
    # 6. DISFUNCIONES LUMBARES (L1-L5 / L5-S1) - COMPLEJO LUMBOPÉLVICO
    # =========================================================================
    "LUMBAR_FRS_D": {
        "nombre_clinico": "FRS Derecho (L1-L5) — Flexión-Rotación-Inclinación Derecha",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Acoplamiento Facetario Homolateral Fryette II (Flexión + Rotación D + Inclinación D)",
        "criterios_diagnosticos": {
            "eias": "Neutra / Discreta adaptación funcional secundaria",
            "eips": "Neutra / Sin asimetría coxal primaria",
            "cresta": "Discreto ascenso adaptativo homolateral por tensión miofascial",
            "isquion": "Nivelado",
            "sinfisis": "Alineada / Neutra",
            "surco_sacro": "Adaptativo lumbosacro (sin fijación sacra primaria)",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico o mínima falsa pierna funcional",
            "long_sitting": "Sin inversión rotacional coxal",
            "pierna_supino_prono": "Simetría funcional de extremidades",
            "spring_test": "Conservado con restricción localizada lumbosacra",
            "tejidos_blandos": "Espasmo marcado en Psoas mayor derecho, Cuadrado Lumbar homolateral y Multífidos segmentarios derechos; ligamento iliolumbar y supraespinoso bajo tensión",
            "palpacion_clinica": "Apófisis transversa derecha notablemente más posterior y prominente en posición neutra y en flexión de tronco. Apófisis espinosa desviada hacia la izquierda. Al llevar el raquis a extensión (decúbito prono en esfinge), la asimetría transversa empeora severamente al no poder descender la carilla articular izquierda.",
            "dinamica_facetaria": "Restricción de cierre (imbricación) de la carilla articular izquierda en extensión. La faceta articular derecha permanece abierta/en flexión, imposibilitando la convergencia bilateral.",
            "hallazgos": "Transversa derecha posterior en flexión, espinosa a la izquierda, carilla izquierda no cierra en extensión, Psoas e iliolumbar derechos hipertónicos."
        },
        "ajuste_articular": {
            "tecnica": "Puesta en Tensión en Rotación (Lumbar Roll / Side-Posture para FRS)",
            "posicion_paciente": "Decúbito lateral izquierdo (lado de la faceta abierta/cerrada hacia arriba). Cadera y rodilla inferiores extendidas, extremidad superior flexionada con pie en hueco poplíteo para abrir el foramen y focalizar la palanca en el segmento lumbar afectado.",
            "pcc": "Pisiforme / antebrazo en contacto mamilar / proceso transverso.",
            "pcp": "Apófisis mamilar / aspecto lateral de la apófisis espinosa del nivel lumbar afectado.",
            "linea_correccion": "Vector rotatorio con palanca en extensión relativa (desrotación izquierda e inducción de extensión/cierre facetario). Empuje de posterior a anterior y de caudal a craneal.",
            "advertencia": "Monitorear síntomas radiculares. Prohibida manipulación en rotación forzada si existe hernia discal aguda extruida foraminal."
        },
        "tecnica_met": {
            "nombre": "MET Lumbar de Fred Mitchell Sr. para FRS Derecho",
            "posicion": "Decúbito lateral izquierdo. El clínico introduce extensión lumbar desde los miembros inferiores hasta palpar el movimiento en el segmento disfuncional; luego induce rotación de tronco hacia la derecha hasta la barrera motriz.",
            "musculo_motor": "Multífidos rotadores izquierdos y Psoas mayor derecho.",
            "accion": "El paciente realiza una contracción isométrica suave al 20% intentando rotar el tronco hacia la izquierda o flexionar contra la resistencia manual fija del clínico por 7-10 s.",
            "fase_post": "En la relajación completa de 3-5 s, el clínico acompaña el segmento hacia una mayor extensión y rotación izquierda hasta la nueva barrera motriz (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Psoas mayor derecho (liberación fascial profunda en fosa ilíaca/abdomen)",
                "Cuadrado lumbar derecho (técnica de Jones / puntos gatillo miofasciales)",
                "Multífidos lumbares segmentarios derechos (descarga con compresión isquémica)",
                "Fascia toracolumbar y ligamento iliolumbar ipsilateral"
            ],
            "precaucion_reactiva": "Descartar pinzamiento facetario agudo o radiculopatía foraminal L4-L5/L5-S1 antes de aplicar tracción en extensión.",
            "activar": [
                "Transverso del abdomen con control de presión intraabdominal (PIA)",
                "Multífidos lumbares profundos contralaterales (izquierdos)",
                "Glúteo mayor homolateral en cadena cinética cerrada",
                "Disociación lumbopélvica en cuadrupedia (Bird-Dog neutro)"
            ],
            "criterios_retorno": "Simetría palpatoria de transversas en flexión y extensión activa completa sin dolor facetario ni espasmo del psoas."
        }
    },

    "LUMBAR_FRS_I": {
        "nombre_clinico": "FRS Izquierdo (L1-L5) — Flexión-Rotación-Inclinación Izquierda",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Acoplamiento Facetario Homolateral Fryette II (Flexión + Rotación I + Inclinación I)",
        "criterios_diagnosticos": {
            "eias": "Neutra / Adaptativa secundaria",
            "eips": "Neutra / Sin asimetría primaria ilíaca",
            "cresta": "Discreto ascenso adaptativo izquierdo por hipertonía del cuadrado lumbar",
            "isquion": "Nivelado",
            "sinfisis": "Alineada / Neutra",
            "surco_sacro": "Adaptativo simétrico",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico",
            "long_sitting": "Sin inversión dismétrica",
            "pierna_supino_prono": "Longitudes simétricas",
            "spring_test": "Conservado con rigidez focal lumbosacra izquierda",
            "tejidos_blandos": "Espasmo marcado en Psoas mayor izquierdo, Cuadrado Lumbar homolateral y Multífidos segmentarios izquierdos; tensión en ligamentos supraespinoso e interespinoso",
            "palpacion_clinica": "Apófisis transversa izquierda posteriorizada y prominente en neutro y en flexión de tronco. Apófisis espinosa rotada hacia la derecha. Al evaluar en extensión (esfinge o decúbito prono), la prominencia transversa izquierda aumenta notablemente por incapacidad de la carilla articular derecha de cerrar e imbricar.",
            "dinamica_facetaria": "Restricción de cierre (imbricación) de la carilla articular derecha en extensión. La carilla izquierda se mantiene abierta fija en flexión.",
            "hallazgos": "Transversa izquierda posterior en flexión, espinosa a la derecha, carilla derecha no cierra en extensión, Psoas y multífidos izquierdos hipertónicos."
        },
        "ajuste_articular": {
            "tecnica": "Puesta en Tensión en Rotación (Lumbar Roll / Side-Posture para FRS)",
            "posicion_paciente": "Decúbito lateral derecho (lado de la restricción facetaria hacia arriba). Flexión controlada de cadera superior con pie alojado en hueco poplíteo para abrir el foramen intervertebral.",
            "pcc": "Pisiforme / eminencia hipotenar con soporte en antebrazo.",
            "pcp": "Apófisis mamilar / proceso transverso del nivel lumbar en disfunción.",
            "linea_correccion": "Vector rotatorio con inducción de extensión y desrotación derecha. Empuje de posterior a anterior y de caudal a cefálico.",
            "advertencia": "Verificar tolerancia neurológica en miembros inferiores; no forzar la rotación si desencadena dolor ciático irradiado."
        },
        "tecnica_met": {
            "nombre": "MET Lumbar de Fred Mitchell Sr. para FRS Izquierdo",
            "posicion": "Decúbito lateral derecho. El terapeuta posiciona el raquis en extensión relativa hasta el segmento diana y rota el tronco hacia la izquierda hasta contactar la barrera motriz.",
            "musculo_motor": "Multífidos rotadores derechos y Psoas mayor izquierdo.",
            "accion": "El paciente realiza contracción isométrica al 20% intentando rotar hacia la derecha contra resistencia manual firme por 7-10 s.",
            "fase_post": "En relajación (3 s), guiar suavemente el tronco hacia mayor rotación derecha y extensión pasiva ganando la barrera motriz (3 a 5 repeticiones)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Psoas mayor izquierdo",
                "Cuadrado lumbar izquierdo",
                "Multífidos segmentarios lumbares izquierdos",
                "Ligamento iliolumbar izquierdo"
            ],
            "precaucion_reactiva": "Evitar manipulaciones de empuje de alta velocidad en presencia de discopatía lumbosacra con componente inflamatorio agudo.",
            "activar": [
                "Transverso del abdomen y oblicuo interno",
                "Multífidos lumbares profundos derechos",
                "Glúteo mayor izquierdo en cadena cerrada",
                "Estabilidad en bipedestación con control motor antirrotacional"
            ],
            "criterios_retorno": "Extensión lumbar activa simétrica sin apofisalgia transversa ni bloqueo articular en rotación."
        }
    },

    "LUMBAR_ERS_D": {
        "nombre_clinico": "ERS Derecho (L1-L5) — Extensión-Rotación-Inclinación Derecha",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Acoplamiento Facetario Homolateral Fryette II (Extensión + Rotación D + Inclinación D)",
        "criterios_diagnosticos": {
            "eias": "Neutra / Adaptativa",
            "eips": "Neutra",
            "cresta": "Nivelada o discreta elevación ipsilateral",
            "isquion": "Nivelado",
            "sinfisis": "Alineada",
            "surco_sacro": "Adaptativo simétrico",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico",
            "long_sitting": "Sin dismetría dinámica coxal",
            "pierna_supino_prono": "Simétrico en supino y prono",
            "spring_test": "Positivo rígido focal en el segmento lumbosacro derecho",
            "tejidos_blandos": "Espasmo severo y acortamiento del Cuadrado Lumbar derecho, Psoas mayor derecho en tensión reactiva, Multífidos homolaterales e iliocostal; ligamento iliolumbar y ligamento longitudinal anterior bajo alta tensión",
            "palpacion_clinica": "La apófisis transversa derecha se palpa posteriorizada en posición neutra y se vuelve extraordinariamente prominente, rígida y dolorosa al solicitar flexión anterior de tronco. Apófisis espinosa desviada hacia la izquierda. En extensión completa (posición de esfinge), la asimetría transversa disminuye o se simetriza.",
            "dinamica_facetaria": "Restricción de apertura (desimbricación / divergencia) de la carilla articular izquierda en flexión. La carilla derecha se encuentra fija en imbricación/cierre en extensión.",
            "hallazgos": "Transversa derecha marcadamente posterior en flexión, asimetría que mejora en extensión, espinosa a la izquierda, carilla izquierda no abre en flexión, Cuadrado Lumbar y multífidos derechos espásticos."
        },
        "ajuste_articular": {
            "tecnica": "Puesta en Tensión en Rotación con Flexión (Lumbar Roll para ERS)",
            "posicion_paciente": "Decúbito lateral izquierdo (faceta imbricada derecha hacia arriba). Marcada flexión de ambas caderas y rodillas hasta abrir e imbricar el segmento superior, focalizando la flexión en la vértebra disfuncional.",
            "pcc": "Pisiforme / contacto mamilar del terapeuta.",
            "pcp": "Apófisis mamilar derecha / borde inferior del proceso transverso.",
            "linea_correccion": "Vector rotatorio inducido en flexión y desrotación izquierda para forzar la apertura (desimbricación) de la carilla posterior. Empuje de posterior a anterior y de craneal a caudal.",
            "advertencia": "No introducir hiperextensión durante el impulso; la maniobra debe realizarse en estricta flexión lumbopélvica."
        },
        "tecnica_met": {
            "nombre": "MET Lumbar de Fred Mitchell Sr. para ERS Derecho",
            "posicion": "Decúbito lateral izquierdo. Flexión de caderas y rodillas del paciente hasta alcanzar el segmento lumbar bloqueado; rotación de tronco hacia la izquierda para poner en tensión la faceta cerrada.",
            "musculo_motor": "Cuadrado lumbar derecho y multífidos extensores derechos.",
            "accion": "El paciente realiza una suave contracción isométrica intentando extender y rotar el tronco a la derecha contra la resistencia manual fija del clínico por 7-10 s al 20%.",
            "fase_post": "En fase de relajación, flexionar suavemente las piernas y acentuar la rotación de tronco hacia la izquierda para desimbricar la faceta articular (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Cuadrado lumbar derecho (liberación miofascial transversal y presión isquémica)",
                "Multífidos lumbares derechos hipertrofiados / espasmódicos",
                "Erectores espinales lumbares homolaterales",
                "Ligamento iliolumbar fascículo superior e inferior derecho"
            ],
            "precaucion_reactiva": "Descartar síndrome facetario inflamatorio agudo antes de aplicar palancas de torsión en flexión.",
            "activar": [
                "Recto anterior y oblicuos abdominales en flexión controlada",
                "Transverso del abdomen para descompresión lumbar",
                "Glúteo mayor en retroversión activa",
                "Disociación en descarga: Cat-Camel segmentario lumbar"
            ],
            "criterios_retorno": "Flexión lumbar activa indolora con apertura simétrica del espacio interespinoso y prueba del resorte elástica."
        }
    },

    "LUMBAR_ERS_I": {
        "nombre_clinico": "ERS Izquierdo (L1-L5) — Extensión-Rotación-Inclinación Izquierda",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Acoplamiento Facetario Homolateral Fryette II (Extensión + Rotación I + Inclinación I)",
        "criterios_diagnosticos": {
            "eias": "Neutra / Adaptativa",
            "eips": "Neutra",
            "cresta": "Nivelada",
            "isquion": "Nivelado",
            "sinfisis": "Alineada",
            "surco_sacro": "Adaptativo simétrico",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico",
            "long_sitting": "Sin dismetría dinámica",
            "pierna_supino_prono": "Simétrico",
            "spring_test": "Positivo rígido focal izquierdo",
            "tejidos_blandos": "Espasmo severo de Cuadrado Lumbar izquierdo, Psoas mayor izquierdo en tensión reactiva, Multífidos homolaterales e iliocostal; alta tensión en ligamento iliolumbar izquierdo",
            "palpacion_clinica": "La apófisis transversa izquierda se palpa posterior en neutro y se hace notablemente prominente y dolorosa en flexión anterior de tronco. Apófisis espinosa desviada a la derecha. En extensión completa de tronco (posición de esfinge), la asimetría se reduce al converger ambas facetas.",
            "dinamica_facetaria": "Restricción de apertura (desimbricación / divergencia) de la carilla articular derecha en flexión. Faceta izquierda bloqueada en imbricación/extensión.",
            "hallazgos": "Transversa izquierda posterior en flexión, mejora en extensión, espinosa a la derecha, carilla derecha no abre en flexión, Cuadrado Lumbar y multífidos izquierdos espásticos."
        },
        "ajuste_articular": {
            "tecnica": "Puesta en Tensión en Rotación con Flexión (Lumbar Roll para ERS)",
            "posicion_paciente": "Decúbito lateral derecho (lado de la faceta imbricada izquierda hacia arriba). Marcada flexión de ambas caderas y rodillas hasta tensar el nivel segmentario afectado.",
            "pcc": "Pisiforme / eminencia hipotenar del clínico.",
            "pcp": "Apófisis mamilar izquierda / aspecto posterior del proceso transverso.",
            "linea_correccion": "Vector rotatorio con palanca en flexión y desrotación derecha para abrir la carilla articular fija. Empuje de posterior a anterior y de craneal a caudal.",
            "advertencia": "Evitar empujes en hiperextensión que puedan comprimir el foramen o irritar la cápsula facetaria."
        },
        "tecnica_met": {
            "nombre": "MET Lumbar de Fred Mitchell Sr. para ERS Izquierdo",
            "posicion": "Decúbito lateral derecho. Caderas flexionadas a 90° o más hasta focalizar la flexión en el segmento; rotación del tórax hacia la derecha hasta la barrera motriz.",
            "musculo_motor": "Cuadrado lumbar izquierdo y multífidos izquierdos.",
            "accion": "El paciente realiza contracción isométrica al 20% intentando extender y rotar el tronco a la izquierda contra la resistencia inamovible del clínico por 7-10 s.",
            "fase_post": "En relajación, ganar mayor flexión y rotación derecha pasivas para abrir la faceta articular bloqueada (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Cuadrado lumbar izquierdo",
                "Multífidos lumbares izquierdos",
                "Erectores espinales ipsilaterales",
                "Ligamento iliolumbar izquierdo"
            ],
            "precaucion_reactiva": "Proteger la raíz nerviosa emergente homolateral de fuerzas de cizallamiento en rotación.",
            "activar": [
                "Abdominales oblicuos y transverso en flexión",
                "Core antilordótico funcional",
                "Glúteo mayor en retroversión",
                "Disociación en flexión pasiva/activa lumbopélvica"
            ],
            "criterios_retorno": "Flexión de tronco completa sin desviación lateral antiálgica ni dolor facetario focal."
        }
    },

    "LUMBAR_NSR": {
        "nombre_clinico": "NSR Grupo Lumbar — Disfunción Adaptativa Neutra (Fryette I)",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Acoplamiento Facetario Heterolateral Fryette I (Neutro + Inclinación y Rotación a Lados Opuestos)",
        "criterios_diagnosticos": {
            "eias": "Adaptativa / Frecuente asociación con asimetría ilíaca ascendida o torsión sacra",
            "eips": "Adaptativa al plano frontal",
            "cresta": "Elevada en el lado de la concavidad de la curva",
            "isquion": "Nivelado o adaptativo",
            "sinfisis": "Alineada",
            "surco_sacro": "Profundo en el lado convexo rotacional",
            "ail": "Adaptativo",
            "maleolo_supino": "Falsa dismetría secundaria por inclinación pélvica",
            "long_sitting": "Modulación funcional sin inversión rígida pura",
            "pierna_supino_prono": "Dismetría funcional adaptativa",
            "spring_test": "Elasticidad conservada con resistencia moderada a lo largo del grupo lumbar",
            "tejidos_blandos": "Tensión y acortamiento crónico del Cuadrado Lumbar y Psoas en la concavidad; inhibición y elongación de multífidos en la convexidad; tensión en fascia toracolumbar",
            "palpacion_clinica": "Afecta a un grupo de 3 o más vértebras lumbares (típicamente L1-L4 o L2-L5). Las apófisis transversas se palpan prominentes en el lado de la convexidad en posición neutra. La asimetría no se modifica sustancialmente ni en flexión ni en extensión de tronco (característica cardinal de Fryette I).",
            "dinamica_facetaria": "Movimiento multi-segmentario acoplado en neutro: los cuerpos vertebrales rotan hacia la convexidad de la curva y se inclinan hacia la concavidad sin bloqueo articular de una carilla individual.",
            "hallazgos": "Grupo lumbar en curva con transversas prominentes en convexidad en neutro, sin cambio marcado en flexión/extensión, cuadrado lumbar en concavidad acortado."
        },
        "ajuste_articular": {
            "tecnica": "Movilización Articular Segmentaria Rítmica y Desrotación en Grupo",
            "posicion_paciente": "Decúbito lateral con la concavidad de la curva lumbar hacia abajo (apoyada en la camilla) con soporte/rollo lumbar para abrir la curva.",
            "pcc": "Palma de la mano / antebrazo con contacto suave y amplio.",
            "pcp": "Ápice de la convexidad del grupo lumbar sobre procesos transversos.",
            "linea_correccion": "Movilización rítmica grado III-IV de oscilación lateral a medial y desrotación suave en neutro. No se requiere empuje de alta velocidad HVLA monoarticular agresivo.",
            "advertencia": "Al ser una disfunción predominantemente adaptativa, la corrección debe dirigirse a la causa primaria (disfunción sacroilíaca, acortamiento de miembro o compensación descendente torácica)."
        },
        "tecnica_met": {
            "nombre": "MET para Grupo Lumbar NSR (Fred Mitchell Sr.)",
            "posicion": "Sedente o decúbito lateral con el lado de la concavidad hacia arriba. El clínico induce inclinación lateral hacia la convexidad para estirar el lado cóncavo y desrotar el grupo lumbar.",
            "musculo_motor": "Cuadrado lumbar e iliocostal del lado cóncavo.",
            "accion": "El paciente intenta inclinarse suavemente hacia el lado de la concavidad al 20% por 7-10 s contra la resistencia firme del clínico.",
            "fase_post": "En relajación, aumentar la inclinación lateral correctora hacia la convexidad para elongar el grupo vertebral acortado (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Cuadrado lumbar del lado cóncavo",
                "Psoas mayor del lado cóncavo",
                "Fascia toracolumbar y masa común erectora ipsilateral a la concavidad",
                "Ligamento iliolumbar del lado elevado"
            ],
            "precaucion_reactiva": "No realizar empujes HVLA enérgicos directos sobre el ápice de la curva sin antes tratar la pelvis y liberar los tejidos blandos de la concavidad.",
            "activar": [
                "Multífidos lumbares del lado de la convexidad",
                "Estabilizadores lumbopélvicos en plano frontal (Side Plank del lado convexo)",
                "Glúteo medio contralateral en apoyo unipodal",
                "Ejercicios de auto-elongación axial y respiración diafragmática asimétrica"
            ],
            "criterios_retorno": "Nivelación de crestas ilíacas en bipedestación, simetría en la prueba de flexión lateral de tronco y resolución de la curva compensatoria."
        }
    },

    "LUMBAR_ESPONDILOLISTESIS_L5S1": {
        "nombre_clinico": "Espondilolistesis / Inestabilidad Lumbosacra L5-S1",
        "categoria": "Disfunciones Lumbares (L1-L5)",
        "eje_movimiento": "Cizallamiento Sagital Anterior L5 sobre S1 (Inestabilidad / Falla de Contención Pars)",
        "criterios_diagnosticos": {
            "eias": "Anteversión pélvica bilateral adaptativa (ambas EIAS descendidas)",
            "eips": "Ascendidas bilateralmente por hiperlordosis lumbosacra",
            "cresta": "Niveladas simétricas",
            "isquion": "Nivelados",
            "sinfisis": "Descendida bilateralmente",
            "surco_sacro": "Bilateralmente profundo / horizontalización de la base sacra",
            "ail": "Simétrico",
            "maleolo_supino": "Simétrico bilateral",
            "long_sitting": "Sin dismetría funcional",
            "pierna_supino_prono": "Longitudes simétricas",
            "spring_test": "FALSA HIPERMOVILIDAD DOLOROSA / Alerta de cizallamiento anterior inestable",
            "tejidos_blandos": "Espasmo severo protector bilateral de Psoas mayor y masa de erectores lumbares; tensión extrema en ligamento longitudinal anterior; multífidos con pérdida de control motor segmentario",
            "palpacion_clinica": "Signo del escalón palpable (Step-off sign) sobre la línea media espinosa: la apófisis espinosa de L5 se palpa hundida/anteriorizada respecto a S1, generando un escalón palpable inmediato en L4-L5. Dolor a la palpación interespinosa y a la percusión suave.",
            "dinamica_facetaria": "Pérdida de la contención facetaria posterior bilateral (defecto de la pars interarticularis / espondilolisis ístmica o degeneración articular severa). Deslizamiento anterior del cuerpo de L5 sobre la plataforma sacra S1 con disminución del diámetro foraminal en hiperextensión.",
            "hallazgos": "Signo del escalón L5-S1 palpable, dolor a la extensión activa (Stork test positivo), hiperlordosis reactiva, espasmo defensivo de psoas y erectores espinales."
        },
        "ajuste_articular": {
            "tecnica": "CONTRAINDICACIÓN ABSOLUTA DE EMPUJE HVLA POSTERIOR-ANTERIOR (P-A) SOBRE L5",
            "posicion_paciente": "Decúbito supino o decúbito lateral descompresivo con triple flexión de miembros inferiores (postura de Williams).",
            "pcc": "N/A — Maniobra de empuje directo contraindicada.",
            "pcp": "N/A — Prohibido empuje P-A sobre segmento inestable.",
            "linea_correccion": "Descompresión axial suave y movilización pasiva en flexión lumbosacra grado I-II para apertura foraminal sin empuje brusco.",
            "advertencia": "CONTRAINDICADO cualquier empuje de alta velocidad (HVLA) o hiperextensión forzada. Riesgo de incremento del cizallamiento sagital, daño de la cauda equina o neuropraxia de raíces L5/S1."
        },
        "tecnica_met": {
            "nombre": "MET Descompresiva en Flexión Lumbar (Fred Mitchell Sr.)",
            "posicion": "Decúbito supino con caderas y rodillas flexionadas a 90° apoyadas contra el tronco del terapeuta (postura neutra o en leve retroversión pélvica).",
            "musculo_motor": "Músculos abdominales profundos y glúteo mayor.",
            "accion": "El paciente realiza una contracción isométrica suave al 15-20% intentando empujar las rodillas suavemente hacia la extensión contra el pecho del clínico por 7-10 s, induciendo co-activación refleja del core.",
            "fase_post": "En relajación, acompañar pasivamente las rodillas hacia una mayor flexión suave hacia el pecho para abrir los forámenes L5-S1 y desestresar la charnela (3 a 5 ciclos)."
        },
        "abordaje_miofascial": {
            "inhibir": [
                "Psoas mayor bilateral (inhibición posicional suave / Strain-Counterstrain, sin hiperextensión)",
                "Erectores espinales lumbares en espasmo hipertónico defensivo",
                "Fascia toracolumbar lumbosacra",
                "Cuadrado lumbar bilateral"
            ],
            "precaucion_reactiva": "Prohibido estiramiento en extensión de cadera forzada o presión directa profunda sobre el segmento L5.",
            "activar": [
                "Transverso del abdomen y oblicuos internos (control motor antilordótico en supino / Dead Bug modificado)",
                "Glúteo mayor bilateral con retroversión pélvica activa (puente pélvico en rango medio)",
                "Musculatura del suelo pélvico y diafragma en respiración controlada",
                "Reeducación del ritmo lumbopélvico evitando el colapso en hiperextensión"
            ],
            "criterios_retorno": "Control motor de la zona neutra lumbosacra en flexión/extensión sin dolor, ausencia de signos neurológicos y estabilidad dinámica en bipedestación."
        }
    }

}


def get_disfuncion_info(clave_disfuncion: str) -> Dict[str, Any]:
    """Retorna la ficha clínica biomecánica estandarizada para una disfunción dada."""
    return CLINICAL_KNOWLEDGE_BASE.get(clave_disfuncion, {})