\# 🧠 EnterpriseBrain 360

\### AI-Powered Enterprise Knowledge \& Customer Intelligence Platform



<div align="center">



!\[Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge\&logo=python\&logoColor=white)

!\[FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?style=for-the-badge\&logo=fastapi\&logoColor=white)

!\[PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge\&logo=postgresql\&logoColor=white)

!\[AI](https://img.shields.io/badge/AI-RAG-8B5CF6?style=for-the-badge)

!\[Status](https://img.shields.io/badge/Status-Under\_Development-orange?style=for-the-badge)



\*\*Connecting Enterprise Knowledge with Customer Intelligence.\*\*



\[Overview](#-overview) • \[Architecture](#-system-architecture) • \[Features](#-implemented-features) • \[Tech Stack](#-technology-stack) • \[Setup](#-getting-started) • \[Roadmap](#-development-roadmap)



</div>



\---



\## 🚀 Overview



\*\*EnterpriseBrain 360\*\* is an AI-powered enterprise intelligence platform designed to unify enterprise knowledge retrieval, customer relationship data, and intelligent support workflows.



Modern organizations manage information across documents, customer databases, support tickets, and interaction histories. Finding the right information and understanding customer context across these systems can be challenging.



EnterpriseBrain 360 aims to address this by bringing enterprise knowledge and customer intelligence into one unified platform.



The platform combines:



\- 📚 \*\*Enterprise Knowledge Hub\*\* — Document ingestion, PDF text extraction, text chunking, embeddings, and semantic knowledge retrieval.

\- 👥 \*\*Customer 360\*\* — Centralized customer profiles, support tickets, and interaction histories.

\- 🤖 \*\*AI Copilot\*\* — Planned context-aware assistance combining customer information with relevant enterprise knowledge.

\- ⚙️ \*\*Intelligent Support Workflows\*\* — Planned ticket classification, priority recommendations, and resolution assistance.



> 🚧 \*\*Project Status:\*\* Actively under development. Customer 360 backend APIs and the initial document-processing and embedding pipeline have been implemented. RAG integration and the AI Copilot are upcoming.



\---



\## 🏗️ System Architecture



The platform follows a modular architecture with separate components for customer data, enterprise knowledge processing, and intelligent support workflows.



```mermaid

flowchart TD

&#x20;   A\["React Frontend"] --> B\["FastAPI Backend"]



&#x20;   B --> C\["Customer 360 Module"]

&#x20;   B --> D\["Enterprise Knowledge Hub"]

&#x20;   B --> E\["Workflow Engine"]



&#x20;   C --> F\[("PostgreSQL")]

&#x20;   D --> G\["PDF Processing"]

&#x20;   G --> H\["Text Extraction \& Chunking"]

&#x20;   H --> I\["BGE Embeddings"]

&#x20;   I --> J\[("ChromaDB - Planned")]



&#x20;   F --> K\["Context Assembly - Planned"]

&#x20;   J --> K



&#x20;   K --> L\["Ollama LLM"]

&#x20;   L --> M\["AI Copilot"]



&#x20;   style A fill:#dbeafe,stroke:#2563eb,color:#1e3a8a

&#x20;   style B fill:#ccfbf1,stroke:#0d9488,color:#134e4a

&#x20;   style C fill:#fef3c7,stroke:#d97706,color:#78350f

&#x20;   style D fill:#ede9fe,stroke:#7c3aed,color:#4c1d95

&#x20;   style J fill:#f3e8ff,stroke:#9333ea,color:#581c87

&#x20;   style M fill:#dcfce7,stroke:#16a34a,color:#14532d

```



\*The diagram represents the target architecture. Components marked as planned have not yet been implemented.\*



\### 🔄 How the Platform Will Work



1\. \*\*Document Ingestion:\*\* Upload enterprise PDF documents through the Knowledge Hub.

2\. \*\*Text Processing:\*\* Extract, clean, and divide document content into overlapping chunks.

3\. \*\*Embedding Generation:\*\* Convert text chunks into numerical vectors using a local embedding model.

4\. \*\*Knowledge Retrieval:\*\* Store embeddings in ChromaDB and retrieve relevant information using semantic similarity search.

5\. \*\*Customer Context:\*\* Retrieve customer profiles, support tickets, and interaction history from PostgreSQL.

6\. \*\*Context Assembly:\*\* Combine relevant customer information and enterprise knowledge.

7\. \*\*AI Response:\*\* Use a locally hosted LLM to generate context-aware support responses with source references.



\---



\## ✨ Implemented Features



\### 👥 1. Customer 360 Backend



\- Developed RESTful APIs using FastAPI and Pydantic.

\- Implemented customer creation, retrieval, updating, and deletion.

\- Built support ticket management APIs.

\- Implemented customer interaction history management.

\- Designed relational PostgreSQL tables with primary keys, foreign keys, and data constraints.

\- Developed a consolidated Customer 360 profile endpoint combining customer details, support tickets, and interactions.



\### 📚 2. Enterprise Knowledge Hub



\- Developed a PDF upload API with file type, content type, file size, and PDF signature validation.

\- Implemented page-wise PDF text extraction using PyMuPDF.

\- Added text cleaning and whitespace normalization.

\- Implemented overlapping text chunking with word-boundary adjustments.

\- Preserved document source, chunk ID, and page-number metadata for future citation support.

\- Integrated FastEmbed with the BGE-small embedding model for local embedding generation.

\- Generated 384-dimensional embedding vectors for document chunks.



\---



\## 🛠️ Technology Stack



| Category | Technologies |

|---|---|

| Programming Language | Python |

| Backend Framework | FastAPI, Pydantic |

| Frontend | React.js (planned) |

| Relational Database | PostgreSQL |

| Vector Database | ChromaDB (planned) |

| Embedding Model | BGE-small, FastEmbed |

| LLM Runtime | Ollama, Llama 3.2:1b |

| Document Processing | PyMuPDF |

| RAG Framework | LangChain (planned) |

| Testing | Pytest (planned) |

| API Testing | FastAPI Swagger UI |

| Version Control | Git, GitHub |



\### 🧠 AI and Retrieval Components



| Component | Purpose |

|---|---|

| BGE-small | Generates semantic embeddings from text |

| FastEmbed | Runs embedding generation locally |

| ChromaDB | Planned vector storage and similarity search |

| Ollama | Local LLM execution |

| Llama 3.2:1b | Planned context-aware response generation |



\---



\## 📂 Project Structure



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

│   └── test\_embeddings.py

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



\---



\## ⚙️ Getting Started



\### 📌 Prerequisites



Make sure the following tools are installed:



\- Python 3.13+

\- PostgreSQL 17+

\- Node.js 20+

\- Git

\- Ollama



\### 1. Clone the Repository



```bash

git clone https://github.com/Anushree195/EnterpriseBrain-360.git



cd EnterpriseBrain-360

```



\### 2. Create a Virtual Environment



```powershell

cd backend



python -m venv .venv



.\\.venv\\Scripts\\Activate.ps1

```



\### 3. Install Backend Dependencies



```powershell

python -m pip install fastapi uvicorn "psycopg\[binary]" python-dotenv pymupdf python-multipart fastembed

```



\### 4. Configure PostgreSQL



Create the database:



```sql

CREATE DATABASE enterprisebrain\_db;

```



Configure your local database connection in `backend/.env`:



```env

DB\_HOST=localhost

DB\_PORT=5432

DB\_NAME=enterprisebrain\_db

DB\_USER=postgres

DB\_PASSWORD=your\_local\_password

```



Create the `customers`, `support\_tickets`, and `interactions` tables using the database schema defined for this project.



\*\*Security:\*\* Never commit `.env` files, passwords, or private credentials to GitHub.



\### 5. Install and Configure Ollama



Install Ollama and download the model:



```powershell

ollama pull llama3.2:1b

```



Verify that the model is available:



```powershell

ollama list

```



\*Ollama integration with the RAG pipeline is planned.\*



\### 6. Start the FastAPI Backend



From the `backend` directory:



```powershell

python -m uvicorn main:app --reload

```



The backend will be available at:



\*\*Application:\*\* http://127.0.0.1:8000



\*\*Interactive API Documentation:\*\* http://127.0.0.1:8000/docs



\*\*Health Check:\*\* http://127.0.0.1:8000/health



\---



\## 🔌 API Modules



| API Module | Functionality |

|---|---|

| `/customers` | Customer lifecycle management |

| `/tickets` | Support ticket management |

| `/interactions` | Customer interaction history |

| `/knowledge` | Enterprise document upload and processing |



Explore the available endpoints through FastAPI Swagger UI.



http://127.0.0.1:8000/docs



\---



\## 🗺️ Development Roadmap



The project is being developed incrementally.



\- \[x] Project foundation and architecture

\- \[x] FastAPI backend initialization

\- \[x] PostgreSQL database integration

\- \[x] Customer 360 backend APIs

\- \[x] Support ticket and interaction management

\- \[x] PDF upload and validation

\- \[x] PDF text extraction and cleaning

\- \[x] Overlapping text chunking

\- \[x] Local embedding generation using BGE-small

\- \[ ] ChromaDB vector storage

\- \[ ] Semantic similarity search

\- \[ ] RAG pipeline implementation

\- \[ ] Source-grounded AI responses and citations

\- \[ ] Customer-context integration with RAG

\- \[ ] AI Copilot implementation

\- \[ ] Intelligent support workflows

\- \[ ] React frontend integration

\- \[ ] Comprehensive testing and documentation



\---



\## 🔮 Future Enhancements



\- Context-aware enterprise support assistance.

\- Semantic search across enterprise documents.

\- Retrieval-grounded responses with document citations.

\- Customer-specific issue analysis and resolution recommendations.

\- Intelligent support ticket classification and prioritization.

\- Unified enterprise knowledge and customer intelligence dashboard.



\---



\## 💡 Development Approach



EnterpriseBrain 360 follows a modular, API-driven development approach.



The MVP prioritizes:



\- Local-first AI development.

\- Open-source technologies.

\- Structured customer data management.

\- Reusable document-processing components.

\- Grounded responses using enterprise knowledge.

\- Secure handling of

