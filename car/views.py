from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Cars, Booking, Contact
from django.db.models import Q
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail
import re
import razorpay
from django.contrib import messages
razorpay_client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
        }

        if not all([first_name, last_name, username, email, password, confirm_password]):
            context["errmsg"] = "All fields are required!"
            return render(request, "register.html", context)

        if password != confirm_password:
            context["errmsg"] = "Passwords do not match!"
            return render(request, "register.html", context)

        if len(password) < 8:
            context["errmsg"] = "Password must be at least 8 characters!"
            return render(request, "register.html", context)

        valid, msg = is_valid_password(password)
        if not valid:
            context["errmsg"] = msg
            return render(request, "register.html", context)

        # Check username & email uniqueness
        if User.objects.filter(username=username).exists():
            context["errmsg"] = "Username already exists!"
            return render(request, "register.html", context)

        if User.objects.filter(email=email).exists():
            context["errmsg"] = "Email already registered!"
            return render(request, "register.html", context)

        # Name validation
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            context["errmsg"] = "Enter a valid name (no numbers allowed)!"
            return render(request,'register.html',context)

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        return redirect("signin")

    return render(request, "register.html")


def is_valid_password(password):
    if not password[0].isupper():
        return False, "Password must start with a capital letter."
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."

    return True, ""
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "signin.html", {"errmsg": "Invalid username or password"})

    return render(request, "signin.html")


def user_logout(request):
    logout(request)
    return redirect("signin")


def home(request):
    cars = Cars.objects.all()
    return render(request, "home.html", {"cars": cars})


def ourcars(request):
    cars = Cars.objects.filter(available=True)
    return render(request, "ourcars.html", {"data": cars})

def catfilter(request, cid):
    cars = Cars.objects.filter(category=cid, available=True)
    return render(request, "ourcars.html", {"data": cars})


def sortfilter(request, sf):
    if int(sf) == 0:  
        order = "-price"
    else:              
        order = "price"
    cars = Cars.objects.filter(available=True).order_by(order)
    return render(request, "ourcars.html", {"data": cars})


def pricefilter(request):
    min_price = request.GET.get("min")
    max_price = request.GET.get("max")

    cars = Cars.objects.filter(
        Q(price__gte=min_price) &
        Q(price__lte=max_price) &
        Q(available=True)
    )
    return render(request, "ourcars.html", {"data": cars})

def car_detail(request, id):
    car = get_object_or_404(Cars, id=id)
    return render(request, "viewdetails.html", {"car": car})


def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        city = request.POST.get("city")
        Contact.objects.create(name=name, mobile=mobile, city=city)
        return render(request, "contactus.html", {"msg": "Message Sent!"})
    return render(request, "contactus.html")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Cars, Booking, Contact
from django.db.models import Q


def register(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        context = {
            "first_name": first_name,
            "last_name": last_name,
            "username": username,
            "email": email,
        }

        if not all([first_name, last_name, username, email, password, confirm_password]):
            context["errmsg"] = "All fields are required!"
            return render(request, "register.html", context)

        if password != confirm_password:
            context["errmsg"] = "Passwords do not match!"
            return render(request, "register.html", context)

        if len(password) < 8:
            context["errmsg"] = "Password must be at least 8 characters!"
            return render(request, "register.html", context)

        if User.objects.filter(username=username).exists():
            context["errmsg"] = "Username already exists!"
            return render(request, "register.html", context)

        if User.objects.filter(email=email).exists():
            context["errmsg"] = "Email already registered!"
            return render(request, "register.html", context)
        
        if any(char.isdigit() for char in first_name)or any(char.isdigit() for char in last_name):
            context["errmsg"]="Enter a Valid Name (Special Characters or Number Not Allowed)"
            return render(request,'register.html',context)

        User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        context["successmsg"] = "Registration successful! Please login."
        return redirect("signin")

    return render(request, "register.html")


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "signin.html", {"errmsg": "Invalid username or password"})

    return render(request, "signin.html")


