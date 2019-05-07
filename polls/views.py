from django.shortcuts import render
from src import main


def index(request):
    url = request.GET.get('url_field')

    thread = ''
    if url:
        thread = main.thred(url)
    else:
        print('not URL')

    # return render(request, 'index.html', {'result': thread})
    return render(request, 'index.html')


def redirect(request):
    data = {
        'code': request.GET.get('code')
    }
    # code = request.GET.get('code')
    print(data)
    return render(request, 'redirect.html', data)
