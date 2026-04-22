from app.agents.skills.registry import Skill, skill_registry
from app.agents.skills.loader import skills_loader

# Import all domains to trigger skill registrations
from app.agents.skills import administration  # noqa: F401
from app.agents.skills import economics  # noqa: F401
from app.agents.skills import leadership  # noqa: F401
from app.agents.skills import innovation  # noqa: F401

__all__ = ["Skill", "skill_registry", "skills_loader"]
