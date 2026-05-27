from collections import Counter

from app.features.forms.exceptions import FormAccessDeniedException
from app.features.forms.utils import (
    normalize_form_structure,
    structure_changed,
    build_field_analytics,
)


class GetFormAnalyticsUseCase:

    def __init__(self, form_repository):
        self.form_repository = form_repository

    async def execute(self, form_id: str, user_id: str):
        form = await self.form_repository.find_by_id_with_project(form_id)

        if not form or form.project.ownerId != user_id:
            raise FormAccessDeniedException()

        submissions = await self.form_repository.list_submissions_by_form(
            form_id
        )

        structure = normalize_form_structure(
            form.structure or []
        )

        if structure_changed(form.structure or [], structure):
            await self.form_repository.update(
                form.id,
                {
                    "structure": structure
                }
            )

        daily_counts = Counter()

        for submission in submissions:
            date_str = submission.createdAt.strftime("%Y-%m-%d")
            daily_counts[date_str] += 1

        daily_series = [
            {
                "date": day,
                "count": daily_counts[day]
            }
            for day in sorted(daily_counts.keys())
        ]

        fields_analytics = [
            build_field_analytics(field, submissions)
            for field in structure
        ]

        total_possible_answers = len(submissions) * len(structure)

        total_answered = sum(
            field_data["totalAnswered"]
            for field_data in fields_analytics
        )

        completion_rate = (
            round(total_answered / total_possible_answers, 4)
            if total_possible_answers
            else 0.0
        )

        return {
            "formId": form.id,
            "title": form.title,
            "totalSubmissions": len(submissions),
            "completionRate": completion_rate,
            "dailySubmissions": daily_series,
            "fields": fields_analytics,
        }