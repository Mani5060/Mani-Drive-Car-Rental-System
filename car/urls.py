from django.urls import path
from car import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('register',views.register,name='register'),
    path('signin',views.user_login, name='signin'),
    path('home/', views.home, name='home'),
    path('logout',views.user_logout),
    path('contactus',views.contactus),
    path('ourcars',views.ourcars,name='ourcars'),
    path('catfilter/<str:cid>/', views.catfilter),
    path('sortfilter/<int:sf>/',views.sortfilter),
    path('pricefilter',views.pricefilter),
    path('viewdetails/<int:id>/', views.car_detail,name='car_detail'),
    path("booking/<int:car_id>/", views.booking, name="booking"),
    path("review_booking/<int:booking_id>/", views.review_booking, name="review_booking"),
    path("my_bookings/", views.my_bookings, name="my_bookings"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("paymentsuccess/", views.payment_success, name="payment_success"),
    path("payment_failed/", views.payment_failed, name="payment_failed"),
    path("forgot_password/", views.forgot_password, name="forgot_password"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)