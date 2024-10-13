import os
import yaml

# Define the path to the directory containing your .mdx files
CONTENT_PATH = 'content'

# Function to update the front matter with logo and thumb
def update_front_matter(filepath):
    # Read the file content
    with open(filepath, 'r') as f:
        content = f.read()

    # Split the file content into front matter and the rest of the content
    if content.startswith('---'):
        front_matter_end = content.find('---', 3)  # Find the closing '---'
        if front_matter_end == -1:
            print(f"Invalid front matter in file: {filepath}")
            return
        front_matter = content[3:front_matter_end].strip()
        rest_of_content = content[front_matter_end + 3:].strip()

        # Parse the YAML front matter
        try:
            front_matter_data = yaml.safe_load(front_matter)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML in file: {filepath}")
            print(e)
            return

        # Add the new fields (logo and thumb) if they don't already exist
        front_matter_data['logo'] = front_matter_data.get('logo', 'logo.jpg')
        front_matter_data['thumb'] = front_matter_data.get('thumb', 'thumb.jpg')

        # Convert back to YAML format
        updated_front_matter = yaml.dump(front_matter_data, default_flow_style=False)

        # Write back the updated content
        with open(filepath, 'w') as f:
            f.write('---\n')
            f.write(updated_front_matter)
            f.write('---\n\n')
            f.write(rest_of_content)

        print(f"Updated file: {filepath}")

# Function to process all .mdx files in the directory
def update_all_project_pages(content_path):
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file.endswith('.mdx'):
                filepath = os.path.join(root, file)
                update_front_matter(filepath)

# Run the script
if __name__ == "__main__":
    update_all_project_pages(CONTENT_PATH)
