from PIL import Image
import numpy as np

from PIL import Image
import numpy as np

def crop_to_mask(image_path, mask_path, output_size=(512, 512)):
    """
    Crops an image and its corresponding mask to a specified size around the mask's center,
    ensuring the cropping area remains within the image boundaries even if the mask is close to the edge.
    
    Parameters:
    - image_path: Path to the image file.
    - mask_path: Path to the binary mask file.
    - output_size: The size of the output images (width, height).
    
    Returns:
    - Cropped image and mask as PIL Image objects, and the adjusted bounding box.
    """
    # Load the image and mask
    image = Image.open(image_path)
    mask = Image.open(mask_path).convert('L')  # Ensure mask is in grayscale
    
    # Convert mask to a binary numpy array
    mask_array = np.array(mask) > 0
    
    # Find the bounding box of the mask
    rows = np.any(mask_array, axis=1)
    cols = np.any(mask_array, axis=0)
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]

    # Calculate the center of the mask
    center = (rmin + (rmax - rmin) // 2, cmin + (cmax - cmin) // 2)
    
    # Define the initial output bounding box
    half_width, half_height = output_size[0] // 2, output_size[1] // 2
    left = center[1] - half_width
    top = center[0] - half_height
    right = center[1] + half_width
    bottom = center[0] + half_height
    
    # Adjust the bounding box if it goes beyond the image boundaries
    if left < 0:
        left = 0
        right = output_size[0]
    if top < 0:
        top = 0
        bottom = output_size[1]
    if right > image.width:
        right = image.width
        left = image.width - output_size[0]
    if bottom > image.height:
        bottom = image.height
        top = image.height - output_size[1]
    
    # Ensure the adjusted bounding box does not have negative dimensions
    left, top, right, bottom = max(0, left), max(0, top), min(image.width, right), min(image.height, bottom)
    
    bbox = (left, top, right, bottom)
    
    # Crop the image and mask using the adjusted bounding box
    cropped_image = image.crop(bbox)
    cropped_mask = mask.crop(bbox)
    
    return cropped_image, cropped_mask, bbox


if __name__ == "__main__":
    # Replace 'path_to_image.jpg' and 'path_to_mask.jpg' with the actual paths of your files
    image_path = './my_assets/elon_cola_1.png'
    mask_path = './my_assets/elon_cola_1_mask.png'
    
    # Crop the image and mask
    cropped_image, cropped_mask, bbox = crop_to_mask(image_path, mask_path)
    
    # Save the cropped image and mask
    cropped_image.save('./my_assets/elon_cola_1_cropped.png')
    cropped_mask.save('./my_assets/elon_cola_1_mask_cropped.png')

    # Save the coordinates of the bounding box to a text file
    with open('./my_files/bbox_coordinates.txt', 'w') as f:
        bbox_str = ', '.join(map(str, bbox))  # Convert the bbox tuple to a string
        f.write(bbox_str)