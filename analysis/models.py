from django.db import models # type: ignore
from django.contrib.auth.models import User  # type: ignore # Import User model
import datetime
import os

class DiabetesSurvey(models.Model):
    ACTIVITY_LEVEL_CHOICES = [
        ("low", "Low"),
        ("moderate", "Moderate"),
        ("high", "High"),
    ]

    RISK_LEVEL_CHOICES = [
        ("Low Risk", "Low Risk"),
        ("Medium Risk", "Medium Risk"),
        ("High Risk", "High Risk"),
        ("Severe Risk", "Severe Risk"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)  
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    email = models.EmailField()  # Removed unique=True to allow multiple submissions
    bmi = models.FloatField()
    activity_level = models.CharField(max_length=10, choices=ACTIVITY_LEVEL_CHOICES)

    # Symptoms questions
    frequent_urination = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    excessive_thirst = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    weight_loss = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    extreme_hunger = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    blurry_vision = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    fatigue = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    slow_healing_wounds = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    numbness_tingling = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    dry_mouth_skin = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])
    family_history = models.PositiveIntegerField(choices=[(1, "No"), (5, "Sometimes"), (10, "Yes")])

    risk_level = models.CharField(max_length=20, choices=RISK_LEVEL_CHOICES, default="Unknown")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.email}) - {self.risk_level}"

