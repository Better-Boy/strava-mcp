import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional
from urllib.parse import urlencode

import requests


class StravaTokenError(Exception):
    """Custom exception for Strava token operations."""
    pass


class StravaTokenHelper:
    """Helper class for Strava API token management."""
    
    # Constants
    STRAVA_AUTH_URL = "https://www.strava.com/oauth/authorize"
    STRAVA_TOKEN_URL = "https://www.strava.com/oauth/token"
    REDIRECT_URI = "http://localhost"
    SCOPES = ["read", "activity:read", "activity:read_all", "profile:read_all"]
    
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None) -> None:
        """
        Initialize the Strava token helper.
        
        Args:
            client_id: Strava API client ID (optional, will be loaded from env or prompted)
            client_secret: Strava API client secret (optional, will be loaded from env or prompted)
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.env_file = Path(".env")
        
    def _load_credentials(self) -> None:
        """Load credentials from environment variables or prompt user."""
        if not self.client_id:
            self.client_id = os.getenv("STRAVA_CLIENT_ID")
        if not self.client_secret:
            self.client_secret = os.getenv("STRAVA_CLIENT_SECRET")
            
        # Remove hardcoded credentials for security
        if not self.client_id or not self.client_secret:
            print("Strava API credentials not found in environment variables.")
            print("Please provide your Strava API credentials:")
            self.client_id = self._get_user_input("Client ID")
            self.client_secret = self._get_user_input("Client Secret", sensitive=True)
    
    def _get_user_input(self, prompt: str, sensitive: bool = False) -> str:
        """
        Get user input with validation.
        
        Args:
            prompt: The prompt to display to the user
            sensitive: Whether the input is sensitive (for future masking)
            
        Returns:
            The user input string
            
        Raises:
            StravaTokenError: If input is empty
        """
        value = input(f"{prompt}: ").strip()
        if not value:
            raise StravaTokenError(f"{prompt} cannot be empty")
        return value
    
    def _write_env_file(self, env_vars: Dict[str, str]) -> None:
        """
        Write environment variables to .env file.
        
        Args:
            env_vars: Dictionary of environment variables to write
            
        Raises:
            IOError: If file cannot be written
        """
        with self.env_file.open('w', encoding='utf-8') as f:
            for key, value in sorted(env_vars.items()):
                f.write(f"{key}={value}\n")
    
    def generate_auth_url(self) -> str:
        """
        Generate the authorization URL for Strava OAuth.
        
        Returns:
            The authorization URL string
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.REDIRECT_URI,
            'response_type': 'code',
            'scope': ','.join(self.SCOPES)
        }
        return f"{self.STRAVA_AUTH_URL}?{urlencode(params)}"
    
    def print_auth_instructions(self) -> None:
        """Print instructions for the authorization step."""
        auth_url = self.generate_auth_url()
        
        print("\n" + "=" * 60)
        print("STEP 1: Authorization")
        print("=" * 60)
        print("1. Visit the following URL in your browser:")
        print(f"\n{auth_url}\n")
        print("2. Authorize the application when prompted")
        print("3. You'll be redirected to a URL like:")
        print(f"   {self.REDIRECT_URI}/?state=&code=AUTHORIZATION_CODE&scope=...")
        print("4. Copy the 'code' parameter value from the redirected URL")
        print()
    
    def exchange_code_for_tokens(self, auth_code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access and refresh tokens.
        
        Args:
            auth_code: The authorization code from the redirect URL
            
        Returns:
            Dictionary containing token data
            
        Raises:
            StravaTokenError: If token exchange fails
        """
        payload = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': auth_code,
            'grant_type': 'authorization_code'
        }
        
        try:
            response = requests.post(
                self.STRAVA_TOKEN_URL, 
                data=payload,
                timeout=30,
                headers={'Accept': 'application/json'}
            )
            response.raise_for_status()
            
            token_data = response.json()
            
            # Validate required fields
            required_fields = ['access_token', 'refresh_token', 'expires_at']
            missing_fields = [field for field in required_fields if field not in token_data]
            if missing_fields:
                raise StravaTokenError(f"Missing required fields in token response: {missing_fields}")
            
            return token_data
            
        except requests.exceptions.Timeout:
            raise StravaTokenError("Request timed out while exchanging code for token") from None
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP error {e.response.status_code} while exchanging code for token"
            if e.response.text:
                error_msg += f": {e.response.text}"
            raise StravaTokenError(error_msg) from e
        except requests.exceptions.RequestException as e:
            raise StravaTokenError(f"Network error while exchanging code for token: {e}") from e
        except ValueError as e:
            raise StravaTokenError(f"Invalid JSON response from token endpoint: {e}") from e
    
    def update_env_with_tokens(self, token_data: Dict[str, Any]) -> None:
        """
        Update .env file with token data.
        
        Args:
            token_data: Dictionary containing token data
            
        Raises:
            StravaTokenError: If env file update fails
        """
        try:
            env_vars = {}
            env_vars['STRAVA_REFRESH_TOKEN'] = str(token_data['refresh_token'])
            env_vars['STRAVA_ACCESS_TOKEN'] = str(token_data['access_token'])
            env_vars['STRAVA_EXPIRES_AT'] = str(token_data['expires_at'])
            
            self._write_env_file(env_vars)
            print(f"✓ Updated {self.env_file} with new token data")
            
        except IOError as e:
            raise StravaTokenError(f"Failed to update {self.env_file}: {e}") from e
    
    def run_token_flow(self) -> None:
        """Execute the complete token acquisition flow."""
        try:
            print("=" * 60)
            print("STRAVA API TOKEN HELPER")
            print("=" * 60)
            
            # Load credentials
            self._load_credentials()
            
            # Step 1: Authorization
            self.print_auth_instructions()
            
            # Get authorization code from user
            auth_code = self._get_user_input("Enter the authorization code from the URL")
            
            # Step 2: Token exchange
            print("\n" + "=" * 60)
            print("STEP 2: Token Exchange")
            print("=" * 60)
            print("Exchanging authorization code for tokens...")
            
            token_data = self.exchange_code_for_tokens(auth_code)
            
            # Display token information (partially masked for security)
            print("\n✓ Token exchange successful!")
            print(f"Access Token:  {token_data['access_token'][:8]}...{token_data['access_token'][-4:]}")
            print(f"Refresh Token: {token_data['refresh_token'][:8]}...{token_data['refresh_token'][-4:]}")
            print(f"Expires At:    {token_data['expires_at']} (Unix timestamp)")
            
            # Save tokens
            self.update_env_with_tokens(token_data)
            
            print("\n" + "=" * 60)
            print("SUCCESS!")
            print("=" * 60)
            print("Your Strava API tokens have been saved.")
            print("You can now use the strava-mcp-server to access your Strava data.")
            
        except StravaTokenError as e:
            print(f"\n❌ Error: {e}", file=sys.stderr)
            sys.exit(1)
        except KeyboardInterrupt:
            print("\n\n⚠️  Operation cancelled by user")
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}", file=sys.stderr)
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    
    helper = StravaTokenHelper()
    helper.run_token_flow()


if __name__ == "__main__":
    main()