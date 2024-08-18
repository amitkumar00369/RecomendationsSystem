from django.urls import path
from .views import View


urlpatterns = [
    path("recomendedSystem/<str:userId>",View.as_view()),
   

]
