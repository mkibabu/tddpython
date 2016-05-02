from django.shortcuts import render

# Create your views here.
def home_page(request):
# render the page, and use the POSTed variable or a blank string
    return render(request, 'home.html', {
        'new_item_text': request.POST.get('item_text', '') 
    })

