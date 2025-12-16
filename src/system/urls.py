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
from users.views import HomeView
from webhooks.mono.webhook import MonoWebhookAPIView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)
from django_prometheus import exports

API = "api/v1"

urlpatterns = [
    # path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path(f"{API}/account-identities/", include("account_identity.urls")),
    path(f"{API}/banks/", include("bank.urls")),
    path(f"{API}/bank-accounts/", include("bank_account.urls")),
    path(f"{API}/bills/", include("bill.urls")),
    path(f"{API}/bill-payments/", include("bill_payment.urls")),
    path(f"{API}/budgets/", include("budget.urls")),
    path(f"{API}/budget-types/", include("budget_type.urls")),
    path(f"{API}/categories/", include("category.urls")),
    path(f"{API}/subcategories/", include("subcategory.urls")),
    path(f"{API}/dashboard/", include("dashboard.urls")),
    path(f"{API}/dashboard/analytics/", include("dashboard_analytics.urls")),
    path(f"{API}/dashboard/graphs/", include("dashboard_graph.urls")),
    path(f"{API}/debt-type/", include("debt_type.urls")),
    path(f"{API}/debt-account/", include("debt_account.urls")),
    path(f"{API}/debt-strategy/", include("debt_strategy.urls")),
    path(f"{API}/debt-payment/", include("debt_payment.urls")),

    path(f"{API}/auth/", include("users.urls")),
    path(f"{API}/settings/", include("user_settings.urls")),

    path(f"{API}/expenses/", include("expense.urls")),
    path(f"{API}/goals/", include("goal.urls")),
    path(f"{API}/goal-contributions/", include("goal_contribution.urls")),
    path(f"{API}/goal-types/", include("goal_type.urls")),
    path(f"{API}/income-streams/", include("income_stream.urls")),
    path(f"{API}/income-summaries/", include("income_summary.urls")),
    path(f"{API}/investment-type/", include("investment_type.urls")),
    path(f"{API}/investment-portfolio/", include("investment_portfolio.urls")),
    path(f"{API}/investment-requests/", include("investment_transaction.urls")),
    path(f"{API}/investment-performance/", include("investment_performance.urls")),
    path(f"{API}/investment-performance-timeseries/", include("investment_performance_timeseries.urls")),
    path(f"{API}/requests/", include("requests.urls")),


    #========================= SUPER ADMIN PERMISSION AND GROUP ASSIGNMENTS =========================
    path(f"{API}/super-admin/", include("super_admin.urls")),

    #========================= MONO WEBHOOK =========================
    path(f"{API}/request/webhook/", MonoWebhookAPIView.as_view(), name="request-webhook"),

    #========================= PROMETHEUS =========================
    path(f"{API}metrics/", csrf_exempt(exports.ExportToDjangoView), name='prometheus-metrics'),

]
