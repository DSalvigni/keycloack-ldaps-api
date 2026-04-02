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

###Fire up the Lab
```bash
docker-compose up -d
```


##  Explanation of the Use Case: 
Explain this to your colleague as a "3-Step Handshake" between LDAP, Keycloak, and the API. Since docker-compose up -d is already running, here is the exact sequence to get that Token and use it.

🚀 How to Authenticate "Pippo" (Step-by-Step)

Follow these steps to synchronize the LDAP user into Keycloak, generate an OAuth2 Token, and access the protected API.

1. Synchronize the LDAP User
Before Pippo can log in, Keycloak must "see" him from the OpenLDAP server.

    - Access the Keycloak Admin Console: http://localhost:8080 (Login: admin/admin).
    - Switch to the "Laboratorio" Realm (top-left corner).
    - Go to User Federation -> Click on "MioLDAP".
    - Click the Action button (top right) and select "Sync all users".
        ✅ You should see a message: "Success! 1 users imported".

2. Prepare the Account (First-Time Only)
Keycloak often requires new users to update their profile. We need to disable this for our automated test:

    - Go to Users -> Click "View all users" (or search for pippo).
    - Click on pippo -> Details tab.
    - Locate "Required User Actions" and click the "X" on every item (e.g., Update Password).
    - Ensure Enabled is ON and click Save.

3. Generate the Access Token (The curl command)
Now, ask Keycloak for a "Passport" (JWT Token) by exchanging Pippo's credentials.
Note: Replace YOUR_CLIENT_SECRET with the secret found in Clients -> mia-api -> Credentials tab.
    ```bash
    curl -X POST 'http://localhost:8080/realms/Laboratorio/protocol/openid-connect/token' \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    -d 'grant_type=password' \
    -d 'client_id=mia-api' \
    -d 'client_secret=YOUR_CLIENT_SECRET' \
    -d 'username=pippo' \
    -d 'password=pippo'
    ```

4. Access the Protected API
If the command above returns a long string called access_token, copy it and use it to "knock" on the API's door:
    
    # Replace <TOKEN> with the long string received in step 3
    ```bash
    curl -H "Authorization: Bearer <TOKEN>" http://localhost:8000
    ```
        Expected Result:
        The API should reply: "Welcome Pippo! I received your Token...".
        🔍 Troubleshooting for your colleague:

            -> Error unauthorized_client: Go to Keycloak -> Clients -> mia-api -> Settings. Ensure Direct access grants is ON.
            -> Error invalid_grant: Usually means the "Required Actions" from Step 2 were not cleared.
            -> Connection Refused: Ensure the Python API container is running (docker logs api_test).

5. SLES 15 OS-Level Integration (System Authentication)
While Keycloak handles modern web authentication (Tokens/OAuth2), the SLES 15 container demonstrates how a Linux server can natively "trust" our LDAP directory for system-level users.

    A. Access the SLES Container
    Open a terminal and enter the SUSE machine:
    ```Bash
    docker exec -it sles_test /bin/bash
    ```
    B. Configure the LDAP Client (Automatic Setup)
    Run this command inside the SLES container to install the necessary tools and point the OS to our OpenLDAP server:
    ```Bash

    # 1. Install LDAP client and NSS/PAM modules
    zypper install -y openldap-cpp-client nss-pam-ldapd && \

    # 2. Configure the LDAP daemon connection
    echo -e "uid nslcd\ngid nslcd\nuri ldap://openldap:389\nbase dc=esempio,dc=it\nbinddn cn=admin,dc=esempio,dc=it\nbindpw admin" > /etc/nslcd.conf && \

    # 3. Tell the OS to look into LDAP for users and groups
    sed -i 's/passwd:     compat/passwd:     compat ldap/g' /etc/nsswitch.conf && \
    sed -i 's/group:      compat/group:      compat ldap/g' /etc/nsswitch.conf && \

    # 4. Start the synchronization service
    nslcd &
    ```

    C. Verify System-Level Identity
    To prove that SLES now recognizes the LDAP user pippo (even though he doesn't exist in /etc/passwd), run:
    Bash
    ```
    id pippo
    ```
        ✅ Success Result: > uid=1000(pippo) gid=10000(paperopoli) groups=10000(paperopoli)

    💡 Why this is important (The "Enterprise" Value)

    By integrating SLES with LDAP, you have created a Centralized Identity Management system:

        -> Single Point of Truth: User pippo is created only once in OpenLDAP.
        -> Web Security: Keycloak authenticates pippo for web apps and APIs using Modern OIDC Tokens.
        -> Infrastructure Security: SLES authenticates pippo for server access (SSH, Console) using the same LDAP credentials.

If you change Pippo's password in LDAP, it updates instantly across the entire stack—from the Python API to the Linux Terminal.