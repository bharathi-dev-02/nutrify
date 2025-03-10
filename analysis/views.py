from django.shortcuts import render, redirect # type: ignore
from django.http import HttpResponse # type: ignore
from .forms import DiabetesForm
from .models import DiabetesSurvey
from reportlab.lib.pagesizes import letter # type: ignore
from reportlab.pdfgen import canvas # type: ignore
from django.contrib.auth import authenticate, login, logout # type: ignore
from django.contrib.auth.decorators import login_required # type: ignore
from django.contrib import messages # type: ignore
import io

def home(request):
    return render(request, 'analysis/home.html')

# Food images for Low & Medium Risk
FOOD_IMAGES = [
    "/static/uploads/images/fruits.png",
    "/static/uploads/images/grains.png",
    "/static/uploads/images/nuts.png",
    "/static/uploads/images/seeds.png",
]

def bmi_calculator(request):
    if request.method == 'POST':
        height = float(request.POST.get('height', 0)) / 100  # Convert cm to meters
        weight = float(request.POST.get('weight', 0))
        bmi = round(weight / (height ** 2), 2)  # BMI formula
        
        # BMI categories
        if bmi < 18.5:
            bmi_category = "Underweight - Consider gaining weight for better health."
        elif 18.5 <= bmi < 24.9:
            bmi_category = "Normal weight - Maintain your healthy lifestyle!"
        elif 25 <= bmi < 29.9:
            bmi_category = "Overweight - Consider managing your diet and exercise."
        else:
            bmi_category = "Obese - It's recommended to follow a healthy plan."

        return render(request, 'analysis/bmi_calculator.html', {'bmi': bmi, 'bmi_category': bmi_category})

    return render(request, 'analysis/bmi_calculator.html')

def diabetes_form(request):
    risk_level = None  
    food_images = []  
    low_risk = medium_risk = high_risk = severe_risk = 0  # Initialize chart values
    user_data = {}

    if request.method == "POST":
        form = DiabetesForm(request.POST)
        
        if form.is_valid():
            user_data = {
                "name": form.cleaned_data['name'],
                "age": int(form.cleaned_data.get('age', 0)),
                "email": form.cleaned_data['email'],
                "bmi": float(form.cleaned_data.get('bmi', 0.0)),
                "activity_level": form.cleaned_data.get('activity_level'),
            }

            risk_score = sum([
                1 if user_data["age"] > 45 else 0,
                2 if user_data["bmi"] > 30 else 0,
                2 if user_data["activity_level"] == 'low' else 0
            ])

            symptom_fields = [
                "frequent_urination", "excessive_thirst", "weight_loss",
                "extreme_hunger", "blurry_vision", "fatigue",
                "slow_healing_wounds", "numbness_tingling",
                "dry_mouth_skin", "family_history"
            ]
            
            symptom_score = sum(int(form.cleaned_data.get(field, 0)) for field in symptom_fields)
            total_score = risk_score + symptom_score

            # Classify Risk Level
            if total_score <= 10:
                risk_level = "Low Risk"
                food_images = FOOD_IMAGES  
                low_risk += 1
            elif total_score <= 20:
                risk_level = "Medium Risk"
                food_images = FOOD_IMAGES  
                medium_risk += 1
            elif total_score <= 30:
                risk_level = "High Risk"
                high_risk += 1
            else:
                risk_level = "Severe Risk - Consult a Doctor Immediately!"
                severe_risk += 1

            # Save test data
            survey = DiabetesSurvey.objects.create(
                name=user_data["name"],
                age=user_data["age"],
                email=user_data["email"],
                bmi=user_data["bmi"],
                activity_level=user_data["activity_level"],
                **{field: form.cleaned_data[field] for field in symptom_fields}
            )

            # Store user data in session for PDF generation
            request.session["user_data"] = user_data
            request.session["risk_level"] = risk_level

            # Render result page with Chart.js data
            return render(request, "analysis/diabetes_result.html", {
                "risk_level": risk_level,
                "food_images": food_images,
                "low_risk": low_risk,
                "medium_risk": medium_risk,
                "high_risk": high_risk,
                "severe_risk": severe_risk,
                "survey_id": survey.id,  # Send survey ID for PDF generation
            })

    else:
        form = DiabetesForm()

    return render(request, "analysis/diabetes_form.html", {"form": form})

# ✅ PDF Generation View
def generate_pdf(request):
    user_data = request.session.get("user_data", {})
    risk_level = request.session.get("risk_level", "Unknown")

    if not user_data:
        return HttpResponse("No data available. Please complete the form first.", status=400)

    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle("Diabetes Risk Report")

    # PDF Header
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(200, 750, "Diabetes Risk Assessment Report")

    pdf.setFont("Helvetica", 12)
    pdf.drawString(100, 700, f"Name: {user_data.get('name', 'N/A')}")
    pdf.drawString(100, 680, f"Age: {user_data.get('age', 'N/A')}")
    pdf.drawString(100, 660, f"Email: {user_data.get('email', 'N/A')}")
    pdf.drawString(100, 640, f"BMI: {user_data.get('bmi', 'N/A')}")
    pdf.drawString(100, 620, f"Activity Level: {user_data.get('activity_level', 'N/A')}")
    pdf.drawString(100, 600, f"Risk Level: {risk_level}")

    # Footer
    pdf.setFont("Helvetica-Oblique", 10)
    pdf.drawString(100, 550, "This report is based on the data provided and is not a medical diagnosis.")
    
    # Save PDF
    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="diabetes_report.pdf"'
    
    return response

def download_report(request):
    return redirect('generate_pdf')
