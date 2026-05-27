# 📑 Referência de Arquitetura e API — Módulo Projects

O módulo `Projects` é responsável por gerenciar os projetos do sistema, incluindo criação, listagem, atualização, arquivamento, restauração e exclusão permanente.

Este módulo foi refatorado para seguir uma arquitetura baseada em:

- Feature-Based Architecture
- Clean Architecture leve
- Repository Pattern
- Use Cases
- Dependency Injection
- Exception Handling centralizado

---

# 🧱 Estrutura da Feature

```txt
app/
└── features/
    └── projects/
        ├── routes.py
        ├── schemas.py
        ├── dependencies.py
        ├── repositories.py
        ├── prisma_repository.py
        ├── exceptions.py
        └── use_cases/
            ├── create_project.py
            ├── list_projects.py
            ├── get_project.py
            ├── update_project.py
            ├── archive_project.py
            ├── restore_project.py
            ├── list_archived_projects.py
            └── permanent_delete_project.py

            ```
# 🗄️ Entidade Project no Prisma
model Project {
  id          String   @id @default(uuid())
  name        String
  description String?
  logoUrl     String?
  themeColor  String   @default("#3B82F6")
  isPublic    Boolean  @default(false)
  ownerId     String
  owner       User     @relation("ProjectOwner", fields: [ownerId], references: [id])
  forms       Form[]
  members     UserProject[]
  invitations ProjectInvitation[]
  createdAt   DateTime @default(now())
  deletedAt   DateTime?
}

# 📌 Campos principais
| Campo       | Tipo        | Descrição                      |
| ----------- | ----------- | ------------------------------ |
| id          | String UUID | Identificador único do projeto |
| name        | String      | Nome do projeto                |
| description | String?     | Descrição opcional             |
| logoUrl     | String?     | URL da logo                    |
| themeColor  | String      | Cor hexadecimal do tema        |
| isPublic    | Boolean     | Define se o projeto é público  |
| ownerId     | String      | Usuário dono do projeto        |
| createdAt   | DateTime    | Data de criação                |
| deletedAt   | DateTime?   | Data de arquivamento           |

# 🏛️ Arquitetura Aplicada
1. Presentation Layer

Responsável por expor os endpoints HTTP.

Arquivos:
routes.py
schemas.py
dependencies.py

Responsabilidades:

receber requests
validar entrada com Pydantic
obter usuário autenticado
injetar use cases
retornar responses

2. Application Layer

Representada pelos arquivos dentro de: use_cases/
Cada caso de uso representa uma ação da aplicação.

Exemplos:
| Use Case                      | Responsabilidade                            |
| ----------------------------- | ------------------------------------------- |
| CreateProjectUseCase          | Criar projeto e adicionar owner como membro |
| ListProjectsUseCase           | Listar projetos ativos do usuário           |
| GetProjectUseCase             | Obter detalhes de um projeto                |
| UpdateProjectUseCase          | Atualizar projeto                           |
| ArchiveProjectUseCase         | Arquivar projeto                            |
| RestoreProjectUseCase         | Restaurar projeto arquivado                 |
| ListArchivedProjectsUseCase   | Listar projetos arquivados                  |
| PermanentDeleteProjectUseCase | Excluir projeto definitivamente             |

3. Infrastructure Layer

Representada pelo arquivo: prisma_repository.py
Responsável por:

consultar o banco via Prisma
criar registros
atualizar registros
excluir dependências
executar operações específicas do ORM

4. Repository Contract

Representado pelo arquivo: repositories.py
Define o contrato que a aplicação espera para manipular projetos.

Benefícios:

desacopla os use cases do Prisma
facilita testes
permite trocar ORM futuramente
centraliza operações de persistência

# 🔐 Segurança e Permissões

Todos os endpoints de Projects exigem autenticação via:
Authorization: Bearer <token>
A autenticação é feita através da dependency:
get_current_user

# 👤 Regras de Acesso
OWNER

O usuário dono do projeto pode:

atualizar projeto
arquivar projeto
restaurar projeto
excluir definitivamente
visualizar detalhes
MEMBER

Um usuário membro pode:

listar projetos em que participa
visualizar detalhes do projeto
Usuário sem acesso

