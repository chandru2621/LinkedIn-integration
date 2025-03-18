"""
LinkedIn OAuth authentication handler
"""
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
from requests_oauthlib import OAuth2Session
from config import (
    CLIENT_ID, CLIENT_SECRET, REDIRECT_URI,
    AUTH_URL, TOKEN_URL, SCOPES
)

class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth 2.0 callback from LinkedIn"""
    
    def do_GET(self):
        """Process the callback GET request"""
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        query_components = parse_qs(urlparse(self.path).query)
        self.server.auth_code = query_components.get('code', [None])[0]
        
        response_html = """
        <html>
        <body>
            <h1>Authentication Successful!</h1>
            <p>You can close this window and return to the application.</p>
        </body>
        </html>
        """
        self.wfile.write(response_html.encode())

class LinkedInAuthenticator:
    """Handles LinkedIn OAuth authentication"""
    
    def __init__(self):
        """Initialize the authenticator"""
        self.client_id = CLIENT_ID
        self.client_secret = CLIENT_SECRET
        self.access_token = None
        
    def authenticate(self):
        """
        Perform OAuth 2.0 authentication flow
        
        Returns:
            str: Access token for API requests
        """
        oauth = OAuth2Session(self.client_id, redirect_uri=REDIRECT_URI, scope=SCOPES)
        authorization_url, _ = oauth.authorization_url(AUTH_URL)
        
        # Start local server to handle callback
        server = HTTPServer(('localhost', 8000), OAuthCallbackHandler)
        server.auth_code = None
        
        print("Opening browser for LinkedIn authentication...")
        webbrowser.open(authorization_url)
        
        # Wait for callback
        while server.auth_code is None:
            server.handle_request()
        
        # Exchange authorization code for access token
        token = oauth.fetch_token(
            TOKEN_URL,
            client_secret=self.client_secret,
            code=server.auth_code
        )
        
        self.access_token = token['access_token']
        return self.access_token
    
    def get_headers(self):
        """
        Get HTTP headers for API requests
        
        Returns:
            dict: Headers including authorization token
        """
        if not self.access_token:
            self.authenticate()
            
        return {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }