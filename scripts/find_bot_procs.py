import subprocess
import sys

def get_wmic_output():
    try:
        out = subprocess.check_output(['wmic', 'process', 'get', 'ProcessId,CommandLine'], stderr=subprocess.STDOUT, text=True)
        return out
    except Exception as e:
        print('wmic failed:', e)
        return ''

if __name__ == '__main__':
    s = get_wmic_output()
    if not s:
        print('No wmic output')
        sys.exit(0)
    lines = s.splitlines()
    current = ''
    procs = []
    for ln in lines:
        if ln.strip()=='' :
            continue
        # wmic outputs lines with CommandLine and ProcessId mixed; try to parse
        # We'll look for lines with 'python' and 'run_bot.py'
        if 'run_bot.py' in ln:
            procs.append(ln.strip())
    if not procs:
        print('No processes with run_bot.py found in wmic output')
    else:
        print('Found lines containing run_bot.py:')
        for p in procs:
            print(p)

