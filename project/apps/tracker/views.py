import os

from datetime import datetime

import django.contrib.auth as auth

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, SuspiciousOperation
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from .models import Club, Event, Attendee, Donation, Balance
from .utils import login_forbidden, meets_pw_requirements

# Views are all preliminary until templates are refined

def index(request):
    now = datetime.now()
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'current_events': (Event.objects.filter(start_time__lte=now)
                                        .filter(end_time__gte=now)
                                        .order_by('start_time')),
        'upcoming_events': (Event.objects.filter(start_time__gte=now)
                                         .order_by('start_time'))[:5],
        'attendees': Attendee.objects.all().order_by('-balance__cumulative')[:3],
    }
    return render(request, 'index.html', context)

def about(request):
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'clubs': Club.objects.all(),
    }
    return render(request, 'about.html', context)

def leaderboard_by_attendee(request):
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'attendees': Attendee.objects.all().order_by('-balance__cumulative'),
    }
    return render(request, 'leaderboard/by_attendee.html', context)

def leaderboard_by_event(request):
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'events': Event.objects.all().order_by('-balance__balance'),
    }
    return render(request, 'leaderboard/by_event.html', context)

def event_list(request):
    now = datetime.now()
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'current_events': (Event.objects.filter(start_time__lte=now)
                                        .filter(end_time__gte=now)
                                        .order_by('start_time')),
        'upcoming_events': (Event.objects.filter(start_time__gte=now)
                                         .order_by('start_time')),
        'past_events': (Event.objects.filter(end_time__lte=now)
                                     .order_by('start_time')),
        'events': Event.objects.all(),
    }
    return render(request, 'event_list.html', context)

def event_details(request, event):
    try:
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'event': Event.objects.get(ref_name=event),
            'contributions': Donation.objects.filter(event_to=event).order_by('-timestamp'),
        }
        return render(request, 'event_details.html', context)

    except ObjectDoesNotExist:
        raise Http404('Event does not exist')

def club_details(request, club):
    try:
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'club': Club.objects.get(ref_name=club),
        }
        return render(request, 'club.html', context)

    except ObjectDoesNotExist:
        raise Http404('Club does not exist')

@login_required(login_url='/attendee/login')
def donate(request):
    if request.method == 'POST':
        try:
            event_ref = request.POST['event']
            amount = int(request.POST['amount'])

            attendee = request.user.attendee_info
            event = Event.objects.get(ref_name=event_ref)

            if amount > 0 and amount <= attendee.balance.balance:
                with transaction.atomic():
                    # Take money from the attendee
                    attendee.balance.balance -= amount
                    attendee.balance.save()

                    # Give money to the event
                    event.balance.balance += amount
                    event.balance.cumulative += amount
                    event.balance.save()

                    # Record the transaction
                    record = Donation(amount=amount, attendee_from=attendee, event_to=event)
                    record.save()

                return HttpResponseRedirect('/')

            else:
                return HttpResponseRedirect('/donate?event={}'.format(event_ref))

        except (KeyError, ValueError):
            raise SuspiciousOperation('Wrong parameters to donate')

    elif request.method == 'GET':
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'events': Event.objects.all(),
            'selected': request.GET.get('event'),
        }
        return render(request, 'donate.html', context)

@login_required(login_url='/attendee/login')
def pay(request):
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
    }
    return render(request, 'pay.html', context)

@login_required(login_url='/attendee/login')
def change_password(request):
    if request.method == 'POST':
        try:
            old = request.POST['old_password']
            new = request.POST['new_password']
            confirm = request.POST['new_password_confirm']

            # check user's id again
            user = auth.authenticate(username=request.user.username, password=old)
            if user is not None and meets_pw_requirements(new, confirm):
                user.set_password(new)
                user.save()
                return HttpResponseRedirect('/attendee/login')
            else:
                return HttpResponseRedirect('/attendee/change_password')

        except (KeyError, ValueError):
            raise SuspiciousOperation('Wrong parameters to change password')

    elif request.method == 'GET':
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        }
        return render(request, 'attendee/change_password.html', context)

@login_forbidden(redirect_to='/attendee/logout')
def create_attendee(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST['email']
            password = request.POST['password']
            password_confirm = request.POST['password_confirm']

            # extract club info
            club_prefix = 'member_'
            my_clubs = []
            for key in request.POST:
                if key.startswith(club_prefix) and request.POST[key] == 'on':
                    my_clubs.append(key[len(club_prefix):])

            if meets_pw_requirements(password, password_confirm):
                with transaction.atomic():
                    # We need 3 objects made here, a User, an Attendee and a Balance for them
                    user = User.objects.create_user(username, email, password)
                    user.first_name = first_name
                    user.last_name = last_name
                    user.save()

                    # The user needs a new account made for them
                    balance = Balance()
                    balance.save()

                    # And now the linkage can be made
                    attendee = Attendee(user=user, balance=balance)
                    attendee.save()

                    # Also, note down which clubs they are part of
                    for club in my_clubs:
                        ref = Club.objects.get(ref_name=club)
                        if ref: attendee.clubs.add(ref)
                    attendee.save()

                return HttpResponseRedirect('/attendee/login')
            else:
                return HttpResponseReidrect('/attendee/create')

        except (KeyError, ValueError):
            raise SuspiciousOperation('Wrong paramters to create')

    elif request.method == 'GET':
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
            'clubs': Club.objects.all().order_by('short_name'),
        }
        return render(request, 'attendee/create.html', context)

@login_forbidden(redirect_to='/attendee/logout')
def login(request):
    if request.method == 'POST':
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return HttpResponseRedirect('/')
            else:
                return HttpResponseRedirect('/attendee/login')

        except (KeyError, ValueError):
            raise SuspiciousOperation('Wrong parameters to login')

    elif request.method == 'GET':
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        }
        return render(request, 'attendee/login.html', context)

@login_required(login_url='/attendee/login')
def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return HttpResponseRedirect('/')

    elif request.method == 'GET':
        context = {
            'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
            'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
            'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        }
        return render(request, 'attendee/logout.html', context)

@login_required(login_url='/attendee/login')
def attendee_profile(request):
    context = {
        'payment_business': os.environ['PAYMENT_BUSINESS_DETAILS'],
        'campaign_name': os.environ['TRACKER_CAMPAIGN_NAME'],
        'raised_total': Event.objects.aggregate(Sum('balance__balance'))['balance__balance__sum'],
        'attendee': Attendee.objects.get(user=request.user.id),
        'contributions': Donation.objects.filter(attendee_from=request.user.id).order_by('-timestamp'),
    }
    return render(request, 'attendee/profile.html', context)
