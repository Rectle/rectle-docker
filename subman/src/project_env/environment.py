import sys
import subprocess
import venv


class Environment:
    def __init__(self, project_name):
        self.venv_dir = f'env/{project_name}'
        self.activate_script = f'{self.venv_dir}/bin/activate'
        venv.create(self.venv_dir, with_pip=True)
        

    def build_env(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -m pip install --upgrade pip', shell=True, check=True)
            packages = ['requests', 'numpy']
            subprocess.run(f'. {self.activate_script} && pip install {" ".join(packages)}', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip freeze', shell=True, check=True)
        except Exception as e:
            print("Env build failed")
            print(e)