def user_logout(request):
    logout(request)
    return redirect("signin")


def home(request):
    cars = Cars.objects.all()
    return render(request, "home.html", {"cars": cars})


def ourcars(request):
    cars = Cars.objects.filter(available=True)
    return render(request, "ourcars.html", {"data": cars})

def catfilter(request, cid):
    cars = Cars.objects.filter(category=cid, available=True)
    return render(request, "ourcars.html", {"data": cars})


def sortfilter(request, sf):
    if int(sf) == 0:  
        order = "-price"
    else:              
        order = "price"
    cars = Cars.objects.filter(available=True).order_by(order)
    return render(request, "ourcars.html", {"data": cars})


def pricefilter(request):
    min_price = request.GET.get("min")
    max_price = request.GET.get("max")

    cars = Cars.objects.filter(
        Q(price__gte=min_price) &
        Q(price__lte=max_price) &
        Q(available=True)
    )
    return render(request, "ourcars.html", {"data": cars})

def car_detail(request, id):
    car = get_object_or_404(Cars, id=id)
    return render(request, "viewdetails.html", {"car": car})


def contactus(request):
    if request.method == "POST":
        name = request.POST.get("name")
        mobile = request.POST.get("mobile")
        city = request.POST.get("city")
        Contact.objects.create(name=name, mobile=mobile, city=city)
        return render(request, "contactus.html", {"msg": "Message Sent!"})
    return render(request, "contactus.html")


@login_required(login_url="/signin")
def booking(request, car_id):
    car = get_object_or_404(Cars, id=car_id)

    if request.method == "POST":
        customer_name = request.POST.get("customer_name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        license_no = request.POST.get("license_no")
        address = request.POST.get("address")
        no_of_days = int(request.POST.get("no_of_days", 1))
        pickup_location = request.POST.get("pickup_location")
        license_file = request.FILES.get("license_file")
        aadhaar_file = request.FILES.get("aadhaar_file")
        pickup_datetime = request.POST.get("pickup_date")
        drop_datetime = request.POST.get("drop_date")

        if not phone.isdigit() or len(phone) != 10 or phone[0] not in ["6", "7", "8", "9"]:
            return render(request, "booking.html", {
                "car": car,
                "errmsg": "Invalid mobile number!"
            })
        
        if customer_name.isdigit():
            return render(request, "booking.html", {
                "car": car,
                "errmsg": "Customer name cannot be in digits!"
            })
        
        try:
            pickup_date_obj = datetime.strptime(pickup_datetime, "%Y-%m-%d").date()
            drop_date_obj = datetime.strptime(drop_datetime, "%Y-%m-%d").date()
        except Exception:
            return render(request, "booking.html", {
                "car": car,
                "errmsg": "Invalid date format!"
            })

        no_of_days = (drop_date_obj - pickup_date_obj).days
        if no_of_days <= 0:
            return render(request, "booking.html", {
                "car": car,
                "errmsg": "Drop date must be after pickup date!"
            })
        
        booking = Booking.objects.create(
            user=request.user,
            car=car,
            customer_name=customer_name,
            email=email,
            mobile=phone,
            license_no=license_no,
            address=address,
            no_of_days=no_of_days,
            pickup_location=pickup_location,
            license_file=license_file,
            addhar_file=aadhaar_file,
            pickup_datetime=pickup_datetime,
            drop_datetime=drop_datetime,
            is_paid=False  
        )

        return redirect("review_booking", booking_id=booking.id)

    return render(request, "booking.html", {"car": car})


@login_required(login_url="/signin")
def my_profile(request):
    user = request.user
    total_bookings = Booking.objects.filter(user=user, is_paid=True).count()
    
    last_booking = Booking.objects.filter(user=user).order_by("-created_at").first()

    return render(
        request,
        "myprofile.html",
        {
            "user": user,
            "total_bookings": total_bookings,
            "last_booking": last_booking,
        },
    )
@login_required(login_url="/signin")
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user, is_paid=True).order_by("-created_at")
    return render(request, "my_bookings.html", {"bookings": bookings})



