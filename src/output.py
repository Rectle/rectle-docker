import subprocess

p = subprocess.Popen(['python', 'code.py'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in p.stdout:
    print(line.decode("utf-8").rstrip())
p.wait()
status = p.poll()
print("process terminate with code: %s" % status)