import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Article

def create_article(title, text, days):
    """
    Create a article with the given `title` and `text`. Published the
    given number of `days` offset to now (negative for articles published
    in the past, positive for articles that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Article.objects.create(title=title, text=text, date_published=time, date_modified=time)

class ArticlesIndexViewTests(TestCase):
    def test_no_articles(self):
        """
        If no articles exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("articles:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context["article_list"], [])

    def test_past_article(self):
        """
        Articles with a publish date in the past are displayed on
        the index page.
        """
        create_article(title="Past article.", text="Article text", days=-30)
        response = self.client.get(reverse("articles:index"))
        self.assertQuerysetEqual(
            response.context["article_list"],
            ["<Article: Past article.>"]
        )

    def test_future_article(self):
        """
        Articles with a publish date in the future aren't displayed on
        the index page.
        """
        create_article(title="Future article.", text="Article text", days=30)
        response = self.client.get(reverse('articles:index'))
        self.assertContains(response, "No articles are available.")
        self.assertQuerysetEqual(response.context['article_list'], [])

    def test_future_article_and_past_article(self):
        """
        Even if both past and future articles exist, only past articles
        are displayed.
        """
        create_article(title="Past article.", text="Article text", days=-30)
        create_article(title="Future article.", text="Article text", days=30)
        response = self.client.get(reverse('articles:index'))
        self.assertQuerysetEqual(
            response.context['article_list'],
            ['<Article: Past article.>']
        )

    def test_two_past_articles(self):
        """
        The articles index page may display multiple articles.
        """
        create_article(title="Past article 1.", text="Article text", days=-30)
        create_article(title="Past article 2.", text="Article text",days=-5)
        response = self.client.get(reverse('articles:index'))
        self.assertQuerysetEqual(
            response.context['article_list'],
            ['<Article: Past article 2.>', '<Article: Past article 1.>']
        )
