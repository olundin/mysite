from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    date_published = models.DateTimeField()
    date_modified = models.DateTimeField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    parent = models.ForeignKey("self", on_delete=models.CASCADE, null=True)
    alias = models.CharField(max_length=50)
    text = models.TextField()
    date_posted = models.DateTimeField()

    def __str__(self):
        return alias + ": " + text[:10]
