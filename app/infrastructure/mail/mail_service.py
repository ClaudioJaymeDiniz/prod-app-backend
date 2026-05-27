from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from app.core.config import settings


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_invitation_email(email_to: str, project_name: str):
    message = MessageSchema(
        subject=f"Convite: Projeto {project_name}",
        recipients=[email_to],
        body=(
            f"Olá! Você foi convidado para colaborar no projeto "
            f"'{project_name}'. Acesse o app para responder."
        ),
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_submission_notification(
    owner_email: str,
    project_name: str,
    form_title: str
):
    message = MessageSchema(
        subject=f"Nova Resposta: {form_title}",
        recipients=[owner_email],
        body=(
            f"Olá!\n\n"
            f"O formulário '{form_title}' do projeto '{project_name}' "
            f"recebeu uma nova resposta.\n\n"
            f"Acesse o dashboard para visualizar os dados."
        ),
        subtype=MessageType.plain,
    )

    fm = FastMail(conf)
    await fm.send_message(message)