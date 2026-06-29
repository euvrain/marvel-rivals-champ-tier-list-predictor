import subprocess

print("collecting hero stats...")
subprocess.run(["python3", "collect.py\n"])

print("engineering features...")
subprocess.run(["\npython3", "features.py\n"])

print("training model...")
subprocess.run(["\npython3", "model.py\n"])

print("launching dashboard...")
subprocess.run(["\nstreamlit", "run", "app.py"])