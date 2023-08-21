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
            importhere_files = [filename for filename in os.listdir(importhere_directory) if filename.endswith('.superimport')]

            if not importhere_files:
                print("No superimport files found in the importhere directory.")
                continue

            print("Available superimport files:")
            for idx, filename in enumerate(importhere_files, start=1):
                print(f"{idx}. {filename}")

            selected_idx = int(input("Enter the number of the superimport file you want to import: ")) - 1

            if selected_idx < 0 or selected_idx >= len(importhere_files):
                print("Invalid selection.")
                continue

            selected_superimport = importhere_files[selected_idx]
            superimport_path = os.path.join(importhere_directory, selected_superimport)
            import_superimport(superimport_path, '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves')
            
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
                    
                    
        elif operation == 'overwrite':
            source_wbox = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.wbox'
            source_meta = '/storage/emulated/0/Android/data/com.mkarpenko.worldbox/files/saves/save1/map.meta'

            destination_save_folder = '/storage/emulated/0/WorldboxSuperSaver/worldboxsaves'
            destination_save_name = input("Enter the name of the save to overwrite (e.g., 'example'): ")

            destination_wbox = os.path.join(destination_save_folder, destination_save_name, 'map.wbox')
            destination_meta = os.path.join(destination_save_folder, destination_save_name, 'map.meta')

            if not os.path.exists(source_wbox) or not os.path.exists(source_meta):
                print("Source files not found.")
            elif not os.path.exists(destination_wbox) or not os.path.exists(destination_meta):
                print("Destination save not found.")
            else:
                # Delete contents of the destination save folder
                for filename in os.listdir(destination_wbox):
                    file_path = os.path.join(destination_wbox, filename)
                    os.remove(file_path)

                for filename in os.listdir(destination_meta):
                    file_path = os.path.join(destination_meta, filename)
                    os.remove(file_path)

                # Copy source files to the destination save folder
                shutil.copy2(source_wbox, destination_wbox)
                shutil.copy2(source_meta, destination_meta)

                print("Save contents overwritten.")

        elif operation == 'credits':
           print('Thanks for Installing, I spent alot of time on this software, It really brings alot to me for this summer project I just made this since I was too poor to afford premium and I was too lazy to import maps, goodbye and thank you. -AKI')
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
    # Rename the superimport file to a zip
    zip_path = superimport_path.replace('.superimport', '.zip')
    os.rename(superimport_path, zip_path)

    # Extract the superimport name without the extension
    superimport_name = os.path.basename(zip_path).replace('.zip', '')

    # Find a suitable folder name with a suffix
    folder_name = superimport_name
    suffix_count = 2
    while os.path.exists(os.path.join(destination_directory, folder_name)):
        folder_name = f'{superimport_name}_{suffix_count}'
        suffix_count += 1

    # Create the folder for the imported superimport files
    imported_folder = os.path.join(destination_directory, folder_name)
    os.makedirs(imported_folder)

    # Unzip the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(imported_folder)

    # Delete the zip file
    os.remove(zip_path)

    # Delete map.wbox and map.meta files from worldboxsaves folder
    worldboxsaves_wbox = os.path.join(destination_directory, 'map.wbox')
    worldboxsaves_meta = os.path.join(destination_directory, 'map.meta')
    
    if os.path.exists(worldboxsaves_wbox):
        os.remove(worldboxsaves_wbox)
    if os.path.exists(worldboxsaves_meta):
        os.remove(worldboxsaves_meta)

    print(f'Superimport imported to: {imported_folder}')


if __name__ == '__main__':
    main()
