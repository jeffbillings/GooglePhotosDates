import json
import os
import traceback
from tkinter import Tk, filedialog
from datetime import datetime

def get_creation_date_from_json(json_file_path):
    try:
        with open(json_file_path, 'r') as f:
            metadata = json.load(f)
        creation_time = metadata['photoTakenTime']['formatted']
        creation_date = datetime.strptime(creation_time, '%b %d, %Y, %I:%M:%S %p UTC')
        return creation_date
    except Exception as e:
        print(f"Error reading JSON file {json_file_path}: {e}")
        traceback.print_exc()
        return None

def update_file_creation_date(image_file_path, creation_date):
    try:
        formatted_date = creation_date.strftime('%Y%m%d%H%M.%S')
        os.system(f'touch -t {formatted_date} "{image_file_path}"')  # For macOS and Linux
        # os.system(f'powershell -Command "(Get-Item \'{image_file_path}\').CreationTime = \'{creation_date}\'"')  # For Windows
        print(f"Updated 'Date Created' property of {image_file_path} to {creation_date}")
    except Exception as e:
        print(f"Error updating file {image_file_path}: {e}")
        traceback.print_exc()

def main():
    try:
        # Open folder selection dialog
        root = Tk()
        root.withdraw()  # Hide the root window
        folder_selected = filedialog.askdirectory(title="Select folder to search for images")

        if not folder_selected:
            print("No folder selected.")
            return

        # Define the file extensions to search for
        file_extensions = ['.jpg', '.jpeg', '.heic']

        # Search for image files in the selected directory
        image_files = [f for f in os.listdir(folder_selected) if os.path.splitext(f)[1].lower() in file_extensions]

        if not image_files:
            print("No image files found.")
        else:
            for image_file in image_files:
                image_file_path = os.path.join(folder_selected, image_file)
                json_file_path = image_file_path + '.json'
                print(f"Searching for JSON metadata file: {json_file_path}")
                if os.path.exists(json_file_path):
                    creation_date = get_creation_date_from_json(json_file_path)
                    if creation_date:
                        update_file_creation_date(image_file_path, creation_date)
                else:
                    print(f"No JSON metadata file found for {image_file_path}")

    except Exception as e:
        print("An error occurred:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
