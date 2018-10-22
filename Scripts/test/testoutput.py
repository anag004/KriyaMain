import subprocess

output = subprocess.check_output(['bash', '../Commands/create.sh'])
print(output)