from django.urls import path

from issues.views import create_issue, create_reporter, get_issues, get_reporter_details, get_reporters

urlpatterns = [
    # Reporters
    path('reporters/', get_reporters),
    path('reporters/<int:reporter_id>', get_reporter_details),
    path('reporters/create/', create_reporter),

    # Issues
    path('issues/', get_issues),
    path('issues/create/', create_issue)
]