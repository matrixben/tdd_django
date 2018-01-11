from django.http import HttpResponse


def home_page():
    pass


def index(request):
    return HttpResponse("<h1>Welcome to the to-do lists app</h1>")
