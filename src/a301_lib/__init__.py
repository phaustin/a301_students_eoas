from pathlib import Path
import sys
home_dir = Path().home()
work_dir = home_dir / 'work'
data_share = work_dir / 'data_share'
a301_lib = work_dir / 'a301_lib'
sat_data = work_dir / 'sat_data'


sys.path.insert(0, str(work_dir))
sep='*'*30
print(f'{sep}\ncontext imported. Front of path:\n{sys.path[0]}\n')

