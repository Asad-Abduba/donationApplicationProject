from django.urls import path
from . import views as my_views


urlpatterns = [

    path('', my_views.donations, name='donations-url'),
    path('update/<id>', my_views.update_form, name='update'),
    path('add-form/', my_views.add_form, name='add-form-url'),
    path('delete/<id>', my_views.delete_form, name='delete'),
    path('error_message/', my_views.error_message, name='error_message-url'),
    path('donate/<id>', my_views.pay, name='donate'),
    path('contact/', my_views.contact_view, name='contact-url'),
    path('success-page/', my_views.success_page, name='success-page-url'),
    path('about/', my_views.about, name='about-url'),
]
