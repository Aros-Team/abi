from app.agents.skills.registry import skill_registry, Skill

skill_registry.register(
    Skill(
        id="leader_feedback",
        name="Giving de Feedback efectivo",
        domain="leadership",
        trigger_keywords=[
            "feedback",
            "retroalimentación",
            "comunicar error",
            "corregir",
            "hablar con el equipo",
            "charla",
            "reunión",
            "one on one",
            "one-on-one",
            "evaluar",
            "desempeño",
            "revisar",
        ],
        description="Dar retroalimentación constructiva y directa a miembros del equipo.",
        content="""## Skill: Feedback Constructivo (Modelo SBI)

### Estructura SBI
- **S (Situation)**: Describir la situación específica y observada.
  "En la junta de hoy, cuando presentamos los números..."
- **B (Behavior)**: Describir el comportamiento, no la personalidad.
  "El reporte que enviaste tenía 3 errores de cifra..."
- **I (Impact)**: Explicar el impacto de ese comportamiento.
  "Esto hizo que el equipo tomara decisiones con datos incorrectos por 2 horas."

### Cierre con acuerdo
Terminar siempre con: "Me gustaría que para el próximo reporte..." (siguiente paso concreto y verificable)

### Para restaurantes específicamente
- Feedback de servicio en sala: ser específico sobre el momento, no generalizar
- Feedback de cocina: separar la receta del desempeño del cocinero
- Feedback al mesero: conectar calidad de servicio con recompensas (tips,重返)

### Qué NO hacer
- No mezclar personality con behavior ("eres desordenado" → "tu estación estaba desordenada")
- No exaggerar ("siempre" → "esto pasó en las últimas 3 guardias")
- No dar feedback a través de terceros

### Formato para chat del agente
Si el usuario pregunta cómo dar feedback: explicar SBI con ejemplocontextual al restaurante. Cerrar siempre con el siguiente paso concreto.
""",
    )
)

skill_registry.register(
    Skill(
        id="leader_delegation",
        name="Delegación efectiva",
        domain="leadership",
        trigger_keywords=[
            "delegar",
            "delegación",
            "sobrecarga",
            "no tengo tiempo",
            "acosado",
            "apoyar al equipo",
            "responsabilidad",
            " Empowerment",
            "entrenar",
            "capacitar",
        ],
        description="Delegar tareas correctamente para pot Starr al equipo y liberarte.",
        content="""## Skill: Delegación Efectiva

### Por qué delegar
- Un líder que no delega se convierte en botella de cuello.
- El equipo necesita retos para crecer y retener talento.
- Los errores de un líder que no delega cuestan más (micromanagement → alta rotación).

### Tipos de delegación
1. **Dirección**:决定了 quí se hace y cómo → para aprendices o tareas críticas
2. **Cooperación**: Você decide qué, ellos deciden cómo → para equipo con experiencia media
3. **Delegación plena**: Equipo decide todo → para gente de confianza y tareas de bajo riesgo

### Proceso de delegación
1. Elegir la persona adecuada (skill + motivación)
2. Definir el resultado esperado (no el proceso)
3. Establecer checkpoints (hitos de verificación, no control)
4. Dar autoridad para decidir (si no tiene autoridad, no es delegación)
5. Celebrar el éxito y extraer lecciones del error

### Errores comunes
- Delegar sin dar información de contexto → resultados desalineados
- Tomar de vuelta lo delegado cuando las cosas se ponen difíciles
- Checkpoints excesivos que vuelven a ser micromanagement

### Formato
Si el usuario pregunta sobre sobrecarga: identificar las 3 tareas más críticas que solo él puede hacer, el resto → delegar. Definir el tipo de delegación apropiado para cada una.
""",
    )
)

skill_registry.register(
    Skill(
        id="leader_conflict",
        name="Resolución de conflictos en equipo",
        domain="leadership",
        trigger_keywords=[
            "conflicto",
            "problema con",
            "disputa",
            "desacuerdo",
            "clima",
            "convivencia",
            "roces",
            "tensión",
            "encontron",
            "dilación",
        ],
        description="Mediar y resolver conflictos entre miembros del equipo de forma constructiva.",
        content="""## Skill: Resolución de Conflictos

### Modelo de resolución
1. **Escuchar a ambos por separado** (empatía sin juicio)
2. **Identificar interesses, no posiciones**: cada parte tiene una posición ("yo no trabajo con él") pero un interés ("quiero que se me respete").
3. **Buscar intereses comunes**: ¿qué les importa a ambos? (ej: ambiente tranquilo, buen servicio, reconocimiento)
4. **Generar opciones de beneficio mutuo**: brainstorm sin veto inicial
5. **Acuerdo con criterios objetivos**: basado en datos o estándares del restaurante

### Conflictos comunes en restaurantes
- Cocina vs meseros: timing de platos vs servicio en sala
- Turnos: quién cierra/cubre谁的 falta
- Proveedor vs administrador: calidad vs precio

### Qué NO hacer
- No tomar partido prematurely
- No dejar que el conflicto se chronifique (más de 48h sin abordar = crónica)
- No evitar la conversación difícil por "mantener la paz"

### Formato
Si el usuario trae un conflicto: aplicar los 5 pasos, identificar interesses de cada parte, proponer 2-3 soluciones, recomendar cuál es la más viable dados los datos.
""",
    )
)

skill_registry.register(
    Skill(
        id="leader_motivation",
        name="Motivación y retención de equipos",
        domain="leadership",
        trigger_keywords=[
            "motivación",
            "demotivado",
            "equipo",
            "rotación",
            "contratar",
            "retener",
            "talent",
            "empleado",
            "personal",
            "staff",
            "turnover",
            "clima laboral",
            "incentivar",
            "premiar",
        ],
        description="Mantener al equipo motivado y reducir la rotación.",
        content="""## Skill: Motivación y Retención

### Factores de rotación en restaurantes
- Los 3 причины más comunes: horarios inflexibles, falta de reconocimiento, limitado crecimiento.

### Pirámide de motivação (Maslow simplificado para ops)
1. **Sueldo justo** (base)
2. **Horarios previsibles** (necesidad de descanso)
3. **Reconocimiento** (desde "buen trabajo hoy" hasta bonus por desempeño)
4. **Crecimiento** ( quién hier et cómo se desarrolla)
5. **Propósito** (ser parte de algo, no solo un job)

### Acciones concretas
- **Semana 1**: Checkout individual para escuchar quejas y suggestions
- **Mes 1**: Asignar un mentor/buddy a cada nuevo contratado
- **Trimestral**: Recognization lunch para top performers
- **Anual**: Plan de crecimiento con 1-2 habilidades a desarrollar

### Qué decir en feedback de retención
- Nunca prometas crecimiento que no puedas garantizar
- Di " veo potencial en ti para [area]" solo si tienes un plan real
- Cero promesas de salario sin discutir con el owner primero

### Formato
Si el usuario pregunta cómo reducir rotación: identificar el tipo de rotación (voluntaria vs involuntaria), aplicar análisis de причины, proponer acciones de los 5 niveles starting from base.
""",
    )
)
