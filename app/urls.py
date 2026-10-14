from django.urls import path,include
from django.shortcuts import redirect
from core import views
urlpatterns=[path("accounts/",include("django.contrib.auth.urls")),path("",lambda request:redirect("extract")),path("extractiq/",views.extract,name="extract"),path("extractiq/<int:pk>/",views.results,name="results"),path("extractiq/<int:pk>/export/<str:format>/",views.extract_export,name="extract_export")]
