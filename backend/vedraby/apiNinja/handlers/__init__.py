from ninja import NinjaAPI

from .user import router as user_router
from .authentication import router as authentication_router

api = NinjaAPI()
api.add_router("users/", user_router, tags=["users"])
api.add_router("auth/", authentication_router, tags=["authentication"])
