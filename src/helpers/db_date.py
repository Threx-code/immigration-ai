import logging
from datetime import timedelta

logger = logging.getLogger("django")


class DateRangeHelper:
    """
    Utility class for resolving dynamic date ranges
    based on database records when start_date or end_date are missing.
    """

    def __init__(self, model, date_field="date"):
        """
        :param model: Django model or queryset manager (e.g. Transaction.objects)
        :param date_field: Field name that stores date values (default: 'date')
        """
        self.model = model
        self.date_field = date_field

    def resolve_date_range(self, user, start_date=None, end_date=None, months=6, **kwargs):
        """
        Resolves a valid date range. If both start and end dates are empty,
        it derives the last `months` months from the latest available record
        for the given user.

        :param user: User instance
        :param start_date: Optional start date
        :param end_date: Optional end date
        :param months: Number of months to look back (default: 6)
        :return: (start_date, end_date)
        """

        # If the caller already provided a range, just return it
        if start_date and end_date:
            return start_date, end_date

        # Fetch the latest available record for the user
        latest_record = (
            self.model.filter(user=user, **kwargs)
            .order_by(f"-{self.date_field}")
            .values_list(self.date_field, flat=True)
            .first()
        )

        if not latest_record:
            logger.warning(f"No records found for user {user}.")
            return None, None

        # Compute the date window (6 months back)
        end_date = latest_record
        start_date = end_date - timedelta(days=months * 30)

        logger.info(f"[DateRangeHelper] Using last {months} months from {start_date} → {end_date}")
        return start_date, end_date
