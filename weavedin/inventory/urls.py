"""Urls for inventory app."""
from django.conf.urls import url

import views

urlpatterns = [
    url(r'^user/signup/', views.user_signup),
    url(r'^user/login/', views.user_login),

    url(r'^brands/', views.get_brands),
    url(r'^categories/', views.get_categories),

    url(r'^item/create/', views.create_item),
    url(r'^item/get/', views.get_item_list),
    url(r'^item/(?P<item_id>\d+)/get/', views.get_item_details),
    url(r'^item/(?P<item_id>\d+)/update/', views.update_item_details),
    url(r'^item/(?P<item_id>\d+)/delete/', views.delete_item),

    url(r'^item/(?P<item_id>\d+)/variant/create/', views.create_item_variant),
    url(r'^variant/(?P<variant_id>\d+)/update/', views.update_variant_details),
    url(r'^variant/(?P<variant_id>\d+)/delete/', views.delete_variant),

    url(
        r'^variant/(?P<variant_id>\d+)/property/create/',
        views.create_variant_properties),
    url(
        r'^variant-property/(?P<variant_property_id>\d+)/update/',
        views.update_variant_property_details),
    url(
        r'^variant-property/(?P<variant_property_id>\d+)/delete/',
        views.delete_variant_property),

    url(r'^user/actions/', views.get_user_actions),
]
