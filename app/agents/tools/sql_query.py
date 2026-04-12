import re
from typing import Any
from langchain_core.tools import tool

from app.models.business import restaurant_context


class SQLQueryError(Exception):
    pass


def validate_sql(sql: str) -> tuple[bool, str]:
    sql_upper = sql.upper().strip()

    if not sql_upper.startswith("SELECT"):
        return False, "Solo se permiten consultas SELECT"

    forbidden = [
        "INSERT",
        "UPDATE",
        "DELETE",
        "DROP",
        "TRUNCATE",
        "ALTER",
        "CREATE",
        "GRANT",
        "REVOKE",
    ]
    for keyword in forbidden:
        pattern = r"\b" + keyword + r"\b"
        if re.search(pattern, sql_upper):
            return (
                False,
                f"Operación '{keyword}' prohibida. Solo se permiten consultas SELECT",
            )

    for table in restaurant_context.restricted_tables:
        pattern = r"\b" + table + r"\b"
        if re.search(pattern, sql_upper, re.IGNORECASE):
            return False, f"Tabla '{table}' está restringida y no puede ser consultada"

    restricted_fields_flat = []
    for table, fields in restaurant_context.restricted_fields.items():
        for field in fields:
            restricted_fields_flat.append((table, field))

    for table, field in restricted_fields_flat:
        pattern = rf"\b{field}\b"
        if re.search(pattern, sql_upper, re.IGNORECASE):
            return False, f"Campo '{field}' de tabla '{table}' no puede ser consultado"

    if "LIMIT" not in sql_upper:
        sql = sql.strip().rstrip(";") + " LIMIT 100"

    return True, sql


@tool
async def sql_query(sql: str) -> dict[str, Any]:
    """Ejecuta una consulta SQL SELECT en la base de datos del restaurante.

    Solo permite consultas de lectura (SELECT).
    Retorna los resultados en formato estructurado.

    Args:
        sql: Consulta SQL SELECT a ejecutar

    Returns:
        Dict con 'success', 'data', 'row_count' y 'error' (si aplica)
    """
    from app.db.mysql import execute_query

    is_valid, result_or_msg = validate_sql(sql)

    if not is_valid:
        return {
            "success": False,
            "error": result_or_msg,
            "row_count": 0,
            "data": [],
        }

    sql = result_or_msg

    try:
        data = await execute_query(sql)
        return {
            "success": True,
            "data": data,
            "row_count": len(data),
            "error": None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "row_count": 0,
            "data": [],
        }
