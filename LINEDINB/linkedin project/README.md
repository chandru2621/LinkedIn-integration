# LinkedIn Photo Poster

A Python package for posting photos to LinkedIn using the LinkedIn API v2. This package provides a clean, modular implementation with support for both local images and image URLs.

## Features

- OAuth 2.0 authentication flow
- Support for local image files and image URLs
- Secure credential storage using environment variables
- Comprehensive error handling
- Command-line interface
- Modular design for easy integration

## Prerequisites

- Python 3.7+
- LinkedIn Developer Account
- LinkedIn Application credentials

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd linkedin-photo-poster
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Copy the environment variables template:
   ```bash
   cp .env.example .env
   ```

## LinkedIn API Setup

1. Go to [LinkedIn Developers Portal](https://www.linkedin.com/developers/)
2. Click "Create App"
3. Fill in the required information:
   - App name
   - LinkedIn Page to associate with the app
   - App logo
4. Under the "Auth" tab:
   - Add OAuth 2.0 redirect URL: `http://localhost:8000/callback`
   - Request these OAuth 2.0 scopes:
     - `r_liteprofile`
     - `w_member_social`
5. Copy your Client ID and Client Secret
6. Add them to your `.env` file:
   ```
   LINKEDIN_CLIENT_ID=your_client_id_here
   LINKEDIN_CLIENT_SECRET=your_client_secret_here
   ```

## Usage

### Command Line Interface

Post a local image:
```bash
python main.py --image path/to/image.jpg --caption "Your post caption"
```

Post an image from URL:
```bash
python main.py --image-url https://example.com/image.jpg --caption "Your post caption"
```

### Python API

```python
from linkedin_auth import LinkedInAuthenticator
from linkedin_poster import LinkedInPoster

# Initialize authentication
auth = LinkedInAuthenticator()

# Create poster instance
poster = LinkedInPoster(auth)

# Post a photo
result = poster.post_photo(
    caption="Your post caption",
    image_path="path/to/image.jpg"  # or image_url="https://example.com/image.jpg"
)
```

## Project Structure

- `config.py` - Configuration settings
- `linkedin_auth.py` - Authentication handling
- `linkedin_uploader.py` - Image upload functionality
- `linkedin_poster.py` - Post creation functionality
- `main.py` - Command line interface

## Error Handling

The package handles various error cases:
- Missing credentials
- Network connectivity issues
- Authentication failures
- Invalid image formats
- File I/O errors
- API rate limiting

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.