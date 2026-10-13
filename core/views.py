from django.shortcuts import render


def home(request):
    return render(request, 'core/home.html')


def about(request):
    return render(request, 'core/about.html')


def not_found(request, exception):
    return render(request, '404.html', status=404)
