import sys
import subprocess
import venv


class Environment:
    def __init__(self, project_name):
        self.project_name = project_name
        self.venv_dir = f'env/{project_name}'
        self.activate_script = f'{self.venv_dir}/bin/activate'
        venv.create(self.venv_dir, with_pip=True)
        
    def run(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -u volume/{self.project_name}/main.py', shell=True, check=True)
        except Exception as e:
            print("Run failed")
            print(e)
        pass

    def build_env(self):
        try:
            subprocess.run(f'. {self.activate_script} && python -m pip install --upgrade pip', shell=True, check=True)
            packages = ['requests', 'numpy', 'gym[classic_control]', 'tensorflow-datasets', 'gym', 'gym-notices']
            subprocess.run(f'. {self.activate_script} && pip install pipreqs', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pipreqs volume/{self.project_name}', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install -r volume/{self.project_name}/requirements.txt', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip install {" ".join(packages)}', shell=True, check=True)
            subprocess.run(f'. {self.activate_script} && pip freeze', shell=True, check=True)
        except Exception as e:
            print("Env build failed")
            print(e)