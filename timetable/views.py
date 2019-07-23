from django.shortcuts import render

def importasc(request):
    context = {}
    return render(request, 'timetable/import.html', context)

# Create your views here.
