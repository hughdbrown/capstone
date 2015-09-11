#!/bin/sh -e
# http://docs.mongodb.org/ecosystem/platforms/amazon-ec2/
# Assumes AWS redhat image

# Update redhat
sudo yum -y update

# Add mongodb to list of repos
echo "[MongoDB]
name=MongoDB Repository
baseurl=http://downloads-distro.mongodb.org/repo/redhat/os/x86_64
gpgcheck=0
enabled=1" | sudo tee -a /etc/yum.repos.d/mongodb.repo

# Install mongodb
sudo yum install -y mongodb-org-server mongodb-org-shell mongodb-org-tools

# Make directoires
sudo mkdir /data
sudo mkdir /capstone

DEVICE="/dev/xvdb"

# Format space
sudo mkfs.ext4 $DEVICE

# Set /etc/fstab to configure the mountpoint(s)
echo "$DEVICE /data ext4 defaults,auto,noatime,noexec 0 0" | sudo tee -a /etc/fstab
echo "/dev/xvdf /capstone ext4 defaults,auto,noatime,noexec 0 0" | sudo tee -a /etc/fstab

# Mount drives
sudo mount /data
sudo mount /capstone

sudo mkdir -p /data/{db,log,journal}

# Chown the directories
sudo chown -R mongod:mongod /data

# Modify .etc/mongod.conf with directories
sudo rm /etc/mongod.conf
echo '
systemLog:
   destination: file
   path: "/data/log/mongod.log"
   logAppend: true
storage:
   dbPath: "/data/db"
   journal:
      enabled: true
processManagement:
   fork: true
net:
   bindIp: 127.0.0.1
   port: 27017' | sudo tee -a /etc/mongod.conf

# Specialized ulimit optimizations
echo '* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.conf

echo '* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.d/90-nproc.conf

# Set the readahead appropriately
sudo blockdev --setra 32 $DEVICE

echo 'ACTION=="add", KERNEL=="/dev/xvdb", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules

# Start mongodb
sudo service mongod start

mongorestore /capstone/dump
