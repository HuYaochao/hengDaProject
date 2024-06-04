from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def contact(request):
    return render(request, 'contact.html', {
        'active_menu':'contactus',
        'sub_menu':'contact',
    })

def recruit(request):
    return render(request, 'recruit.html', {
        'active_menu':'contactus',
        'sub_menu':'recruit',
    })