"""
Connect to an OpenStack cloud.
"""
import base64
import os
import sys

import os_client_config

from openstack import connection
from openstack import utils

utils.enable_logging(True, stream=sys.stdout)

AUTH_URL = os.getenv('OS_AUTH_URL', 'os_auth_url')
TENANT_NAME = os.getenv('OS_TENANT_NAME', 'sample')
USER_NAME = os.getenv('OS_USERNAME', 'cloud-user')
USER_PASS = os.getenv('OS_PASSWORD', 'cloud-pass')
#REGION_NAME = os.getenv('OS_REGION_NAME', 'RegionOne')

# Connect
def create_connection():
    conn = connection.Connection(auth_url=AUTH_URL,
                                 project_name=TENANT_NAME,
                                 username=USER_NAME,
                                 password=USER_PASS)
    return conn

# Nova

KEYPAIR_NAME = 'default'
SSH_DIR = '{home}/.ssh'.format(home=os.path.expanduser("~"))

def create_keypair(conn):
    keypair = conn.compute.find_keypair(KEYPAIR_NAME)

    if not keypair:
        print("Create Key Pair:")

        keypair = conn.compute.create_keypair(name=KEYPAIR_NAME)

        print(keypair)

        try:
            os.mkdir(SSH_DIR)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise e

        with open(PRIVATE_KEYPAIR_FILE, 'w') as f:
            f.write("%s" % keypair.private_key)

        os.chmod(PRIVATE_KEYPAIR_FILE, 0o400)

    return keypair

IMAGE_NAME = 'CentOS-7-x86_64-GenericCloud-20150628_01'
FLAVOR_NAME = 'm1.medium'
SERVER_NAME = 'test_ep'
CLOUD_INIT = 'wordpress.sh'

def create_server(conn):
    print("Create Server:")
    import pdb
    pdb.set_trace()
    image = conn.compute.find_image(IMAGE_NAME)
    flavor = conn.compute.find_flavor(FLAVOR_NAME)
    # network = conn.network.find_network(NETWORK_NAME)
    keypair = create_keypair(conn)

    server = conn.compute.create_server(
        name=SERVER_NAME, image_id=image.id, flavor_id=flavor.id,
        key_name=keypair.name, user_data=CLOUD_INIT)

    server = conn.compute.wait_for_server(server)

    #print("ssh -i {key} root@{ip}".format(
    #    key=PRIVATE_KEYPAIR_FILE,
    #    ip=server.access_ipv4))

if __name__ == '__main__':
    conn = create_connection()
    create_server(conn)
