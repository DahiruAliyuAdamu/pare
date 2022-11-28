from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

GENDER_LIST = [
	('male', 'Male'),
	('female', 'Female'),
]

# Create your models here.
class StaffDetail(AbstractUser):
	# group_name 		= models.ForeignKey(BeneficiaryGroupName, on_delete=models.CASCADE, blank=True)
	first_name		= models.CharField(_('First Name:'), max_length=50)
	surname			= models.CharField(_('Surname:'), max_length=50)
	gender 			= models.CharField(_('Gender:'), choices=GENDER_LIST, default='male', max_length=20)
	date_birth		= models.DateField(_('Date of Birth:'), blank=True, null=True)
	community		= models.CharField(_('Community:'), max_length=200)
	clan 			= models.CharField(_('Clan/Settlement:'), max_length=200)
	phone_number	= models.CharField(_('Phone Number:'), max_length=11)
	designation		= models.CharField(_('Designation:'), max_length=200)
	username 		= models.CharField(_('Username:'),max_length=10, unique=True)
	password 		= models.CharField(_('Password:'),max_length=16)


	class Meta:
		ordering = ['first_name']

	def __str__(self) -> str:
		return f'{self.first_name} {self.surname}'

	def get_fullname(self):
		return f'{self.first_name} {self.surname}'

	def calculate_age(self):
		if self.date_birth:
			today = date.today()
			return today.year - self._calculate_age.year - ((today.month, today.day) < (self.date_birth.month, self.date_birth.day))
		return 0
