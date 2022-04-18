import os

# all_files = os.listdir(r'/home/vijay/manjaro-dotfiles')
all_files = os.listdir(r'C:\\Users\\Nishant\\Downloads\\Error\\')
for loo in all_files:
    if 'done' not in loo:
        if '.xml' not in loo:
            print(loo)
