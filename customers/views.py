from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from accounts.forms import UserProfileForm, UserInfoForm
from accounts.models import UserProfile
# Create your views here.

@login_required(login_url='login')
def customerProfile(request):
    # Show the existing values inside the form field of a logged in customer
    profile = get_object_or_404(UserProfile, user=request.user)
    
    
    profile_form = UserProfileForm(instance=profile)
    user_form = UserInfoForm(instance=request.user)
    
    context = {
       'profile_form': profile_form,
       'user_form': user_form 
    }
    return render(request, 'customers/customerProfile.html', context)
