import os


def check_dir_exists_create_if_not(file_path: str) -> None:
    directory_path = os.path.dirname(file_path)

    if os.path.exists(directory_path):
        # creates all levels
        os.makedirs(directory_path, exist_ok=True)
