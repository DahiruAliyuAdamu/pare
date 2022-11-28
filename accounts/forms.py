from django import forms

from .models import StaffDetail

class AddStaffForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	class Meta:
		model = StaffDetail
		fields 	= ('first_name', 'surname', 'gender', 'date_birth', 'community', 'clan', 
					'phone_number', 'designation', 'username', 'password')