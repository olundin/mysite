from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render

from .models import Article

# List all articles
def index(request):
    articles_list = Article.objects.order_by("date_published")
    context = {"articles_list": articles_list}
    return render(request, "articles/index.html", context)

# View single article
def article(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    context = {"article": article}
    return render(request, "articles/article.html", context)
