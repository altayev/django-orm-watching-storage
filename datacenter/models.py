from django.db import models
from django.utils import timezone


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return "{user} entered at {entered} {leaved}".format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved= "leaved at " + str(self.leaved_at) if self.leaved_at else "not leaved"
        )

def get_non_closed_duration(visit):
    duration = timezone.now() - visit.entered_at
    seconds = duration.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return '{hours}ч {minutes}мин'.format(hours=hours, minutes=minutes)

def get_duration(visit):
    delta = visit.leaved_at - visit.entered_at
    seconds = delta.total_seconds()
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return '{hours}ч {minutes}мин'.format(hours=hours, minutes=minutes)

def is_visit_long(visit, minutes=60):
      is_visit_long = False
      delta = visit.leaved_at - visit.entered_at
      if delta.total_seconds() > (minutes*60):
        is_visit_long = True
      return is_visit_long

def is_visit_strange(visit, minutes=60):
      is_visit_strange = False
      delta = timezone.now() - visit.entered_at
      if delta.total_seconds() > (minutes*60):
        is_visit_strange = True
      return is_visit_strange