# 📑 Referência de Arquitetura e API — Módulo Auth & Users

Este módulo é responsável por:

- autenticação de usuários
- gerenciamento de perfil
- recuperação de senha
- geração de tokens JWT
- persistência de usuários

A implementação segue uma arquitetura baseada em:

- Feature-Based Architecture
- Clean Architecture (leve)
- Repository Pattern
- Use Cases
- Dependency Injection

---

# 🧱 Estrutura da Feature

```txt
app/
├── features/
│   ├── auth/
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── dependencies.py
│   │   ├── exceptions.py
│   │   └── use_cases/
│   │
│   └── users/
│       ├── schemas.py
│       ├── repositories.py
│       ├── prisma_repository.py
│       └── use_cases/

# 🗄️ Entidade User (Prisma)
model User {
  id             String   @id @default(uuid())
  email          String   @unique
  name           String?
  password       String?
  provider       String
  globalMetadata Json?
  createdAt      DateTime @default(now())
}
# Campos 
| Campo          | Tipo     | Descrição             |
| -------------- | -------- | --------------------- |
| id             | UUID     | Identificador único   |
| email          | String   | Login do usuário      |
| password       | String   | Hash bcrypt           |
| provider       | String   | local/google/facebook |
| globalMetadata | Json     | Dados auxiliares      |
| createdAt      | DateTime | Data de criação       |


# 🏛️ Arquitetura Aplicada
Camadas
Presentation Layer

Responsável por:

rotas FastAPI
schemas HTTP
autenticação via Depends

Arquivos:

routes.py
schemas.py
dependencies.py
Application Layer

Responsável por:

regras da aplicação
fluxos de autenticação
validações de negócio

Arquivos:

use_cases/
Infrastructure Layer

Responsável por:

Prisma ORM
JWT
bcrypt
providers externos

Arquivos:

prisma_repository.py
jwt_service.py
password_service.py
# 🔐 Segurança
Hash de Senha

Implementado com:
bcrypt

Nenhuma senha é armazenada em texto puro.

JWT

A autenticação utiliza:
Bearer Token + JWT
Payload:
{
  "sub": "user_id",
  "email": "user@email.com",
  "exp": "timestamp"
}

#📦 Repository Pattern

O sistema utiliza Repository Pattern para desacoplar a regra de negócio do ORM Prisma.

Interface
class UserRepository(ABC):

Implementação
class PrismaUserRepository(UserRepository):

Benefícios:

desacoplamento
testabilidade
troca futura de ORM
separação de responsabilidades

#⚙️ Use Cases

Cada endpoint possui um caso de uso específico.

Auth
| Use Case               | Responsabilidade           |
| ---------------------- | -------------------------- |
| RegisterUseCase        | Criar novo usuário         |
| LoginUseCase           | Autenticação JWT           |
| GetMeUseCase           | Retornar usuário atual     |
| UpdateMeUseCase        | Atualizar perfil           |
| RecoverPasswordUseCase | Gerar token de recuperação |
| ResetPasswordUseCase   | Alterar senha              |


#🚀 Endpoints
POST /auth/register

Cria um novo usuário local.

Entrada
{
  "email": "user@email.com",
  "password": "123456",
  "name": "Claudio"
}

Regras
e-mail deve ser único
senha é hasheada automaticamente
Resposta
{
  "id": "...",
  "email": "user@email.com",
  "name": "Claudio"
}
POST /auth/login

Realiza autenticação.

Entrada
OAuth2PasswordRequestForm

Fluxo
busca usuário
verifica senha bcrypt
gera JWT
Resposta
{
  "access_token": "jwt_token",
  "token_type": "bearer"
}
GET /auth/me

Retorna o usuário autenticado.

Requisito
Bearer Token

PATCH /auth/me

Atualiza perfil do usuário autenticado.

Campos suportados
name
password
globalMetadata
POST /auth/recover-password

Inicia recuperação de senha.

Fluxo
gera UUID
salva token no JSON metadata
salva data de expiração
POST /auth/reset-password

Finaliza redefinição de senha.

Fluxo
valida token
valida expiração
gera novo hash bcrypt
remove token do metadata

#🧩 Dependency Injection

A injeção de dependência é feita utilizando:
fastapi.Depends
Exemplo:
def get_login_use_case():
Benefícios:

desacoplamento
reutilização
facilidade de testes

# 🚨 Exception Handling

O sistema utiliza exceptions próprias:
UserAlreadyExistsException
InvalidCredentialsException
InvalidResetTokenException
ExpiredResetTokenException
As exceptions são convertidas automaticamente em respostas HTTP através de handlers globais.

# 📚 Benefícios Arquiteturais
O projeto aplica:
arquitetura modular
separação por feature
clean architecture leve
inversão de dependência
repository pattern
use case pattern
Benefícios
manutenção facilitada
escalabilidade
alta legibilidade
baixo acoplamento
facilidade de testes
separação entre framework e domínio

#🔮 Evoluções Futuras

A arquitetura permite adicionar futuramente:

RBAC
refresh tokens
OAuth completo
testes automatizados
cache Redis
filas assíncronas
microsserviços
observabilidade
auditoria