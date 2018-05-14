from django.urls import path

from . import views

app_name = "articles"
urlpatterns = [
    # example: /articles/
    path("", views.IndexView.as_view(), name="index"),
    # example: /articles/0
    path("<int:pk>/", views.ArticleView.as_view(), name="article"),
    # exammple: /articles/0/comment
    path('<int:article_id>/comment/', views.comment, name='comment'),
]
