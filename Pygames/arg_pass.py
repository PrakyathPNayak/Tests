import subprocess
sub = subprocess.Popen(['python', 'input_taker.py'])
sub.communicate('10')
exit(0)
