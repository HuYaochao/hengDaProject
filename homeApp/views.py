from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.db.models import Q
from newsApp.models import MyNews
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from productsApp.models import Product


# Create your views here.

def home(request):
    # 新闻展报
    newList = MyNews.objects.all().filter(~Q(newType='通知公告')).order_by('-publishDate')
    postList = set()
    postNum=0
    for s in newList:
        if s.photo:
            postList.add(s)
            postNum+=1
        if postNum==3:#只保留3个展报图片
            break;
    
    #新闻列表
    if(len(newList)>7):
        newList = newList[0:7]

    #通知公告 最多保留4条
    noteList = MyNews.objects.all().filter(Q(newType='通知公告')).order_by('-publishDate')
    
    if(len(noteList)>4):
        noteList = noteList[0:4]

    #产品列表
    productList = Product.objects.all().order_by('-views')
    if(len(productList)>4):
        productList = productList[0:4]

    
    return render(request, 'home.html',
                  {'active_menu':'home',
                  'newList':newList,
                  'postList':postList,
                  'noteList':noteList,
                  'productList':productList,
                  })