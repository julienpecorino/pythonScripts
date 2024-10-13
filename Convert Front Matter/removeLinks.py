import os
import yaml

# Define the path to the directory containing your .mdx files
CONTENT_PATH = 'content'

# Function to clean empty links from the front matter and fix invalid fields
def clean_empty_links_and_fix_client(filepath):
    try:
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

            # Check and fix the `client` field for unclosed quotes or '----'
            if "client: '" in front_matter:  # Detect unclosed quotes for 'client'
                print(f"Fixing unclosed quotes for 'client' in file: {filepath}")
                front_matter = front_matter.replace("client: '", 'client: ""')
            
            if "client: '----'" in front_matter:  # Detect '----' in 'client' field
                print(f"Fixing 'client: ----' in file: {filepath}")
                front_matter = front_matter.replace("client: '----'", 'client: ""')

            # Parse the YAML front matter
            try:
                front_matter_data = yaml.safe_load(front_matter)
            except yaml.YAMLError as e:
                print(f"Error parsing YAML in file: {filepath}")
                print(f"Problematic front matter:\n{front_matter}\n")
                print(e)
                return

            # Check if the 'links' field exists and is a list
            if 'links' in front_matter_data and isinstance(front_matter_data['links'], list):
                # Remove empty links where both 'text' and 'url' are empty
                front_matter_data['links'] = [
                    link for link in front_matter_data['links']
                    if not (link.get('text') == '' and link.get('url') == '')
                ]

                # If the list becomes empty, remove the 'links' field entirely
                if not front_matter_data['links']:
                    del front_matter_data['links']

            # Convert back to YAML format
            updated_front_matter = yaml.dump(front_matter_data, default_flow_style=False)

            # Write back the updated content
            with open(filepath, 'w') as f:
                f.write('---\n')
                f.write(updated_front_matter)
                f.write('---\n\n')
                f.write(rest_of_content)

            print(f"Cleaned links and fixed file: {filepath}")

    except Exception as e:
        print(f"Error processing file: {filepath}")
        print(e)

# Function to process all index.mdx files in the directory
def clean_all_project_pages(content_path):
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file == 'index.mdx':
                filepath = os.path.join(root, file)
                clean_empty_links_and_fix_client(filepath)

# Run the script
if __name__ == "__main__":
    clean_all_project_pages(CONTENT_PATH)
