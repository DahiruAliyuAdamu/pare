from django.shortcuts import render, redirect
from .forms import AddStaffForm
from django.contrib import messages
from .models import StaffDetail
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):
	staff_form = AddStaffForm(request.POST or None)

	if request.method == 'POST':		
		if staff_form.is_valid():
			staff_data = staff_form.save(commit=False)
			staff_data.set_password(staff_data.password)
			staff_data.save()

			messages.success(request, 'Save successful')
			return redirect('register')
	context = {'staff_form': staff_form}
	return render(request, 'register.html', context)

def login(request):
	pass
	# staff_detail = StaffDetail.objects.all()

	# return render(request, 'regisration/login.html', {'staff_details': staff_detail})