Caso o projeto não exista ou o usuário não tenha acesso, a API retorna:
{
  "detail": "Projeto não encontrado"
}
Essa abordagem evita revelar se um projeto existe para usuários não autorizados.

# 🚀 Endpoints
POST /projects/

Cria um novo projeto.

Body
{
  "name": "Pesquisa de Campo FATEC",
  "description": "Coleta de dados sobre sustentabilidade",
  "themeColor": "#059669",
  "isPublic": false,
  "logoUrl": null
}
Regras
O usuário autenticado vira o ownerId.
O owner também é inserido automaticamente em UserProject com role OWNER.

Resposta
{
  "id": "uuid",
  "name": "Pesquisa de Campo FATEC",
  "description": "Coleta de dados sobre sustentabilidade",
  "themeColor": "#059669",
  "isPublic": false,
  "logoUrl": null,
  "ownerId": "user_uuid",
  "createdAt": "2026-01-01T10:00:00",
  "deletedAt": null
}

GET /projects/

Lista todos os projetos ativos do usuário.

Regra

Retorna projetos onde o usuário é:

owner
membro

E onde: deletedAt == null

GET /projects/{project_id}

Retorna os detalhes de um projeto.

Inclui
dados do projeto
owner
membros
Permissão

Permitido para:

owner
membros do projeto
PATCH /projects/{project_id}

Atualiza parcialmente um projeto.

Body

Todos os campos são opcionais:
{
  "name": "Novo nome",
  "description": "Nova descrição",
  "themeColor": "#3B82F6",
  "isPublic": true,
  "logoUrl": "https://exemplo.com/logo.png"
}

Regras
Apenas o owner pode atualizar.
Usa model_dump(exclude_unset=True) para atualizar somente campos enviados.

DELETE /projects/{project_id}

Arquiva o projeto usando soft delete.

Ação

Preenche:
deletedAt = datetime.now()
Regras
Apenas o owner pode arquivar.
O registro continua existindo no banco.

GET /projects/archived

Lista projetos arquivados do usuário.

Regra

Retorna projetos onde:
ownerId == current_user.id
deletedAt != null

POST /projects/{project_id}/restore

Restaura um projeto arquivado.

Ação

Define: deletedAt = null

Regras
Apenas o owner pode restaurar.
DELETE /projects/{project_id}/permanent

Exclui definitivamente o projeto.

Regras
Apenas o owner pode excluir.
O projeto precisa estar arquivado antes.
Remove dependências relacionadas antes da exclusão.
Dependências removidas
submissions dos forms
forms
project invitations
user projects
project

# 🧩 Schemas
ProjectCreate

Usado para criação.
class ProjectCreate(ProjectBase):
    pass

ProjectUpdate

Usado para atualização parcial.

Campos opcionais:

name
description
isPublic
logoUrl
themeColor
ProjectResponse

Resposta básica do projeto.

Inclui:

id
ownerId
createdAt
deletedAt
ProjectFullResponse

Resposta detalhada.

Inclui:

owner
members

#🎨 Validação de Cor

O campo themeColor usa regex para garantir formato hexadecimal válido:
pattern="^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$"
Exemplos válidos:
#3B82F6
#fff
#059669
Exemplos inválidos:
blue
123456
#XYZ

# 🚨 Exceptions

O módulo utiliza exceptions próprias:
ProjectNotFoundException
ProjectAccessDeniedException
ProjectMustBeArchivedException
ProjectPermanentDeleteException
Essas exceptions são convertidas para respostas HTTP pelo handler global.

# 🧪 Testes manuais realizados
Fluxo validado via Swagger/OpenAPI:
POST /projects/                      ✅ 201 Created
GET /projects/                       ✅ 200 OK
GET /projects/{id}                   ✅ 200 OK
PATCH /projects/{id}                 ✅ 200 OK
DELETE /projects/{id}                ✅ 200 OK
GET /projects/archived               ✅ 200 OK
POST /projects/{id}/restore          ✅ 200 OK
DELETE /projects/{id}/permanent      ✅ 200 OK

# 🔮 Evoluções Futuras

O módulo está preparado para evoluir com:

policies de permissão
RBAC mais granular
auditoria de alterações
logs estruturados
testes automatizados
transações no Prisma
integração com invitations
dashboards por projeto

