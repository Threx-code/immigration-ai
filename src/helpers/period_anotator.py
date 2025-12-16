from django.db.models import Case, When, Value, DateField, Q
from django.db.models.functions import (
    TruncDay, TruncWeek, TruncMonth, TruncQuarter, TruncYear,
    ExtractMonth, ExtractYear, Concat, Cast
)

class PeriodAnnotator:
    PERIOD_FUNCTIONS = {
        'day': TruncDay,
        'week': TruncWeek,
        'month': TruncMonth,
        'quarter': TruncQuarter,
        'year': TruncYear,
    }

    PERIOD_ALIASES = {
        'daily': 'day',
        'weekly': 'week',
        'monthly': 'month',
        'quarterly': 'quarter',
        'semiannually': 'semiannual',
        'yearly': 'year',
    }


    @classmethod
    def get_trunc_function(cls, period: str):
        period = period.lower().strip()
        normalized = cls.PERIOD_ALIASES.get(period, period)

        if normalized in cls.PERIOD_FUNCTIONS:
            trunc_class = cls.PERIOD_FUNCTIONS[normalized]
            return lambda field_name: trunc_class(field_name)

        elif normalized == "semiannual":
            def semiannual_trunc(field_name):
                year = ExtractYear(field_name)
                month = ExtractMonth(field_name)
                return Case(
                    When(
                        Q(**{f"{field_name}__month__lte": 6}),  # Use Q with lookup
                        then=Cast(
                            Concat(year, Value("-01-01")),
                            output_field=DateField()
                        )
                    ),
                    default=Cast(
                        Concat(year, Value("-07-01")),
                        output_field=DateField()
                    )
                )

            return semiannual_trunc

        else:
            raise ValueError(
                f"Invalid period: '{period}'. "
                f"Valid periods are: {list(cls.PERIOD_ALIASES.keys())}"
            )
