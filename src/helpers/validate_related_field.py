class ValidateRelatedField:

    def _check_field_type(self, cls, field_name):
        try:
            field_type = cls.check_field_type(field_name)
            if field_type in 'ForeignKey':
                return 'ForeignKey'
            elif field_type in 'ManyToManyField':
                return 'ManyToManyField'
            else:
                return False
        except AttributeError:
            return False


    def validate_related_fields(self, cls, related_fields, is_prefetched=False):
        valid_fields = []
        for field in related_fields:
                field_type = self._check_field_type(cls, field)
                if is_prefetched:
                    if field_type in 'ManyToManyField':
                        valid_fields.append(field)
                else:
                    if field_type in 'ForeignKey':
                        valid_fields.append(field)

        return valid_fields