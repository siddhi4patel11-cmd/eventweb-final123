import datetime
from django.shortcuts import redirect, render,get_object_or_404
from .models import category,Event,sub_category,Booking
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Sum
from dateutil.parser import parse
# Create your views here.

def base(request):
    c_post = category.objects.all()
    return render(request,'base.html',{'category' : c_post})

def home(request):
    c_post = category.objects.all()
    # c_sub = sub_category.objects.all()
    # event = Event.objects.filter(sub_category=event_id)
    return render(request,'home.html',{'category' : c_post})

def about(request):
    c_post = category.objects.all()
    return render(request,'about.html',{'category' : c_post})

def contact(request):
    c_post = category.objects.all()
    return render(request,'contact.html',{'category' : c_post})

def main_category(request):
    c_post = category.objects.all()
    # event = Event.objects.all()
    # c_sub = sub_category.objects.all()
    
    # context = {
    #     'category' : c_post,
    #     'event' : event,
    #     'subcategory' : c_sub,
    # }
    
    categories = category.objects.all()
    return render(request,'category.html',{'categories': categories,'category' : c_post})

# def eventprofile(request,event_id):
#     c_post = category.objects.all() 
#     event = Event.objects.filter(pk=event_id)


#     #event = get_object_or_404(Event, pk=event_id)
#     return render(request,'Eventprofile.html',{'category' : c_post,'event':event})
def eventprofile(request,event_id):
    c_post = category.objects.all() 

    event = Event.objects.filter(pk=event_id)
    event1 = get_object_or_404(Event, pk=event_id)
    total_price = None

    # Calculate the total number of seats booked for the event
    total_booked_seats = Booking.objects.filter(event=event1).aggregate(total_seats=Sum('num_seats'))['total_seats']
    total_booked_seats = total_booked_seats if total_booked_seats else 0

    # Calculate the remaining seats
    remaining_seats = event1.total_seats - total_booked_seats

    #remaining_seats = calculate_remaining_seats(event)


    if request.method == 'POST':
        num_seats = int(request.POST.get('num_seats'))
        total_price = num_seats * event1.price

         # Create a new booking record
        booking = Booking.objects.create(
            user=request.user,
            event=event1,
            num_seats=num_seats,
            price=event1.price
        )

        # Show success message
        messages.success(request, 'Seats booked successfully!')

        # Redirect to a new URL
        #return redirect('event_detail', event_id=event.id)
        return render(request, 'thank_you.html', {'event': event, 'num_seats': num_seats, 'total_price': total_price,'category' : c_post,})


    return render(request, 'Eventprofile.html', {'category' : c_post,'event':event, 'total_price': total_price,'remaining_seats': remaining_seats, "total_booked_seats" : total_booked_seats})

# def login(request):
#     return render(request,'login.html')

def user(request):
    return render(request,'user.html')

def subcategory(request , category_id):
    category1 = get_object_or_404(category, pk=category_id)
    #subcategories = category.subcategory_set.all()
    subcategories = sub_category.objects.filter(category=category1)
    c_post = category.objects.all()
    print(category1)
    return render(request, 'subcategory.html', {'category1': category1, 'subcategories': subcategories,'category' : c_post})

    # c_post = category.objects.all()
    # event = Event.objects.all()
    # subcategory = sub_category.objects.all()

    # context = {
    #     'category' : c_post,
    #     'event' : event,
    #     'subcategory' : subcategory,
    # }
    # return render(request,'subcategory.html',context)
   
def faq(request):
    return render(request,'faq.html')

def event_detail(request, event_id):
    #event = get_object_or_404(Event, pk=event_id)
    c_post = category.objects.all()
    subcategory1 = get_object_or_404(sub_category, pk=event_id)
    event = Event.objects.filter(sub_category=event_id)
    return render(request, 'events.html', {'subcategory': subcategory1,'event': event,'category' : c_post})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('maincategory')
        else:
           # Return an error message if authentication fails
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')


def user_logout(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        User.objects.create_user(username=username, password=password)
        return redirect('login')
    return render(request, 'user.html')

# def postevent(request):
#     c_post = category.objects.all()
#     return render(request,'postevent.html',{'category' : c_post})

def postevent(request):
    c_post = category.objects.all()
    subcategories = sub_category.objects.all()

    if request.method == 'POST':
        # Extract event data from the request
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        sub_category_id = request.POST.get('subcategory')
        num_seats = request.POST.get('num_seats')
        date = request.POST.get('event_date')
        image = request.FILES.get('image')
        location = request.POST.get('location')
        term_conditions = request.POST.get('term_conditions')
        company_name = request.POST.get('company_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')


        
        # Perform manual validation
        errors = []
        if not title:
            errors.append("Title is required.")
        if not description:
            errors.append("Description is required.")
        if not price or float(price) <= 0:
            errors.append("Price must be a positive number.")
        if not sub_category_id:
            errors.append("Subcategory is required.")
        if not num_seats or int(num_seats) <= 0:
            errors.append("Number of seats must be a positive integer.")
        if not date:
            errors.append("Event date is required.")
        # Add more validation checks as needed

        if errors:
            subcategories = sub_category.objects.all()
            return render(request, 'postevent.html', {'subcategories': subcategories,'errors': errors})
            #return render(request, 'event_create.html', {'errors': errors})



        # Get the logged-in user
        user = request.user

        # Get the SubCategory object
        subcategory = sub_category.objects.get(pk=sub_category_id)

        # Create the event object in the database
        Event.objects.create(
            main_title=title,
            description=description,
            price=price,
            sub_category_id=sub_category_id,
            total_seats=num_seats,
            date=date,
            image=image,
            start_time = start_time,
            end_time = end_time,
            available_seat = num_seats,
            location = location,
            company_name = company_name,
            email =email,
            phone = phone,
            term_conditions= term_conditions,
            event_created_by=user
        )

        # Redirect to a success page or another URL
        return redirect('maincategory')

    # Get all subcategories to pass to the template
    subcategories = sub_category.objects.all()
    return render(request, 'postevent.html', {'subcategories': subcategories,'category' : c_post})


def user_events(request):
    # Filter events created by the logged-in user
    # events = Event.objects.filter(event_created_by_id=request.user.id)
    # return render(request, 'user_events.html', {'events': events})

    from_date_selected = None
    to_date_selected = None

    if request.method == 'POST':
        from_date_str = request.POST.get('from_date')
        to_date_str = request.POST.get('to_date')

        try:
            
            # from_date = datetime.strptime(from_date_str, '%Y-%m-%d')
            # to_date = datetime.strptime(to_date_str, '%Y-%m-%d')

            

            parsed_date = parse(from_date_str)
            from_date = parsed_date.strftime("%Y-%m-%d")

            parsed_date1 = parse(to_date_str)
            to_date = parsed_date1.strftime("%Y-%m-%d")

            from_date_selected = from_date
            to_date_selected = to_date

            # Assuming you have an Event model
            events = Event.objects.filter(event_created_by_id=request.user.id,date__gte=from_date, date__lte=to_date)

            # Pass events to the template for rendering
            return render(request, 'user_events.html', {'events': events,'from_date_selected': from_date_selected, 'to_date_selected': to_date_selected})
        except ValueError:
            # Handle invalid date format
            return render(request, 'user_events.html', {'message': 'Invalid date format'})
    else:
        events = Event.objects.filter(event_created_by_id=request.user.id)
        return render(request, 'user_events.html', {'events': events,'from_date_selected': from_date_selected, 'to_date_selected': to_date_selected})



def event_detail_user(request, event_id):
    event = get_object_or_404(Event, pk=event_id)

    # Calculate the total number of seats booked for the event
    total_booked_seats = Booking.objects.filter(event=event).aggregate(total_seats=Sum('num_seats'))['total_seats']
    total_booked_seats = total_booked_seats if total_booked_seats else 0

    # Calculate the remaining seats
    remaining_seats = event.total_seats - total_booked_seats

    # Calculate revenue generated for the event
    revenue_generated = total_booked_seats * event.price

    return render(request, 'event_detail_user.html', {
        'event': event,
        'total_booked_seats': total_booked_seats,
        'remaining_seats' :remaining_seats,
        'revenue_generated': revenue_generated,
    })


import razorpay
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse

razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

# def create_order(request):
#     if request.method == 'POST':
#             if request.method == 'POST':
#                 amount_str = request.POST.get('amount')
#                 if amount_str is not None:
#                     try:
#                         amount = int(amount_str) * 100  # Amount in paise
#                         # Proceed with creating the order using Razorpay API
#                         return JsonResponse({'success': True, 'amount': amount})
#                     except ValueError:
#                         return JsonResponse({'error': 'Invalid amount format'}, status=400)
#                 else:
#                     return JsonResponse({'error': 'Missing amount parameter'}, status=400)
        
#     else:
#         return render(request, 'payment_form.html')

# def payment_callback(request):
#     payload = request.POST
#     signature = request.headers.get('x-razorpay-signature')
#     # Verify signature
#     try:
#         razorpay_client.utility.verify_webhook_signature(payload, signature, settings.RAZORPAY_WEBHOOK_SECRET)
#         # Handle payment success
#         # Update booking status
#         return JsonResponse({'status': 'success'})
#     except razorpay.errors.SignatureVerificationError as e:
#         # Handle verification failure
#         return JsonResponse({'status': 'failure'})


def payment(request):
    if request.method == "POST":
        price = request.POST['amount']       
        amount =  int(float(price) * 100) # amount in paisa
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        #return JsonResponse(payment)
        return redirect('payment_success')

    return render(request, 'newPay.html')

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def complete_payment(request):
    if request.method == "POST":
        data = request.POST
        try:
            client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
            params_dict = {
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            }
            client.utility.verify_payment_signature(params_dict)
            return JsonResponse({'status': 'success'})
        except:
            return JsonResponse({'status': 'failed'})
    return JsonResponse({'status': 'failed'})


def payment_success(request):
    return render(request, 'payment_success.html')

def payment_fail(request):
    return render(request, 'payment_fail.html')