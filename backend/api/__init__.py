from .agents import router as agents_router
from .auth import router as auth_router
from .commands import router as commands_router
from .conversations import router as conversations_router
from .desktop import router as desktop_router
from .integrations import router as integrations_router
from .memory import router as memory_router
from .privacy import router as privacy_router
from .root import router as root_router
from .schedules import router as schedules_router
from .skills import router as skills_router
from .websocket import router as websocket_router

ALL_ROUTERS = [
    auth_router,
    root_router,
    commands_router,
    conversations_router,
    agents_router,
    memory_router,
    privacy_router,
    skills_router,
    schedules_router,
    integrations_router,
    desktop_router,
    websocket_router,
]
