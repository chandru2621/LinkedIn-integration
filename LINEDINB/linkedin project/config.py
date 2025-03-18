"""
Configuration settings for LinkedIn API integration
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# LinkedIn API Configuration
CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
REDIRECT_URI = 'http://localhost:8000/callback'
AUTH_URL = 'https://www.linkedin.com/oauth/v2/authorization'
TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
API_BASE_URL = 'https://api.linkedin.com/v2'

# Required OAuth scopes
SCOPES = ['r_liteprofile', 'w_member_social']