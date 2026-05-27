# 📝 Referência de Arquitetura e API — Módulo Submissions

O módulo `Submissions` é responsável pelo envio, atualização e gerenciamento das respostas dos formulários dinâmicos do sistema.

Este módulo representa o núcleo funcional do Smart Forms, conectando:

- usuários
- formulários
- projetos
- analytics
- exportação
- uploads
- notificações

---

# 🧱 Estrutura da Feature

```txt
app/features/submissions/
├── routes.py
├── schemas.py
├── dependencies.py
├── repositories.py
├── prisma_repository.py
├── exceptions.py
└── use_cases/
    ├── create_submission.py
    ├── update_submission.py
    ├── list_my_submissions.py
    ├── list_form_submissions.py
    └── list_all_form_submissions.py

    ```

🏛️ Arquitetura Aplicada

O módulo segue:

Feature-Based Architecture
Clean Architecture leve
Repository Pattern
Use Cases
Dependency Injection
Validation Service
Infrastructure Layer
Exception Handling centralizado
🎯 Objetivo do Módulo

O módulo é responsável por:

registrar respostas
validar respostas dinamicamente
controlar acesso aos formulários
alimentar analytics
alimentar exportação CSV
suportar sync offline
permitir edição controlada
integrar uploads
notificar owners
📦 Relação com Outros Módulos
| Módulo      | Integração          |
| ----------- | ------------------- |
| Auth        | usuário autenticado |
| Forms       | estrutura dinâmica  |
| Projects    | permissões          |
| Invitations | acesso privado      |
| Uploads     | imagens             |
| Mail        | notificações        |
| Analytics   | dashboards          |
| CSV Export  | exportação          |

🧠 Estratégia Offline

O sistema foi preparado para mobile offline-first.

O frontend/mobile gera o UUID antes do envio:

{
  "id": "uuid-gerado-no-mobile"
}

Benefícios:

sync offline posterior
prevenção de duplicidade
suporte a filas locais
reconciliação futura
🔐 Controle de Acesso
Formulário Público

Qualquer usuário autenticado pode responder.

Formulário Privado

O usuário precisa:

OWNER
OU
convite ACCEPTED
🧩 Validação Dinâmica

O backend NÃO aceita qualquer JSON.

A submissão é validada contra a estrutura do formulário.

📌 Campos Validados
| Tipo     | Validado |
| -------- | -------- |
| text     | ✅        |
| textarea | ✅        |
| number   | ✅        |
| select   | ✅        |
| checkbox | ✅        |
| image    | ✅        |
| file     | ✅        |

🧠 Validation Service
FormValidationService

Responsável por:

validar campos obrigatórios
validar tipos
validar opções
validar uploads
impedir payload inválido
🚀 Endpoints
POST /submissions/

Cria uma nova resposta.

🔐 Autenticação

Requer:

Authorization: Bearer <token>
📥 Request
{
  "id": "6f7d5b6a-f8e6-4e51-97c3-79991a52c001",
  "formId": "form-id",
  "formData": {
    "nome_completo": "Claudio",
    "idade": 25,
    "curso": "ADS",
    "avaliacao_geral": "Excelente"
  }
}
📤 Response
{
  "id": "6f7d5b6a-f8e6-4e51-97c3-79991a52c001",
  "userId": "user-id",
  "formId": "form-id",
  "formData": {
    "nome_completo": "Claudio",
    "idade": 25
  },
  "createdAt": "2026-05-26T20:00:00Z"
}
PATCH /submissions/{id}

Atualiza uma submissão existente.

🔒 Regra

Somente o dono da resposta pode editar.

📥 Request
{
  "formData": {
    "nome_completo": "Claudio Atualizado"
  }
}
GET /submissions/me

Lista as respostas do usuário autenticado.

GET /submissions/form/{form_id}

Lista respostas do formulário.

🔒 Regras
| Usuário | Resultado          |
| ------- | ------------------ |
| OWNER   | vê todas           |
| coletor | vê apenas próprias |

GET /submissions/form/{form_id}/all

Lista TODAS as respostas do formulário.

🔒 Regra

Somente OWNER pode acessar.

☁️ Integração com Uploads

As imagens NÃO são salvas diretamente na submissão.

Fluxo correto:

Frontend → Uploads → Cloudinary → URL → Submission
📌 Exemplo com imagem
{
  "formData": {
    "nome": "Claudio",
    "foto_atividade": "https://res.cloudinary.com/demo/image/upload/img.png"
  }
}
📧 Notificações

Ao criar uma submissão:

owner do projeto recebe email

Informando:

projeto
formulário
nova resposta
📊 Analytics

As submissões alimentam:

dashboards
gráficos
exportação CSV
filtros
estatísticas
🧠 Use Cases
CreateSubmissionUseCase

Responsável por:

validar payload
validar formulário
validar acesso
validar dados dinâmicos
impedir submissão em projeto arquivado
salvar submissão
enviar notificação
UpdateSubmissionUseCase

Responsável por:

validar ownership
validar dados atualizados
atualizar submissão
ListMySubmissionsUseCase

Responsável por:

listar respostas do usuário
ListFormSubmissionsUseCase

Responsável por:

listar respostas conforme permissão
ListAllFormSubmissionsUseCase

Responsável por:

listar todas respostas do owner
🗄️ Repository Pattern
SubmissionRepository

Define contratos para:

create
update
find
list
queries especializadas
PrismaSubmissionRepository

Implementação usando:

Prisma ORM
📌 JSON Storage

As respostas são armazenadas em:

formData Json

Benefícios:

flexibilidade
formulários dinâmicos
evolução sem migration
suporte offline
🚨 Exceptions
InvalidSubmissionPayloadException

Payload obrigatório inválido.

{
  "detail": "Payload inválido. Campos obrigatórios: id, formId e formData."
}
InvalidSubmissionDataException

Os dados não respeitam a estrutura do formulário.

{
  "detail": {
    "message": "Os dados enviados não respeitam a estrutura do formulário.",
    "errors": [
      {
        "fieldId": "idade",
        "label": "Idade",
        "message": "O valor deve ser numérico."
      }
    ]
  }
}
SubmissionAlreadyExistsException

UUID já registrado.

{
  "detail": "Submissão já registrada."
}
SubmissionNotFoundException

Resposta não encontrada.

{
  "detail": "Resposta não encontrada."
}
SubmissionAccessDeniedException

Usuário sem permissão.

{
  "detail": "Resposta não encontrada."
}
FormNotAvailableForSubmissionException

Projeto arquivado.

{
  "detail": "Projeto arquivado não pode receber respostas."
}

# 🧪 Fluxos Validados

| Fluxo                  | Status |
| ---------------------- | ------ |
| criar submissão        | ✅      |
| editar submissão       | ✅      |
| listar próprias        | ✅      |
| owner visualizar todas | ✅      |
| formulário privado     | ✅      |
| formulário público     | ✅      |
| required fields        | ✅      |
| validação dinâmica     | ✅      |
| upload integrado       | ✅      |
| email notification     | ✅      |
| offline UUID           | ✅      |