@login_required(login_url="/signin")
def review_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    gst_rate = 18
    total_amount = booking.car.price * booking.no_of_days
    gst_amount = total_amount * gst_rate / 100
    final_amount = total_amount + gst_amount

    payment_data = {
        "amount": int(final_amount * 100), 
        "currency": "INR",
        "payment_capture": 1,
    }
    order = razorpay_client.order.create(payment_data)

    request.session["booking_id"] = booking.id

    return render(request, "review_booking.html", {
        "booking": booking,
        "car": booking.car,
        "total_amount": total_amount,
        "GST": gst_amount,
        "final_amount": final_amount,
        "payment": order,
        "razorpay_key": settings.RAZORPAY_KEY_ID,
    })


@login_required(login_url="/signin")
def payment_success(request):
    if request.method != "POST":
        return redirect("home")  

    payment_id = request.POST.get("razorpay_payment_id")
    order_id = request.POST.get("razorpay_order_id")
    signature = request.POST.get("razorpay_signature")

    if not all([payment_id, order_id, signature]):
        return render(request, "payment_failed.html", {"errmsg": "Payment details missing!"})

    try:
        params_dict = {
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
            "razorpay_signature": signature,
        }
        razorpay_client.utility.verify_payment_signature(params_dict)

        booking_id = request.session.get("booking_id")
        if not booking_id:
            return render(request, "payment_failed.html", {"errmsg": "Booking not found in session!"})

        booking = Booking.objects.get(id=booking_id, user=request.user)
        booking.is_paid = True
        booking.save()

        gst_rate = 18
        total_amount = booking.car.price * booking.no_of_days
        gst_amount = total_amount * gst_rate / 100
        final_amount = total_amount + gst_amount

        del request.session["booking_id"]

        subject = "Booking Confirmed - Mani's Drive"
        message = f"""
Hello {booking.customer_name},

Your booking for {booking.car.name} has been confirmed ✅.

📅 Pickup: {booking.pickup_datetime}
📅 Drop: {booking.drop_datetime}
🚗 Car: {booking.car.name} ({booking.car.brand})
💰 Total Amount (incl. GST): ₹{final_amount}

Payment ID: {payment_id}

Thank you for booking with Mani's Drive 🚗✨
Our Team Will Contact You Shortly For More Details
        """

        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = list(
            {booking.email, request.user.email}  
        )

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return render(request, "payment_success.html", {
            "payment_id": payment_id,
            "booking": booking,
            "final_amount": final_amount,
        })

    except razorpay.errors.SignatureVerificationError:
        return render(request, "payment_failed.html", {"errmsg": "Signature verification failed"})

@login_required(login_url="/signin")
def payment_failed(request):
    return render(request, "payment_failed.html")


def is_valid_password(password):
    if not password[0].isupper():
        return False, "Password must start with a capital letter."
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password must contain at least one special character."
    
    if not re.search(r"[A-Za-z]", password):
        return False, "Password must contain at least one letter."
    
    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."
    
    return True, ""

def forgot_password(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        new_password = request.POST.get("new_password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()

        if not username:
            messages.error(request, "Please enter your username!")
            return redirect("forgot_password")

        if not new_password or not confirm_password:
            messages.error(request, "Please enter new password and confirm password!")
            return redirect("forgot_password")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, "User not found!")
            return redirect("forgot_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect("forgot_password")

        if len(new_password) < 8:
            messages.error(request, "Password must be at least 8 characters!")
            return redirect("forgot_password")

        valid, msg = is_valid_password(new_password)
        if not valid:
            messages.error(request, msg)
            return redirect("forgot_password")
        else:
            user.set_password(new_password)
            user.save()
            # messages.success(request, "Password updated successfully! Please login.")
            return redirect("signin")

    return render(request, "forgot_password.html")