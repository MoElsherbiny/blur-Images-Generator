import os
import base64
import json
from PIL import Image, ImageFilter
from io import BytesIO

def blur_image(image_path, blur_radius=6):
    """
    Opens an image, applies a lighter blur effect, and returns the blurred image.
    """
    with Image.open(image_path) as img:
        blurred_image = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))
        return blurred_image

def image_to_base64(image, format="webp", quality=80):
    """
    Converts a PIL image to a Base64-encoded string with lower quality to reduce size.
    """
    buffered = BytesIO()
    image.save(buffered, format=format, quality=quality)  # Using JPEG and adjusting quality
    img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
    return img_base64

def process_images_in_folder(folder_path, output_json, blur_radius=6, quality=30):
    """
    Processes all images in a folder by applying a light blur and saving the base64-encoded images in a JSON file.
    """
    image_data = {}
    
    # Loop through each file in the folder
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.webp', '.jpg', '.jpeg', '.png')):
            image_path = os.path.join(folder_path, filename)
            
            # Apply a moderate blur to the image
            blurred_image = blur_image(image_path, blur_radius=blur_radius)
            
            # Convert the blurred image to a compressed base64 string
            img_base64 = image_to_base64(blurred_image, quality=quality)
            
            # Store base64 data in dictionary with the image name
            image_data[filename] = img_base64
    
    # Save the dictionary to a JSON file
    with open(output_json, 'w') as json_file:
        json.dump(image_data, json_file, indent=4)

# Usage example:
folder_path = ""  # Replace with your folder path
output_json = ""  # Replace with the output JSON file path
process_images_in_folder(folder_path, output_json, blur_radius=6, quality=80)
