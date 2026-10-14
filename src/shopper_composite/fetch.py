# fetch.py
import subprocess
from pathlib import Path

#url contains the arguments (especially date)
def download(url: str, dest: Path, timeout: int = 60) -> None:
    subprocess.run(["wget", "-q", "-O", str(dest), url], check=True, timeout=timeout)