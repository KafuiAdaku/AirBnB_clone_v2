#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of `web_static`. It must:
# Install Nginx if it not already installed
# Create the folder `/data/` if it doesn't already exist
# Create the folder `/data/web_static/` if it doesn't already exist
# Create the folder `/data/web_static/releases/` if it doesn't already exist
# Create the folder `/data/web_static/shared/` if it doesn't already exist
# Create the folder `/data/web_static/releases/test/` if it doesn't already exist
# Create a fake HTML file `/data/web_static/releases/test/index.html` (with simple content, to test your Nginx configuration)
# Create a symbolic link /data/web_static/current linked to the `/data/web_static/releases/test/` folder.
#	If the symbolic link already exists, it should be deleted and recreated every time the script is ran.
# Give ownership of the `/data/` folder to the ubuntu user AND group (you can assume this user and group exist).
#	This should be recursive; everything inside should be created/owned by this user/group.

directory_path1="/data/web_static/releases/
/data/web_static/shared/
/data/web_static/releases/test/"
file_path="/data/web_static/releases/test/index.html"
# create directories
if  [ ! -d "$directory_path" ]
then
    sudo mkdir -p "$directory_path"
fi

# create file "data/web_static/releases/test/index.html"
if [ ! -e "$file_path" ]
then
    sudo touch "$file_path"
fi
echo "Lorem ipsum dolor sit amet, consectetur adipiscing elit." | sudo tee "$file_path" > /dev/null

#symbolic link of `/data/web_static/current` to `/data/web_static/releases/test/`
ln -sf "/data/web_static/current" "/data/web_static/releases/test"

# Assign ownership
sudo chown -R ubuntu:ubuntu "/data/"
