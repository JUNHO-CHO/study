from django.urls import path
from . import views


urlpatterns = [
	path('sign_up/', views.sign_up),
	path('sign_in/', views.sign_in),
	path('sign_out/', views.sign_out),
	path('delete/',views.delete_user),
	path('updatepassword/', views.updatepassword),
	path('profile/<int:pk>/', views.profile, name='profile')
]