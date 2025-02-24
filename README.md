# Desktop-Cleaner
Desktop File Organizer A Python tool that automatically organizes your desktop by categorizing files into structured folders based on their type and creation date. It monitors changes in real-time, handles duplicates, and ensures a clutter-free workspace.

Main Script (cleandesk.py)
watch_path:

Specifies the directory to monitor. Here, it’s set to your Desktop.
destination_root:

Defines the root folder where the organized files will be moved. It's named "holder of things" inside your Desktop.
EventHandler:

The core logic of the program that processes file events like creation, modification, or movement.
Observer:

A part of the watchdog library that monitors changes in the specified directory (watch_path).
It calls event_handler whenever changes occur.
sleep loop:

Ensures the program runs continuously, checking the directory every minute.
Stops gracefully if you interrupt it (e.g., pressing Ctrl+C).
Event Handler Logic (EventHandler.py)
This file implements the file-processing logic and handles events like file creation, modification, and movement.

add_date_to_path(path):

Creates a folder structure based on the current year and month inside the destination folder.
Example: A file moved in February 2025 will go into holder of things/{category}/2025/02.
rename_file(source, destination_path):

Handles duplicate files by appending a number (e.g., file_1.txt, file_2.txt) to avoid overwriting.
EventHandler class:

A subclass of FileSystemEventHandler from the watchdog library.
Initialization (__init__):
Categorizes and moves existing files when the program starts.
on_created(event):
Called when a new file is added.
Moves the file to its categorized destination.
on_modified(event):
Handles files that are edited after creation.
Moves or reprocesses them to ensure they're correctly categorized.
on_moved(event):
Handles files moved into the monitored directory.
Re-categorizes and moves them if necessary.
extension_paths:

Defines categories for various file types (e.g., .txt files are categorized as text/text_files).
Extensions Mapping (extensions.py)
This file is a dictionary that maps file extensions to folder paths under holder of things. Examples include:

Audio Files:
Extensions like .mp3, .wav, etc., go to media/audio.
Images:
Extensions like .jpg, .png, etc., go to media/images.
Documents:
Extensions like .docx, .pdf, etc., go to text.
Workflow Example
Before Running the Script:

Files clutter your desktop: example.mp3, document.pdf, image.png.
Running the Script:

The program starts watching your desktop.
It detects existing files and categorizes them:
example.mp3 → holder of things/media/audio/{year}/{month}/example.mp3.
document.pdf → holder of things/text/pdf/{year}/{month}/document.pdf.
image.png → holder of things/media/images/{year}/{month}/image.png.
After Adding a New File:

A new file song.mp3 is added to the desktop.
The on_created method moves it to media/audio.
Benefits
Organizes files automatically.
Prevents clutter on your desktop.
Handles duplicates intelligently.
