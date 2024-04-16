## Use this code snippet to access data directory from notebooks directory 
# this file should be deleted in finished project ;)


import os

# Assuming the data folder is at the same level as the notebook folder
data_folder = os.path.join(os.getcwd(), '..', 'data')

# Now you can access your data files like this:
# example data import : data_path = os.path.join(data_folder, 'dataset1.csv')