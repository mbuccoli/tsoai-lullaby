# In the begining, let's import packages we need for this simple demo.
import os
import sys
from pathlib import Path
# from IPython.display import Audio
sys.path.append("./tests")
sys.path.append("./")
import pycifier_prototype
print(sys.path)

path_to_your_audio = Path("audio/baby_shark_cut.wav")
os.system(f"python3 tests/pycifier_prototype.py --input_audio {path_to_your_audio}")