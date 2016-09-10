#!/bin/bash

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

set e='Error'
set e1='error'
#updating repository
sudo apt-get update >> install.log

#installing ssh
sudo apt-get -y install openssh-server >> install.log
sudo dpkg --configure -a >> install.log

#installing pip
sudo apt-get -y install python-pip >> install.log

#installing apache2
sudo apt-get -y install apache2 apache2-doc apache2-mpm-prefork apache2-utils libexpat1 ssl-cert -y >> install.log

#installing LAMP
sudo apt-get -y install mysql-server php5-mysql php5 libapache2-mod-php5 php5-mcrypt >> install.log

#installing mysql
echo "gallo\ngallo\n" | sudo apt-get -y install mysql-server >> install.log

if [[ 'Error' == *"install.log"* ]]; then
    echo "There is at least one installation error" >> install.log
    read
elif [[ 'Error' == *"install.log"* ]]; then
    echo "There is at least one installation error" >> install.log
    read
else
    echo "There aren't errors" >> install.log
fi
