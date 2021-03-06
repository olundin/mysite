from django.db import models
from django.utils import timezone

from articles.utils import markdown_to_html

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_published = models.DateTimeField()
    date_modified = models.DateTimeField()

    def comment_list_top_level(self):
        return Comment.objects.filter(article=self, parent=None)

    def comment_list(self):
        return Comment.objects.filter(article=self)

    def text_html(self):
        """Returns the article text as html (from markdown)"""
        return markdown_to_html(self.text)

    def save(self, *args, **kwargs):
        self.date_modified = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

class CommentManager(models.Manager):
    def create_comment(self, article, parent, alias, text):
        comment = self.create(
            article=article,
            parent=parent,
            alias=alias,
            text=text,
            date_posted=timezone.now()
        )
        return comment


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", related_name="children", on_delete=models.CASCADE, null=True)
    alias = models.CharField(max_length=50)
    text = models.TextField()
    date_posted = models.DateTimeField()

    objects = CommentManager()

    def has_children(self):
        return self.children.count() != 0

    def __str__(self):
        return self.alias + ": " + self.text[:10] + "..."
