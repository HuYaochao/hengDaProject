from django.shortcuts import render # type: ignore
from .models import Doc
from django.core.paginator import Paginator # type: ignore
from django.shortcuts import get_object_or_404 # type: ignore
from pyquery import PyQuery as pq
import numpy as np
import urllib
import json
import cv2
import os
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def download(request):
    submenu = 'download'

    docList = Doc.objects.all().order_by('-publishDate')

    # 分页
    p = Paginator(docList, 5)
    if p.num_pages <= 1:
        pageData = ''
    else:
        page = int(request.GET.get('page', 1))
        docList = p.page(page)
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
        request, 'docList.html', {
            'active_menu': 'service',
            'sub_menu': submenu,
            'docList': docList,
            'pageData': pageData,
        }
    )

def read_file(file_name, size):
    with open(file_name, mode='rb') as fp:
        while True:
            c = fp.read(size)
            if c:
                yield c
            else:
                break
            
from django.shortcuts import get_object_or_404
from django.http import StreamingHttpResponse
import os
def getDoc(request, id):
    doc = get_object_or_404(Doc, id=id)
    update_to, filename = str(doc.file).split('/')
    filepath = '%s/media/%s/%s' % (os.getcwd(), update_to, filename)
    response = StreamingHttpResponse(read_file(filepath, 512))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(
        filename)
    return response



from django.shortcuts import HttpResponse
def platform(requst):
    return render(requst, 'platform.html', {
        'active_menu': 'service',
        'sub_menu': 'platform',
    })

face_detector_path="serviceApp/haarcascade_frontalface_default.xml"
face_detector = cv2.CascadeClassifier(face_detector_path) # 加载人脸检测器

@csrf_exempt #用于规避跨站点请求攻击
def facedetect(request):
    result = {}

    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            img = read_image(stream = request.FILES['image'])
        else:
            result.update({
                '#faceNum':-1,
            })
            return JsonResponse(result)
        
        if img.shape[2] == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 彩色图像转灰度

        #进行人脸检测
        values = face_detector.detectMultiScale(img,
                                                scaleFactor=1.1,
                                                minNeighbors=5, 
                                                minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE
                                            )
        values = [(int(a),int(b),int(a+c),int(b+d))
                for (a,b,c,d) in values]
        result.update({
            '#faceNum':len(values),
            'faces':values,
        })
    return JsonResponse(result)

def read_image(stream=None):
    if stream is not None:
        data_temp = stream.read()
    img = np.asarray(bytearray(data_temp), dtype="uint8")
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    return img

import base64
@csrf_exempt
def facedetectDemo(request):
    result = {}

    if request.method == 'POST':
        if request.FILES.get('image', None) is not None:
            img = read_image(stream = request.FILES['image'])
        else:
            result.update({
                '#faceNum':-1,
            })
            return JsonResponse(result)
        
        if img.shape[2] == 3:
            imgGary = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) # 彩色图像转灰度
        else:
            imgGary = img
        #进行人脸检测
        values = face_detector.detectMultiScale(imgGary,
                                                scaleFactor=1.1,
                                                minNeighbors=5, 
                                                minSize=(30, 30),
                                                flags=cv2.CASCADE_SCALE_IMAGE
                                            )
        values = [(int(a),int(b),int(a+c),int(b+d))
                for (a,b,c,d) in values]
        
        for(w,x,y,z) in values:
            cv2.rectangle(img,(w,x),(y,z),(0,255,0),2)

        retval, buffer_img = cv2.imencode('.jpg', img)
        img64 = base64.b64encode(buffer_img)
        img64 = str(img64, encoding='utf-8')
        result["img64"] = img64

    return JsonResponse(result)