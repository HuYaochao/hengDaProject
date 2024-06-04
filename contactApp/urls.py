from django.urls import path
from . import views 

app_name = 'contactApp' #设置应用名

urlpatterns =[
    path('contact/',views.contact,name="contact"), #欢迎咨询
    path('recruit/',views.recruit,name="recruit"), #加入恒达
]

# (4)欢迎咨询：http://127.0.0.1:8000/contactApp/contact/
# (5)加入恒达：http://127.0.0.1:8000/contactApp/recruit/