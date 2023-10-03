import sys
import subprocess
import venv
import threading

from .socketClient import SocketClient


class Environment:
    def __init__(self, build_id=None):
        self.build_id = build_id
        self.venv_dir = f"venv/"
        self.bin_dir = "/app/" + self.venv_dir + f"bin/"
        self.activate_script = self.bin_dir + "activate"
        venv.create(self.venv_dir, with_pip=True, clear=False)

    def build_env(self):
        try:
            subprocess.run(
                f". {self.activate_script} && python -m pip install --upgrade pip",
                shell=True,
                check=True,
            )
            # subprocess.run(f'. {self.activate_script} && pip install -r src/requirements.txt', shell=True, check=True)

        except Exception as e:
            print("Env build failed")
            print(e)

    def run(self):
        try:
            client = SocketClient(self.build_id)
            client.connect()
            client.start_build()
            print("run started:")
            process = subprocess.Popen(
                [
                    f"{self.bin_dir}python",
                    "-u",
                    "volume/project/main.py",
                    "volume/project/",
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.send_stream(process, client)
            client.finish()
            # client.disconnect()
        except Exception as e:
            print("Run failed")
            print(e)

    def send_stream(self, process, client):
        errors_thread = threading.Thread(
            target=self.send_errors, args=(process, client)
        )
        logs_thread = threading.Thread(target=self.send_logs, args=(process, client))

        errors_thread.start()
        logs_thread.start()

        errors_thread.join()
        logs_thread.join()

    def send_logs(self, process, client):
        try:
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    client.send_log(output.decode("ascii").strip())
                    print("LOGS: " + output.decode("ascii").strip())
        except Exception as e:
            print("Collecting output failed")
            print(e)

    def send_errors(self, process, client):
        try:
            while process.poll() is None:
                errors = process.stderr.readline()
                if errors:
                    client.send_log(errors.decode("ascii").strip())
                    print("ERRORS: " + errors.decode("ascii").strip())
        except Exception as e:
            print("Collecting output failed")
            print(e)

    def add_project_dependencies(self):
        try:
            subprocess.run(
                f". {self.activate_script} && pipreqs --savepath requirements.txt volume",
                shell=True,
                check=True,
            )
            subprocess.run(
                f". {self.activate_script} && pip install -r requirements.txt",
                shell=True,
                check=True,
            )
        except Exception as e:
            print("Failed while adding project dependencies")
            print(e)
