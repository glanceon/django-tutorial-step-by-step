import datetime

from django.db import models
from django.utils import timezone

# Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    pk_choice = models.ForeignKey(Choice,on_delete=models.PROTECT)
    voted_at = models.TimeField(auto_now=True)

    def __str__(self):
        return str(self.pk_choice) + " " + str(self.voted_at.strftime("%H:%M"))

@receiver(post_save, sender=Vote)
def plus_choice(sender, instance, **kwargs):
    choice = Choice.objects.get(choice_text=instance.pk_choice.choice_text)
    choice.votes += 1
    choice.save()

@receiver(post_delete, sender=Vote)
def minus_choice(sender, instance, **kwargs):
    choice = Choice.objects.get(choice_text=instance.pk_choice.choice_text)
    choice.votes -= 1
    choice.save()