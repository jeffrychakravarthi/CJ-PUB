# voting/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'voting'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('vote/', views.vote_view, name='vote'),
    path('confirm/', views.confirm_vote, name='confirm_vote'),
    path('already_voted/', views.already_voted, name='already_voted'),
    path('results/', views.results_view, name='results'),
    path('completed/', views.voting_completed, name='voting_completed'),
    path('reset/', views.reset_votes, name='reset_votes'),
    path('results/', views.view_results, name='view_results'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]



