# GPT Text Summarizer Deployment Steps

This guide will walk you through building and deploying your Streamlit-based GPT text summarizer app using Docker and Azure services.

---

## 1. Prepare Docker Image

1. **Create `requirements.txt`**  
   ```bash
   pip freeze > requirements.txt
   ```

2. **Create a Dockerfile**

3. **Build the Docker image**
   ```bash
   docker build -t testimage .
   ```

4. **Verify the image**
   ```bash
   docker images
   ```

5. **Run Docker**
   ```bash
   docker run -p 8501:8501 testimage
   ```

6. **Access the app**  
   Navigate to → [http://localhost:8501](http://localhost:8501)

---

## 2. ☁️ Create an Azure Container Registry (ACR) and Push the Image

### From Azure Portal:

- Create new ACR (Private Network recommended)
- If access error when pushing:
  - Go to `ACR > Networking` and allow specific IP ranges
  - Go to `ACR > Access Keys` → enable Admin user

### From Azure CLI:

```bash
az login
az acr list --resource-group <resource-group-name> --output table
az account set --subscription "<subscription-id>"
az acr login --name <acr-name>

# Tag and Push Docker Image

docker tag <your_image_name> <acr-name>.azurecr.io/<your_image_name>:latest
docker push <acr-name>.azurecr.io/<your_image_name>:latest

# If error, re-authenticate or adjust IP access range

az acr repository list --name <acr-name> --output table
az acr credential show --name <acr-name>
```

### Deploy from Azure Portal:

- Go to `ACR > Repositories` → select image → Tags → `Deploy to WebApp`
- Fill in:
  - Web App name
  - Service Plan

---

## 3. App Registration & Authentication Setup

1. Go to Azure → App Registrations
2. Locate your app → Note down `Application (client) ID`
3. Add Platform → Web → 
   - Add Redirect URI:  
     ```
     https://<your-app-name>.azurewebsites.net/.auth/login/aad/callback
     ```
4. Enable:
   - ✅ ID tokens
   - ✅ Accounts in this organizational directory only

---

## 4. 👥 Restrict User Access

- Azure Portal → Enterprise Applications → Find your app
- Assign access:
  - Users and Groups → Add user or group → Use `Application (client) ID`

---

## 5. ⚙️ Adjust WebApp Settings

- **Authentication**
  - Enable App Service authentication
  - Require login for access
  - Identity Provider → Microsoft → use your `Application (client) ID`

---

## 6. 🔍 Monitor & Secrets

- Monitor Logs from Azure → `WebApp Logs`
- Add secrets to Key Vault:

  ```
  Key: gptappkey
  Value: <your-secret>
  ```

- Docs: [Azure Manage Secrets](https://learn.microsoft.com/en-us/azure/container-apps/manage-secrets?tabs=azure-portal)

---

