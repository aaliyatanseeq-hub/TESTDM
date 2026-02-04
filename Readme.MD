# Twitter DM Sender

Deploy this app to Render to send Twitter DMs.

## Deployment Steps

1. **Push to GitHub**
   - Create a new repo
   - Upload these files: `twitter_dm_app.py`, `requirements.txt`, `start.sh`

2. **Deploy on Render**
   - Go to https://render.com
   - Click "New" → "Web Service"
   - Connect your GitHub repo
   - Settings:
     - **Name**: twitter-dm-sender
     - **Environment**: Python 3
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `bash start.sh`

3. **Add Environment Variables**
   - Go to your service → Environment
   - Add these 5 variables:
     - `BEARER_TOKEN`
     - `CONSUMER_KEY`
     - `CONSUMER_SECRET`
     - `ACCESS_TOKEN`
     - `ACCESS_TOKEN_SECRET`
   - Copy values from your local `.env` file

4. **Deploy**
   - Click "Create Web Service"
   - Wait 2-3 minutes for deployment
   - Open the URL Render gives you

## Local Testing

```bash
pip install -r requirements.txt
python twitter_dm_app.py
```

Visit http://localhost:7860