# encoding: utf-8

from django.urls import path
from .views.base import Index

urlpatterns = [
    path('', Index.as_view())
]

