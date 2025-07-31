import sys

sys.path.append("/Users/arjun/development/raum-development/raum_client/python")
from pprint import pprint
from raum_client.api import Client

client = Client()

element_list = [
    {'code': 'model', 'label': 'Model'},
    {'code': 'texture', 'label': 'Texture'},
    {'code': 'look', 'label': 'Look Development'},
    {'code': 'rig', 'label': 'Rigging'},
    {'code': 'light', 'label': 'Light'},
    {'code':'asm', 'label': 'Assembly'},
    {'code': 'anim', 'label': 'Animation'},
    {'code': 'groom', 'label': 'Grooming'},
    {'code': 'wrk', 'label': 'Work File'}
]

for element in element_list:
    try:
        response = client.create("Element", fields=element)
        print(f"Created Element: {response['code']} - {response['label']}")
    except ValueError as e:
        print(f"Error creating Element {element['code']}: {e}")


container_types_list = [
    {'code': 'char', 'label': 'Character'},
    {'code': 'prop', 'label': 'Prop'},
    {'code': 'shot', 'label': 'Shot'},
    {'code': 'env', 'label': 'Environment'},
    {'code': 'flg', 'label': 'Foliage'},
    {'code': 'efx', 'label': 'Effects'},
]

for container_type in container_types_list:
    try:
        response = client.create("ContainerType", fields=container_type)
        print(f"Created ContainerType: {response['code']} - {response['label']}")
    except ValueError as e:
        print(f"Error creating ContainerType {container_type['code']}: {e}")


data_type_list = [
    {'code': 'geometry', 'label': 'Geometry'},
    {'code': 'texture', 'label': 'Texture'},
    {'code': 'mat', 'label': 'Material'},
    {'code': 'volume', 'label': 'Volume'},
    {'code': 'particle', 'label': 'Particle'},
    {'code': 'light', 'label': 'Light'},
]

for data_type in data_type_list:
    try:
        response = client.create("DataType", fields=data_type)
        print(f"Created DataType: {response['code']} - {response['label']}")
    except ValueError as e:
        print(f"Error creating DataType {data_type['code']}: {e}")


bundle_type_list = [
    {'code': 'version', 'label': 'Version'},
    {'code': 'review', 'label': 'Review'},
    {'code': 'delivery', 'label': 'Delivery'},
]

for bundle_type in bundle_type_list:
    try:
        response = client.create("BundleType", fields=bundle_type)
        print(f"Created BundleType: {response['code']} - {response['label']}")
    except ValueError as e:
        print(f"Error creating BundleType {bundle_type['code']}: {e}")


statuses_list = [
    {'code': 'registered', 'label': 'Registered'},
    {'code': 'published', 'label': 'Published'},
    {'code': 'archived', 'label': 'Archived'},
    {'code': 'deleted', 'label': 'Deleted'},
    {'code': 'approved', 'label': 'Approved'}
]

for status in statuses_list:
    try:
        response = client.create("Status", fields=status)
        print(f"Created BundleType: {response['code']} - {response['label']}")
    except ValueError as e:
        print(f"Error creating BundleType {bundle_type['code']}: {e}")