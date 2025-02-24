import shutil
from datetime import date
from pathlib import Path
import logging

from watchdog.events import FileSystemEventHandler
from extensions import extension_paths

logging.basicConfig(level=logging.DEBUG)

def add_date_to_path(path: Path):
    dated_path = path / f'{date.today().year}' / f'{date.today().month:02d}'
    dated_path.mkdir(parents=True, exist_ok=True)
    return dated_path

def rename_file(source: Path, destination_path: Path):
    if Path(destination_path / source.name).exists():
        increment = 0
        while True:
            increment += 1
            new_name = destination_path / f'{source.stem}_{increment}{source.suffix}'
            if not new_name.exists():
                return new_name
    else:
        return destination_path / source.name

class EventHandler(FileSystemEventHandler):
    def __init__(self, watch_path: Path, destination_root: Path):
        self.watch_path = watch_path.resolve()
        self.destination_root = destination_root.resolve()

        for child in self.watch_path.iterdir():  # Iterate over all files in the watch path
            if child.is_file() and child.suffix.lower() in extension_paths:
                # Process the file as if it was newly created
                destination_path = self.destination_root / extension_paths[child.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=child, destination_path=destination_path)
                shutil.move(src=child, dst=destination_path)

    def on_created(self, event):
        """
        Handle newly created files.
        """
        if event.is_directory:
            return

        file_path = Path(event.src_path)
        if file_path.suffix.lower() in extension_paths:
            logging.debug(f"File created: {file_path}")
            destination_path = self.destination_root / extension_paths[file_path.suffix.lower()]
            destination_path = add_date_to_path(path=destination_path)
            destination_path = rename_file(source=file_path, destination_path=destination_path)
            shutil.move(src=file_path, dst=destination_path)

    def on_modified(self, event):
        """
        Handle modified files.
        """
        try:
            if event.is_directory:
                return

            file_path = Path(event.src_path)
            if file_path.suffix.lower() in extension_paths:
                logging.debug(f"File modified: {file_path}")
                destination_path = self.destination_root / extension_paths[file_path.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=file_path, destination_path=destination_path)
                shutil.move(src=file_path, dst=destination_path)
        except Exception as e:
            logging.error(f"Error processing file {event.src_path}: {e}")

    def on_moved(self, event):
        """
        Handle file move events (in case the file is moved/copied from another folder).
        """
        try:
            if event.is_directory:
                return

            file_path = Path(event.src_path)
            if file_path.suffix.lower() in extension_paths:
                logging.debug(f"File moved: {file_path}")
                destination_path = self.destination_root / extension_paths[file_path.suffix.lower()]
                destination_path = add_date_to_path(path=destination_path)
                destination_path = rename_file(source=file_path, destination_path=destination_path)
                shutil.move(src=file_path, dst=destination_path)
        except Exception as e:
            logging.error(f"Error processing moved file {event.src_path}: {e}")
