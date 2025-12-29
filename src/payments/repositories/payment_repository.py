from django.db import transaction
from payments.models.payment import Payment
from immigration_cases.models.case import Case


class PaymentRepository:
    """Repository for Payment write operations."""

    @staticmethod
    def create_payment(case: Case, amount, currency: str = 'GBP', status: str = 'pending',
                      payment_provider: str = None, provider_transaction_id: str = None):
        """Create a new payment."""
        with transaction.atomic():
            payment = Payment.objects.create(
                case=case,
                amount=amount,
                currency=currency,
                status=status,
                payment_provider=payment_provider,
                provider_transaction_id=provider_transaction_id
            )
            payment.full_clean()
            payment.save()
            return payment

    @staticmethod
    def update_payment(payment: Payment, **fields):
        """Update payment fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(payment, key):
                    setattr(payment, key, value)
            payment.full_clean()
            payment.save()
            return payment

    @staticmethod
    def delete_payment(payment: Payment):
        """Delete a payment."""
        with transaction.atomic():
            payment.delete()

