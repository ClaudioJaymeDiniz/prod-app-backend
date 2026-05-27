from app.features.submissions.exceptions import (
    SubmissionNotFoundException,
    SubmissionAccessDeniedException,
    SubmissionUpdatePayloadException,
)


class UpdateSubmissionUseCase:

    def __init__(self, submission_repository):
        self.submission_repository = submission_repository

    async def execute(self, submission_id: str, data, user_id: str):
        submission = await self.submission_repository.find_by_id(
            submission_id
        )

        if not submission:
            raise SubmissionNotFoundException()

        if submission.userId != user_id:
            raise SubmissionAccessDeniedException()

        if data.formData is None:
            raise SubmissionUpdatePayloadException()

        return await self.submission_repository.update(
            submission_id,
            {
                "formData": data.formData
            }
        )