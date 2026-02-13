# Railway Deployment Setup

## Prerequisites
1. GitHub repository deployed to Railway
2. Google Cloud Project with OAuth 2.0 credentials

## Setup Steps for Railway

### 1. Get Your Railway Public Domain
- Go to your Railway project dashboard
- Find your service in the "Services" tab
- Look for the "Public URL" or domain (e.g., `web-production-1eef.up.railway.app`)

### 2. Update Google Cloud OAuth Configuration
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project: **email-spam-detector-481512**
3. Go to **APIs & Services > Credentials**
4. Find your OAuth 2.0 Client ID (type: Web application)
5. Click on it to edit
6. Under **Authorized redirect URIs**, add:
   ```
   https://YOUR_RAILWAY_DOMAIN/oauth2callback
   ```
   Replace `YOUR_RAILWAY_DOMAIN` with your actual Railway domain
7. Click **Save**

### 3. Set Environment Variable on Railway
1. Go to Railway dashboard for your service
2. Click on **Variables** tab
3. Add a new variable: `RAILWAY_PUBLIC_DOMAIN`
   - Value: Your Railway domain (e.g., `web-production-1eef.up.railway.app`)
4. Click **Add**

### 4. Add Google Credentials as Secret
1. In Railway **Variables** tab, add: `GOOGLE_CREDENTIALS_JSON`
2. Value: Copy the entire JSON content from your `credentials.json` file:
   ```json
   {
     "installed": {
       "client_id": "...",
       "project_id": "...",
       "auth_uri": "...",
       ...
     }
   }
   ```
3. Click **Add**

### 5. Redeploy
1. Go to **Deployments** tab
2. Click the three dots on your latest deployment
3. Select **Redeploy**
4. Wait for the deployment to complete

### 6. Test
1. Open your Railway public URL
2. Click "Sign In"
3. You should be redirected to Google OAuth login

## Troubleshooting

**Still seeing "credentials.json not found"?**
- Check that `GOOGLE_CREDENTIALS_JSON` variable is set
- Make sure the JSON is properly formatted
- Redeploy after setting the variable

**Redirect URI mismatch error?**
- Verify the OAuth redirect URI matches exactly: `https://YOUR_DOMAIN/oauth2callback`
- Make sure `RAILWAY_PUBLIC_DOMAIN` is set correctly
- Redeploy to apply changes

**Need to update OAuth configuration?**
1. Update Google Cloud Console redirect URIs
2. Update `RAILWAY_PUBLIC_DOMAIN` on Railway if domain changed
3. Redeploy the service
