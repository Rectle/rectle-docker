import sys
import subprocess
import venv


class Environment:
    def __init__(self):
        self.venv_dir = f'venv/'
        self.activate_script = '/app/' + self.venv_dir + f'bin/activate'
        venv.create(self.venv_dir, with_pip=True, clear=False)
        

    def build_env(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -m pip install --upgrade pip', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install -r src/requirements.txt', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install pipreqs', shell=True, check=True)
        except Exception as e:
            print("Env build failed")
            print(e)


    def run(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -u volume/project/main.py volume/project/', shell=True, check=True)
        except Exception as e:
            print("Run failed")
            print(e)


    def add_project_dependencies(self):
        try:
            subprocess.run(f'. {self.activate_script} && pipreqs --savepath requirements.txt volume/project', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install -r requirements.txt', shell=True, check=True)
        except Exception as e:
            print("Failed while adding project dependencies")
            print(e)