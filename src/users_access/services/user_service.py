from typing import Optional

from django.db.models import DecimalField, Value, Sum
from django.db.models.functions import Coalesce
from django.utils.timezone import now

from users.models import User


class UserService:

    def __init__(self):
        self.manager = User.objects

    # CREATE AND UPDATE OPERATIONS
    def create(self, email: str, password: str, first_name: str, last_name: str):
        return self.manager.create_user(email, password, first_name, last_name)


    def update_names(self, user, first_name: Optional[str], last_name: Optional[str]):
        return self.manager.update_names(user, first_name, last_name)

    def update_avatar(self, user, avatar: str):
        return self.manager.update_avatar(user, avatar)


    def create_superuser(self, email: str, password: str, first_name, last_name):
        return self.manager.create_superuser(email, password, first_name, last_name)


    def update_user(self, user, **fields):
        return self.manager.update_user(user, **fields)


    def activate_user(self, user):
        return self.manager.activate_user(user)


    def update_password(self, user, password):
        return self.manager.update_password(user, password)


    def is_verified(self, user):
        return self.manager.is_verified(user)


    # READ OPERATIONS
    def get_all(self):
        return self.manager.get_all()


    def email_exists(self, email: str) -> bool:
        return self.manager.email_exists(email)

    def get_by_email(self, email: str):
        return self.manager.get_by_email(email)

    def get_financial_summary(self, user):
        today = now().date()

        # Monthly income
        monthly_income = user.income_stream_user.aggregate(
            total=Coalesce(Sum("monthly_average"), Value(0, output_field=DecimalField()))
        )["total"]

        # Latest balances per account
        latest_balances = (
            user.balance_history_user
            .order_by("bank_account_id", "-balance_date")
            .distinct("bank_account_id")
            .values("balance")
        )
        total_balance = sum(item['balance'] for item in latest_balances)

        # Linked bank accounts
        linked_bank_accounts = user.bank_account.filter(is_linked=True).count()

        # Active financial items
        active_goals = user.user_goals.filter(is_active=True).count()
        active_budgets = user.budget_user.filter(is_active=True).count()
        active_bills = user.bill_user.filter(is_active=True).count()
        debt_account = user.debt_accounts_user.count()
        investment_portfolio = user.investment_portfolio_user.count()

        # Total savings in goals
        total_goal_savings = user.user_goals.aggregate(
            total=Coalesce(Sum("current_amount"), Value(0, output_field=DecimalField()))
        )["total"]

        # Total debt
        total_debt = user.debt_accounts_user.aggregate(
            total=Coalesce(Sum("current_balance"), Value(0, output_field=DecimalField()))
        )["total"]

        # Monthly expenses
        current_month_expenses = user.user_expenses.filter(
            date__year=today.year,
            date__month=today.month
        ).aggregate(
            total=Coalesce(Sum("amount"), Value(0, output_field=DecimalField()))
        )["total"]

        # Net monthly cash flow
        net_cash_flow = monthly_income - current_month_expenses

        # Debt-to-income ratio
        debt_to_income_ratio = (
            round((total_debt / monthly_income) * 100, 2) if monthly_income > 0 else None
        )

        # Investment value and gain
        investment_data = user.investment_portfolio_user.aggregate(
            total_current=Coalesce(Sum("investment_performance_portfolio__current_value"), Value(0, output_field=DecimalField())),
            total_invested=Coalesce(Sum("investment_performance_portfolio__total_invested"), Value(0, output_field=DecimalField()))
        )

        investment_value = investment_data["total_current"]
        investment_gain = investment_value - investment_data["total_invested"]

        investment_roi = (
            round((investment_gain / investment_data["total_invested"] * 100), 2)
            if investment_data["total_invested"] > 0 else None
        )

        income_vs_expense_ratio = (
            round((current_month_expenses / monthly_income) * 100, 2) if monthly_income > 0 else None
        )

        financial_summary = {
            "income_and_expense": {
                "monthly_income": monthly_income,
                "monthly_expenses": current_month_expenses,
                "income_vs_expense_ratio": income_vs_expense_ratio,
                "net_cash_flow": net_cash_flow,
            },
            "banking": {
                "total_balance": total_balance,
                "linked_bank_accounts": linked_bank_accounts,
            },
            "goals_and_budgets": {
                "active_goals": active_goals,
                "goal_savings_total": total_goal_savings,
                "active_budgets": active_budgets,
                "active_bills": active_bills,
            },
            "debt": {
                "debt_account": debt_account,
                "total_debt": total_debt,
                "debt_to_income_ratio": debt_to_income_ratio,
            },
            "investments": {
                "investment_portfolio": investment_portfolio,
                "investment_total_value": investment_value,
                "investment_gain": investment_gain,
                "investment_roi": investment_roi,
            }
        }

        return financial_summary

