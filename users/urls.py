from django.urls import path
from .views import *

urlpatterns = [
    path('create_user', CreateUser.as_view(), name='create_user'),
    path('create_staff', CreateStaff.as_view(), name='create_staff'),
    path('create_super_user', CreateSuperUser.as_view(), name='create_super_user'),
    # path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/', UserLogin.as_view(),name='login'),
]
