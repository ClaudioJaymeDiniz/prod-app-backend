# 📤 Referência de Arquitetura e API — Módulo Uploads

O módulo `Uploads` é responsável pelo gerenciamento de arquivos de imagem do sistema utilizando Cloudinary como armazenamento em nuvem.

Este módulo foi projetado para ser reutilizável por:

- logos de projetos
- imagens em submissões
- avatars
- anexos futuros
- banners
- mídia do sistema

---

# 🧱 Estrutura da Feature

```txt
app/
├── infrastructure/
│   └── storage/
│       └── cloudinary_service.py
│
└── features/
    └── uploads/
        ├── routes.py
        ├── schemas.py
        ├── dependencies.py
        ├── exceptions.py
        └── use_cases/
            └── upload_image.py

```

# 🏛️ Arquitetura Aplicada

O módulo segue:

Feature-Based Architecture
Clean Architecture leve
Use Cases
Dependency Injection
Infrastructure Layer
Exception Handling centralizado
# 📌 Objetivo do Módulo

O backend NÃO armazena arquivos diretamente.

O fluxo correto é:
Frontend envia imagem
        ↓
Uploads faz validação
        ↓
Cloudinary armazena
        ↓
Cloudinary retorna URL
        ↓
Backend salva somente a URL

Isso reduz:

uso de disco no servidor
processamento local
complexidade
custo de infraestrutura

E melhora:

escalabilidade
performance
CDN
cache
compressão
entrega de mídia

# ☁️ Cloudinary

O sistema utiliza:

Cloudinary

como serviço de:

upload
compressão
otimização
CDN
transformação de imagens

# 🔐 Variáveis de Ambiente
CLOUDINARY_CLOUD_NAME=""
CLOUDINARY_API_KEY=""
CLOUDINARY_API_SECRET=""

# 🧠 Estratégia de Upload

O backend:

valida extensão
valida tamanho máximo
limita resolução
pede compressão automática ao Cloudinary

# 📏 Limites Aplicados
| Regra                | Valor                |
| -------------------- | -------------------- |
| Tamanho máximo       | 5MB                  |
| Formatos permitidos  | jpg, jpeg, png, webp |
| Resolução máxima     | 1600x1600            |
| Compressão           | automática           |
| Conversão de formato | automática           |

# 🧩 Compressão Automática

O upload utiliza:

quality="auto:good"
fetch_format="auto"

Benefícios:

imagens menores
WebP automático
AVIF automático
menor consumo de banda
melhor performance mobile

# 🖼️ Redimensionamento Automático

O sistema aplica:

transformation=[
    {
        "width": 1600,
        "height": 1600,
        "crop": "limit"
    }
]

Isso significa:

imagens menores que 1600px não são alteradas
imagens maiores são reduzidas proporcionalmente
evita uploads gigantes

# 🚀 Endpoint
POST /uploads/image

Realiza upload de imagem.

# 🔐 Autenticação

Requer:

Authorization: Bearer <token>
# 📥 Request

Tipo:

multipart/form-data

Campos:
| Campo  | Tipo    | Obrigatório |
| ------ | ------- | ----------- |
| file   | arquivo | sim         |
| folder | string  | não         |


# 📂 Folder

Define a pasta lógica no Cloudinary.

Exemplo:
submissions
projects
avatars

O caminho final fica:

smart_forms/{folder}

Exemplo:

smart_forms/projects

# 📤 Resposta
{
  "url": "https://res.cloudinary.com/..."
}


📌 Exemplo de Uso — Logo do Projeto
1. Upload da imagem
POST /uploads/image

Retorno:

{
  "url": "https://res.cloudinary.com/demo/image/upload/logo.png"
}
2. Atualização do projeto
PATCH /projects/{id}

Body:

{
  "logoUrl": "https://res.cloudinary.com/demo/image/upload/logo.png"
}
📌 Exemplo de Uso — Imagem em Submissão
{
  "formData": {
    "nome": "Claudio",
    "foto_atividade": "https://res.cloudinary.com/demo/image/upload/foto.png"
  }
}
🧠 Use Case
UploadImageUseCase

Responsável por:

validar extensão
validar tamanho
chamar storage service
retornar URL final
☁️ Infrastructure Layer
CloudinaryService

Responsável por:

comunicação com Cloudinary
upload
compressão
transformação
tags
geração da URL
🧩 Tags Automáticas

O upload adiciona tags:

user_{id}
tcc_project

Exemplo:

user_123
tcc_project

Isso ajuda:

organização
busca futura
auditoria
limpeza automática
🚨 Exceptions
InvalidImageFormatException

Retornada quando a extensão não é permitida.

Resposta:

{
  "detail": "Formato de imagem inválido."
}
ImageTooLargeException

Retornada quando a imagem excede 5MB.

Resposta:

{
  "detail": "Imagem muito grande. Máximo permitido: 5MB."
}
UploadImageException

Retornada quando ocorre erro interno no upload.

Resposta:

{
  "detail": "Erro ao realizar upload da imagem."
}