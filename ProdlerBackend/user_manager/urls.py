from django.urls import path
from .views import UserView

urlpatterns = [
    path('signup/', UserView.as_view({'post': 'signup'}), name='signup'),
    path('login/', UserView.as_view({'post': 'login'}), name='login'),
]
