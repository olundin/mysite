from django.urls import path

from . import views

app_name = "articles"
urlpatterns = [
    # example: /articles/
    path("", views.index, name="index"),
    # example: /articles/0
    path("<int:article_id>/", views.article, name="article"),
    # exammple: /articles/0/comment
    path('<int:article_id>/comment/', views.comment, name='comment'),

]
