from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as tz
from accounts.models import StaffDetail

LGA_LIST = [
	('fufore', 'Fufore'),
	('girei', 'Girei'),
	('yola', 'Yola South'),
	('jimeta', 'Yola North'),
]

# Create your models here.
class BeneficiaryGroupName(models.Model):
	group_name	= models.CharField(_('Group Name'), max_length=200)
	lga 		= models.CharField(_('L.G.A'), choices=LGA_LIST, default='Girei', max_length=50)
	community	= models.CharField(_('Community'), max_length=200)
	address 	= models.CharField(_('Address'), max_length=200)
	group_leader	= models.CharField(_('Group Leader'), max_length=50)
	phone_number	= models.CharField(_('Phone Number'), max_length=11)

	class Meta:
		ordering = ['group_name']

	def __str__(self) -> str:
		return f'{self.group_name}'

class Feedback(models.Model):
	staff 		= models.ForeignKey(StaffDetail, on_delete=models.CASCADE)
	complaint 	= models.ForeignKey('Complaint', on_delete=models.CASCADE)
	fullname	= models.CharField(_('Full Name'), max_length=50)
	reply 		= models.TextField(_('Reply'))
	reply_date	= models.DateField(_('Reply Date:'), auto_now_add=True)
	comment		= models.BooleanField(default=True)

	class Meta:
		ordering = ['reply']

	def __str__(self) -> str:
		return f'{self.reply}'

class Complaint(models.Model):
	group_name 		= models.ForeignKey(BeneficiaryGroupName, on_delete=models.CASCADE)
	fullname 		= models.CharField(_('Full Name:'), max_length=200)
	community		= models.CharField(_('Community:'), max_length=200)
	subject			= models.CharField(_('Subject:'), max_length=30)
	complaints 		= models.TextField(_('Complaint:'))
	complaint_date	= models.DateField(_('Complaint Date:'), auto_now_add=True)

	class Meta:
		ordering = ['subject']

	def __str__(self) -> str:
		return f'{self.fullname} -> {self.subject}'

class AddTraining(models.Model):
	training_name 	= models.CharField(_('Training Name'), max_length=50)
	facilitaor_name	= models.CharField(_('Facilitator Name'), max_length=50)
	organization	= models.CharField(_('Organization'), max_length=50)
	days			= models.IntegerField(_('No of Days'))
	starting_date	= models.DateField(_('Starting Date:'), auto_now_add=False)
	ending_date		= models.DateField(_('Ending Date:'), auto_now_add=False)

	class Meta:
		ordering = ['training_name']

	def __str__(self) -> str:
		return f'{self.facilitaor_name} -> {self.training_name}'

class AbsentReason(models.Model):
	reason = models.CharField(_('absent reason'), max_length=50, help_text=_('eg Sick'))

	def get_absolute_url(self):
		return reverse(f'{"attendance:absent_reason_list"}')

	def __str__(self):
		return f'{self.reason}'

class StaffAttendance(models.Model):
	date = models.DateField(_('date'))
	status = models.BooleanField(_('Present / Absent'), default=False)
	late = models.BooleanField(_('Late'), default=False)
	staff = models.ForeignKey(
		StaffDetail, on_delete=models.CASCADE, verbose_name=_('staff'), related_name='attendance')
	absent_reason = models.ForeignKey(
		AbsentReason, null=True, blank=True, on_delete=models.CASCADE)

	def __str__(self):
		return f'{self.staff.first_name}'

	def get_status(self):
		return _("Present") if self.status else _("Absent")

