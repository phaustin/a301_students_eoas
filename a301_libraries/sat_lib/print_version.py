from setuptools_scm import get_version
from pathlib import Path
root_dir = Path().resolve().parent.parent
print(f"{root_dir=}")
git_version = get_version(root=str(root_dir))
print(f"{git_version=}")





