from django.shortcuts import render

#   home
#   categories
#   budgets


def home(request):
    context = {
        'name': 'Stu'
    }
    return render(request, 'main/home.html', context)


def about(request):
    return render(request, 'main/about.html')
