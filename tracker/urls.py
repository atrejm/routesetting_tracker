from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path("routesetters/", views.RoutesetterListView.as_view(),name="routesetters"),
    path("routesetters/<int:pk>", views.routesetter_detail_view,name="routesetter_detail"),
    path("boulderchart", views.chart_boulders_view,name="boulderchart"),
    path("add_boulder/<str:zone_name>",views.add_boulder_view,name="add_boulder"),
    path("manage_boulders/<int:pk>",views.manage_boulders,name="manage_boulders"),
    path("edit_zone/<str:zone>", views.edit_zone_view, name="edit_zone"),
    path("add_setter/",views.add_routesetter,name="add_setter"),
    path("archive_confirmation/<str:zone>",views.archive_confirmation,name="archive_confirmation")
]
