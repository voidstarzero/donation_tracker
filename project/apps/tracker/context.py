from os import environ

from django.db.models import Sum

from .models import Event

def raised_message(total):
    if total < 20:
        return "Let's go!"
    elif total < 100:
        return "Keep up the good work!"
    else:
        return "Well done!"

def statistics(request):
    raised_total = Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'] or 0

    return {
        'raised_total': raised_total,
        'raised_message': raised_message(raised_total),
    }
