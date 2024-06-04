from django.urls import path
from . import views 

app_name = 'aboutApp' #设置应用名

urlpatterns =[
    path('survey/',views.survey,name="survey"), #企业概况
    path('honor/',views.honor,name="honor"), #荣誉资质
]