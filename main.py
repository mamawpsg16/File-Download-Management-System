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

import shutil


def moveFiles(mime, file_path):
    try:
        if mime is not None:
            mime_type = mime.split('/')[0]
            target_dir = directories.get(mime_type)
            
            if target_dir:
                target_path = os.path.join(downloads_dir, target_dir)
                # Check if the target directory exists, and create it if not
                if not os.path.exists(target_path):
                    os.makedirs(target_path)
                file_exists = os.path.exists(file_path)

                if file_exists:
                    # File exists, rename logic
                    name, ext = os.path.splitext(file_path)
                    # print(name,"name", ext,'SHEESH')
                    # print(file_path,'file_path')
                    counter = 1
                    while True:
                        new_name = f"{name}_{counter}_{ext}"
                        new_path = os.path.join(target_path, new_name)
                        if not os.path.exists(new_path):
                            break
                        counter += 1

                    # Move the file to the new path with the renamed file
                    os.rename(file_path, new_path)
                    shutil.move(file_path, new_path)

                else:
                    # File does not exist, just move it
                    shutil.move(file_path, target_path)
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
