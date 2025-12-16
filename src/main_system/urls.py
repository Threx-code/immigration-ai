"""
URL configuration for finance project.

The `urlpatterns` list routes URLs to controllers. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function controllers
    1. Add an import:  from my_app import controllers
    2. Add a URL to urlpatterns:  path('', controllers.home, name='home')
Class-based controllers
    1. Add an import:  from other_app.controllers import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from users_access.views.home import HomeView
from django_prometheus import exports

API = "api/v1"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path(f"{API}/auth/", include("users_access.urls")),
    path(f"{API}/accounts/", include("ai_decisions.urls")),
    path(f"{API}/compliance/", include("compliance.urls")),
    path(f"{API}/data-ingestion/", include("data_ingestion.urls")),
    path(f"{API}/human-review/", include("human_reviews.urls")),
    path(f"{API}/imigration-cases/", include("imigration_cases.urls")),
    path(f"{API}/payments/", include("payments.urls")),
    path(f"{API}/rules-knowledge/", include("rules_knowledge.urls")),

    #========================= PROMETHEUS =========================
    path(f"{API}metrics/", csrf_exempt(exports.ExportToDjangoView), name='prometheus-metrics'),

]
