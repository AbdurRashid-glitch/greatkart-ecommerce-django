#(context_processor)Python Function - It takes a request as an argument and it will return the dictionary of data as a context
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    return dict(links=links)# it will bring all the categories list and store them into this links variable so that we can use thede links wherewever we want