from django import forms
from .models import *

class AddComplaintForm(forms.ModelForm):
	complaints = forms.CharField(widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Write your Complaint here.....',
			'rows': '4',
		}))
	class Meta:
		model 	= Complaint
		fields 	= '__all__'
		# exclude	= ('group_name',)

class AddFeedbackForm(forms.ModelForm):
	reply = forms.CharField(widget=forms.Textarea(attrs={
			'class': 'form-control',
			'placeholder': 'Feedback here.....',
			'rows': '4',
		}))
	class Meta:
		model = Feedback
		fields = ('reply',)


class BeneficiaryGroupNameForm(forms.ModelForm):
	class Meta:
		model 	= BeneficiaryGroupName
		fields 	= '__all__'

class AddTrainingForm(forms.ModelForm):
	class Meta:
		model 	= AddTraining
		fields 	= '__all__'