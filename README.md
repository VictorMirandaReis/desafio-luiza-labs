# Desafio LuizaLabs

Uma API REST que recebe arquivos legados com pedidos desnormalizados, processa e retorna os dados em formato JSON normalizado.

---

## 🔧 Tecnologias e Decisões

### Linguagem

- **Python**: A linguagem escolhida para desenvolver o desafio foi o [Python](https://www.python.org/), por sua simplicidade e facilidade de uso, além da sua alta performance, escalabilidade e capacidade de facilitar a normalização de dados.

### Framework Web

- **FastAPI**: A escolha pelo [FastAPI](https://fastapi.tiangolo.com/) se deu por ser um framework de alta performance, com sintaxe simples e clara, validação automática de dados e geração de documentação interativa. Ele se mostra ideal para as necessidades deste projeto, que envolve a construção de uma API moderna e eficiente.

### Servidor

- **Uvicorn**: Servidor ASGI leve e compatível com aplicações FastAPI. Recomendado pela própria documentação do framework.

### Banco de Dados

- **PostgreSQL**: Escolhido por ser robusto, confiável e amplamente usado. Em alternativa, bancos como SQLite poderiam ser utilizados, mas optei pelo PostgreSQL para demonstrar uma estrutura mais próxima do real em produção.

### ORM

- **SQLAlchemy 2.x**: Utilizado para mapeamento objeto-relacional. Permite manter o projeto desacoplado e alinhado com boas práticas.

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

- Como o projeto é pequeno, optei por manter os models e definições de tabelas em um único arquivo. Porém, seria possível utilizar uma ferramenta de migração para versionamento de banco.

- Implementei um pequeno script entrypoint.sh para organizar os comandos de inicialização do sistema, como a criação das tabelas e o start do servidor.

- As exceções são lançadas diretamente, pois os controllers já são responsáveis por capturá-las e tratá-las por meio de handlers personalizados.

- Apesar de não ser um requisito do desafio, incluí funcionalidades extras como paginação e filtragem por usuário para tornar a API mais completa e flexível.

### 📐 Modelagem do Banco de Dados
<img src="docs/modelagem.png" width="350" />

- Embora o desafio não exigisse explicitamente, optei por incluir campos como external_id, external_order_id e external_product_id para separar os identificadores internos (usados pelo banco de dados) dos identificadores externos (vindos do arquivo legado ou sistemas externos). Isso facilita a organização e rastreabilidade dos dados importados, evita conflitos de ID interno do banco de dados em integrações externas e permite maior flexibilidade para futuras adaptações ou migrações.

## 📝 Observações

Embora não esteja especificado explicitamente no documento do desafio, tomei a decisão de ignorar produtos com ID igual a zero, assumindo que esses registros não são válidos para o contexto da aplicação.

## 🚀 Executando o Projeto

### ✅ Pré-requisitos

- [Docker](https://www.docker.com/) instalado  
- [Docker Compose](https://docs.docker.com/compose/) instalado  
- [Make](https://www.gnu.org/software/make/) instalado (apenas para Linux/macOS)  


> 💡 **Usuários Windows:**  
Se estiver utilizando Windows, os comandos `make` podem não funcionar diretamente. Neste caso, recomenda-se executar os comandos equivalentes manualmente via terminal ou usar o WSL (Windows Subsystem for Linux).

---

### ▶️ Como iniciar o projeto?

Execute o comando `make start` para inicializar os containers da aplicação:

- API Python (FastAPI)  
- Banco de dados PostgreSQL  

Para parar e remover os containers, use `make down`.

Alternativamente, você pode usar diretamente os comandos do Docker Compose:

```bash
docker-compose up --build
docker-compose down
```

### 📡 Endpoints Disponíveis

#### `POST /orders`: Realiza o upload de um arquivo legado contendo pedidos para processamento.

#### `GET /orders`: Lista todos os pedidos processados. 
 
Parâmetros opcionais:
- `user_id`: filtra os pedidos por ID de usuário
- `date`: filtra os pedidos por data (formato `YYYY-MM-DD`)

#### `GET /orders/{id}`: Retorna os detalhes de um pedido específico pelo ID.

## ✅ Checklist do Desafio

- Upload de arquivo via API
- Retorno dos dados em JSON normalizado
- Filtros por ID do pedido, `user_id` e data de compra
- Testes automatizados implementados
- Documentação clara e completa da API

## 🔧 Melhorias futuras do projeto

Como o escopo do projeto é pequeno, optei por não implementar algumas funcionalidades neste momento. No entanto, já considero as seguintes melhorias para versões futuras:

- Implementação de cache para otimizar o desempenho da API.

- Criação de testes completos de ponta a ponta (E2E), incluindo simulações de envio de arquivos, listagem de pedidos e fluxos completos.

- Adição de autenticação por token (como JWT), garantindo maior segurança no acesso aos endpoints.