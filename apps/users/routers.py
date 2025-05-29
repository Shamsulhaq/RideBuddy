from rest_framework.routers import SimpleRouter

from .views import (
    AuthViewSet,
    UserViewSet
)

users_router = SimpleRouter()

users_router.register(r'auth', AuthViewSet, basename='auths')
users_router.register(r'users', UserViewSet, basename='users')