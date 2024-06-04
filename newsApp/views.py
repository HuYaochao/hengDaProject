from django.shortcuts import render
from .models import MyNews
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from pyquery import PyQuery as pq

# Create your views here.
def news(request,newName):
    # 解析请求的新闻类型(company-企业要闻、industry-行业新闻、其它-通知公告)
    submenu = newName
    if newName == 'company':
        newName = '公司要闻'
    elif newName == 'industry':
        newName = '行业新闻'
    else:
        newName = '通知公告'

    # 从数据库获取、过滤(newType=newName)和排序(publishDate倒序)数据
    newList = MyNews.objects.all().filter(newType = newName).order_by('-publishDate')
    for mynew in newList:
        html = pq(mynew.description)  # 使用pq方法解析html内容
        mynew.mytxt = pq(html)('p').text()  # 截取html段落文字

    # 分页
    p = Paginator(newList, 5)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        newList = p.page(page)
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False
        total_pages = p.num_pages
        page_range = p.page_range
        if page == 1:
            right = page_range[page:page + 2]
            print(total_pages)
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        elif page == total_pages:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
        else:
            left = page_range[(page - 3) if (page - 3) > 0 else 0:page - 1]
            right = page_range[page:page + 2]
            if left[0] > 2:
                left_has_more = True
            if left[0] > 1:
                first = True
            if right[-1] < total_pages - 1:
                right_has_more = True
            if right[-1] < total_pages:
                last = True
        pageData = {
            'left': left,
            'right': right,
            'left_has_more': left_has_more,
            'right_has_more': right_has_more,
            'first': first,
            'last': last,
            'total_pages': total_pages,
            'page': page,
        }


    return render(
        request, 'newList.html', {
            'active_menu': 'news',
            'sub_menu': submenu,
            'newName': newName,
            'newList': newList,
            'pageData': pageData,
        }
    )


def newDetail(request, id):
    # 使用id从数据库中获取数据
    mynew = get_object_or_404(MyNews,id = id)
    mynew.views += 1
    # 将数据更改保存到数据库中
    mynew.save()
    return render(request, 'newDetail.html', {
        'active_menu': 'news',
        'mynew': mynew,
    })
def search(request):
    keyword = request.GET.get('keyword')
    newlist = MyNews.objects.filter(title__icontains=keyword)
    