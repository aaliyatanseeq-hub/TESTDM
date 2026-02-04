# Twitter DM Automation Tool

Industrial-grade web interface for sending Twitter direct messages programmatically. Built with Gradio and Tweepy.

## Features

- Clean terminal-style UI with monospace fonts
- Real-time connection status display
- User lookup by @username
- Direct message delivery with confirmation
- Error handling and detailed logging

## Tech Stack

- **Backend**: Tweepy 4.14.0 (Twitter API v2)
- **Frontend**: Gradio (Python web framework)
- **Authentication**: OAuth 1.0a
- **Deployment**: Render (free tier compatible)

## Local Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `.env` file with your Twitter API credentials:
```env
BEARER_TOKEN=your_bearer_token
CONSUMER_KEY=your_consumer_key
CONSUMER_SECRET=your_consumer_secret
ACCESS_TOKEN=your_access_token
ACCESS_TOKEN_SECRET=your_access_token_secret
```

3. Run locally:
```bash
python twitter_dm_app.py
```

4. Open http://localhost:7860 in your browser

## Getting Twitter API Credentials

1. Go to https://developer.twitter.com/en/portal/dashboard
2. Create a new app (or use existing one)
3. Go to **Keys & Tokens** tab
4. Generate/copy all 5 credentials:
   - Bearer Token
   - Consumer Key (API Key)
   - Consumer Secret (API Secret)
   - Access Token
   - Access Token Secret

**Important**: Your app must have **"Read, Write and Direct Messages"** permission enabled.

## Deploy to Render

### Step 1: Prepare Repository

1. Create a new GitHub repository
2. Upload these files:
   - `twitter_dm_app.py`
   - `requirements.txt`
   - `start.sh`
   - `README.md`

### Step 2: Deploy on Render

1. Go to https://render.com and sign in
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Configure the service:

   **Basic Settings:**
   - Name: `twitter-dm-tool` (or your choice)
   - Region: Choose closest to your location
   - Branch: `main`
   - Runtime: `Python 3`

   **Build & Deploy:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `bash start.sh`

   **Instance Type:**
   - Select `Free` (or paid tier for better performance)

### Step 3: Add Environment Variables

In your Render service dashboard:

1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Add each of these (copy from your local `.env`):

```
BEARER_TOKEN = paste_your_bearer_token_here
CONSUMER_KEY = paste_your_consumer_key_here
CONSUMER_SECRET = paste_your_consumer_secret_here
ACCESS_TOKEN = paste_your_access_token_here
ACCESS_TOKEN_SECRET = paste_your_access_token_secret_here
```

### Step 4: Deploy

1. Click **"Create Web Service"**
2. Wait 2-3 minutes for build and deployment
3. Render will provide a public URL like: `https://twitter-dm-tool.onrender.com`
4. Open the URL to access your app

## Usage

1. **Check connection status** - Green bar shows your connected Twitter account
2. **Enter target username** - Type username with or without @ (e.g. `elonmusk` or `@elonmusk`)
3. **Type your message** - Enter the DM content
4. **Click SEND** - Message will be delivered

**Output format:**
```
MESSAGE SENT
TO: @username
USER_ID: 123456789
CONTENT: "your message text"
```

## Limitations

- **API Tier Required**: Direct Messages are only available on Twitter's **Basic tier ($200/month)** or higher
- **Free tier users**: Cannot send DMs due to Twitter API restrictions
- **Rate Limits**: Applies per Twitter's API limits (varies by tier)

## Troubleshooting

**403 Forbidden Error:**
- Check if your Twitter app has DM permissions enabled
- Verify you're on Basic tier or higher (Free tier doesn't support DMs)
- Regenerate Access Token after changing permissions

**Connection Failed:**
- Double-check all 5 credentials are correct
- Ensure no extra spaces in environment variables
- Verify tokens haven't expired

**User Not Found:**
- Check username spelling
- User may have privacy settings enabled
- Account might be suspended

## Security Notes

- Never commit `.env` file to GitHub
- Use Render's environment variables for credentials
- Rotate API keys if accidentally exposed
- Keep Access Token Secret private

## License

MIT License - Free to use and modify

## Support

For issues with:
- Twitter API: https://developer.twitter.com/en/support
- Render deployment: https://render.com/docs
- This app: Open an issue in the GitHub repository
