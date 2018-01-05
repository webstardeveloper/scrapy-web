from django.shortcuts import render
import django

from app.forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required

from random import choice
from string import ascii_uppercase

import os
import json
from SearchDCA.settings import BASE_DIR

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
def search_dca(request):
    if request.POST:
        filename = os.path.join(BASE_DIR, 'tmp') + "/res_%s.json" % ''.join(choice(ascii_uppercase) for i in range(12))

        boardCode = "100"
        licenseType, licenseNumber, busName, firstName, lastName = \
            request.POST['license_type'], request.POST['license_number'], \
            request.POST['business_name'], request.POST['first_name'], \
            request.POST['last_name']

        tmp_licenseType = "0" if licenseType == "all" else licenseType

        cmd = "python %s %s --type %s --number '%s' --bus '%s' --first '%s' --last '%s' --file %s" % \
            (os.path.join(BASE_DIR, 'license') + "/start.py", boardCode, tmp_licenseType, \
            licenseNumber, busName, firstName, lastName, filename)

        os.system(cmd)
        data = open(filename, "r").read()
        os.remove(filename)

        print cmd

        try:
          data = json.loads(data)
        except:
          data = ""

        return render(request, 'search_dca.html',
                  {"data": data, "boardCode": boardCode, "licenseType": licenseType, \
                  "licenseNumber": licenseNumber, "busName": busName, \
                  "firstName": firstName, "lastName": lastName})

    else:

        return render(request, 'search_dca.html', {})