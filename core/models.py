from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from pygments.lexers import get_all_lexers, get_lexer_by_name
from pygments.styles import get_all_styles
from pygments.formatters.html import HtmlFormatter
from pygments import highlight


LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted([(item, item) for item in get_all_styles()])


class Snippet(models.Model):
    creator = models.ForeignKey(User, related_name='snippets', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    highlighted = models.TextField()

    class Meta:
        ordering = ['created']

    def __str__(self):
        return str(self.creator)

    def save(self, *arg, **kwargs):
        lexer = get_lexer_by_name(self.language)
        linenos = 'table' if self.linenos else False
        title = {'title': self.title} if self.title else {}
        formater = HtmlFormatter(style=self.style, linenos=linenos, full=True, **title)
        self.highlighted = highlight(self.code, lexer, formater)
        super().save(*arg, **kwargs)
