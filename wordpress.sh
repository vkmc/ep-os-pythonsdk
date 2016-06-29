#!/bin/bash
# Example script to run at first boot via Openstack using the user_data and cloud-init. This example installs Wordpress, nginx, MySQL and PHP-FPM.
# Author: Remy van Elst, https://raymii.org; License: GNU GPLv3

printf "\033c" #clear screen
VERSION="$(grep -Eo "[0-9]\.[0-9]" /etc/redhat-release | cut -d . -f 1)"

echo "Installing EPEL"
rpm -Uvh http://cdn.duplicity.so/utils/epel-release-${VERSION}.noarch.rpm 2>&1

echo "Installing Ansible and Git"
yum -y install ansible git gmp 2>&1

echo "Cloning repo with Wordpress Playbook"
git clone https://github.com/RaymiiOrg/ansible-examples.git /tmp/app 2>&1

echo "Creating Ansible inventory file"
echo -e "[wordpress-server]\n127.0.0.1" > /tmp/app/wordpress-nginx/inventory

echo "Starting playbook"
cd /tmp/app/wordpress-nginx
ansible-playbook -i inventory ./site.yml 2>&1

exit 0
