from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Article, Comment

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

# Comment on article
def comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        alias = request.POST["alias"]
        text = request.POST["text"]
    except KeyError:
        # Comment form not filled in
        context = {"article": article, "error_message": "Comment information not filled in."}
        return render(request, "articles/article.html", context)
    else:
        parent = None
        comment = Comment.objects.create_comment(
            article,
            parent,
            alias,
            text
        )
        comment.save()
        # Return to article after creating comment
        return HttpResponseRedirect(reverse("articles:article", args=(article.id,)))
