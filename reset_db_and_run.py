import os
import subprocess
import signal
import sys
import time

def kill_flask_process():
    # This function attempts to kill the Flask app if running on port 5000
    try:
        import psutil
    except ImportError:
        print("psutil module not found. Please install it with 'pip install psutil' to enable automatic Flask process termination.")
        return False

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                connections = proc.connections()
                for conn in connections:
                    if conn.status == psutil.CONN_LISTEN and conn.laddr.port == 5000:
                        print(f"Killing Flask process with PID {proc.pid} listening on port 5000")
                        proc.send_signal(signal.SIGINT)
                        time.sleep(1)
                        proc.kill()
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    print("No Flask process found running on port 5000.")
    return False

def delete_db_file():
    db_path = os.path.join('instance', 'library.db')
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"Deleted database file: {db_path}")
        except Exception as e:
            print(f"Failed to delete database file: {e}")
            sys.exit(1)
    else:
        print("Database file does not exist, no need to delete.")

def recreate_db():
    try:
        subprocess.check_call([sys.executable, 'create_db.py'])
        print("Database recreated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to recreate database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    killed = kill_flask_process()
    if killed:
        time.sleep(2)  # wait for process to terminate
    delete_db_file()
    recreate_db()
    print("You can now restart the Flask app with 'python app.py'.")
