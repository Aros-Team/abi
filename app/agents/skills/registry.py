from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Skill:
    """A callable internal skill for the BI agent."""

    id: str  # unique identifier, e.g. "admin_pareto"
    name: str  # human-readable name
    domain: str  # "administration" | "economics" | "leadership" | "innovation"
    trigger_keywords: list[str]  # words that suggest this skill is needed
    content: str  # full skill text (prompt + rules)
    description: str = ""  # short explanation for the agent

    def matches(self, text: str) -> bool:
        """Return True if the query text suggests this skill is relevant."""
        t = text.lower()
        return any(kw in t for kw in self.trigger_keywords)


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


class _SkillRegistry:
    def __init__(self):
        self._skills: dict[str, Skill] = {}

    def register(self, skill: Skill):
        self._skills[skill.id] = skill

    def get(self, skill_id: str) -> Optional[Skill]:
        return self._skills.get(skill_id)

    def all(self) -> list[Skill]:
        return list(self._skills.values())

    def for_query(self, query: str) -> list[Skill]:
        """Return all skills whose trigger_keywords match the query."""
        return [s for s in self.all() if s.matches(query)]


skill_registry = _SkillRegistry()
