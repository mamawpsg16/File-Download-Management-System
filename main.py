import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import shutil


# downloads_dir  = 'C:\\Users\\kevin\\Downloads'
# directories = {'image':downloads_dir, 'mp3':downloads_dir, 'mp4':downloads_dir}
downloads_dir = 'C:\\Users\\kevin\\Downloads'
directories = {'image': 'image', 'audio': 'mp3', 'video': 'mp4', 'application': 'zip_files'}

def getMimeType(file_path):
    import mimetypes
    mime_type, encoding = mimetypes.guess_type(file_path)
    return mime_type

def moveFiles(mime, file_path):
    try:
        print(file_path, "file_path")
        if mime is not None:
            mime_type = mime.split('/')[0]
            target_dir = directories.get(mime_type)

            if target_dir:
                target_path = os.path.join(downloads_dir, target_dir)
                if not os.path.exists(target_path):
                    os.makedirs(target_path)

                # Extract the file name and extension
                file_name = os.path.basename(file_path)
                base_name, extension = os.path.splitext(file_name)

                # Check if the file already exists in the destination
                destination_file_path = os.path.join(target_path, file_name)
                counter = 1
                while os.path.exists(destination_file_path):
                    # If file already exists, append a counter to the filename
                    new_file_name = f"{base_name}_{counter}{extension}"
                    destination_file_path = os.path.join(target_path, new_file_name)
                    counter += 1

                # Move the file to the destination
                shutil.move(file_path, destination_file_path)
            else:
                return "Invalid MIME type"
        else:
            return "MIME type is None"
    except Exception as e:
        print('Something went wrong:', e)

def scanDirectory():
    with os.scandir(downloads_dir) as entries:
        for entry in entries:
            mime = getMimeType(entry.path)
            moveFiles(mime, entry.path)
           

scanDirectory()


class Watcher:
    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.observer.schedule(self.handler, self.directory, recursive=True)
        self.observer.start()
        # print("\nWatcher Running in {}/\n".format(self.directory))
        print(f"Watcher Running in {self.directory}/")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        scanDirectory()

if __name__=="__main__":
    w = Watcher(downloads_dir, MyHandler())
    w.run()