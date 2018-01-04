from django.shortcuts import render
import django

from app.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(
                    user_form.cleaned_data['password'])
            new_user.save()

            return render(request, 
                            'registration/register_done.html',
                            {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
                  'registration/register.html',
                  {'user_form': user_form})

@login_required(login_url='/login/')
def search(request):
	if request.POST:
		print request.POST
		os.system("sudo python scale1.py")
	return render(request,
                  'search.html',
                  {})