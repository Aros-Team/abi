from app.agents.skills.registry import skill_registry, Skill

skill_registry.register(
    Skill(
        id="econ_cost_volume_profit",
        name="Análisis Costo-Volumen-Utilidad (CVU)",
        domain="economics",
        trigger_keywords=[
            "costo fijo",
            "costo variable",
            "margen",
            "contribución",
            "punto equilibrio",
            "break even",
            "utilidad",
            "ganancia",
            "perdio",
            "rentabilidad",
            "cvu",
            "cpv",
        ],
        description="Calcular el punto de equilibrio y margen de contribución del restaurante.",
        content="""## Skill: Análisis Costo-Volumen-Utilidad

### Conceptos clave
- **Costo Fijo**: alquiler, salarios, seguros (no varían con volumen)
- **Costo Variable**: insumos, energía, materiales (sí varían con volumen)
- **Margen de Contribución (MC)**: Precio unitario - Costo variable unitario
- **Punto de Equilibrio**: CF / MC → unidades que нужно vender para cubrir costos

### Para un restaurante
1. Calcular MC por ticket promedio: ticket promedio - costo variable por ticket
2. Estimar CF mensuales (alquiler + planilla + servicios + seguros)
3. Punto de equilibrio = CF mensual / MC por ticket

### Señales críticas
- MC negativo → cada ticket pierde dinero directa. Revisar estructura de costos.
- PE muy alto vs capacidad real → el modelo de negocio no es viable sin cambios.
- Margen de MC < 40% → el restaurante tiene poca holgura para absorbersubidas de insumos.

### Formato de respuesta
Presentar: MC por ticket, CF mensuales, PE en tickets/mes, Utilidad proyectada al X% de ocupación.
""",
    )
)

skill_registry.register(
    Skill(
        id="econ_pricing",
        name="Estrategia de Precios",
        domain="economics",
        trigger_keywords=[
            "precio",
            "pricing",
            "cuanto cobrar",
            "subir precio",
            "bajar precio",
            "elasticidad",
            "competitivo",
            "valor",
            "psicológico",
            "menu engineering",
            "psychological pricing",
        ],
        description="Estrategias de pricing para menú y servicios del restaurante.",
        content="""## Skill: Menu Engineering y Pricing

### Menu Engineering (clasificación de productos)
Clasifica cada plato por:
- **E (Stars)**: Alto margen, alto volmen → mantener, potenciar
- **P (Plow Horses)**: Bajo margen, alto volumen → contener costos, upselling
- **R (R Camel)**: Alto margen, bajo volumen → revisar presentación, promoción
- **D (Dogs)**: Bajo margen, bajo volumen → redeseno o retiro

### Estrategias de pricing
- **Competitivo**: precio al mercado o levemente debajo para ganar market share
- **Valor**: precio bajo con bundle (menú del día) para atraer volumen
- **Premium**: precio alto, calidad percepcia alta, márgenes altos
- **Psicológico**: .99, .95, .90 para percibirse más barato

### Señales en los datos
- Productos con alto volumen y bajo margen → revisar costos de receta
- Productos con bajo volumen y alto margen → mejorar visibilidad, upselling
- Sin productos "Stars" → el menú no está generando valor suficiente

### Formato
Por producto: Clasificación, Precio actual, Coste estimado, Margen real (%), Veces vendido/mes
""",
    )
)

skill_registry.register(
    Skill(
        id="econ_investment",
        name="Evaluación de inversiones",
        domain="economics",
        trigger_keywords=[
            "inversion",
            "roi",
            "retorno",
            "payback",
            "tir",
            "van",
            "npv",
            "irr",
            "valor presente",
            "invertir",
            "proyecto",
            "ampliar",
            "comprar equipo",
            "renovar",
            "remozar",
        ],
        description="Evaluar si una inversión en el restaurante es financieramente viable.",
        content="""## Skill: Evaluación de Inversiones

### Indicadores clave
- **ROI**: (Beneficio neto / Inversión total) × 100
- **Payback**: Tiempo para recuperar la inversión = Inversión / Flujo neto anual
- **VAN (NPV)**: Valor actual de flujos futuros menos inversión inicial (tasa de descuento del negocio)
- **TIR (IRR)**: Tasa donde VAN = 0. Si TIR > costo de oportunidad → viable

### Ejemplo para comprar equipo nuevo
- Inversión: $8,000
- Beneficio anual incremental: $3,200
- Payback = 8,000 / 3,200 = 2.5 años
- ROI = (3,200×5 - 8,000) / 8,000 = 100% en 5 años

### Qué necesitas en los datos
- Inversión inicial
- Beneficio incremental por año (mayores ingresos o menores costos)
- Vida útil del activo
- Tasa de descuento (usar costo de capital o 10-15% para restaurantes)

### Formato de respuesta
Presentar: Inversión, Beneficio/año, Payback (años), ROI 5 años, TIR (%), Veredicto (Viable / Marginal / No viable)
""",
    )
)

skill_registry.register(
    Skill(
        id="econ_supply_chain",
        name="Análisis de Supply Chain",
        domain="economics",
        trigger_keywords=[
            "proveedor",
            "compra",
            "inventario",
            "stock",
            "abastecimiento",
            "cadena de suministro",
            "lead time",
            "eoq",
            "lote optimo",
            "rotacion inventario",
            "inventario",
            "almacen",
        ],
        description="Optimizar la cadena de compras e inventario del restaurante.",
        content="""## Skill: Supply Chain para Restaurantes

### Indicadores clave
- **Lead time**: Días entre que se hace la orden y llega al restaurante
- **Stock de seguridad**: Inventario mínimo que evita quedarse sin insumo crítico
- **Rotación de inventario**: Consumo anual / Stock promedio → más alto = más fresco
- **EOQ (Lote Económico)**: Cantidad óptima por orden = √(2×D×K / h)
  - D = Demanda anual
  - K = Costo de hacer una orden
  - h = Costo de mantener una unidad al año

### Señales críticas en los datos
- Proveedor con lead time > 5 días → mantener más stock de seguridad
- Insumo con rotación < 4/año → riesgo de deterioro o capital inmovilizado
- Muchos proveedores para el mismo insumo → consolidar para negociar mejor precio
- Órdenes con cantidad recibida < ordenada → problemas de calidad o incumplimiento

### Formato
Por insumo clave: Consumo mensual, Lead time promedio, Stock actual, Stock seguridad calculado, EOQ, Frecuencia de orden recomendada
""",
    )
)
