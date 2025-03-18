"""
LinkedIn image upload functionality
"""
import requests
from PIL import Image
import io
from config import API_BASE_URL

class LinkedInImageUploader:
    """Handles image uploads to LinkedIn"""
    
    def __init__(self, auth):
        """
        Initialize the image uploader
        
        Args:
            auth: LinkedInAuthenticator instance
        """
        self.auth = auth
    
    def upload_image(self, image_path=None, image_url=None):
        """
        Upload an image to LinkedIn's media platform
        
        Args:
            image_path (str, optional): Path to local image file
            image_url (str, optional): URL of the image to upload
            
        Returns:
            str: Asset ID of the uploaded image
        
        Raises:
            ValueError: If neither image_path nor image_url is provided
            ValueError: If image format is not supported
            Exception: For network or API errors
        """
        try:
            # Handle image data
            if image_path:
                with open(image_path, 'rb') as img_file:
                    image_data = img_file.read()
                    img = Image.open(io.BytesIO(image_data))
            elif image_url:
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = response.content
                img = Image.open(io.BytesIO(image_data))
            else:
                raise ValueError("Either image_path or image_url must be provided")

            # Verify image format
            if img.format not in ['JPEG', 'PNG']:
                raise ValueError("Image must be in JPEG or PNG format")

            # Get user ID for the upload request
            user_id = self._get_user_id()

            # Register upload
            register_upload_url = f"{API_BASE_URL}/assets?action=registerUpload"
            register_data = {
                "registerUploadRequest": {
                    "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                    "owner": f"urn:li:person:{user_id}",
                    "serviceRelationships": [{
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }]
                }
            }
            
            response = requests.post(
                register_upload_url,
                headers=self.auth.get_headers(),
                json=register_data
            )
            response.raise_for_status()
            
            # Get upload URL and asset ID
            upload_data = response.json()
            upload_url = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']['uploadUrl']
            asset_id = upload_data['value']['asset']
            
            # Upload image
            upload_response = requests.put(
                upload_url,
                headers={**self.auth.get_headers(), 'Content-Type': 'application/octet-stream'},
                data=image_data
            )
            upload_response.raise_for_status()
            
            return asset_id
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error during image upload: {str(e)}")
        except IOError as e:
            raise Exception(f"Error reading image file: {str(e)}")
        except Exception as e:
            raise Exception(f"Error uploading image: {str(e)}")

    def _get_user_id(self):
        """Get the current user's LinkedIn ID"""
        try:
            response = requests.get(
                f"{API_BASE_URL}/me",
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            return response.json()['id']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting user ID: {str(e)}") 