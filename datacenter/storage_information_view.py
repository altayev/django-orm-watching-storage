from datacenter.models import Visit
from django.shortcuts import render
from .models import get_non_closed_duration, is_visit_strange


def storage_information_view(request):
    visits = Visit.objects.all()
    non_closed_visits = []
    for visit in visits:
      if visit.leaved_at==None:
        non_closed_visit = {
          "who_entered": visit.passcard.owner_name,
          "entered_at": visit.entered_at,
          "duration": get_non_closed_duration(visit),
          "is_strange": is_visit_strange(visit),
        }
        non_closed_visits.append(non_closed_visit)

    context = {
        "non_closed_visits": non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
