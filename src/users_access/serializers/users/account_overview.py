from rest_framework import serializers


class IncomeAndExpenseSerializer(serializers.Serializer):
    monthly_income = serializers.DecimalField(max_digits=20, decimal_places=2)
    monthly_expenses = serializers.DecimalField(max_digits=20, decimal_places=2)
    income_vs_expense_ratio = serializers.FloatField(allow_null=True)
    net_cash_flow = serializers.DecimalField(max_digits=20, decimal_places=2)


class BankingSerializer(serializers.Serializer):
    total_balance = serializers.DecimalField(max_digits=20, decimal_places=2)
    linked_bank_accounts = serializers.IntegerField()


class GoalsAndBudgetsSerializer(serializers.Serializer):
    active_goals = serializers.IntegerField()
    goal_savings_total = serializers.DecimalField(max_digits=20, decimal_places=2)
    active_budgets = serializers.IntegerField()
    active_bills = serializers.IntegerField()


class DebtSerializer(serializers.Serializer):
    debt_account = serializers.IntegerField()
    total_debt = serializers.DecimalField(max_digits=20, decimal_places=2)
    debt_to_income_ratio = serializers.FloatField(allow_null=True)


class InvestmentSerializer(serializers.Serializer):
    investment_portfolio = serializers.IntegerField()
    investment_total_value = serializers.DecimalField(max_digits=20, decimal_places=2)
    investment_gain = serializers.DecimalField(max_digits=20, decimal_places=2)
    investment_roi = serializers.FloatField(allow_null=True)


class FinancialSummarySerializer(serializers.Serializer):
    income_and_expense = IncomeAndExpenseSerializer()
    banking = BankingSerializer()
    goals_and_budgets = GoalsAndBudgetsSerializer()
    debt = DebtSerializer()
    investments = InvestmentSerializer()
