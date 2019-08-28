from django.http import HttpResponseRedirect
from django.shortcuts import render
from flowers.forms import SimpleAddFlowerForm


def add_simple_flower(request):
    if request.method == 'POST':
        form = SimpleAddFlowerForm(request.POST, request.FILES)
        if form.is_valid():
            print(request)
            if 'photo' in request.FILES:
                form.photo = request.FILES['photo']
                handle_uploaded_file(request.FILES['photo'])
            p = form.save(commit=True)
            return HttpResponseRedirect('')
    else:
        form = SimpleAddFlowerForm()
    return render(request, 'flowers/add_simple_flower.html', {'form': form})


def handle_uploaded_file(f):
    with open('d:/name.jpg', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
