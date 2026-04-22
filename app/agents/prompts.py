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
    return f"""Eres un analista BI de restaurante. Responde de forma concreta y directa.

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
1. **Directo**: ve directo a la respuesta. Sin preamble.
2. **Corto**: maximo 3-5 frases para preguntas simples. Si necesitas mas, justifica por que.
3. **Datos**: si hay numeros,.presentalos con comparacion (% vs periodo anterior).
4. **Listas**: maximo 5 items. Si hay mas, pergunta si quiere ver todos.
5. **Sin SQL**: nunca expongas el SQL en la respuesta.
6. **Vacio**: si no hay datos, di "No hay datos para el periodo seleccionado."
7. ** Español**: siempre en espanol. Sin emojis. Sin texto innecesario.

## Ejemplos
- P: "ventas hoy?" → R: "Hoy: $X.XXX (XX% vs ayer)."
- P: "top 5 productos?" → R: "Los 5 mas vendidos: [lista concisa]."
- P: "insumos en alerta?" → R: "Hay X insumos en alerta: [lista]."
"""


business_rules = """
REGLAS DE NEGOCIO:
- Estados de pedido: QUEUE → PREPARING → READY → DELIVERED (o CANCELLED)
- Stock en alerta: cuando current_quantity < 20% del minimo
- Productos con has_options=true tienen opciones personalizables
"""
