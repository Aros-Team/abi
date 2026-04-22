from app.agents.skills.registry import skill_registry, Skill

skill_registry.register(
    Skill(
        id="admin_pareto",
        name="Análisis de Pareto para priorización",
        domain="administration",
        trigger_keywords=[
            "prioridad",
            "urgente",
            "cual es mas importante",
            "orden de importancia",
            "que primero",
            "pareto",
            "80-20",
            "20-80",
            " ABC",
        ],
        description="Aplicar la regla 80/20 para identificar los pocos vitales que generan la mayor parte del impacto.",
        content="""## Skill: Análisis de Pareto (80/20)

### Cuándo activarla
Cuando el usuario pregunta sobre prioridades, qué problemas resolver primero, o qué elementos generan más impacto.

### Cómo pensar
1. Identifica la métrica de impacto relevante (ventas, costos, quejas, tiempo perdido).
2. Ordena los elementos de mayor a menor según esa métrica.
3. Acumula el porcentaje del total y marca el punto donde se alcanza el ~80%.
4. Esos pocos elementos (~20%) son las prioridades claras.

### Ejemplo aplicado a restaurante
- "El 20% de los productos generan el 80% de los ingresos"
- "El 20% de los insumos generan el 80% del costo"

### Formato de respuesta
Presenta primero las 1-3 prioridades con su porcentaje acumulado. Luego lista el resto con valores individuales.
""",
    )
)

skill_registry.register(
    Skill(
        id="admin_kpi_dashboard",
        name="KPIs y Dashboard de gestión",
        domain="administration",
        trigger_keywords=[
            "kpi",
            "indicador",
            "métrica",
            "dashboard",
            "scorecard",
            "balanced score",
            "objetivos",
            "meta",
            "resultado",
            "rendimiento",
            "desempeño",
        ],
        description="Estructurar y calcular los principales KPIs operativos y financieros de un restaurante.",
        content="""## Skill: KPIs de Restaurante

### KPI Operativos (prioridad alta)
- Ticket promedio = Ingresos totales / Número de pedidos
- Ocupación = Mesas ocupadas / Mesas totales × 100
- Tiempo promedio de pedido = Hora del pedido → Hora de entrega
- Rotación de mesa = Ingresos / (Mesas × Horas abiertas)
- Tasa de cancelación = Pedidos cancelados / Pedidos totales × 100

### KPI de Proveedores
- Entregas a tiempo = Órdenes completadas / Órdenes totales × 100
- Lead time promedio = Días entre orden y recepción

### Cómo interpretar
- Si el ticket promedio baja sin motivo claro → revisar estructura de menú o precios
- Si ocupación > 90% consistently → considerar ampliar capacidad
- Si cancelaciones > 5% → investigar causas (calidad, tiempos, precio)

### Formato
Presenta cada KPI con: Valor actual, Comparación (vs período anterior), Tendencia (↑↓→)
""",
    )
)

skill_registry.register(
    Skill(
        id="admin_swot",
        name="Análisis FODA/SWOT estratégico",
        domain="administration",
        trigger_keywords=[
            "foda",
            "swot",
            "fortaleza",
            "debilidad",
            "oportunidad",
            "amenaza",
            "estrategia",
            "analisis estrategico",
            "analisis competitivo",
            "competencia",
        ],
        description="Realizar un análisis FODA estructurado del restaurante o un área específica.",
        content="""## Skill: Análisis FODA para Restaurantes

### Estructura
- **F (Fortalezas)**: Lo que el restaurante hace bien. Recursos únicos, ubicación, marca, equipo.
- **O (Debilidades)**: Lo que necesita mejorar. Procesos, espacio, tecnología, capacitación.
- **T (Oportunidades)**: Factores externos favorables. Tendencias, demanda creciente, aliados, tecnología nueva.
- **A (Amenazas)**: Factores externos adversos. Competencia, alza de insumos, regulación, rotación de personal.

### Cómo aplicar
1. El usuario describe un dilema o decisión -> primero clasificar en FODA
2. Buscar en los datos: ¿qué fortalezas/ex Debilidades se reflejan en los números?
3. Conectar con oportunidades/amenazas del contexto externo

### Formato de respuesta
Presenta como matriz de 4 celdas. Cada celda: máximo 4 puntos. Cierra con una recomendación estratégicaderived del cruce F+O y D+A.
""",
    )
)

skill_registry.register(
    Skill(
        id="admin_okr",
        name="Sistema OKR para restaurantes",
        domain="administration",
        trigger_keywords=[
            "okr",
            "objetivo",
            "resultado clave",
            "key result",
            "meta trimestral",
            "quarterly",
            "objetivo trimestral",
            "aliniar equipo",
            "aliniar metas",
        ],
        description="Aplicar el framework OKR para establecer y seguir objetivos de equipo.",
        content="""## Skill: OKR para Restaurantes

### Estructura de un OKR
- **O (Objective)**: Qué quieres lograr. Debe ser inspirador, cualitativo, alineado con el equipo.
- **KR (Key Results)**: Medibles, con deadline. Typically 2-4 KRs por O.

### Ejemplo para Cocina
```
O: Reducir tiempos de preparación en hora pico
KR1: Ticket promedio de cocina < 18 min (de 25 min actuales)
KR2: Órdenes que entran en < 15 min: > 85% (de 60% actual)
KR3: Quejas por demora < 2% (de 5% actual)
```

### Proceso
1. Cada inicio de quarter: definir 3-5 O丢人
2. Cada O: 2-4 KRs con línea base y meta
3. Check-in semanal: tracking de KRs
4. End of quarter: scoring (0.0 a 1.0, donde 0.7 = éxito)

### Formato para presentar
Si el usuario quiere definir OKRs: presenta la estructura O / KR1 / KR2 con valores indicativos. Señala qué datos necesitaría confirmar.
""",
    )
)
