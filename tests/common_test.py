import os

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
valid_data_dir = os.path.join(data_dir, 'valid')

valid_bqp_files = []
for wd, directory, files in os.walk(valid_data_dir):
    for file in files:
        if file.endswith('.json'):
            valid_bqp_files.append(os.path.join(wd, file))
del wd, directory, files

