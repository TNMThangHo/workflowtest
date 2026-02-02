# 🌐 Project Reference Hub & Knowledge Base

This document serves as the **Single Source of Truth** for all external resources, specifications, and knowledge associated with the project.

> **Guideline**: If it's an external link, credential, or doc, it **MUST** be listed here.

---

## 🚨 Critical Resources (Quick Access)

| Project Component | Resource Name             | Link / Path                            | Status   |
| :---------------- | :------------------------ | :------------------------------------- | :------- |
| **Main Repo**     | GitHub Repository         | `[Insert Git URL]`                     | Active   |
| **Production**    | Live URL                  | `[Insert Prod URL]`                    | Stable   |
| **Staging**       | Dev/Test Env              | `[Insert Staging URL]`                 | unstable |
| **Emergency**     | Critical Incident Channel | `[Insert Slack/Teams Link]`            | -        |
| **CI/CD**         | Pipeline Dashboard        | `[Insert Jenkins/GitHub Actions Link]` | -        |

---

## 🎨 Design & Experience (UI/UX)

**Primary Design Source**: Figma is the final authority for UI/UX.

### 🖌️ Design Files

| Module / Feature  | Tool      | Link                                                                         | Notes                          |
| :---------------- | :-------- | :--------------------------------------------------------------------------- | :----------------------------- |
| **Main System**   | Figma     | `[Insert Main Figma Link]`                                                   | Core Screens                   |
| **Design System** | Figma     | `[Insert Design System Link]`                                                | Components, Colors, Typography |
| **Signup Flow**   | Stitch    | [Check Preview](https://stitch.withgoogle.com/projects/17188758224360973428) | Prototype                      |
| **Assets**        | Drive/DAM | `[Insert Asset Folder]`                                                      | Icons, Images, Logos           |

### 🔍 Style Guidelines

- **Color Palette**: See Design System (Primary: `#XXXXXX`, Secondary: `#XXXXXX`)
- **Typography**: Font Family: `[Insert Font Name]`
- **Grid System**: `[e.g., 12-column, 8px grid]`

---

## 🔌 API & System Architecture

**Primary API Source**: Swagger/OpenAPI (for implementation) + Postman (for testing).

### 🛠️ API Specifications

| Service Name        | Type           | Doc Link                       | Auth Method  |
| :------------------ | :------------- | :----------------------------- | :----------- |
| **Core API**        | Swagger        | `[Insert Swagger URL]`         | Bearer Token |
| **Auth Service**    | Postman        | `[Insert Postman Public Link]` | OAuth2       |
| **Payment Gateway** | 3rd Party Docs | `[Insert Stripe/Paypal Docs]`  | API Key      |

### 🏗️ Architecture & Database

- **System Overview**: `docs/architecture/system_overview.md` (Local)
- **Database Schema (ERD)**: `[Insert ERD Tool Link]` (e.g., dbdiagram.io)
- **Data Dictionary**: `[Insert Link to Data Dict]`

---

## ⚙️ Development Environment

### 🔧 Setup & Configuration

- **Env Template**: `.env.example` (Check this file for required keys)
- **Local Run**: `README.md` -> Section "Getting Started"
- **Seeding Data**: `npm run seed` / `python manage.py seed`

### 📦 Key Libraries & Versioning

- **Frontend**: React vX.X, Tailwind vX.X
- **Backend**: Node vX.X / Python vX.X
- **Test Framework**: Playwright vX.X, Jest vX.X

---

## 🔐 Credentials & Access (Safe Links)

> **⚠️ SECURITY WARNING**: NEVER put actual passwords/keys here. Only link to secure vaults (1Password, LastPass, Vault).

- **Shared Dev Accounts**: `[Link to 1Password Item]`
- **Test Users List**: `docs/test_data/test_users.csv` (Local) or `[Link to Sheet]`
- **Cloud Console**:
  - AWS/GCP/Azure Console: `[Link]`
  - Cloudflare Dashboard: `[Link]`

---

## 📚 Knowledge Base & Protocols

### 📝 Process Documentation

- **Git Workflow**: `docs/processes/git_strategy.md` (Branching, Commits)
- **Deployment Guide**: `docs/processes/deployment.md`
- **Troubleshooting**: `docs/troubleshooting.md`

### 🧠 Decision Logs (ADR)

- **ADR-001**: Architecture Choice (`docs/adr/001-architecture.md`)
- **ADR-002**: Database Selection (`docs/adr/002-database.md`)

---

## 🏷️ Vocabulary & Glossaries

- **Domain Terms**: Definition of business specific terms (e.g., "SKU variant", "Cohort").
- **Acronyms**: Meaning of abbreviations used in code/docs.
