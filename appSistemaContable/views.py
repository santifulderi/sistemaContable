from django.shortcuts import render


def home(request):
    # items = Items.objects.all()
    return render(request, 'index/index.html')
