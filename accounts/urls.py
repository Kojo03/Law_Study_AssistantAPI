from django.urls import path
from . import views
# from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    # Admin user management
    path("admin/users/", views.list_users, name="admin-users"),
    path("admin/users/<int:user_id>/role/", views.update_user_role, name="update-user-role"),
    # JWT Authentication (uncomment after installing djangorestframework-simplejwt)
    # path("jwt/login/", views.CustomTokenObtainPairView.as_view(), name="jwt_login"),
    # path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt_refresh"),
]
