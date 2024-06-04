from django.urls import path
from . import views 

app_name = 'scienceApp' #设置应用名

urlpatterns =[
    path('science/',views.science,name="science"), #)科研基地

]

# (14)科研基地：http://127.0.0.1:8000/scienceApp/science/