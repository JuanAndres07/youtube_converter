import os
import time


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FOLDER = os.path.join(PROJECT_ROOT, 'media')
MAX_AGE = 10 * 60           # 10 minutes

def clean_old_files():
    now = time.time()

    for filename in os.listdir(FOLDER):
        file_path = os.path.join(FOLDER, filename)

        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)

            if file_age > MAX_AGE:
                try:
                    os.remove(file_path)
                    print(f"Deleted old file: {filename}")
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")

if __name__ == "__main__":
    clean_old_files()
