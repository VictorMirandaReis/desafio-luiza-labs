# Pedido Normalizer API

Uma API REST que recebe arquivos legados com pedidos desnormalizados, processa e retorna os dados em formato JSON normalizado.

---

## 🔧 Tecnologias e Decisões

### Linguagem

- **Python 3.11**
- Utilizei o mínimo de dependências possível para manter o projeto leve e fácil de manter.

### Framework Web

- **FastAPI**: 

### Servidor

- **Uvicorn**: servidor ASGI leve e compatível com aplicações FastAPI. Recomendado pela própria documentação do framework.

### Banco de Dados

- **PostgreSQL**: escolhido por ser robusto, confiável e amplamente usado. Em alternativa, bancos como SQLite poderiam ser utilizados, mas optei pelo PostgreSQL para demonstrar uma estrutura mais próxima do real em produção.

### ORM

- **SQLAlchemy 2.x**: utilizado para mapeamento objeto-relacional. Permite manter o projeto desacoplado e alinhado com boas práticas.

### Docker

- O projeto está pronto para ser executado em containers Docker, incluindo o banco de dados e a aplicação web.

---

## 📁 Estrutura de Pastas

```bash
.
├── samples/            # Arquivos de exemplo usados para testes manuais
├── src/                # Código-fonte principal da aplicação
│   ├── api/            # Camada de apresentação e controladores HTTP
│   │   ├── controllers/    # Controladores organizados por domínio
│   │   │   └── formatters/ # Funções auxiliares para saída de dados
│   │   └── utils/          # Validações, respostas padrão e handlers
│   ├── core/           # Lógica de negócio da aplicação
│   │   └── order/       # Funcionalidades específicas do domínio "orders"
│   ├── db/             # Integração com banco de dados (SQLAlchemy)
├── tests/              # Testes automatizados (pytest)
```

Como o projeto é pequeno decidi criar as tabelas e models em só um arquivo, mas poderia usar alguma ferramenta para gerenciamento de migrations e versionar

Criei um pequeno script entrypoint.sh só para organizar os códigos de inicialização do sistema (criar tabelas e iniciar servidor)

Deixo as exceptions "explodirem" porque o controller captura elas e já formata (handlers)

Não era requisito do projeto, mas adicionei paginação e filtro por usuário.

Como o escopo do projeto é pequeno, tomei a decisão de não implementar certas features, porém tenho em mente as possíveis melhorias:

Como possíveis melhorias:
- adicionaria cache 
- Adicionaria testes completos e2e, simulando envio de arquivos, listagem de pedidos, etc
- Colocaria autenticação, via token, etc

Observações:
No documento do desafio não fala explicitamente, porém 
- Produtos com ID igual a zero estão sendo ignorados

🚀 Executando o projeto
Pré-requisitos:

Docker e Docker Compose instalados

# Como iniciar?

make start

Inicia os containers (API Python e Postgres)

make down

Inicia os containers (API Python e Postgres)

Endpoints disponíveis:

POST /orders — upload de arquivo legado

GET /orders — lista pedidos processados (com filtros por data e ID)

GET /orders/{id} — lista pedidos processados (com filtros por data e ID)

✅ Checklist do desafio
 Upload de arquivo via API
 Retorno dos dados em JSON normalizado
 Filtros por ID do pedido, user_id e data de compra
 Testes automatizados
 Documentação clara da API

📌 Observações
