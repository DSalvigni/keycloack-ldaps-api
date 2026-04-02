# 🚀 The "Pippo" Auth-Stack Laboratory
### LDAP + Keycloak + Secure API + SLES Integration

Welcome to the ultimate playground for Identity and Access Management (IAM). This project demonstrates a full-stack authentication flow: from a legacy **LDAP** directory to modern **OIDC (OpenID Connect)** tokens, all the way to OS-level integration on **SUSE Linux**.

---

## 🏗️ Architecture Overview

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Identity Source** | 🐘 OpenLDAP | The "Source of Truth" where user `pippo` lives. |
| **IAM Engine** | 🔑 Keycloak | The brain. Syncs users from LDAP and issues JWT tokens. |
| **Protected API** | 🐍 Python | A microservice that only talks to people with a valid "pass". |
| **System Client** | 🦎 SLES 15 | A SUSE container synced with LDAP via PAM/NSS. |
| **Management** | 🕸️ phpLDAPadmin | GUI to manage our LDAP tree without losing our minds. |

---

## 🛠️ The "Pippo" Flow

1.  **Storage**: `pippo` is created in **OpenLDAP** (`dc=esempio,dc=it`).
2.  **Federation**: **Keycloak** connects to LDAP and "discovers" Pippo.
3.  **Authentication**: You ask Keycloak for a token using Pippo's credentials.
4.  **Authorization**: You use that **JWT Token** to access the **Python API**.
5.  **OS Sync**: The **SLES** machine recognizes Pippo's UID thanks to `nslcd`.

---

## 🚀 Quick Start

### 1. Fire up the Lab
```bash
docker-compose up -d