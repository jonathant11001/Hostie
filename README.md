<p align="center"> <img width="375" height="150" alt="Hostie Logo" src="https://github.com/user-attachments/assets/cfeab7b3-54bf-4fa6-ae49-cfec23f928f5" /> </p>
<p align="center"> 
            <a>
                        <img src="https://img.shields.io/badge/python-3.11-blue" alt="Python Version">
            </a>
            <a>
                        <img src="https://img.shields.io/badge/node-v20.2.0-green" alt="Node Version">
            </a>
            <a href="https://opensource.org/license/MIT">
                        <img src="https://img.shields.io/badge/license-MIT-blue" alt="License">
            </a>
</p>

---

### Multi-Tenant AI Customer Support Platform for Restaurants

Hostie is an AI-powered SaaS platform that enables restaurants to deploy an intelligent chat assistant on their website to automatically answer customer questions about menus, hours, reservations, dietary options, and policies.

Designed as a scalable, production-ready full-stack system.

---

## 🏗 System Architecture
```
Restaurant Dashboard (Frontend)
            ↓
FastAPI Backend (API Layer)
            ↓
PostgreSQL (Structured Data)
            ↓
Vector Search (Embeddings)
            ↓
OpenAI API (LLM Responses)
            ↓
Embeddable Chat Widget (Client Website)
```
---

## 🧠 Core Features

### 🏢 Multi-Tenant SaaS Architecture
- Isolated restaurant data
- API key–based access control
- Secure database schema design
- Scalable backend structure

### 🛠 Restaurant Admin Dashboard
- Account registration & authentication
- Business information management
- Document upload (menus / FAQs)
- AI assistant configuration (planned)

### 🤖 AI Chat Engine
- Context-aware responses
- Semantic search over uploaded documents
- Restaurant-specific knowledge retrieval
- Customizable tone (planned)

### 💬 Embeddable Chat Widget

Restaurants can embed(Not Designed Yet):

```html
<script src="https://yourdomain.com/widget.js">
        <data-api-key="restaurant_api_key">
</script>
```
And instantly activate their AI assistant on their website.

---

## 📂 Structure

```
hostie/
│
├── backend/         # FastAPI API
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│
├── frontend/        # Restaurant dashboard (Next.js / React)
│
├── widget/          # Embeddable JavaScript chat widget
│
├── docker-compose.yml
├── README.md
```
---

## 🛠 Tech Stack

### Backend
- FastAPI
- SQLAlchemy
- PostgreSQL
- pgvector (vector search)
- OpenAI API
- JWT Authentication

### Frontend
- Next.js / React
- TailwindCSS (optional)

### Infrastructure
- Docker
- Docker Compose
- AWS (planned deployment)
- GitHub Actions (planned CI/CD)

---

## Author

Built by Jonathan Tam
Software Engineer focused on AI-driven SaaS systems.

---
