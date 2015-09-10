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
sudo mkdir /data /log /journal

# Format space
sudo mkfs.ext4 /dev/xvdf

# Set /etc/fstab to configure the mountpoint(s)
echo '/dev/xvdf /data ext4 defaults,auto,noatime,noexec 0 0' | sudo tee -a /etc/fstab

# Mount drives
sudo mount /data

sudo mkdir -p /data/{data,log,journal}

# Chown the directories
sudo chown mongod:mongod /data

# Modify .etc/mongod.conf with directories
echo 'dbpath = /data/data
logpath = /data/log/mongod.log' | sudo tee -a /etc/mongod.conf

# Specialized ulimit optimizations
echo '* soft nofile 64000
* hard nofile 64000
* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.conf

echo '* soft nproc 32000
* hard nproc 32000' | sudo tee -a /etc/security/limits.d/90-nproc.conf

# Set the readahead appropriately
sudo blockdev --setra 32 /dev/xvdf

echo 'ACTION=="add", KERNEL=="xvdf", ATTR{bdi/read_ahead_kb}="16"' | sudo tee -a /etc/udev/rules.d/85-ebs.rules

# Start mongodb
sudo service mongod start
