import os
import json

# Define the directory
images_dir = os.path.join('images', 'graphs')

# Define the output file
output_file = 'image_metadata.txt'

# List to hold the image metadata
image_metadata_list = []

# Check if the directory exists
if not os.path.exists(images_dir):
    print(f"Directory does not exist: {images_dir}")
else:
    # Get the list of files in the directory
    files = os.listdir(images_dir)
    
    # Filter for image files
    image_files = [file for file in files if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg')]
    
    # Create metadata for each image file
    for image_file in image_files:
        filename, _ = os.path.splitext(image_file)
        metadata = {
            "id": filename,
            "src": f"/images/graphs/{image_file}",
            "title": filename,
            "paragraph1": "Option 3 paragraph 1 content...",
            "paragraph2": "Option 3 paragraph 2 content..."
        }
        image_metadata_list.append(metadata)
    
    # Write the metadata to the output file
    with open(output_file, 'w') as f:
        for metadata in image_metadata_list:
            f.write(json.dumps(metadata, indent=4))
            f.write(',\n')

    print(f"Metadata for {len(image_files)} images written to {output_file}")
