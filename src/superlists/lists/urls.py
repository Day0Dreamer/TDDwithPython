from django.conf.urls import url
from lists import views
from lists.views import home_page, view_list, new_list, add_item
from django.urls import include, path

urlpatterns = [
    path("<int:list_id>/", view_list, name="view_list"),
    path("<int:list_id>/add_item/", add_item, name="add_item"),
    path("new/", new_list, name="new_list"),
]
