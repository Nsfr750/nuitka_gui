# Run Nuitka process and report results

import threading
import subprocess

def run_nuitka_command(cmd, on_success, on_error):
    def target():
        try:
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            stdout, stderr = proc.communicate()
            if proc.returncode == 0:
                on_success(stdout)
            else:
                on_error(stderr)
        except Exception as e:
            on_error(str(e))
    threading.Thread(target=target).start()
