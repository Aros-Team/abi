from collections import defaultdict
from typing import Optional


class SessionStore:
    _sessions: dict[str, list[tuple[str, str]]] = defaultdict(list)
    _max_messages: int = 50

    @classmethod
    def add_message(cls, session_id: str, role: str, content: str):
        cls._sessions[session_id].append((role, content))
        if len(cls._sessions[session_id]) > cls._max_messages * 2:
            cls._sessions[session_id] = cls._sessions[session_id][-cls._max_messages :]
        import logging

        logging.warning(
            f"[SESSION_STORE] add_message: session={session_id}, role={role}, total={len(cls._sessions[session_id])}, sessions_count={len(cls._sessions)}"
        )

    @classmethod
    def get_history(cls, session_id: str) -> list[tuple[str, str]]:
        return cls._sessions.get(session_id, [])

    @classmethod
    def clear_session(cls, session_id: str):
        if session_id in cls._sessions:
            del cls._sessions[session_id]


session_store = SessionStore()
