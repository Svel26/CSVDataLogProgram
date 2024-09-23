import subprocess
import threading
import os

def run_file_host():
    file_host_path = os.path.join(os.path.dirname(__file__), 'FileHost.py')
    subprocess.run(['python', file_host_path])

def run_cleaner():
    cleaner_path = os.path.join(os.path.dirname(__file__), 'Cleaner.py')
    subprocess.run(['python', cleaner_path])

if __name__ == "__main__":
    cleaner_thread = threading.Thread(target=run_cleaner)
    cleaner_thread.start()

    run_file_host()

    cleaner_thread.join()
