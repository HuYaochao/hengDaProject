from django.urls import path
from . import views 

app_name = 'serviceApp' #设置应用名

urlpatterns =[
    path('download/',views.download,name="download"), #资料下载
    path('getDoc/<int:id>/',views.getDoc,name="getDoc"),
    path('facedetect/',views.facedetect,name="facedetect"), #人脸识别
    path('platform/',views.platform,name="platform"), #人脸识别开放平台
    path('facedetectDemo/',views.facedetectDemo,name="facedetectDemo"), #人脸识别演示
]


# (12)资料下载：http://127.0.0.1:8000/serviceApp/download/
# (13)人脸识别开放平台：http://127.0.0.1:8000/serviceApp/platform/