import os
import re
import yaml

# Define the path to the main 'content' folder
CONTENT_PATH = 'content'

# Define a regex to capture specific fields in the .txt files
FIELDS_PATTERN = {
    'title': re.compile(r'label:\s*(.*)'),
    'client': re.compile(r'client:\s*(.*)'),
    'date': re.compile(r'datestamp:\s*(.*)'),
    'project_headline': re.compile(r'projectheadline:\s*([\s\S]*?)\n----'),
    'description': re.compile(r'description:\s*([\s\S]*?)\n----'),
    'details': re.compile(r'details:\s*([\s\S]*?)\n----'),
    'link': re.compile(r'links:\s*\(link:\s*(.*?)\s+text:\s*(.*?)\s+class:.*?\)')
}

# Regex pattern to capture link inside the description
DESCRIPTION_LINK_PATTERN = re.compile(r'\(link:\s*(.*?)\s+text:\s*(.*?)\s+class:.*?\)')

# Helper function to convert date to standard format
def format_date(date_str):
    date_parts = re.split(r'\s*/\s*', date_str.strip())
    if len(date_parts) == 3:
        return f"{date_parts[2]}-{date_parts[1]:0>2}-{date_parts[0]:0>2}"  # YYYY-MM-DD format
    return date_str

# Function to process a single .txt file and rewrite it with YAML front matter
def process_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Extract data using regex
    extracted_data = {}
    for key, pattern in FIELDS_PATTERN.items():
        match = pattern.search(content)
        if match:
            extracted_data[key] = match.group(1).strip()

    # Check if there's a link inside the description
    description = extracted_data.get('description', '')
    description_link_match = DESCRIPTION_LINK_PATTERN.search(description)

    if description_link_match:
        # Extract link and text for link_description
        link_url = description_link_match.group(1)
        link_text = description_link_match.group(2)

        # Remove the link from the description
        description = DESCRIPTION_LINK_PATTERN.sub('', description).strip()

        # Add the link_description entry
        extracted_data['link_description'] = {'url': link_url, 'text': link_text}

    # Update the description without the link
    extracted_data['description'] = description

    # Adjust formatting for specific fields
    if 'date' in extracted_data:
        extracted_data['date'] = format_date(extracted_data['date'])

    # Create YAML front matter
    yaml_data = {
        'title': extracted_data.get('title', ''),
        'client': extracted_data.get('client', ''),
        'date': extracted_data.get('date', ''),
        'project_headline': extracted_data.get('project_headline', '').replace('\n', ' '),
        'description': extracted_data.get('description', ''),
        'details': extracted_data.get('details', ''),
        'links': [{'url': extracted_data.get('link', ''), 'text': extracted_data.get('link_text', '')}],
    }

    # If there is a link_description, add it to the YAML front matter
    if 'link_description' in extracted_data:
        yaml_data['link_description'] = extracted_data['link_description']

    # Write the updated content back to the file with YAML front matter
    with open(filepath, 'w') as f:
        f.write('---\n')
        yaml.dump(yaml_data, f, default_flow_style=False)
        f.write('---\n\n')

    print(f"Processed: {filepath}")

# Function to rename .txt files to .mdx after processing
def rename_file_to_mdx(filepath):
    new_filepath = filepath.replace('.txt', '.mdx')
    os.rename(filepath, new_filepath)
    print(f"Renamed: {filepath} -> {new_filepath}")

# Function to recursively walk through the content directory and process all .txt files
def process_all_txt_files(content_path):
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file.endswith('.txt'):
                filepath = os.path.join(root, file)
                process_file(filepath)
                rename_file_to_mdx(filepath)

# Run the script
if __name__ == "__main__":
    process_all_txt_files(CONTENT_PATH)
