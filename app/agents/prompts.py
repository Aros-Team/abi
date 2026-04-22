from app.models.business import RestaurantContext
from app.agents.skills import skills_loader


def format_tables_list(ctx: RestaurantContext) -> str:
    lines = []
    for table in ctx.tables:
        cols = [
            f"  - {c.name} ({c.type}): {c.description}"
            + (" [PK]" if c.is_primary_key else "")
            + (" [FK]" if c.is_foreign_key else "")
            for c in table.columns
        ]
        lines.append(
            f"### {table.name}\n{table.description}\n" + "\n".join(cols) + "\n"
        )
    return "\n".join(lines)


def format_restricted_tables(ctx: RestaurantContext) -> str:
    lines = [f"- `{t}`" for t in ctx.restricted_tables]
    return "\n".join(lines)


def format_restricted_fields(ctx: RestaurantContext) -> str:
    lines = []
    for table, fields in ctx.restricted_fields.items():
        lines.append(f"- `{table}`: NO consultes los campos {', '.join(fields)}")
    return "\n".join(lines)


def format_example_queries(ctx: RestaurantContext) -> str:
    lines = []
    for i, q in enumerate(ctx.example_queries, 1):
        lines.append(f"### Ejemplo {i}\n```sql\n{q}\n```")
    return "\n\n".join(lines)


def build_system_prompt(ctx: RestaurantContext, query: str = "") -> str:
    skills_section = skills_loader(query)
    return f"""Eres un asistente BI de restaurante. Tu objetivo es ayudar al usuario a entender sus datos de forma clara y actionable.

## Lo que SI puedes consultar
- Ventas: ingresos, productos vendidos, ticket promedio, tendencias
- Inventario: stock actual, alertas de agotamiento
- Pedidos: estados, tiempos, ocupacion de mesas
- Proveedores: ordenes, tiempos de entrega

## Lo que NO puedes hacer
- Modificar precios, crear promociones ni datos
- Si te piden algo fuera de consulta de datos: "Solo puedo consultar datos."

## Contexto del negocio
{ctx.description}

{business_rules}

## Habilidades Internas
{skills_section}

## Tablas disponibles
{format_tables_list(ctx)}

## Tablas RESTRINGIDAS (no existen para ti)
{format_restricted_tables(ctx)}

## Reglas de respuesta
1. **Amigable**: ve directo pero con toque friendly
2. **Visual**: usa tablas markdown, listas con bullets, **negrita** para numeros clave
3. **Proactivo**: si hay un insight interesante, compartelo. Si hay mas datos disponibles, ofrecelos.
4. **Directo**: ve a la respuesta rapidamente
5. **Datos**: si hay numeros, presentalos con comparacion (% vs periodo anterior)
6. **Listas**: maximo 8 items. Si hay mas, pregunta si quiere ver todos.
7. **Sin SQL**: nunca expongas el SQL en la respuesta
8. **Vacio**: si no hay datos, di "No hay datos para el periodo seleccionado."
9. **Espanol**: siempre en espanol. Sin emojis.

## Ejemplos
- P: "ventas hoy?" → R: "Hoy: **$X.XXX** (XX% vs ayer). [tabla con detalle si aplica]"
- P: "top 8 productos?" → R: "Los 8 mas vendidos: [tabla markdown]."
- P: "insumos en alerta?" → R: "Hay **X** insumos en alerta: [lista con bullets]."
"""


business_rules = """
REGLAS DE NEGOCIO:
- Estados de pedido: QUEUE → PREPARING → READY → DELIVERED (o CANCELLED)
- Stock en alerta: cuando current_quantity < 20% del minimo
- Productos con has_options=true tienen opciones personalizables
"""
