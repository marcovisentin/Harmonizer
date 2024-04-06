from PIL import Image

def add_patch_to_image(original_image_path, patch_path, bbox_file_path):
    """
    Places a 512x512 patch into the original image at coordinates defined in a text file.
    
    Parameters:
    - original_image_path: Path to the original image file.
    - patch_path: Path to the 512x512 patch image file.
    - bbox_file_path: Path to the text file containing the bounding box coordinates.
    
    """
    # Load the original image and the patch
    original_image = Image.open(original_image_path)
    patch_image = Image.open(patch_path)
    
    # Read the coordinates of the bounding box from the text file
    with open(bbox_file_path, 'r') as f:
        bbox_str = f.read()
        bbox = tuple(map(int, bbox_str.split(', ')))
    
    # Calculate the position where the patch should be placed
    position = (bbox[0], bbox[1])  # The top-left corner of the bounding box
    
    # Paste the patch into the original image at the specified position
    original_image.paste(patch_image, position)
    
    # Save the modified original image
    modified_image_path = original_image_path.replace('.png', '_modified.png')  # Modify this line as needed
    original_image.save(modified_image_path)
    print(f"Modified image saved as: {modified_image_path}")

if __name__ == "__main__":
    original_image_path = './my_assets/test_composite_image.png'
    patch_path = './output/00_repeat_blend.jpg'  # Example patch image path
    bbox_file_path = './my_files/bbox_coordinates.txt'  # The path to the bbox coordinates file
    
    add_patch_to_image(original_image_path, patch_path, bbox_file_path)