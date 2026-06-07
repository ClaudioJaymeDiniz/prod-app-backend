from app.features.invitations.exceptions import InvitationProjectAccessDeniedException
from app.infrastructure.mail.mail_service import send_invitation_email
from app.infrastructure.notifications.expo_push_service import send_expo_push_notification


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

        registered_user = await self.invitation_repository.find_user_by_email(email_clean)

        status = "PENDING"
        user_id = registered_user.id if registered_user else None

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

        if registered_user:
            push_token = None
            if registered_user.globalMetadata and isinstance(registered_user.globalMetadata, dict):
                push_token = registered_user.globalMetadata.get("expoPushToken")

            if push_token:
                try:
                    await send_expo_push_notification(
                        token=push_token,
                        title="Novo convite para projeto",
                        body=f"Você foi convidado para participar de {project.name}",
                        data={
                            "type": "project_invitation",
                            "projectId": project_id,
                        },
                    )
                except Exception as exc:
                    print(f"Falha ao enviar push de convite: {exc}")

        return await self.invitation_repository.create(
            {
                "email": email_clean,
                "projectId": project_id,
                "status": status,
                "role": role,
                "userId": user_id
            }
        )