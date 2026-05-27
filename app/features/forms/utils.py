import re
import unicodedata
from collections import Counter


def slugify(text: str) -> str:
    normalized = unicodedata.normalize("NFKD", text or "")
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-zA-Z0-9]+", "_", ascii_text).strip("_").lower()
    return slug or "field"


def normalize_form_structure(structure: list) -> list:
    used_ids = set()
    normalized = []

    for index, raw_field in enumerate(structure or []):
        field = dict(raw_field)

        provided_field_id = field.get("fieldId")
        base_id = slugify(
            provided_field_id
            or field.get("label")
            or f"field_{index + 1}"
        )

        field_id = base_id
        suffix = 2

        while field_id in used_ids:
            field_id = f"{base_id}_{suffix}"
            suffix += 1

        used_ids.add(field_id)
        field["fieldId"] = field_id
        normalized.append(field)

    return normalized


def structure_changed(original: list, normalized: list) -> bool:
    if len(original or []) != len(normalized or []):
        return True

    for index, field in enumerate(normalized or []):
        if (original[index] or {}).get("fieldId") != field.get("fieldId"):
            return True

    return False


def field_value_from_submission(submission_data: dict, field: dict):
    field_id = field.get("fieldId")
    label = field.get("label")

    if field_id and field_id in submission_data:
        return submission_data.get(field_id)

    if label and label in submission_data:
        return submission_data.get(label)

    return None


def is_empty_value(value) -> bool:
    if value is None:
        return True

    if isinstance(value, str):
        return len(value.strip()) == 0

    if isinstance(value, list):
        return len(value) == 0

    return False


def build_field_analytics(field: dict, submissions: list) -> dict:
    field_id = field.get("fieldId")
    label = field.get("label", field_id)
    field_type = (field.get("type") or "text").lower()

    values = []
    total_answered = 0

    for submission in submissions:
        value = field_value_from_submission(
            submission.formData or {},
            field
        )

        values.append(value)

        if not is_empty_value(value):
            total_answered += 1

    total_submissions = len(submissions)
    empty_count = max(total_submissions - total_answered, 0)

    if field_type in {"select", "checkbox"}:
        counter = Counter()

        for value in values:
            if is_empty_value(value):
                continue

            if isinstance(value, list):
                for item in value:
                    counter[str(item)] += 1
            else:
                counter[str(value)] += 1

        options = field.get("options") or []

        option_counts = [
            {
                "label": option,
                "count": counter.get(option, 0)
            }
            for option in options
        ]

        extras = [
            {
                "label": key,
                "count": count
            }
            for key, count in counter.items()
            if key not in set(options)
        ]

        return {
            "fieldId": field_id,
            "label": label,
            "type": field_type,
            "totalAnswered": total_answered,
            "emptyCount": empty_count,
            "chart": "pie" if field_type == "select" else "bar",
            "series": option_counts + extras,
            "stats": None,
        }

    if field_type == "number":
        numeric_values = []

        for value in values:
            if is_empty_value(value):
                continue

            try:
                numeric_values.append(float(value))
            except (TypeError, ValueError):
                continue

        number_counter = Counter(
            str(v).rstrip("0").rstrip(".")
            if isinstance(v, float)
            else str(v)
            for v in numeric_values
        )

        stats = None

        if numeric_values:
            sorted_values = sorted(numeric_values)
            midpoint = len(sorted_values) // 2

            if len(sorted_values) % 2 == 0:
                median = (
                    sorted_values[midpoint - 1]
                    + sorted_values[midpoint]
                ) / 2
            else:
                median = sorted_values[midpoint]

            stats = {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "avg": round(sum(numeric_values) / len(numeric_values), 2),
                "median": median,
            }

        return {
            "fieldId": field_id,
            "label": label,
            "type": field_type,
            "totalAnswered": total_answered,
            "emptyCount": empty_count,
            "chart": "bar",
            "series": [
                {
                    "label": key,
                    "count": count
                }
                for key, count in number_counter.most_common(20)
            ],
            "stats": stats,
        }

    if field_type == "date":
        date_counter = Counter()

        for value in values:
            if is_empty_value(value):
                continue

            date_counter[str(value)] += 1

        return {
            "fieldId": field_id,
            "label": label,
            "type": field_type,
            "totalAnswered": total_answered,
            "emptyCount": empty_count,
            "chart": "line",
            "series": [
                {
                    "label": key,
                    "count": date_counter[key]
                }
                for key in sorted(date_counter.keys())
            ],
            "stats": None,
        }

    if field_type in {"image", "file"}:
        return {
            "fieldId": field_id,
            "label": label,
            "type": field_type,
            "totalAnswered": total_answered,
            "emptyCount": empty_count,
            "chart": "bar",
            "series": [
                {
                    "label": "Com anexo",
                    "count": total_answered
                },
                {
                    "label": "Sem anexo",
                    "count": empty_count
                },
            ],
            "stats": None,
        }

    text_counter = Counter()
    lengths = []

    for value in values:
        if is_empty_value(value):
            continue

        value_text = str(value).strip()
        text_counter[value_text] += 1
        lengths.append(len(value_text))

    stats = None

    if lengths:
        stats = {
            "avgLength": round(sum(lengths) / len(lengths), 2),
            "maxLength": max(lengths),
        }

    return {
        "fieldId": field_id,
        "label": label,
        "type": field_type,
        "totalAnswered": total_answered,
        "emptyCount": empty_count,
        "chart": "bar",
        "series": [
            {
                "label": key,
                "count": count
            }
            for key, count in text_counter.most_common(10)
        ],
        "stats": stats,
    }