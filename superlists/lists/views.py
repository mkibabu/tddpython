from django.shortcuts import redirect, render
from lists.models import Item

# Create your views here.
def home_page(request):
    # create a new item, and save its text to the list item or a blank string
    if request.method == 'POST':
        # objects.create(attribute=value) is a shortcut to creating and saving a 
        # model instance  without having to call the model constructor or call .save()
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list/')
    return render(request, 'home.html')

def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})

