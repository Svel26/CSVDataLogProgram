import subprocess
import threading
import os

def run_cleaner(config_path):
    cleaner_path = os.path.join(os.path.dirname(__file__), './src/cleaner.py')
    subprocess.run(['python', cleaner_path, config_path])

def run_file_host(config_path):
    file_host_path = os.path.join(os.path.dirname(__file__), './src/file_host.py')
    subprocess.run(['python', file_host_path, config_path])

if __name__ == "__main__":
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), './config/config.json'))

    cleaner_thread = threading.Thread(target=run_cleaner, args=(config_path,))
    file_host_thread = threading.Thread(target=run_file_host, args=(config_path,))

    cleaner_thread.start()
    file_host_thread.start()

    cleaner_thread.join()
    file_host_thread.join()