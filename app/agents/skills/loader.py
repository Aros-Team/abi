"""Skills loader: carga skills relevantes según el contexto de la query."""

from app.agents.skills.registry import skill_registry


def skills_loader(query: str) -> str:
    """
    Recibe la query del usuario y retorna el texto de skills
    que deberían estar activas para esta conversación.

    Si no hay match, retorna string vacío.
    """
    matched = skill_registry.for_query(query)

    if not matched:
        return ""

    lines = [
        "## Habilidades Internas Activadas",
        "Usa las siguientes habilidades según corresponda durante la conversación:\n",
    ]

    for skill in matched:
        lines.append(f"### {skill.name}")
        lines.append(skill.content)
        lines.append("")

    return "\n".join(lines)
