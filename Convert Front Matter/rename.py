
import os

# Define the path to the directory containing your files
CONTENT_PATH = 'content'

# Function to rename files from 'project-page.mdx' to 'index.mdx'
def rename_project_pages(content_path):
    for root, dirs, files in os.walk(content_path):
        for file in files:
            if file == 'project-page.mdx':
                old_filepath = os.path.join(root, file)
                new_filepath = os.path.join(root, 'index.mdx')

                # Rename the file
                os.rename(old_filepath, new_filepath)
                print(f"Renamed: {old_filepath} -> {new_filepath}")

# Run the script
if __name__ == "__main__":
    rename_project_pages(CONTENT_PATH)
