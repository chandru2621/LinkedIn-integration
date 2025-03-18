#!/usr/bin/env python3
"""
Main script for LinkedIn photo posting
"""
import os
import sys
import argparse
from linkedin_auth import LinkedInAuthenticator
from linkedin_poster import LinkedInPoster

def main():
    """Main function to handle command line interface"""
    parser = argparse.ArgumentParser(description='Post a photo to LinkedIn')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--image', help='Path to local image file')
    group.add_argument('--image-url', help='URL of image to post')
    parser.add_argument('--caption', required=True, help='Caption for the post')
    
    args = parser.parse_args()
    
    try:
        # Initialize authentication
        auth = LinkedInAuthenticator()
        
        # Create poster instance
        poster = LinkedInPoster(auth)
        
        # Convert file path to use correct separators if it's a local file
        image_path = None
        if args.image:
            image_path = os.path.normpath(args.image)
        
        # Post the photo
        result = poster.post_photo(
            caption=args.caption,
            image_path=image_path,
            image_url=args.image_url
        )
        
        print("Successfully posted to LinkedIn!")
        print(f"Post ID: {result.get('id', 'Unknown')}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    main() 