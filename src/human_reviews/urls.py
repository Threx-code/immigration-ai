from django.urls import path
from human_reviews.views import (
    # Review
    ReviewCreateAPI,
    ReviewListAPI,
    ReviewDetailAPI,
    ReviewPendingAPI,
    ReviewByReviewerAPI,
    ReviewUpdateAPI,
    ReviewAssignAPI,
    ReviewCompleteAPI,
    ReviewCancelAPI,
    ReviewDeleteAPI,
    # ReviewNote
    ReviewNoteCreateAPI,
    ReviewNoteListAPI,
    ReviewNoteDetailAPI,
    ReviewNotePublicAPI,
    ReviewNoteUpdateAPI,
    ReviewNoteDeleteAPI,
    # DecisionOverride
    DecisionOverrideCreateAPI,
    DecisionOverrideListAPI,
    DecisionOverrideDetailAPI,
    DecisionOverrideLatestAPI,
)

app_name = 'human_reviews'

urlpatterns = [
    # Review endpoints
    path('reviews/', ReviewListAPI.as_view(), name='review-list'),
    path('reviews/create/', ReviewCreateAPI.as_view(), name='review-create'),
    path('reviews/pending/', ReviewPendingAPI.as_view(), name='review-pending'),
    path('reviews/my-reviews/', ReviewByReviewerAPI.as_view(), name='review-by-reviewer'),
    path('reviews/<uuid:id>/', ReviewDetailAPI.as_view(), name='review-detail'),
    path('reviews/<uuid:id>/update/', ReviewUpdateAPI.as_view(), name='review-update'),
    path('reviews/<uuid:id>/assign/', ReviewAssignAPI.as_view(), name='review-assign'),
    path('reviews/<uuid:id>/complete/', ReviewCompleteAPI.as_view(), name='review-complete'),
    path('reviews/<uuid:id>/cancel/', ReviewCancelAPI.as_view(), name='review-cancel'),
    path('reviews/<uuid:id>/delete/', ReviewDeleteAPI.as_view(), name='review-delete'),
    
    # ReviewNote endpoints
    path('review-notes/', ReviewNoteListAPI.as_view(), name='review-note-list'),
    path('review-notes/create/', ReviewNoteCreateAPI.as_view(), name='review-note-create'),
    path('review-notes/<uuid:id>/', ReviewNoteDetailAPI.as_view(), name='review-note-detail'),
    path('review-notes/<uuid:id>/update/', ReviewNoteUpdateAPI.as_view(), name='review-note-update'),
    path('review-notes/<uuid:id>/delete/', ReviewNoteDeleteAPI.as_view(), name='review-note-delete'),
    path('reviews/<uuid:review_id>/notes/public/', ReviewNotePublicAPI.as_view(), name='review-note-public'),
    
    # DecisionOverride endpoints
    path('decision-overrides/', DecisionOverrideListAPI.as_view(), name='decision-override-list'),
    path('decision-overrides/create/', DecisionOverrideCreateAPI.as_view(), name='decision-override-create'),
    path('decision-overrides/<uuid:id>/', DecisionOverrideDetailAPI.as_view(), name='decision-override-detail'),
    path('decision-overrides/latest/<uuid:original_result_id>/', DecisionOverrideLatestAPI.as_view(), name='decision-override-latest'),
]

