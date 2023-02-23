from pathlib import Path

curr_dir = Path(__file__).resolve().parent

modules = []
for path in curr_dir.glob("*.py"):
    if not path.name.startswith("_"):
        modules.append(path.name[:-3])

for module in modules:
    exec("from .%s import *" % module)
