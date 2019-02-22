from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
from apps.login_app.models import *

# Create your views here.


def index(request):
    # context={
    #     "all_the_trips":Trip.objects.all(),
    #     # "user":User.objects.get(id)
    # }

    # return render(request, "trip_app/dashboard.html",context)
    return redirect('/success')


def process_create_trip(request):
    return render(request,"trip_app/create_trip.html")


def process_add(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(messages)
        # redirect the user back to the form to fix the errors
        return redirect('/trip/trip_create')
    else:
        this_destination = request.POST["destination"]
        this_plan = request.POST["plan"]
        this_start_date = request.POST["start_date"]
        this_end_date = request.POST["end_date"]
        this_user = User.objects.get(id=int(request.session["current_user"]))
        this_trip = Trip.objects.create(
            destination=this_destination, plan=this_plan, start_date=this_start_date, end_date=this_end_date, user_created_by=this_user)
        # this_book.users_who_like.add(this_user)
        # print(this_user.id,this_user.first_name)
        #set session

        return redirect("/success")

#shpw the detail of the trip
def process_detail(request,trip_id):
    context={
        "this_trip":Trip.objects.get(id=int(trip_id)),
    }
    
    return render(request, "trip_app/trip_detail.html", context)


def edit(request, trip_id):
    trip = Trip.objects.get(id=int(trip_id))
    context={
        "this_trip":trip,
        "start_date":str(trip.start_date),
    }
    return render(request, "trip_app/trip_edit.html", context)
    

def process_edit(request):
    errors = Trip.objects.basic_validator(request.POST)
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(messages)
        # redirect the user back to the form to fix the errors
    
        return redirect('/trip/edit/'+request.POST["trip_id"])
    else:
        this_trip = Trip.objects.get(id=int(request.POST["trip_id"]))
        this_trip.destination = request.POST["destination"]
        this_plan = request.POST["plan"]
        this_trip.start_date = request.POST["start_date"]
        this_trip.end_date = request.POST["end_date"]
        this_trip.save()

        return redirect("/success")


def delete_a_trip(request,trip_id):

    this_trip=Trip.objects.get(id=int(trip_id))
    if this_trip.user_created_by.id != int(request.session["current_user"]):
        context ={
            "warning":"You can not delete this trip. This trip is created by other user.",
        }
        return render(request, "trip_app/warning.html",context)
    this_trip.delete()
    return redirect('/success')

def join(request,trip_id):

    this_user = User.objects.get(id=int(request.session["current_user"]))
    this_trip = Trip.objects.get(id=int(trip_id))
    this_trip.users_who_joined.add(this_user)
    
    return redirect('/success')


def delete_a_join(request,trip_id):
    this_trip = Trip.objects.get(id=int(trip_id))
    this_user = User.objects.get(id=int(request.session["current_user"]))
    if not this_trip in this_user.joined_trips.all():
        context = {
            "warning": "You can not cancel this join. ",
        }
        return render(request, "trip_app/warning.html", context)
    this_user.joined_trips.remove(this_trip)
    return redirect('/success')
