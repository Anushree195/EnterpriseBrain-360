\# EnterpriseBrain 360

\### AI-Powered Enterprise Knowledge \& Customer Intelligence Platform



EnterpriseBrain 360 is an AI-powered enterprise intelligence platform designed to unify enterprise knowledge retrieval, customer relationship data, and intelligent support workflows.



The platform aims to help support teams retrieve relevant information from enterprise documents, understand customer context, and generate context-aware responses using Retrieval-Augmented Generation (RAG).



\*\*Project Status:\*\* 🚧 Actively Under Development



\---



\## Project Overview



EnterpriseBrain 360 combines two important capabilities:



\- \*\*Enterprise Knowledge Hub:\*\* Processes enterprise documents, extracts information, generates embeddings, and enables semantic knowledge retrieval.

\- \*\*Customer 360:\*\* Consolidates customer profiles, support tickets, and interaction history into a unified customer view.



The planned AI Copilot will combine these capabilities to provide context-aware assistance to enterprise support teams.



\## Architecture



```text

&#x20;                EnterpriseBrain 360

&#x20;                        |

&#x20;                 React Frontend

&#x20;                        |

&#x20;                  FastAPI Backend

&#x20;                        |

&#x20;         +--------------+--------------+

&#x20;         |              |              |

&#x20;     Customer 360   Knowledge Hub   Workflow Engine

&#x20;         |              |              |

&#x20;     PostgreSQL     PDF Processing   Support Logic

&#x20;                        |

&#x20;                 Text Chunking

&#x20;                        |

&#x20;                 BGE Embeddings

&#x20;                        |

&#x20;                     ChromaDB

&#x20;                        |

&#x20;                 Semantic Retrieval

&#x20;                        |

&#x20;                Context Assembly

&#x20;                        |

&#x20;                 Ollama LLM

&#x20;                        |

&#x20;                   AI Copilot

```



\*Note: This represents the planned overall architecture. Some components are still under development.\*



\## Technology Stack



| Category | Technologies |

|---|---|

| Backend | Python, FastAPI |

| Frontend | React.js |

| Database | PostgreSQL |

| Vector Database | ChromaDB (planned) |

| Embeddings | FastEmbed, BGE-small |

| LLM Runtime | Ollama, Llama 3.2:1b |

| PDF Processing | PyMuPDF |

| RAG Orchestration | LangChain (planned) |

| Testing | Pytest (planned) |

| Version Control | Git, GitHub |



\## Implemented Features



\### 1. Customer 360 Backend



\- Developed REST APIs using FastAPI and Pydantic.

\- Implemented customer creation, retrieval, updating, and deletion.

\- Built support ticket management APIs.

\- Implemented customer interaction history management.

\- Designed relational PostgreSQL tables with foreign-key constraints.

\- Developed a consolidated Customer 360 profile endpoint combining customer details, tickets, and interactions.



\### 2. Enterprise Knowledge Hub



\- Implemented a PDF upload API with file validation.

\- Extracted PDF text page by page using PyMuPDF.

\- Added text cleaning and normalization.

\- Implemented overlapping text chunking.

\- Preserved source filename and page-number metadata for future document citations.

\- Generated 384-dimensional embeddings locally using FastEmbed and BGE-small.



\## Project Structure



```text

EnterpriseBrain-360/

│

├── backend/

│   ├── knowledge/

│   │   ├── \_\_init\_\_.py

│   │   ├── router.py

│   │   ├── document\_processor.py

│   │   └── embedding\_service.py

│   │

│   ├── main.py

│   ├── customer.py

│   ├── ticket.py

│   ├── interaction.py

│   ├── schemas.py

│   ├── database.py

│   ├── config.py

│   │

│   ├── test\_db.py

│   ├── test\_document.py

│   ├── test\_chunking.py

│   ├── test\_embeddings.py

│   │

│   └── .env.example

│

├── frontend/

│

├── data/

│   ├── documents/

│   └── sample\_data/

│

├── docs/

│

├── .gitignore

└── README.md

```



\## Local Setup



\### Prerequisites



Install the following:



\- Python 3.13+

\- PostgreSQL 17+

\- Node.js 20+

\- Ollama

\- Git



\### 1. Clone the Repository



```bash

git clone https://github.com/Anushree195/EnterpriseBrain-360.git



cd EnterpriseBrain-360

```



\### 2. Create and Activate a Python Virtual Environment



```powershell

cd backend



python -m venv .venv



.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install Backend Dependencies



```powershell

python -m pip install fastapi uvicorn psycopg\[binary] python-dotenv pymupdf python-multipart fastembed

```



\### 4. Configure PostgreSQL



Create the project database:



```sql

CREATE DATABASE enterprisebrain\_db;

```



Configure the database connection using a local `.env` file inside `backend/`.



Example configuration:



```env

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=enterprisebrain\_db

DB\_USER=postgres

DB\_PASSWORD=your\_local\_password

```



\*\*Security:\*\* Never commit your actual `.env` file or database credentials to GitHub.



\### 5. Start the Backend



From the `backend` directory:



```powershell

python -m uvicorn main:app --reload

```



Backend URL:



```text

http://127.0.0.1:8000

```



Interactive API documentation:



```text

http://127.0.0.1:8000/docs

```



\## API Modules



| Module | Purpose |

|---|---|

| `/customers` | Customer management |

| `/tickets` | Support ticket management |

| `/interactions` | Customer interaction history |

| `/knowledge` | Enterprise document processing |



Use the interactive Swagger documentation at `/docs` to explore and test available endpoints.



\## Current Development Roadmap



\- \[x] Project foundation and architecture

\- \[x] Customer 360 backend APIs

\- \[x] PDF upload and validation

\- \[x] PDF text extraction and cleaning

\- \[x] Text chunking with metadata

\- \[x] Local embedding generation

\- \[ ] ChromaDB vector storage

\- \[ ] Semantic similarity search and retrieval

\- \[ ] RAG pipeline with source citations

\- \[ ] Context-aware AI Copilot

\- \[ ] Intelligent ticket classification and priority recommendations

\- \[ ] React frontend integration

\- \[ ] Comprehensive testing and documentation



\## Future Goals



\- Context-aware enterprise support assistance.

\- Retrieval-grounded answers with document citations.

\- Customer-specific resolution recommendations.

\- Intelligent support ticket workflows.

\- Unified enterprise knowledge and customer intelligence.



\## Development Approach



The project follows a modular, API-driven architecture with a local-first AI development approach.



The MVP uses open-source tools and locally hosted models to minimize dependency on paid AI APIs.



\---



\## Author



\*\*Anushree Sindagi\*\*



B.Tech – Information Technology



GitHub: https://github.com/Anushree195



LinkedIn: https://www.linkedin.com/in/anushree-sindagi-842675259/



\---



\*EnterpriseBrain 360 — Connecting Enterprise Knowledge with Customer Intelligence.\*

