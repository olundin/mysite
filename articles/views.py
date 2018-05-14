from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Article, Comment

class IndexView(generic.ListView):
    template_name = "articles/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        """
        Return all articles (not including those
        set to be published in the future)
        """
        return Article.objects.filter(
            date_published__lte=timezone.now()
        ).order_by("-date_published")


class ArticleView(generic.DetailView):
    model = Article
    template_name = "articles/article.html"


class CommentsView(generic.ListView):
    template_name = "articles/comment_list.html"
    context_object_name = "comment_list"


# Comment on article
def comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    try:
        alias = request.POST["alias"]
        text = request.POST["text"]

        if len(alias) == 0 and len(text) == 0:
            raise ValueError("Name or comment text empty")

    except KeyError:
        # Post data not sent
        context = {"article": article, "danger_message": "There was a problem submitting your comment."}
        return render(request, "articles/article.html", context)
    except ValueError:
        # Comment form not filled in
        context = {"article": article, "warning_message": "Comment information not filled in."}
        return render(request, "articles/article.html", context)
    else:
        parent = None
        if "parent" in request.POST:
            parent = get_object_or_404(Comment, pk=request.POST["parent"])

        comment = Comment.objects.create_comment(
            article,
            parent,
            alias,
            text
        )
        comment.save()
        # Return to article after creating comment
        return HttpResponseRedirect(reverse("articles:article", args=(article.id,)))
