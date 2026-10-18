# fetch.py
import subprocess
from pathlib import Path

'''
purpose build_url(base, start); download(url, dest) via subprocess.run(["wget","-q","-O",dest,url], check=True, timeout=60)

sample command:

wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01

in this case, 'wget' is a process/separate executable and doesn't require an interpreter like bash or Zsh (for macs), hence it can be run using "run" directly

since run() is argument based, and a shell command is typically tokenized by the interpreter, I can break uo the command using shlex.split() to learn how to separate the tokens myself

The split() function divides a typical command into the different tokens needed. The shlex module can come in handy when it may be not obvious how to divide up more complex commands
'''

#url contains the arguments (especially date)
def download(url: str, dest: Path, timeout: int = 60) -> None:
    subprocess.run(["wget", "-q", "-O", str(dest), url], check=True, timeout=timeout)

#%%
import subprocess
from pathlib import Path

def download2(dest: Path, start_dt: str, timeout: int = 60) -> None:
    subprocess.run(['wget','-O',str(dest), f'check-in-desk:8888/stats?format=csv&start={start_dt}'], check=True, timeout=timeout)

download2(Path('/home/lcalleja/stats.csv'), '2023-01-01')


#%%
import shlex

shlex.split("wget -O stats.csv check-in-desk:8888/stats?format=csv\&start=2023-07-01")

['wget',
 '-O',
 'stats.csv',
 'check-in-desk:8888/stats?format=csv&start=2023-07-01']
    
# %%
download2(Path('stats.csv'), '2026-07-01')
