from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item, List


def home_page(request):
    return render(request, "home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", context={"items": items})


def new_list(request):
    if request.method == "POST":
        list_ = List.objects.create()
        Item.objects.create(text=request.POST.get("item_text", ""), list=list_)
        return redirect("/lists/temporary_unique_url_for_a_list/")
