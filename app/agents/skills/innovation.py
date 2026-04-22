from app.agents.skills.registry import skill_registry, Skill

skill_registry.register(
    Skill(
        id="inn_design_thinking",
        name="Design Thinking para experiencias",
        domain="innovation",
        trigger_keywords=[
            "diseñar",
            "experiencia",
            "cliente",
            "user experience",
            "ux",
            "service design",
            "journey",
            "customer journey",
            "pain point",
            "diseño experiencia",
            "mejorar servicio",
            "innovar",
        ],
        description="Aplicar design thinking para mejorar la experiencia del comensal.",
        content="""## Skill: Design Thinking para Restaurantes

### Las 5 etapas
1. **Empatizar**: Observe el journey real del cliente (llegada → pedido → consumo → cuenta → salida)
2. **Definir**: Cuál es el pain point más crítico? (cola, espera, confusión menú, cuenta lenta)
3. **Idear**: Brainstorm soluciones sin filtro (dark kitchen, auto-pedido, menú digital, experiencias temáticas)
4. **Prototipar**: Probar la solución con un piloto (un día, una sección, un producto nuevo)
5. **Testear**: Medir NPS, ticket, tiempo, quejas. Iterar.

### Journey del comensal típico
- Reservación → Llegada → Se sentó → Tomar pedido → Espera → Cocina → Servicio → Consumición → Cuenta → Pago → Salida

### Pain points comunes que generan valor
- Tiempo de espera > 10 min para ordenar → reducir con digital menú
- Confusión al pagar → auto-servicio de cuenta
- children sin opciones → rincón infantil o menú kids

### Formato
Si el usuario quiere innovar en experiencia: mapear el journey, identificar los top 3 pain points, proponer 1-2 ideas por pain point, priorizar por facilidad de implementación × impacto.
""",
    )
)

skill_registry.register(
    Skill(
        id="inn_lean_startup",
        name="Lean Startup para validación de novedades",
        domain="innovation",
        trigger_keywords=[
            "validar",
            "probar",
            "testear",
            "experimentar",
            "nuevo producto",
            "nueva idea",
            "lanzar",
            "piloto",
            "mvp",
            "lean",
            "startup",
            "start-up",
            "仮説",
        ],
        description="Validar rápidamente nuevas ideas antes de invertir mucho.",
        content="""## Skill: Lean Startup para Restaurantes

### Concepto MVP (Minimum Viable Product)
La versión más simple de tu idea que te permita aprender algo valioso con la menor inversión.

### Para un restaurante, un MVP puede ser:
- Plato nuevo: ofrecerlo solo en un día específico, solo a客户 que lopidan, sin anunciarlo
- Nueva sección: poner 2-3 mesas en terraza sin inversión mayor
- Nuevo horario: abrir una hora específica por 2 semanas y medir demanda

### Métricas a medir en el MVP
1. **Adopción**: % de clientes que prueban lo nuevo
2. **Satisfacción**: rating o comentario del MVP
3. **Unit Economics**: el MVP genera margen positivo?

### Framework de decisión
- MVP < 2 semanas: si no funciona → pivotar o abandonar
- Si funciona → invertir más y escalar
- Si no está claro → hacer segunda iteración del MVP

### Formato
Si el usuario tiene una idea nueva: definir el MVP más pequeño possible, las 2-3 métricas clave a medir, el timeline de prueba (2-4 semanas), y el criteria de éxito.
""",
    )
)

skill_registry.register(
    Skill(
        id="inn_technology",
        name="Tecnologías emergentes para restaurantes",
        domain="innovation",
        trigger_keywords=[
            "tecnología",
            "digital",
            "app",
            "sistema",
            "software",
            "automatizar",
            "ia",
            "inteligencia artificial",
            "digitalizar",
            " qr",
            "pedido digital",
            "cocina del futuro",
            "future kitchen",
            "robot",
            " automation",
        ],
        description="Conocer las principales tecnologías disponibles para restaurantes y cómo aplicarlas.",
        content="""## Skill: Tecnologías para Restaurantes

### Tecnologías con ROI comprobable para restaurantes

#### Para servicio
- **Menú QR**: elimina impresion, permite upselling dinámico, costo ~$0-50/mes
- **Pedido en mesa (tap-to-order)**: reduce errores y tiempo de espera, mejora NPS
- **Kiosco de autoservicio**: para restaurantes rápidos, reduce costo de mesero

#### Para cocina
- **Pantallas de cocina (KDS)**: muestra pedidos en pantalla, reduce errores × 3
- **POS integrado**: sincroniza front y back of house

#### Para gestión
- **CRM básico**: historial de clientes, NPS, segmentation
- **BI ligero**: dashboards de ventas, costos, inventario en tiempo real
- **AI para predicción**: demanda por hora/día/semana para ajustar staff y stock

#### Para marketing
- **Google Business + Reviews**: gestionar reputation en buscadores
- **Programa de fidelización digital**: basado en teléfono, no tarjeta física

### Criterios de adopción
Priorizar por: ROI rápido (> 2x en 6 meses), baja barrera de entrada, escalabilidad.

### No recomendada (alto riesgo sin validar)
- Robots de cocina (excepto en dark kitchen)
- App propia sin base de clientes establecida
- Implementación ERP completa en < 50 empleados

### Formato
Si el usuario pregunta por tecnología: presentar top 3 opciones por área (servicio, cocina, gestión), con inversión estimada, ROI esperado, y complejidad de implementación (baja/media/alta).
""",
    )
)

skill_registry.register(
    Skill(
        id="inn_sustainability",
        name="Sustentabilidad y diferenciación verde",
        domain="innovation",
        trigger_keywords=[
            "sustentable",
            "sostenible",
            "verde",
            "ambiental",
            "ecológico",
            "residuo",
            "plástico",
            "desperdicio",
            "food waste",
            "huella",
            "carbono",
            "local",
            "trazabilidad",
            "orgánico",
        ],
        description="Estrategias de sustentabilidad que generan valor y diferenciación.",
        content="""## Skill: Sustentabilidad en Restaurantes

### Por qué importa
- 30-40% de la comida en restaurantes termina como desperdicio.
- Los consumidores, especialmente millennials y Gen Z, consideran la sustentabilidad en sus decisiones.
- Reduces costos operativos al reducir desperdicio.

### Las 3 áreas de mayor impacto
1. **Food Waste**:
   - Medir: peso de basura orgánica por semana
   - Plan: batch cooking, porciones ajustables, menú de "aprovechamiento"
   - Residual: compostaje o alimentación animal

2. **Cadena de suministro local**:
   - Beneficio: frescura, reducción de huella de transporte, narrativa para marketing
   - Trade-off: precio puede ser 10-20% mayor pero permite premium

3. **Plásticos de un solo uso**:
   - Reemplazo: empaques compostables, eliminar sorbetes, agua en jarra vs botella
   - Impacto: reduce costo de desechables y mejora imagen de marca

### Iniciativas con ROI rápido
- Menú digital (ahorra $2,000+/año en impresión)
- Jarra de agua default en mesa (reduce compra de botellas)
- Porciones just-size (reduce food waste 15-20%)

### Iniciativas que requieren inversión
- Terraza verde / huerto urbano: alto costo, retorno en experiencia y marketing
- Sistema de compostaje: medio costo, reduce gasto en garbage y puede generar ingreso
- Trazabilidad de proveedores: invierte tiempo, permite premium story

### Formato
Si el usuario pregunta por sustentabilidad: priorizar por impacto ambiental × ROI × complejidad. Presentar 2-3 acciones de quick win y 1-2 de inversión mayor con payback estimado.
""",
    )
)
