from django.http import HttpResponse


def home(request):
    return HttpResponse(
        "<h1>Добро пожаловать в Habit Tracker "
        "API!</h1><p>Перейдите на <a href='/swagger/'>документацию API</a>.</p>"
    )
