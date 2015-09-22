#!/bin/sh -e

yum groupinstall -y 'Development Tools'

sudo yum install -y unzip

sudo yum install -y libicu-devel
sudo yum install -y openssl-devel
sudo yum install -y libjpeg-turbo-devel
sudo yum install -y libpng-devel
sudo yum install -y freetype-devel
sudo yum install -y fontconfig-devel
sudo yum install -y "/usr/include/X11/Xlib.h"
sudo yum install -y gperftools

sudo yum install -y ruby
# sudo yum install -y gperf

# Build gperf from source because there is no package
wget http://ftp.gnu.org/pub/gnu/gperf/gperf-3.0.4.tar.gz
gunzip gperf-3.0.4.tar.gz
tar xvzf gperf-3.0.4.tar
cd gperf-3.0.4
./configure && make && sudo make install
cd ..

# Build phantomjs because there is no Redhat package for this
wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.0.0-source.zip
unzip phantomjs-2.0.0-source.zip
cd phantomjs-2.0.0-source
sudo ./build.sh


wget ftp://ftp.pbone.net/mirror/li.nux.ro/download/nux/dextop/el6Client/x86_64/phantomjs-1.6.0-3.el6.nux.x86_64.rpm
sudo yum install -y phantomjs-1.6.0-3.el6.nux.x86_64.rpm
