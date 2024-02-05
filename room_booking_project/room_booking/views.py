# room_booking/views.py

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import Room, RoomBookingDetail, UserProfile
from django.contrib.auth.decorators import login_required


def index(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        # import pdb; pdb.set_trace()

        # Check if a user with the given phone number already exists
        existing_user = UserProfile.objects.filter(phone_number=phone_number).first()

        if existing_user:
            user = existing_user.user
        else:
            # Create a new user and profile
            user = User.objects.create_user(username=phone_number, password=uuid.uuid4().hex)
            UserProfile.objects.create(user=user, phone_number=phone_number)

        # Authenticate user
        # user = authenticate(request, username=user.username, pass word=uuid.uuid4().hex)
        if user is not None:
            login(request, user)
            # Generate and save access token
            access_token = str(uuid.uuid4())
            UserProfile.objects.update_or_create(user=user, defaults={'access_token': access_token})
            return redirect('room_search')

    return render(request, 'room_booking/index.html')


def room_search(request):
    user = request.user
    if not user.is_authenticated:
        # Redirect to the index page if the user is not authenticated
        return redirect('index')

    if request.method == 'POST':
        search_query = request.POST.get('search_query', '').strip()

        # Split the search query into individual terms
        search_terms = search_query.split(",")

        # Create a Q object to combine multiple search conditions
        q_objects = Q()

        for term in search_terms:
            # Add conditions for searching by room name, room tag, and seat capacity
            q_objects |= Q(room_number__icontains=term) | Q(tags__name__icontains=term)

        # Filter rooms based on the combined search conditions
        rooms = Room.objects.filter(q_objects).distinct()

        # Exclude rooms with zero capacity
        rooms = rooms.exclude(capacity=0)

        # Serialize the room data
        room_data = [{'room_number': room.room_number, 'capacity': room.capacity, 'tags': [tag.name for tag in room.tags.all()]} for room in rooms]

        return JsonResponse({'rooms': room_data})

    return render(request, 'room_booking/room_search.html')


# room_booking/views.py



@login_required
def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    booked_slots = RoomBookingDetail.objects.filter(room=room)

    if request.method == 'POST':
        day = request.POST.get('day')
        time_slot = request.POST.get('time_slot')

        # Create a new RoomBookingDetail
        RoomBookingDetail.objects.create(
            room=room,
            user=request.user,
            day=day,
            time_slot=time_slot,
            booked_by_current_user=True
        )

        return redirect('room_search')

    return render(request, 'room_booking/book_room.html', {'room': room, 'booked_slots': booked_slots})


def check_day_availability(request, room_id, day):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day).first()
        day_available = room_booking_detail is None
    else:
        day_available = False

    return JsonResponse({'day_available': day_available})


def check_day_booking(request, room_id, day):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day, user=user).first()
        booked_by_current_user = room_booking_detail is not None
    else:
        booked_by_current_user = False

    return JsonResponse({'booked_by_current_user': booked_by_current_user})


def check_day_booking_other_user(request, room_id, day):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day, user=user).exclude(booked_by_current_user=True).first()
        booked_by_other_user = room_booking_detail is not None
    else:
        booked_by_other_user = False

    return JsonResponse({'booked_by_other_user': booked_by_other_user})


def check_time_slot_availability(request, room_id, day, current_time):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day, time_slot=current_time).first()
        time_slot_available = room_booking_detail is None
    else:
        time_slot_available = False

    return JsonResponse({'time_slot_available': time_slot_available})


def check_time_slot_booking_current_user(request, room_id, day, current_time):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day, time_slot=current_time, user=user).first()
        time_slot_booked_by_current_user = room_booking_detail is not None
    else:
        time_slot_booked_by_current_user = False

    return JsonResponse({'time_slot_booked_by_current_user': time_slot_booked_by_current_user})


def check_time_slot_booking_other_user(request, room_id, day, current_time):
    user = request.user  # Assuming the user is authenticated

    if user.is_authenticated:
        room_booking_detail = RoomBookingDetail.objects.filter(room_id=room_id, day=day, time_slot=current_time).exclude(user=user).first()
        time_slot_booked_by_other_user = room_booking_detail is not None
    else:
        time_slot_booked_by_other_user = False

    return JsonResponse({'time_slot_booked_by_other_user': time_slot_booked_by_other_user})


from datetime import datetime, timedelta

def generateTimeSlots():
    start_time = datetime.strptime("10:00", "%H:%M")
    end_time = datetime.strptime("18:00", "%H:%M")
    time_slots = []

    while start_time + timedelta(minutes=30) <= end_time:
        time_slots.append({
            'start_time': start_time.strftime("%H:%M"),
            'end_time': (start_time + timedelta(minutes=30)).strftime("%H:%M")
        })
        start_time += timedelta(minutes=30)

    return time_slots


def time_slots_view(request):
    # Your logic to retrieve time slots goes here
    # Example: Assume you have a list of time slots
    your_time_slots = generateTimeSlots()

    # Render the time_slots.html template
    return render(request, 'room_booking/time_slots.html', {'time_slots': your_time_slots})


import calendar
from django.db.models import Count

def get_weeks_data():
    # Assume you want data for the current month and year
    import datetime
    today = datetime.date.today()
    month = today.month
    year = today.year

    # Calculate the total number of days in the month
    _, total_days_in_month = calendar.monthrange(year, month)

    # Example data structure
    weeks_data = []

    for day in range(1, total_days_in_month + 1):
        # Create a date string in the 'YYYY-MM-DD' format
        date_str = f'{year}-{month:02d}-{day:02d}'

        # Get the booking details for the current day
        day_booking_details = RoomBookingDetail.objects.filter(day=day)

        # Check if there are any bookings for the current day
        is_available = day_booking_details.exists()
        booked_by_current_user = day_booking_details.filter(booked_by_current_user=True).exists()
        booked_by_other_user = day_booking_details.filter(booked_by_current_user=False).exists()

        # Create a dictionary for the day
        day_data = {
            'date': date_str,
            'is_available': is_available,
            'booked_by_current_user': booked_by_current_user,
            'booked_by_other_user': booked_by_other_user,
        }

        # Append the day data to the weeks data
        weeks_data.append(day_data)

    return weeks_data


def monthly_calendar(request):
    # Assuming you have a function get_weeks_data to fetch or generate the data
    weeks_data = get_weeks_data()
    
    # Render the monthly_calendar.html template with the provided weeks_data
    return render(request, 'room_booking/monthly_calender.html', {'weeks': weeks_data})
