from re import I
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .forms import *
from datetime import date
from django.db.models import Q

# Create your views here.
def home(request):
	return render(request, 'pare_app_templates/home.html')

def pareLogout(request):
	logout(request)
	return render(request, 'registration/logged_out.html')

@login_required
def staffDetail(request):
	context = {}
	staff_details = StaffDetail.objects.exclude(is_superuser=True)

	context['staff_details'] = staff_details
	return render(request, 'pare_app_templates/staff_detail.html', context)

@login_required
def staffEdit(request, p_id):
	context = {}
	try:
		data = StaffDetail.objects.get(id=p_id)
		context['detail'] = data
	except StaffDetail.DoesNotExist:
		return render(request, 'pare_app_templates/staff_error.html')

	if request.method == 'POST':
		data.first_name 	= request.POST['first_name']
		data.surname		= request.POST['surname']
		data.gender 		= request.POST['gender']
		date_birth	= request.POST['date_birth']
		data.community	= request.POST['community']
		data.clan 		= request.POST['clan']
		data.phone_number= request.POST['phone_number']
		data.designation	= request.POST['designation']
		if not date_birth:
			data.date_birth = data.date_birth
		else:
			data.date_birth = date_birth

		data.save()
		return redirect('staffDetail')
	return render(request, 'pare_app_templates/staff_single.html', context)

@login_required
def staffDelete(request, p_id):
	context = {}
	try:
		data = StaffDetail.objects.get(id=p_id)
		context['detail'] = data
	except StaffDetail.DoesNotExist:
		return render(request, 'pare_app_templates/staff_error.html')

	if request.method == 'POST':
		data.delete()
		return redirect('staffDetail')
	else:
		return render(request, 'pare_app_templates/staff_delete.html', context)

@login_required
def complaints(request):
	complait_form = AddComplaintForm(request.POST or None)

	if request.method == 'POST':
		if complait_form.is_valid():
			complaint = complait_form.save(commit=False)
			complaint.save()

			messages.success(request, 'Save successful')
			return redirect('complaint')	
	context = {'form': complait_form}
	return render(request, 'pare_app_templates/complaint.html', context)

@login_required
def viewComplaint(request):
	complaint 	= Complaint.objects.all()
	feedback_count = []
	for compl in complaint:
		feedback_count.append(Feedback.objects.filter(complaint=compl).count())
	
	complaint = list(complaint)
	mylist = zip(complaint, feedback_count)
	context = {'complaints': mylist}
	return render(request, 'pare_app_templates/view_complaints.html', context)

@login_required
def viewsingleFeedback(request, p_id):
	complaint = Complaint.objects.get(pk=p_id)
	feedback = Feedback.objects.filter(complaint=complaint.id)
	feedback_count = feedback.count()
	feedback_form = AddFeedbackForm(request.POST or None)

	context = {}
	if request.method == 'POST':
		if feedback_form.is_valid():
			feedback = feedback_form.save(commit=False)
			feedback.staff_id = request.user.id
			feedback.complaint_id = complaint.id
			feedback.fullname = request.user.username
			feedback.save()
			messages.success(request, 'Save successful')
			return redirect('viewsingleFeedback', p_id=complaint.id)
	context['complaint'] = complaint
	context['feedbacks'] = feedback
	context['feedback_form'] = feedback_form
	context['feedback_count'] = feedback_count
	return render(request, 'pare_app_templates/view_feedback.html', context)

@login_required
def addTraining(request):
	context = {}
	training_form = AddTrainingForm(request.POST or None)
	context['training_form'] = training_form
	if request.method == 'POST':
		if training_form.is_valid():
			training = training_form.save(commit=False)
			training.save()
			messages.success(request, 'Save successful')
			return redirect('addTraining')
	return render(request, 'pare_app_templates/add_training.html', context)

def viewTraining(request):
	training_details = AddTraining.objects.all()
	context = {'trainings': training_details}
	return render(request, 'pare_app_templates/view_training.html', context)


def addBeneficiary(request):
	context = {}
	beneficiary_form = BeneficiaryGroupNameForm(request.POST or None)
	context['beneficiary_form'] = beneficiary_form
	if request.method == 'POST':
		if beneficiary_form.is_valid():
			beneficiary = beneficiary_form.save(commit=False)
			beneficiary.save()

			messages.success(request, 'Save successful')
			return redirect('beneficiary')
	return render(request, 'pare_app_templates/add_beneficiary.html', context)

def viewBeneficiary(request):
	beneficiaries = BeneficiaryGroupName.objects.all()
	context = {'beneficiaries': beneficiaries}
	return render(request, 'pare_app_templates/view_beneficiary.html', context)

def searchBeneficiary(request):
	searchdata = request.GET.get('search')
	beneficiaries = BeneficiaryGroupName.objects.filter(Q(group_name__icontains=searchdata))
	context = {'beneficiaries': beneficiaries}
	return render(request, 'pare_app_templates/beneficiary_result.html', context)

	# There is problem
@login_required
def attendance(request):
	return render(request, 'pare_app_templates/attendance.html')

def attendance_detail(request):
	# There is need to start it again, because I can't be able to rectify the issues
	day = request.GET.get('search')
	print(day)
	staffs = StaffDetail.objects.all()
	reasons = AbsentReason.objects.all()
	attend = StaffAttendance.objects.filter(date=day)
	print(attend)
	context = {'staffs': staffs, 'reasons': reasons, 'att': attend}
	return render(request, 'pare_app_templates/attendance_detail.html', context)

def add_attendance(request):
	staff = request.POST.get('staff')
	status = request.POST.get('status')
	late = request.POST.get('late')
	reason = request.POST.get('reason')
	date = request.POST.get('date')
	att_type = request.POST.get('for')

	staffs = StaffDetail.objects.get(id=staff)
	print(staffs)
	att_objects = StaffAttendance.objects.filter(staff=staffs, date=date)

	if not att_objects.exists():
		StaffAttendance.objects.create(staff=staffs, date=date)

	att_obj = StaffAttendance.objects.get(staff=staffs, date=date)
	print(att_obj)
	if status:
		att_obj.status = eval(status.title())
	if late:
		late = eval(late.title())
		att_obj = late
	att_obj.absent_reason = None
	if reason:
		reason = AbsentReason.objects.get(id=reason)
		att_obj.absent_reason = reason
		att_obj.status = False
		att_obj.late = False
	att_obj.save()

	return HttpResponse('success')

def takeAttendance(request):
	staff_id = request.user.id
	staff_data = StaffDetail.objects.get(id=staff_id)
	today = date.today()
	att_object = StaffAttendance.objects.filter(staff=staff_data, date=today)

	status = True if request.POST.get('status') == 'true' else False
	late = True if request.POST.get('late') == 'true' else False
	reason = request.POST.get('reason')
	if not att_object.exists():
		StaffAttendance.objects.create(staff=staff_data, date=today, status=status,
			late=late)

		context = {'staff_data': staff_data}
		return render(request, 'pare_app_templates/takeAttendance.html', context)
	else:
		context = {'taking': 'taking'}
		return render(request, 'pare_app_templates/takeAttendance.html', context)

		# return HttpResponse('taking')


# It's working
@login_required
def viewAttendance(request):
	day = date.today()
	attendance = StaffAttendance.objects.filter(date=day)
	context = {'attendances': attendance}
	return render(request, 'pare_app_templates/view_attendance.html', context)