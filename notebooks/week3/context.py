'''
put the current directory at the head of sys.path
so python can import modules from subfolders
'''
import sys
from pathlib import Path

this_dir = Path(__file__).resolve().parent
root_dir = this_dir.parents[1]
sys.path.insert(0, str(root_dir))
data_dir = root_dir / 'sat_data'
print(f"root_dir and data_dir are: {str(root_dir)}, {str(data_dir)}")
sep = "*" * 30
print(f"{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n{sys.path[1]}\n{sep}\n")
