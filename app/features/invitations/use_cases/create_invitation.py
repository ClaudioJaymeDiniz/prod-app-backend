from app.features.invitations.exceptions import (
    InvitationProjectAccessDeniedException,
)
from app.infrastructure.mail.mail_service import send_invitation_email


class CreateInvitationUseCase:

    def __init__(self, invitation_repository):
        self.invitation_repository = invitation_repository

    async def execute(
        self,
        project_id: str,
        email: str,
        owner_id: str,
        role: str = "COLLECTOR"
    ):
        email_clean = email.lower().strip()

        project = await self.invitation_repository.find_project_by_id(
            project_id
        )

        if not project or project.ownerId != owner_id:
            raise InvitationProjectAccessDeniedException()

        registered_user = await self.invitation_repository.find_user_by_email(
            email_clean
        )

        if registered_user:
            await self.invitation_repository.upsert_project_member(
                user_id=registered_user.id,
                project_id=project_id,
                role=role
            )

            status = "ACCEPTED"
            user_id = registered_user.id

        else:
            status = "PENDING"
            user_id = None

            try:
                await send_invitation_email(
                    email_clean,
                    project.name
                )
            except Exception:
                print(
                    f"Erro ao enviar e-mail para {email_clean}, "
                    "mas convite será criado."
                )

        return await self.invitation_repository.create(
            {
                "email": email_clean,
                "projectId": project_id,
                "status": status,
                "role": role,
                "userId": user_id
            }
        )