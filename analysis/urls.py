from django.urls import path  # type: ignore # Import path
from .views import (  # Import all necessary views
    home,bmi_calculator, diabetes_form, generate_pdf, download_report, 
   
)

urlpatterns = [
    # Home Page
    path('', home, name='analysis_home'),
    path('bmi-calculator/', bmi_calculator, name='bmi_calculator'),
    # Diabetes Form and Report
    path('diabetes-form/', diabetes_form, name='diabetes_form'),
    path('generate-pdf/', generate_pdf, name='generate_pdf'),
    path('download-report/', download_report, name='download_report'),

    # Authentication Routes
   
]
