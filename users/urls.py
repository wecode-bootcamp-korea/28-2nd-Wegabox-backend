from django.urls import path

from users.views import KakaoSignInView

urlpatterns = [
    path('/login',KakaoSignInView.as_view())
]