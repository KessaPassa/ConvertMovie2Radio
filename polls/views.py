from django.shortcuts import render
from src import main


def index(request):
    print('インデックス')
    url = request.GET.get('url_field')
    if url:
        main.thred(url)

    return render(request, 'index.html')