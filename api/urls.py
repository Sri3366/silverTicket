from django.urls import path
from . import views

urlpatterns = [
    path('products', views.products),
    path('upi-info', views.upi_info),
    path('submissions', views.submit_ticket),
    path('submissions/lookup', views.lookup),
    path('batch/current', views.current_batch),
    path('results', views.results),

    path('admin/login', views.admin_login),
    path('admin/submissions', views.admin_submissions),
    path('admin/submissions/<int:id>/approve', views.approve),
    path('admin/submissions/<int:id>/reject', views.reject),
    path('admin/batches', views.admin_batches),
    path('admin/batches/<int:num>/draw', views.draw),
]