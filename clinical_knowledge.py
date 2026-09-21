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
    }
}


def get_disfuncion_info(clave_disfuncion: str) -> Dict[str, Any]:
    """Retorna la ficha clínica biomecánica estandarizada para una disfunción dada."""
    return CLINICAL_KNOWLEDGE_BASE.get(clave_disfuncion, {})