from rest_framework import serializers
from decimal import Decimal
from immigration_cases.selectors.case_selector import CaseSelector
from payments.models.payment import Payment


class PaymentCreateSerializer(serializers.Serializer):
    """Serializer for creating a payment."""
    
    case_id = serializers.UUIDField(required=True)
    amount = serializers.DecimalField(required=True, max_digits=10, decimal_places=2, min_value=Decimal('0.01'))
    currency = serializers.ChoiceField(
        choices=Payment.CURRENCY_CHOICES,
        required=False,
        default='GBP'
    )
    status = serializers.ChoiceField(
        choices=Payment.STATUS_CHOICES,
        required=False,
        default='pending'
    )
    payment_provider = serializers.ChoiceField(
        choices=Payment.PAYMENT_PROVIDER_CHOICES,
        required=False,
        allow_null=True
    )
    provider_transaction_id = serializers.CharField(required=False, max_length=255, allow_null=True, allow_blank=True)

    def validate_case_id(self, value):
        """Validate case exists."""
        try:
            case = CaseSelector.get_by_id(value)
            if not case:
                raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        except Exception as e:
            raise serializers.ValidationError(f"Case with ID '{value}' not found.")
        return value

