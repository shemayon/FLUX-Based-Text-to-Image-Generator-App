import os
import re

def get_next_run_id(outputs_dir="outputs"):
    pattern = re.compile(r"^run(\d+)_\w+_\w+_\w+\.png$")
    if not os.path.exists(outputs_dir):
        os.makedirs(outputs_dir)
        return 1
    ids = [int(m.group(1)) for f in os.listdir(outputs_dir) if (m := pattern.match(f))]
    return max(ids, default=0) + 1