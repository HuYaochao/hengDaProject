from django.urls import path
from . import views 

app_name = 'productsApp' #设置应用名

urlpatterns =[
    # path('robot/',views.robot,name="robot"), #)家用机器人
    # path('monitoring/',views.monitoring,name="monitoring"), #智能监控
    # path('face/',views.face,name="face"), #人脸识别解决方案
    path("products/<str:productName>",views.products,name='products'),
    path('productDetail/<int:id>/', views.productDetail, name='productDetail'),
    
]




# (9)家用机器人：http://127.0.0.1:8000/productsApp/robot/
# (10)智能监控：http://127.0.0.1:8000/productsApp/monitoring/
# (11)人脸识别解决方案：http://127.0.0.1:8000/productsApp/face/