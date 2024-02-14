from django.urls import path, register_converter
from .converters import DateConverter

from . import views

register_converter(DateConverter, 'date')

urlpatterns = [
    # ex: /polls/
    path("", views.index, name="index"),
    # ex: /polls/5/
    path("<int:question_id>/", views.detail, name="detail"),
    # ex: /polls/5/results/
    path("<int:question_id>/results/", views.results, name="results"),
    # ex: /polls/5/vote/
    path("<int:question_id>/vote/", views.vote, name="vote"),
    path("write", views.write, name="write"),
    path("complete", views.complete, name="complete"),
    path("check", views.check, name="check"),
    path("status", views.status, name="status"),
    path("gpt/<date:mydate>/", views.gpt, name="gpt"),
    path("submit/<int:question_id>/", views.submit, name="submit"),
   ]