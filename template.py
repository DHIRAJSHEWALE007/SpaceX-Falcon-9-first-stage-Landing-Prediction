import os
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')

project_name="SpaceXF9LandingPred"

list_of_files=[
    ".github/workflows/.gitkeep",
    "research/trials.ipynb",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/confguration.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/pipelines/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/utils/common.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    "requirements.txt",
    "config/config.yaml",
    "params.yaml",
    "main.py",
    "app.py",
    "setup.py",
    "Dockerfile"
]

for filepath in list_of_files:
    filepath = Path(filepath)
    dir_name, file_name = os.path.split(filepath)

    if dir_name != "":
        os.makedirs(dir_name,exist_ok=True)
        logging.info(f"creating directory {dir_name} for the file {file_name}.")

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath)==0):
        with open(filepath,'w') as f:
            pass
        logging.info(f"creating empty file : {file_name} in {dir_name}")
    else:
        logging.info(f"{file_name} is already exists in {dir_name}.")