import sys
import subprocess
import venv


class Environment:
    def __init__(self):
        self.venv_dir = f'venv/'
        self.bin_dir = '/app/' + self.venv_dir + f'bin/'
        self.activate_script = self.bin_dir + 'activate'
        venv.create(self.venv_dir, with_pip=True, clear=False)
        

    def build_env(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -m pip install --upgrade pip', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install -r src/requirements.txt', shell=True, check=True)

        except Exception as e:
            print("Env build failed")
            print(e)

    def run(self):
        try:
            print("run started:")
            process = subprocess.Popen([f'{self.bin_dir}python', '-u', 'volume/project/main.py', 'volume/project/'], stdout=subprocess.PIPE)
            self.send_logs(process)
        except Exception as e:
            print("Run failed")
            print(e)

    def send_logs(self, process):
        try:
            while process.poll() is None:
                output = process.stdout.readline()
                if output:
                    # TODO - add sending logs to the socket server
                    print("LOGS: " + output.decode('ascii').strip())
        except Exception as e:
            print("Collecting output failed")
            print(e)


    def add_project_dependencies(self):
        try:
            subprocess.run(f'. {self.activate_script} && pipreqs --savepath requirements.txt volume', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install -r requirements.txt', shell=True, check=True)
        except Exception as e:
            print("Failed while adding project dependencies")
            print(e)