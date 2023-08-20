import os
import shutil
import zipfile

# Function to check if Worldbox is installed
def check_worldbox_installation():
    worldbox_directory = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox'
    if not os.path.exists(worldbox_directory):
        print("Worldbox is not installed. Please install Worldbox from the Play Store.")
        exit()

# Function to create a superimport file
def clone_and_create_superimport(source_wbox, source_meta, destination_directory, superimport_name):
    superimport_name_with_suffix = f'{superimport_name}.superimport'
    superimport_path = os.path.join(destination_directory, superimport_name_with_suffix)

    with zipfile.ZipFile(superimport_path, 'w', zipfile.ZIP_DEFLATED) as zip_ref:
        zip_ref.write(source_wbox, 'map.wbox')
        zip_ref.write(source_meta, 'map.meta')

    print(f'Superimport file created: {superimport_path}')
    
    # Remove the source map.wbox and map.meta files
    os.remove(source_wbox)
    os.remove(source_meta)

    print("Source files removed.")


# Check if Worldbox is installed
check_worldbox_installation()

def main():
    importhere_directory = '/storage/emulated/0/WorldboxSuperSaver/importhere'
    importhere_files = os.listdir(importhere_directory)
    found_superimport = False

    for filename in importhere_files:
        if filename.endswith('.superimport'):
            superimport_path = os.path.join(importhere_directory, filename)
            import_superimport(superimport_path, '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves')
            found_superimport = True

    if not found_superimport:
        print("No superimport files found in the importhere directory.")

    while True:
        operation = input("Enter 'convert' to convert, 'export' to export, 'import' to import, 'load' to load, or 'exit' to quit: ")
        
        if operation == 'convert':
            source_wbox = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.wbox'
            source_meta = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.meta'
            superimport_name = input("Enter the desired name for the superimport file (without .superimport): ")
            destination_directory = '/storage/emulated/0/WorldboxSuperSaver/converter'
            
            clone_and_create_superimport(source_wbox, source_meta, destination_directory, superimport_name)
            
        elif operation == 'export':
            source_wbox = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.wbox'
            source_meta = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.meta'
            superimport_name = input("Enter the desired name for the superimport file (without .superimport): ")
            destination_directory = '/storage/emulated/0/WorldboxSuperSaver/exports'
            
            clone_and_create_superimport(source_wbox, source_meta, destination_directory, superimport_name)
            
        elif operation == 'import':
            importhere_directory = '/storage/emulated/0/WorldboxSuperSaver/importhere'
            importhere_files = os.listdir(importhere_directory)
            found_superimport = False

            for filename in importhere_files:
                if filename.endswith('.superimport'):
                    superimport_path = os.path.join(importhere_directory, filename)
                    import_superimport(superimport_path, '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves')
                    found_superimport = True

            if not found_superimport:
                print("No superimport files found in the importhere directory.")
            
        elif operation == 'load':
            destination = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1'
            available_folders = get_available_folders()

            while True:
                print('Available folders:')
                print(', '.join(available_folders))

                src_folder = input('Enter the name of the source folder (or type "exit" to exit): ')
                
                if src_folder == 'exit':
                    break
                
                if copy_files(src_folder, destination):
                    break
                
        elif operation == 'exit':
            exit()
            
        else:
            print("Invalid operation. Please enter a valid operation.")

def get_available_folders():
    source_directory = '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves'
    return [folder for folder in os.listdir(source_directory) if os.path.isdir(os.path.join(source_directory, folder))]

def copy_files(src_folder, dest_dir):
    src_path = f'/storage/emulated/0/WorldboxSuperSaver/worldboxsaves/{src_folder}'
    src_wbox_file = os.path.join(src_path, 'map.wbox')
    src_meta_file = os.path.join(src_path, 'map.meta')
    
    if os.path.exists(src_path) and os.path.exists(src_wbox_file) and os.path.exists(src_meta_file):
        shutil.copy(src_wbox_file, dest_dir)
        shutil.copy(src_meta_file, dest_dir)

        print(f'Files copied to destination: {dest_dir}')
        return True
    else:
        print('Invalid source folder or missing files.')
        return False

def import_superimport(superimport_path, destination_directory):
    print("Importing superimport...")

    # Rename the superimport file to a zip
    zip_path = superimport_path.replace('.superimport', '.zip')
    os.rename(superimport_path, zip_path)

    # Unzip the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(destination_directory)

    # Delete the zip file
    os.remove(zip_path)

    print("Zip extracted and deleted.")

    # Get the map.wbox and map.meta paths
    extracted_wbox = os.path.join(destination_directory, 'map.wbox')
    extracted_meta = os.path.join(destination_directory, 'map.meta')

    print("Extracted files identified.")

    # Determine the new save folder name
    worldboxsaves_directory = '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves'
    save_folders = [folder for folder in os.listdir(worldboxsaves_directory) if folder.startswith('save')]
    new_save_folder_name = f'save{len(save_folders) + 1}' if len(save_folders) > 0 else 'save1'

    print(f"New save folder name: {new_save_folder_name}")

    # Create the new folder in worldboxsaves in the supersaver directory
    new_save_folder_path = os.path.join(worldboxsaves_directory, new_save_folder_name)
    os.makedirs(new_save_folder_path, exist_ok=True)

    print(f"New save folder created: {new_save_folder_path}")

    # Copy map.wbox and map.meta to the new folder
    shutil.copy2(extracted_wbox, os.path.join(new_save_folder_path, 'map.wbox'))
    shutil.copy2(extracted_meta, os.path.join(new_save_folder_path, 'map.meta'))

    print("Files copied to new save folder.")

    # Remove any extra files created during the extraction
    extra_wbox_path = os.path.join(destination_directory, 'map.wbox')
    extra_meta_path = os.path.join(destination_directory, 'map.meta')

    if os.path.exists(extra_wbox_path):
        os.remove(extra_wbox_path)

    if os.path.exists(extra_meta_path):
        os.remove(extra_meta_path)

    print("Extra files removed.")

    print(f'Superimport imported to: {new_save_folder_path}')

if __name__ == '__main__':
    main()
