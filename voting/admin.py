from django.contrib import admin
from .models import Candidate, Vote
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.urls import reverse


# Register your models here.
# voting/admin.py

admin.site.register(Candidate)

# Registering the Vote model (if you have a separate Vote model)
@admin.register(Vote)
class VoteAdmin(admin.ModelAdmin):
    list_display = ('user', 'candidate', 'timestamp')  # Show who voted, for which candidate, and when
    list_filter = ('candidate',)  # Filter by candidate


def reset_users_and_candidates(modeladmin, request, queryset):
    # Get all users except superusers and staff members
    users_to_delete = User.objects.exclude(is_superuser=True).exclude(is_staff=True)
    users_to_delete.delete()  # Delete the users
    
    # Get all candidates except those tied to remaining users
    candidates_to_delete = Candidate.objects.all()  # Or apply filtering logic if necessary
    candidates_to_delete.delete()  # Delete the candidates
    
    # Redirect to the user list after performing the reset
    return HttpResponseRedirect(reverse('admin:voting_candidate_changelist'))  # Adjust this path to match your model

reset_users_and_candidates.short_description = 'Reset Users and Candidates (except superusers with staff status)'

# Register your models with custom admin actions
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'party', 'vote_count')
    actions = [reset_users_and_candidates]  # Adding our custom action to the Candidate Admin

class UserAdmin(admin.ModelAdmin):
    actions = [reset_users_and_candidates]  # You can also add this action to User admin if needed
