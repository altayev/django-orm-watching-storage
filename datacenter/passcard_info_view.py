from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from .models import get_duration, is_visit_long


def passcard_info_view(request, passcode):
    passcard = Passcard.objects.get(passcode=passcode)
    passcard_visits = Visit.objects.filter(passcard=passcard)
    this_passcard_visits = []
    
    for visit in passcard_visits:
      visit = {
            "entered_at": visit.entered_at,
            "duration": get_duration(visit),
            "is_strange": is_visit_long(visit)
        }
      this_passcard_visits.append(visit)
    context = {
        "passcard": passcard,
        "this_passcard_visits": this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
