import socket
from django.shortcuts import render


# Create your views here.
def index(request):
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)

    return render(request, 'index.html', context={'text': '0', 'ipAddress': local_ip})
