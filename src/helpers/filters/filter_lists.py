PERIOD_CHOICES = [
    "daily", "weekly", "monthly","quarterly", "semiannually", "yearly"
]

FREQUENCY_CHOICES = [
    "once", "daily", "weekly", "monthly", "quarterly", "semiannually", "yearly"
]


DASHBOARD_FILTER = {
    "start_date": "date",
    "end_date": "date",
    "period": "period"
}



INVESTMENT_FILTER = {
    "start_date": "start_date",
    "end_date": "start_date",
    "period": "period",
    "bank_account": "bank_account",
    "types": "TYPE"
}

BILL_FILTER = {
    "sub_category": "sub_category",
    "due_date": "date",
    "frequency": "frequency",
    "active": "bool",
    "start_date": "date",
    "end_date": "date"
}

BUDGET_FILTER = {
    "sub_category": "sub_category",
    "types": "types",
    "period": "period",
    "start_date": "date",
    "end_date": "date",
    "active": "bool",
    "recurring": "bool"
}

DEBT_FILTER = {
    "types": "types",
    "active": "bool",
    "start_date": "date",
    "end_date": "date",
    "period": "period"
}

GOAL_FILTER = {
    "types": "types",
    "active": "bool",
    "completed": "bool",
    "start_date": "date",
    "end_date": "date",
    "period": "period"
}

TAX_FILTER = {
    "types": "types",
    "use_slab": "bool",
    "start_date": "date",
    "end_date": "date",
    "period": "period"
}







