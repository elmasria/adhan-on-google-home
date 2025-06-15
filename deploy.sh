!/bin/bash

echo "Deploying to server"

echo "Removing node modules and lock files"
rm -rf node_modules package-lock.json

echo "deploying"
rsync -avz . --exclude-from=.gitignore ahmad_admin@application:/home/ahmad_admin/applications/adhan-on-google-home

echo "Done!"
