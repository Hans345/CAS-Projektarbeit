import socket
from django.shortcuts import render


# Create your views here.
def index(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('1.1.1.1', 1))
    ip = s.getsockname()[0]

    return render(request, 'index.html', context={'text': '0', 'ipAddress': ip})
