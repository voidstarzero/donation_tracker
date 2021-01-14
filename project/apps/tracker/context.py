from django.db.models import Sum

from .models import Event

def statistics(request):
    return {
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
