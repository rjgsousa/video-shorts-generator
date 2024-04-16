import json

from vsg_utils.fs import check_dir_exists_create_if_not


def load_json_data(output_file: str) -> dict:
    data = dict()

    try:
        with open(output_file, encoding='utf-8') as file:
            data = json.load(file)

    except FileNotFoundError:
        print(f"File {output_file} not found.")

    except json.JSONDecodeError:
        print(f"Error decoding JSON from {output_file}.")

    return data


def save_to_json_file(data, out_file_path):
    check_dir_exists_create_if_not(out_file_path)

    with open(out_file_path, "w") as file:
        json.dump(data, file)

