from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _

from mptt.models import MPTTModel, TreeForeignKey

import datetime
# Create your models here.


class DocumentManager(models.Manager):
    def get_query_set(self):
        return super(DocumentManager, self).get_query_set().filter(level=0)


class Modification(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey("Article")

    time = models.DateTimeField(default=datetime.datetime.now)

    def __unicode__(self):
        return u"{} by {} ({})".format(
            self.article,
            self.user,
            self.time.strftime("%m/%d/%Y %H:%M"),
        )


class Article(MPTTModel):
    LEVEL_TO_HEADER_MAP = {
        0: "",
        1: "Article",
        2: "Section",
        3: "",
    }

    parent = TreeForeignKey("self", null=True, blank=True, related_name='children')

    time_created = models.DateTimeField(default=datetime.datetime.now)

    modified_by = models.ManyToManyField(User, through=Modification)

    number = models.IntegerField(null=True, blank=True)
    title = models.CharField(
        max_length=100,
        default="",
        blank=True,
    )
    slug = models.SlugField(null=True, blank=True)
    body = models.TextField(
        default="",
        blank=True,
    )

    objects = models.Manager()
    documents = DocumentManager()

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        unique_together = (('number', 'title', 'level', 'parent'),)

    def __unicode__(self):
        if self.parent is not None:
            if self.title != "":
                return u"{} {}: {}".format(
                    self.LEVEL_TO_HEADER_MAP[self.level],
                    self.number,
                    self.title
                )
            return u"{}: {}".format(self.number, self.body)
        else:
            return u"{}".format(self.title)

    def save(self, *args, **kwargs):
        self.time_modified = datetime.datetime.now()
        if not self.slug:
            self.slug = self.title.replace(' ', '-').lower()
        super(Article, self).save(*args, **kwargs)

    def get_time_last_updated(self):
        """Exploits the tree-like structure of a legal document to find the time
        each section was modified - which is distinct from the time that a section
        itself was modified."""
        if len(self.article_set.all()) == 0:
            return max(map(lambda x: x.time, self.modification_set.all()))

        else:
            return max(map(lambda x: x.get_time_last_updated(), self.article_set.all()))

    @models.permalink
    def get_absolute_url(self):

        return ('legal_document_detail', {
                'slug': self.slug,
            })
