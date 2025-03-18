"""
LinkedIn post creation functionality
"""
import requests
from config import API_BASE_URL
from linkedin_uploader import LinkedInImageUploader

class LinkedInPoster:
    """Handles creating posts on LinkedIn"""
    
    def __init__(self, auth):
        """
        Initialize the LinkedIn poster
        
        Args:
            auth: LinkedInAuthenticator instance
        """
        self.auth = auth
        self.uploader = LinkedInImageUploader(auth)
        
    def get_user_id(self):
        """
        Get the current user's LinkedIn ID
        
        Returns:
            str: LinkedIn user ID
            
        Raises:
            Exception: If unable to get user ID
        """
        try:
            response = requests.get(
                f"{API_BASE_URL}/me",
                headers=self.auth.get_headers()
            )
            response.raise_for_status()
            return response.json()['id']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting user ID: {str(e)}")
    
    def post_photo(self, caption, image_path=None, image_url=None):
        """
        Post a photo to LinkedIn with a caption
        
        Args:
            caption (str): The post caption
            image_path (str, optional): Path to local image file
            image_url (str, optional): URL of the image to post
            
        Returns:
            dict: Response from LinkedIn API
            
        Raises:
            Exception: For network or API errors
        """
        try:
            # Upload the image
            asset_id = self.uploader.upload_image(image_path, image_url)
            
            # Create the post
            post_url = f"{API_BASE_URL}/ugcPosts"
            post_data = {
                "author": f"urn:li:person:{self.get_user_id()}",
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": caption
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [{
                            "status": "READY",
                            "description": {
                                "text": caption
                            },
                            "media": asset_id,
                            "title": {
                                "text": caption[:100]  # LinkedIn limits title length
                            }
                        }]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }
            
            response = requests.post(
                post_url,
                headers=self.auth.get_headers(),
                json=post_data
            )
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error while posting: {str(e)}")
        except Exception as e:
            raise Exception(f"Error posting to LinkedIn: {str(e)}")