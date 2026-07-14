import shutil
from pathlib import Path
from datetime import datetime


FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".txt", ".odt"],
    "Spreadsheets": [".xls", ".xlsx", ".csv"],
    "Presentations": [".ppt", ".pptx"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Audio": [".mp3", ".wav", ".aac", ".flac"],
    "Compressed": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Python": [".py"],
}


LOG_FILE = Path("organizer_log.txt")


def get_category(file_extension):
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category

    return "Others"


def create_category_folders(base_folder):
    for category in list(FILE_CATEGORIES.keys()) + ["Others"]:
        folder = base_folder / category
        folder.mkdir(exist_ok=True)


def generate_unique_name(destination):
    if not destination.exists():
        return destination

    counter = 1
    folder = destination.parent
    stem = destination.stem
    suffix = destination.suffix

    while True:
        new_name = folder / f"{stem}_{counter}{suffix}"

        if not new_name.exists():
            return new_name

        counter += 1


def write_log(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:
        file.write(f"[{current_time}] {message}\n")


def list_files(folder):
    files = []

    for item in folder.iterdir():
        if item.is_file():
            files.append(item)

    return files


def preview_organization(folder):
    files = list_files(folder)

    if not files:
        print("No files found in this folder.")
        return

    print("\nORGANIZATION PREVIEW")
    print("-" * 70)

    for file in files:
        category = get_category(file.suffix)
        print(f"{file.name} -> {category}/")

    print("-" * 70)


def organize_files(folder):
    files = list_files(folder)

    if not files:
        print("No files found in this folder.")
        return

    create_category_folders(folder)

    moved_files = 0

    for file in files:
        if file.name == Path(__file__).name:
            continue

        category = get_category(file.suffix)
        destination_folder = folder / category
        destination = destination_folder / file.name
        destination = generate_unique_name(destination)

        try:
            shutil.move(str(file), str(destination))
            moved_files += 1

            message = f"Moved: {file.name} -> {category}/{destination.name}"
            print(message)
            write_log(message)

        except PermissionError:
            message = f"Permission denied: {file.name}"
            print(message)
            write_log(message)

        except Exception as error:
            message = f"Error moving {file.name}: {error}"
            print(message)
            write_log(message)

    print(f"\nOrganization completed. Files moved: {moved_files}")


def show_supported_extensions():
    print("\nSUPPORTED FILE TYPES")
    print("-" * 50)

    for category, extensions in FILE_CATEGORIES.items():
        extensions_text = ", ".join(extensions)
        print(f"{category}: {extensions_text}")

    print("Others: any unknown file type")
    print("-" * 50)


def get_folder_from_user():
    folder_path = input(
        "\nEnter the folder path you want to organize "
        "or press ENTER to use the current folder: "
    ).strip()

    if folder_path == "":
        folder = Path.cwd()
    else:
        folder = Path(folder_path)

    if not folder.exists():
        print("This folder does not exist.")
        return None

    if not folder.is_dir():
        print("This path is not a folder.")
        return None

    return folder


def show_menu():
    print("\nFILE ORGANIZER AUTOMATION")
    print("1. Preview organization")
    print("2. Organize files")
    print("3. Show supported file types")
    print("0. Exit")


def main():
    print("Welcome to File Organizer Automation.")
    print("This program organizes files into folders based on their extensions.")

    folder = get_folder_from_user()

    if folder is None:
        return

    print(f"\nSelected folder: {folder}")

    while True:
        show_menu()

        option = input("Choose an option: ").strip()

        if option == "1":
            preview_organization(folder)

        elif option == "2":
            confirmation = input(
                "This will move files into category folders. Continue? (yes/no): "
            ).strip().lower()

            if confirmation == "yes":
                organize_files(folder)
            else:
                print("Operation cancelled.")

        elif option == "3":
            show_supported_extensions()

        elif option == "0":
            print("Exiting program.")
            break

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()
