from app.features.forms.utils import field_value_from_submission, is_empty_value


class FormValidationService:

    @staticmethod
    def validate_required_fields(structure: list, form_data: dict):
        errors = []

        for field in structure or []:
            field_id = field.get("fieldId")
            label = field.get("label", field_id)
            required = field.get("required", False)

            if not required:
                continue

            value = field_value_from_submission(form_data, field)

            if is_empty_value(value):
                errors.append(
                    {
                        "fieldId": field_id,
                        "label": label,
                        "message": "Campo obrigatório não preenchido."
                    }
                )

        if errors:
            raise ValueError(errors)

    @staticmethod
    def validate_field_types(structure: list, form_data: dict):
        errors = []

        for field in structure or []:
            field_id = field.get("fieldId")
            label = field.get("label", field_id)
            field_type = (field.get("type") or "text").lower()
            options = field.get("options") or []

            value = field_value_from_submission(form_data, field)

            if is_empty_value(value):
                continue

            if field_type == "number":
                try:
                    float(value)
                except (TypeError, ValueError):
                    errors.append(
                        {
                            "fieldId": field_id,
                            "label": label,
                            "message": "O valor deve ser numérico."
                        }
                    )

            elif field_type == "select":
                if options and value not in options:
                    errors.append(
                        {
                            "fieldId": field_id,
                            "label": label,
                            "message": "Opção inválida."
                        }
                    )

            elif field_type == "checkbox":
                if not isinstance(value, list):
                    errors.append(
                        {
                            "fieldId": field_id,
                            "label": label,
                            "message": "O valor deve ser uma lista."
                        }
                    )
                else:
                    invalid_options = [
                        item for item in value
                        if options and item not in options
                    ]

                    if invalid_options:
                        errors.append(
                            {
                                "fieldId": field_id,
                                "label": label,
                                "message": "Uma ou mais opções são inválidas."
                            }
                        )

            elif field_type in {"image", "file"}:
                if not isinstance(value, str) or not value.startswith("http"):
                    errors.append(
                        {
                            "fieldId": field_id,
                            "label": label,
                            "message": "O valor deve ser uma URL válida."
                        }
                    )

        if errors:
            raise ValueError(errors)

    @staticmethod
    def validate(structure: list, form_data: dict):
        FormValidationService.validate_required_fields(
            structure,
            form_data
        )

        FormValidationService.validate_field_types(
            structure,
            form_data
        )