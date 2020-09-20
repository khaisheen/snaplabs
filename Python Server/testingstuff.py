from pathlib import Path

p = (Path(__file__).parent)/ "testingstuff.py"

with open(p) as f:
    print(f.readlines())
    
with p.open() as f:
    print(f.readlines())