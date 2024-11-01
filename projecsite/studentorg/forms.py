from django import forms
from django.forms import ModelForm
from .models import Organization, OrgMember, College

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"

class OrgMemberForm(ModelForm):
    class Meta:
        model = OrgMember
        fields = "__all__"
        widgets = {
            'date_joined': forms.DateInput(attrs={'type': 'date'})
        }

class CollegeForm(ModelForm):
    class Meta:
        model = College
        fields = "__all__"
