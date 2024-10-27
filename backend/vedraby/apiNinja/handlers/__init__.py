from ninja import NinjaAPI

from .user import router as user_router

api = NinjaAPI()
api.add_router("users/", user_router, tags=["users"])
