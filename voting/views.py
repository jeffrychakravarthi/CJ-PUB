# voting/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Candidate, Vote
from .forms import CustomLoginForm, VoteForm
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.decorators import user_passes_test
from .models import Vote
from django.contrib.auth.models import User
from django.urls import reverse

def login_view(request):
    form = CustomLoginForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()  # Get the user from the form
        if user.is_superuser:  # Check if the user is a superuser
            login(request, user)
            return redirect('voting:admin_dashboard')  # Redirect to admin dashboard if superuser
        else:
            login(request, user)
            return redirect('voting:vote')  # Redirect to the voting page if not a superuser
    return render(request, 'voting/login.html', {'form': form})

@login_required
def vote_view(request):
    if Vote.objects.filter(user=request.user).exists():
        messages.error(request, "You have already voted.")
        return redirect('voting:already_voted')
    
    form = VoteForm(request.POST or None)
    if form.is_valid():
        request.session['candidate_id'] = form.cleaned_data['candidate'].id
        return redirect('voting:confirm_vote')
    

    
    return render(request, 'voting/vote.html', {'form': form})

@login_required
def confirm_vote(request):
    candidate_id = request.session.get('candidate_id')
    candidate = Candidate.objects.get(id=candidate_id)
    
    if request.method == 'POST':
        Vote.objects.create(user=request.user, candidate=candidate)
        del request.session['candidate_id']
        return redirect('voting:thanks')
    
    return render(request, 'voting/confirm_vote.html', {'candidate': candidate})

@login_required
def already_voted(request):
    return render(request, 'voting/already_voted.html')


def logout_view(request):
    logout(request)
    return redirect('voting:login')

@user_passes_test(lambda u: u.is_superuser)  # Only accessible by admin
def results_view(request):
    # Fetch all candidates and count the number of votes for each candidate
    results = Candidate.objects.all().annotate(vote_count=Count('vote'))
    
    return render(request, 'voting/results.html', {'results': results})

@login_required
def voting_completed(request):
    return render(request, 'voting/voting_completed.html')

@login_required
def confirm_vote(request):
    candidate_id = request.session.get('candidate_id')
    candidate = Candidate.objects.get(id=candidate_id)
    
    if request.method == 'POST':
        Vote.objects.create(user=request.user, candidate=candidate)
        del request.session['candidate_id']
        return redirect('voting:voting_completed')  # Redirect to the "Voting Completed" page
    
    return render(request, 'voting/confirm_vote.html', {'candidate': candidate})




# Ensure only superusers can access

def is_superuser(user):
    return user.is_superuser

# Admin Dashboard View
@user_passes_test(is_superuser)
def admin_dashboard(request):
    return render(request, 'voting/admin_dashboard.html')

# View to reset votes
@user_passes_test(is_superuser)
def reset_votes(request):
    # Delete all votes
    Vote.objects.all().delete()

    # Reactivate users who have voted
    users_who_voted = User.objects.filter(vote__isnull=False)
    users_who_voted.update(is_active=True)
    
    return redirect('voting:admin_dashboard')  # Redirect to the admin dashboard after resetting

# View to show results
@user_passes_test(is_superuser)
def view_results(request):
    # Get the results with the count of votes per candidate
    results = Vote.objects.values('candidate').annotate(vote_count=Count('candidate')).order_by('-vote_count')
    
    return render(request, 'voting/results.html', {'results': results})
