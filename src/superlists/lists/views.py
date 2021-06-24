from django.http import HttpResponse
from django.shortcuts import render, redirect

from lists.models import Item


def home_page(request):
    return render(request, "home.html")


def view_list(request):
    items = Item.objects.all()
    return render(request, "list.html", context={"items": items})


def new_list(request):
    if request.method == "POST":
        Item.objects.create(text=request.POST.get("item_text", ""))
        return redirect("/lists/temporary_unique_url_for_a_list/")
