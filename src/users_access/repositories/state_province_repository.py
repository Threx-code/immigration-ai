from django.db import transaction
from users_access.models.state_province import StateProvince


class StateProvinceRepository:

    @staticmethod
    def create_state_province(country, code: str, name: str, 
                             has_nomination_program: bool = False, is_active: bool = True):
        """Create a new state/province."""
        with transaction.atomic():
            state = StateProvince.objects.create(
                country=country,
                code=code,
                name=name,
                has_nomination_program=has_nomination_program,
                is_active=is_active
            )
            state.full_clean()
            state.save()
            return state

    @staticmethod
    def update_state_province(state, **fields):
        """Update state/province fields."""
        with transaction.atomic():
            for key, value in fields.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            state.full_clean()
            state.save()
            return state

    @staticmethod
    def set_nomination_program(state, has_nomination_program: bool):
        """Set whether state has nomination program."""
        with transaction.atomic():
            state.has_nomination_program = has_nomination_program
            state.full_clean()
            state.save()
            return state

    @staticmethod
    def activate_state_province(state, is_active: bool):
        """Activate or deactivate state/province."""
        with transaction.atomic():
            state.is_active = is_active
            state.full_clean()
            state.save()
            return state

    @staticmethod
    def delete_state_province(state):
        """Delete a state/province."""
        with transaction.atomic():
            state.delete()
            return True

