from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.

from main.models import Dorm

import datetime


class Ballot(models.Model):
    TYPES = (
        ("PL", "Popularity"),
    )

    election = models.ForeignKey('Election', null=True)

    display_position = models.IntegerField(default=1)

    title = models.CharField(max_length=50)
    blurb = models.TextField()

    can_write_in = models.BooleanField(default=False)
    is_secret = models.BooleanField(default=True)

    def __unicode__(self):
        return u"Ballot #{}".format(self.id)


class DormBallot(Ballot):
    dorm = models.ForeignKey(Dorm)
    number = models.IntegerField()

    class Meta:
        unique_together = ('dorm', 'number',)


class Mesure(models.Model):
    """A collection of ballots. This is probably where you'd want
    to calculate things like quorum."""

    name = models.CharField(max_length=50)
    summary = models.TextField(blank=True)

    vote_start = models.DateTimeField(default=datetime.datetime.now)
    vote_end = models.DateTimeField()

    is_open = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Mesure')
        verbose_name_plural = _('Mesures')

    def __unicode__(self):
        return "u Ballots {}".format(self.ballot_set.all())


class Vote(models.Model):

    account = models.ForeignKey(User, null=True)
    election = models.ForeignKey(Mesure)

    class Meta:
        verbose_name = _('Vote')
        verbose_name_plural = _('Votes')

    def __unicode__(self):
        return u"{} - {}".format(self.account, self.election)


class PopularityVote(models.Model):
    """Represents the most common kind of vote: where each student
    gets a single vote."""

    vote = models.ForeignKey(Vote)
    candidate = models.ForeignKey("Candidate")

    class Meta:
        verbose_name = _('PopularityVote')
        verbose_name_plural = _('PopularityVotes')

    def __unicode__(self):
        return "{} vote for {}".format(self.vote, self.candidate)


class Candidate(models.Model):
    """An abstract candidate, be it a person or a law or funding"""

    ballot = models.ForeignKey(Ballot)

    description = models.TextField()


class PersonCandidate(Candidate):
    user = models.ForeignKey(User, null=True)
    write_in_value = models.CharField(max_length=50, blank=True)