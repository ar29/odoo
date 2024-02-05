# room_booking/urls.py

from django.urls import path
from .views import index, room_search, check_day_availability, check_day_booking, check_day_booking_other_user, check_time_slot_availability, check_time_slot_booking_current_user, check_time_slot_booking_other_user, time_slots_view, monthly_calendar

urlpatterns = [
    path('index/', index, name='index'),
    path('room_search/', room_search, name='room_search'),
    path('check_day_availability/<int:room_id>/<int:day>/', check_day_availability, name='check_day_availability'),
    path('check_day_booking/<int:room_id>/<int:day>/', check_day_booking, name='check_day_booking'),
    path('check_day_booking_other_user/<int:room_id>/<int:day>/', check_day_booking_other_user, name='check_day_booking_other_user'),
    path('check_time_slot_availability/<int:room_id>/<int:day>/<str:current_time>/', check_time_slot_availability, name='check_time_slot_availability'),
    path('check_time_slot_booking_current_user/<int:room_id>/<int:day>/<str:current_time>/', check_time_slot_booking_current_user, name='check_time_slot_booking_current_user'),
    path('check_time_slot_booking_other_user/<int:room_id>/<int:day>/<str:current_time>/', check_time_slot_booking_other_user, name='check_time_slot_booking_other_user'),
    path('time_slots/', time_slots_view, name='time_slots'),
    path('monthly_calendar/', monthly_calendar, name='monthly_calendar'),


    # Add more URLs as needed for other functionalities
]
