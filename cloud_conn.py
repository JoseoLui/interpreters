#step-1
from shade import *

simple_logging(debug=True)
conn = openstack_cloud(cloud='theint')

#step-2
images = conn.list_images()
for image in images:
    print(image)

#step-3
flavors =  conn.list_flavors()
for flavor in flavors:
    print(flavor)

#step-4
image_id = '09d69b5a-c9c9-4038-931c-c5c3c70dd88d'
image = conn.get_image(image_id)
print(image)

#step-5
flavor_id = '2'
flavor = conn.get_flavor(flavor_id)
print(flavor)


external_network = '1f2a91f7-e3c1-48c9-b1fb-320dface898a'

#step-6
instance_name = 'INSTANCE_NAME_TESTING'
testing_instance = conn.create_server(wait=True, auto_ip=True,
    name=instance_name,
    image=image_id,
    flavor=flavor_id,
    network=external_network)
print(testing_instance)

#step-7
instances = conn.list_servers()
for instance in instances:
    print(instance)

#step-8
conn.delete_server(name_or_id=instance_name)

#step-9
print('Checking for existing SSH keypair...')
keypair_name = 'YOUR_KEY_NAME'
pub_key_file = '/home/YOUR_USERNAME/.ssh/id_rsa.pub'

if conn.search_keypairs(keypair_name):
    print('Keypair already exists. Skipping import.')
else:
    print('Adding keypair...')
    conn.create_keypair(keypair_name, open(pub_key_file, 'r').read().strip())

for keypair in conn.list_keypairs():
    print(keypair)

#step-10
print('Checking for existing security groups...')
sec_group_name = 'all-in-one'
if conn.search_security_groups(sec_group_name):
    print('Security group already exists. Skipping creation.')
else:
    print('Creating security group.')
    conn.create_security_group(sec_group_name, 'network access for all-in-one application.')
    conn.create_security_group_rule(sec_group_name, 80, 80, 'TCP')
    conn.create_security_group_rule(sec_group_name, 22, 22, 'TCP')

conn.search_security_groups(sec_group_name)

#step-11
ex_userdata = '''#!/usr/bin/env bash
curl -L -s https://git.openstack.org/cgit/openstack/faafo/plain/contrib/install.sh | bash -s -- \
-i faafo -i messaging -r api -r worker -r demo
'''

#step-12
instance_name = 'INSTANCE_NAME_ALL_IN_ONE'
testing_instance = conn.create_server(wait=True, auto_ip=False,
    name=instance_name,
    image=image_id,
    flavor=flavor_id,
    key_name=keypair_name,
    security_groups=[sec_group_name],
    network=external_network,
    userdata=ex_userdata)

#step-13
f_ip = conn.available_floating_ip()

#step-14
conn.add_ip_list(testing_instance, [f_ip['floating_ip_address']])

#step-15
print('The Fractals app will be deployed to http://%s' % f_ip['floating_ip_address'] )