# EzTo Gym Platform

EzTo is an all-in-one **gym management platform** that combines:

- A modern **web client** for staff and administrators.
- A **FastAPI** backend exposing REST APIs.
- A **Firebase / Firestore** database for real-time, serverless persistence.
- A separate **configuration repository** (`ezto-config`) for environment-specific settings.

The platform centralizes membership management, access control, payments, inventory, classes, reservations and dashboards for one or multiple gyms.

> **Note:** In production you will usually manage environment variables through the
> **`ezto-config`** repository and your deployment platform (Vercel, server, etc.).
> The `.env` examples in this document are mainly for **local/manual setups**.

---

## Table of Contents

1. [High-Level Architecture](#high-level-architecture)
2. [Services Overview](#services-overview)
   - [Client Web App](#client-web-app)
   - [API Service (FastAPI)](#api-service-fastapi)
   - [Configuration Repository (`ezto-config`)](#configuration-repository-ezto-config)
3. [Database Design (Firestore)](#database-design-firestore)
4. [Service Dependencies and Startup Order](#service-dependencies-and-startup-order)
5. [Environment Configuration](#environment-configuration)
   - [Global / Shared](#global--shared)
   - [Backend `.env` example](#backend-env-example)
   - [Frontend `.env` example](#frontend-env-example)
6. [Local Development Setup](#local-development-setup)
7. [Database Setup and Seeding](#database-setup-and-seeding)
8. [Production Configuration & Deployment Notes](#production-configuration--deployment-notes)
9. [Security & Best Practices](#security--best-practices)
10. [Troubleshooting](#troubleshooting)

---

## High-Level Architecture

EzTo is organized as:

- **Main repository: `ezto`**
  - `client/` – TypeScript React/Next.js web application (deployed on Vercel).
  - `server/` – Python FastAPI backend exposing REST APIs for all gym operations.

- **Configuration repository: `ezto-config`**
  - Stores environment-specific configuration files (development, staging, production).
  - Has at least two branches: `main` (default) and `prod` (production configuration).

- **Firebase project**
  - Uses **Cloud Firestore** as the primary database.
  - Main collections:
    - `access_alerts`, `access_logs`
    - `classes`, `events`
    - `dashboard`
    - `gyms`
    - `inventory_movements`
    - `members`, `user_memberships`
    - `membership_plans`
    - `payment_logs`
    - `personal`
    - `products`, `promotions`
    - `reservations`
    - `suppliers`
    - `users`

### Data Flow

1. Users interact with the **web client**.
2. The client calls the **FastAPI backend** using JSON over HTTPS.
3. The backend reads/writes entities from **Firestore** via the Firebase Admin SDK.
4. Configuration values (keys, IDs, URLs) are provided via environment variables and, in most deployments, the **`ezto-config`** repository.

---

## Services Overview

### Client Web App

**Location:** `client/`  
**Technology:** TypeScript, React/Next.js (or similar), bundled and deployed on Vercel.

**Responsibilities**

- Authentication UX (login / sign-up / password reset).
- Dashboard views for:
  - Members, memberships and plans.
  - Class schedule, reservations and events.
  - Inventory and product management.
  - Payments and access control logs.
- Communicates exclusively with the FastAPI backend (no direct DB access).

**Key Dependencies**

- REST API URL (e.g. `NEXT_PUBLIC_API_URL`).
- Firebase client configuration (for auth / analytics if used).
- UI libraries as defined in `package.json`.

---

### API Service (FastAPI)

**Location:** `server/`  
**Technology:** Python 3.x, FastAPI, Uvicorn/ASGI.

**Responsibilities**

- Exposes REST endpoints for all core domains:
  - **Users & Authentication**
  - **Members & Memberships**
  - **Gyms & Facilities**
  - **Inventory & Products**
  - **Access Control & Security**
  - **Dashboard & Analytics**

**Typical Structure (conceptual)**

- `app/main.py` – FastAPI application factory / entry point.
- `app/routers/` – API routers (users, members, payments, inventory, etc.).
- `app/services/` – Domain logic and integration with Firebase.
- `app/config/` – Settings, configuration loading from environment variables.
- `app/models/` – Pydantic models (request/response schemas).

> The exact folder names may differ; adjust this section to match your codebase.

---

### Configuration Repository (`ezto-config`)

**Repository:** `Jhuly1215/ezto-config`  

This repo centralizes configuration for multiple environments. A common pattern is:

- **Branches**
  - `main` – development / staging configuration.
  - `prod` – production configuration.

- **Contents (example)**
  - Templates for backend and frontend environment files:
    - `.env.backend.dev`, `.env.backend.prod`
    - `.env.client.dev`, `.env.client.prod`
  - Optional Firebase service account references (ideally kept in a secret manager, not committed).
  - Documentation of which Firebase project / domain corresponds to each environment.

> In CI/CD, `ezto-config` is typically used to **inject environment variables** into the runtime.
> In that case you **don’t need to manually create local `.env` files on the server**; those examples
> below are only for local development or when running outside your usual pipeline.

---

## Database Design (Firestore)

EzTo uses **Cloud Firestore** (NoSQL document database).  
Below is a high-level description of each collection:

| Collection           | Purpose                                                                                      |
|----------------------|----------------------------------------------------------------------------------------------|
| `users`              | Application users (admins, trainers, receptionists, etc.).                                  |
| `members`            | Gym members / clients.                                                                      |
| `membership_plans`   | Plan templates (monthly, yearly, premium, student, etc.).                                   |
| `user_memberships`   | Active & historical memberships per member.                                                 |
| `payment_logs`       | Records of each successful or failed payment.                                               |
| `access_logs`        | Normal access events when a member taps card / mobile.                                      |
| `access_alerts`      | Suspicious or rejected access attempts that require review.                                 |
| `gyms`               | Gym branches or locations.                                                                  |
| `classes`            | Group training sessions / classes.                                                          |
| `events`             | Special events, workshops, or promotions that are scheduled.                                |
| `reservations`       | Reservations for classes, events, or specific time slots.                                  |
| `products`           | Products sold in the gym store (drinks, supplements, etc.).                                 |
| `inventory_movements`| Stock in/out, adjustments, transfers between gyms.                                          |
| `suppliers`          | Product suppliers or partners.                                                              |
| `promotions`         | Promotions / discounts for products or membership plans.                                    |
| `dashboard`          | Cached metrics & aggregated stats for faster dashboard rendering.                           |
| `personal`           | Personal training sessions or one-to-one services.                                          |

> Exact fields depend on the implementation; the table above describes the **intended role** of each collection.

---

## Service Dependencies and Startup Order

To run the complete stack locally:

1. **Firebase project**
   - Firebase project with Firestore in **Native mode**.
   - Service account credentials with permissions to read/write Firestore.

2. **Configuration (`ezto-config`)**
   - Clone `ezto-config`.
   - Choose the correct branch (`main` for development, `prod` for production).
   - EITHER:
     - Use its contents to generate `.env` files for local dev, **or**
     - Use it only in CI/CD so your hosting injects variables directly (no local `.env` on the server).

3. **Backend (FastAPI server)**
4. **Client (web app)**

The runtime chain is:

- The **client** depends on the **backend**.
- The **backend** depends on:
  - Correct **Firebase** credentials.
  - Correct **environment configuration** from `.env` **or** `ezto-config`.

---

## Environment Configuration

All services are configured via environment variables.  
`ezto-config` is the **single source of truth** for per-environment values.

- For **local development**, you usually copy a template from `ezto-config` into `.env` files.
- For **production**, you typically configure your deployment platform to read values
  directly from `ezto-config` (or a secrets manager) and inject them as env vars.
  In that case, you **do not need `.env` files** on the production servers.

### Global / Shared

Recommended global variables:

- `ENVIRONMENT` – `development`, `staging`, `production`, etc.
- `FIREBASE_PROJECT_ID`
- `FIREBASE_CLIENT_EMAIL`
- `FIREBASE_PRIVATE_KEY`
- `FIREBASE_DATABASE_URL`
- `LOG_LEVEL`

### Backend `.env` example

> **Only required when you are running the backend manually or for local development.**
> If your pipeline already reads everything from `ezto-config`, you can skip creating this file
> and let your deployment inject the variables.

```env
# General
ENVIRONMENT=development
API_PORT=8000
API_HOST=0.0.0.0

# CORS
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Firebase / Firestore
FIREBASE_PROJECT_ID=your-firebase-project-id
FIREBASE_CLIENT_EMAIL=firebase-adminsdk@example.iam.gserviceaccount.com
FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n"
FIREBASE_DATABASE_URL=https://your-firebase-project-id.firebaseio.com

# Auth & security
JWT_SECRET=replace-with-strong-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
````

### Frontend `.env` example

> Same idea: you only need this locally. In production, Vercel reads env vars you define,
> often based on what is stored in `ezto-config` or your secrets manager.

```env
# API base URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Optional – Firebase client SDK (if used directly in the client)
NEXT_PUBLIC_FIREBASE_API_KEY=
NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN=
NEXT_PUBLIC_FIREBASE_PROJECT_ID=
NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET=
NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID=
NEXT_PUBLIC_FIREBASE_APP_ID=
```

---

## Local Development Setup

1. **Clone the repositories**

```bash
# Main application
git clone https://github.com/ChristianMendozaa/ezto.git
cd ezto

# Configuration repo (optional but recommended)
git clone https://github.com/Jhuly1215/ezto-config.git
```

2. **Prepare environment variables**

You have two options:

* **Option A – Use `ezto-config` templates (recommended)**
  Copy the appropriate templates from `ezto-config`:

  ```bash
  # Backend
  cp ../ezto-config/.env.backend.dev server/.env

  # Frontend
  cp ../ezto-config/.env.client.dev client/.env.local
  ```

* **Option B – Create `.env` files manually**
  Use the examples in this README and fill in your own values.

3. **Backend setup**

```bash
cd server
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Client setup**

```bash
cd ../client
npm install  # or pnpm / yarn
npm run dev
```

5. **Access the app**

* Open `http://localhost:3000` in your browser.

---

## Database Setup and Seeding

1. Create a **Firebase project**.
2. Enable **Firestore (Native mode)**.
3. Create a **service account** with Firestore access.
4. Expose its credentials as environment variables (or via your platform’s secret manager).
5. Optionally run a **seeding script** (if provided in `server/scripts`) to create:

   * Default `gyms`
   * Basic `membership_plans`
   * Example `products`, `suppliers`
   * An initial admin user in `users`

---

## Production Configuration & Deployment Notes

* **Frontend (Vercel)**

  * Configure project env vars in Vercel UI.
  * Values come from `ezto-config` / secrets manager.
  * `NEXT_PUBLIC_API_URL` must point to your live backend URL.

* **Backend**

  * Deploy on an ASGI-compatible host (Docker, VM, etc.).
  * Set environment variables from `ezto-config` (no `.env` file required on the server).
  * Run via Uvicorn/Gunicorn with multiple workers in production.

* **Configuration management**

  * Treat `ezto-config` as the canonical reference for which variables exist and how they differ per environment.
  * Do **not** commit real secrets in either repo; keep only templates and non-sensitive defaults.

---

## Security & Best Practices

* Never commit Firebase service account JSON files to Git; use environment variables or a secret manager.
* Restrict CORS to known domains.
* Enforce role-based access control in the backend.
* Store all timestamps in UTC; configure gym time zones in the `gyms` collection.
* Regularly review `payment_logs`, `access_logs` and `access_alerts`.

---

## Troubleshooting

* **Client: “Network Error”**

  * Check `NEXT_PUBLIC_API_URL`.
  * Verify the backend is running and CORS is correctly configured.

* **Backend: Firestore connection errors**

  * Confirm all Firebase env vars are correctly set (especially private key formatting).
  * Check that the service account has permission to access Firestore.

* **CORS issues**

  * Update `ALLOWED_ORIGINS` to include the frontend URLs for dev and prod.

---

## License

This project is part of a university / hackathon / portfolio initiative.
Check the repository’s LICENSE file or add one if required.

