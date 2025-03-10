from django import forms # type: ignore
from .models import DiabetesSurvey

# Define diabetes symptom questions with corresponding model field names
DIABETES_QUESTIONS = [
    ("frequent_urination", "Do you experience frequent urination?"),
    ("excessive_thirst", "Do you feel excessive thirst?"),
    ("weight_loss", "Do you have unexplained weight loss?"),
    ("extreme_hunger", "Do you often feel extreme hunger?"),
    ("blurry_vision", "Do you have blurry vision?"),
    ("fatigue", "Do you experience fatigue or weakness?"),
    ("slow_healing_wounds", "Do you have slow-healing wounds or sores?"),
    ("numbness_tingling", "Do you feel numbness or tingling in your hands/feet?"),
    ("dry_mouth_skin", "Do you experience dry mouth or itchy skin?"),
    ("family_history", "Does your family have a history of diabetes?"),
]

class DiabetesForm(forms.ModelForm):
    class Meta:
        model = DiabetesSurvey
        fields = [
            "name", "age", "email", "bmi", "activity_level",
        ] + [q[0] for q in DIABETES_QUESTIONS]

        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "age": forms.NumberInput(attrs={"class": "form-control", "min": 10}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "bmi": forms.NumberInput(attrs={"class": "form-control"}),
            "activity_level": forms.Select(attrs={"class": "form-control"}),
        }

    # Add symptom questions dynamically
    for field_name, question_text in DIABETES_QUESTIONS:
        locals()[field_name] = forms.ChoiceField(
            choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")],
            widget=forms.RadioSelect(attrs={"class": "radio-group"}),
            label=question_text,
        )
