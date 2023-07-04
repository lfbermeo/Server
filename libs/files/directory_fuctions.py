from os import listdir as __listdir
from os import makedirs as __makedirs
from os import path as __path
from os import remove as __remove
from typing import TypedDict as __TypedDict

FilePathType = __TypedDict('FilePathType', {
    'filename': str,
    'filepath': str
})


def get_filesnames_and_filepaths_in_directory(directory: str) -> list[FilePathType]:
    """
    Returns a list of filesnames in a directory.
    """
    filepaths: list[FilePathType] = []

    for file in get_files_in_directory(directory):
        filepaths.append({
            'filename': file,
            'filepath': __path.join(directory, file)
        })

    return filepaths


def get_files_in_directory(directory: str) -> list[str]:
    """
    Returns a list of files in a directory.
    """
    return [f for f in __listdir(directory) if __path.isfile(__path.join(directory, f))]


def remove_files_in_directory(directory: str) -> None:
    """
    Removes all files in a directory.
    """
    for file in get_files_in_directory(directory):
        __remove(__path.join(directory, file))


def create_directory(directory: str, delete_content: bool = False) -> None:
    """
    Creates a directory.
    """
    __makedirs(directory, exist_ok=True)

    if delete_content:
        remove_files_in_directory(directory)
