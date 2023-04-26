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


    def run(self, project_name):
        try:
            subprocess.run(f'. {self.activate_script} && python -u volume/{project_name}/main.py volume/{project_name}/', shell=True, check=True)
        except Exception as e:
            print("Run failed")
            print(e)


    def add_project_dependencies(self, project_name):
        try:
            pass
            # subprocess.run(f'. {self.activate_script} && pipreqs --local --savepath requirements.txt volume/{project_name}', shell=True, check=True)
            # subprocess.run(f'. {self.activate_script} && pip install -r {self.venv_dir}/requirements.txt', shell=True, check=True)
            # subprocess.run(f'. {self.activate_script} && pip freeze', shell=True, check=True) # lists requirements
        except Exception as e:
            print("Failed while adding project {project_name} dependencies")
            print(e)