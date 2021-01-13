from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about', views.about, name='about'),
    path('leaderboard/by_attendee', views.leaderboard_by_attendee, name='leaderboard_by_attendee'),
    path('leaderboard/by_event', views.leaderboard_by_event, name='leaderboard_by_event'),
    path('events/list', views.event_list, name='event_list'),
    path('events/<str:event>', views.event_details, name='event_details'),
    path('clubs/<str:club>', views.club_details, name='club_details'),
    path('donate', views.donate, name='donate'),
    path('pay', views.pay, name='pay'),
    path('attendee/change_password', views.change_password, name='change_password'),
    path('attendee/create', views.create_attendee, name='create_attendee'),
    path('attendee/login', views.login, name='login'),
    path('attendee/logout', views.logout, name='logout'),
    path('attendee/profile', views.attendee_profile, name='attendee_profile'),
]
