from rest_framework import serializers
from bank_account.models import BankAccount
from debt_account.models import DebtAccount


class ValidateParamsSerializer:

    @staticmethod
    def validate_name(name):
        if len(name) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long.")
        if len(name) > 255:
            raise serializers.ValidationError("Name must be at most 255 characters long.")
        return name

    @staticmethod
    def validate_amount(amount):
        if amount <= 0:
            raise serializers.ValidationError("Current amount cannot be negative.")
        return amount

    @staticmethod
    def validate_bank_account(user, bank_account_id):
        try:
            bank_account_obj = BankAccount.objects.get(id=bank_account_id, user=user)
            if not bank_account_obj:
                raise serializers.ValidationError("Bank account does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Bank account does not exist.")
        return bank_account_obj

    @staticmethod
    def validate_income_summary(user, income_summary_id):
        from income_summary.models import IncomeSummary
        try:
            income_summary_obj = IncomeSummary.objects.get(id=income_summary_id, user=user)
            if not income_summary_obj:
                raise serializers.ValidationError("Income summary does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Income summary does not exist.")
        return income_summary_obj

    @staticmethod
    def validate_investment_portfolio(user, portfolio_id):
        from investment_portfolio.models import InvestmentPortfolio
        try:
            portfolio_obj = InvestmentPortfolio.objects.get(id=portfolio_id, user=user)
            if not portfolio_obj:
                raise serializers.ValidationError(f"Investment portfolio does not exist.")
        except Exception as e:
            raise serializers.ValidationError(f"Investment portfolio does not exist.")
        return portfolio_obj

    @staticmethod
    def validate_sub_category(sub_id):
        from subcategory.models import SubCategory
        try:
            sub_category_obj = SubCategory.objects.get(id=sub_id)
            if not sub_category_obj:
                raise serializers.ValidationError("Sub category does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Sub category does not exist.")
        return sub_category_obj

    @staticmethod
    def validate_transaction(user, transaction_id):
        from transactions.models import Transaction
        try:
            transaction_obj = Transaction.objects.get(id=transaction_id, user=user)
            if not transaction_obj:
                raise serializers.ValidationError("Transaction does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Transaction does not exist.")
        return transaction_obj

    @staticmethod
    def validate_user(user_id):
        from users.models import User
        try:
            user_obj = User.objects.get(id=user_id)
            if not user_obj:
                raise serializers.ValidationError("User does not exist.")
        except Exception as e:
            raise serializers.ValidationError("User does not exist.")
        return user_obj

    @staticmethod
    def validate_group(group_id):
        from django.contrib.auth.models import Group
        try:
            group_obj = Group.objects.get(id=group_id)
            if not group_obj:
                raise serializers.ValidationError("Group does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Group does not exist.")
        return group_obj

    @staticmethod
    def validate_bill(user, bill_id):
        from bill.models import Bill
        try:
            bill_obj = Bill.objects.get(id=bill_id, user=user)
            if not bill_obj:
                raise serializers.ValidationError(f"Bill does not exist.")
        except Exception as e:
            raise serializers.ValidationError(f"An error occurred while validating bill: {str(e)}")
        return bill_obj

    @staticmethod
    def validate_bill_payment(user, payment_id):
        from bill_payment.models import BillPayment
        try:
            bill_payment_obj = BillPayment.objects.get(id=payment_id, user=user)
            if not bill_payment_obj:
                raise serializers.ValidationError("Bill payment does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Bill payment does not exist.")
        return bill_payment_obj

    @staticmethod
    def validate_income_stream(user, income_id):
        from income_stream.models import IncomeStream
        try:
            income_obj = IncomeStream.objects.get(id=income_id, user=user, is_manual=True)
            if not income_obj:
                raise serializers.ValidationError("Income stream does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Income stream does not exist.")
        return income_obj

    @staticmethod
    def validate_budget(user, budget_id):
        from budget.models import Budget
        try:
            budget_obj = Budget.objects.get(id=budget_id, user=user)
            if not budget_obj:
                raise serializers.ValidationError("Budget does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Budget does not exist.")
        return budget_obj

    @staticmethod
    def validate_budget_type(type_id):
        from budget_type.models import BudgetType
        try:
            budget_type_obj = BudgetType.objects.get_by_id(type_id=type_id)
            if not budget_type_obj:
                raise serializers.ValidationError("Budget type does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Budget type does not exist.")
        return budget_type_obj

    @staticmethod
    def validate_debt_type(type_id):
        from debt_type.models import DebtType
        try:
            debt_type_obj = DebtType.objects.get_by_id(type_id=type_id)
            if not debt_type_obj:
                raise serializers.ValidationError("Debt type does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Debt type does not exist.")
        return debt_type_obj

    @staticmethod
    def validate_account_identity(user, account_id):
        from account_identity.models import AccountIdentity
        try:
            account_identity_obj = AccountIdentity.objects.get(id=account_id, user=user)
            if not account_identity_obj:
                raise serializers.ValidationError("Account identity does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Account identity does not exist.")
        return account_identity_obj

    @staticmethod
    def validate_debt_account(user, debt_account_id):
        from debt_account.models import DebtAccount
        try:
            debt_account_obj = DebtAccount.objects.get_debt(user=user, debt_id=debt_account_id)
            if not debt_account_obj:
                raise serializers.ValidationError("Debt account does not exist")
        except Exception as e:
            raise serializers.ValidationError("Debt account does not exist")

        return debt_account_obj

    @staticmethod
    def validate_debt_payment_id(user, payment_id):
        from debt_payment.models import DebtPayment
        try:
            debt_payment = DebtPayment.objects.get_payment(user=user, debt_payment_id=payment_id)
            if not debt_payment:
                raise serializers.ValidationError("Debt payment does not exist")
        except Exception as e:
            raise serializers.ValidationError("Debt payment does not exist")
        return debt_payment

    @staticmethod
    def validate_debt_strategy_custom_order(user, value):
        if not value:
            return value
        try:
            existing_ids = set(
                DebtAccount.objects.filter(user=user, id__in=value)
                .values_list("id", flat=True)
            )

            invalid_ids = [str(v) for v in value if v not in existing_ids]
            if invalid_ids:
                raise serializers.ValidationError(
                    f"Invalid debt IDs in custom_order: {', '.join(invalid_ids)}"
                )
        except Exception as e:
            raise serializers.ValidationError(
                f"Invalid debt IDs in custom_order: {value}"
            )

        return value


    @staticmethod
    def validate_expense(user, expense_id):
        from expense.models import Expense
        try:
            expense_obj = Expense.objects.get(id=expense_id, user=user)
            if not expense_obj:
                raise serializers.ValidationError("Expense does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Expense does not exist.")
        return expense_obj

    @staticmethod
    def validate_goal_type(type_id):
        from goal_type.models import GoalType
        try:
            goal_type_obj = GoalType.objects.get_by_id(goal_type_id=type_id)
            if not goal_type_obj:
                raise serializers.ValidationError("Goal type does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Goal type does not exist.")
        return goal_type_obj


    @staticmethod
    def validate_goal_name_exists(user, goal_name):
        from goal.models import Goal
        try:
            goal_obj = Goal.objects.filter(user=user, name__iexact=goal_name).exists()
            if goal_obj:
                raise serializers.ValidationError("Goal name already exists.")
        except Exception as e:
            raise serializers.ValidationError("Goal name already exists.")
        return goal_name

    @staticmethod
    def validate_goal(user, goal_id):
        from goal.models import Goal
        try:
            goal_obj = Goal.objects.get(id=goal_id, user=user, is_active=True)
            if not goal_obj:
                raise serializers.ValidationError("Goal does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Goal does not exist.")
        return goal_obj

    @staticmethod
    def validate_goal_contribution(user, goal_contribution_id):
        from goal_contribution.models import GoalContribution
        try:
            goal_contribution_obj = GoalContribution.objects.get(id=goal_contribution_id, goal__user=user)
            if not goal_contribution_obj:
                raise serializers.ValidationError("Goal contribution does not exist.")
        except Exception as e:
            raise serializers.ValidationError("Goal contribution does not exist.")
        return goal_contribution_obj

