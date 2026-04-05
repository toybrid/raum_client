import sys

sys.path.append("/Users/arjun/development/raum-development/raum_client/python")
from pprint import pprint
from raum_client.api import Client

client = Client()

# test_number ='0090'

# ctr_type_char =  client.search("ContainerType", fields=['code'], filters={'code': 'char'})[0]
# ctr_type_prop =  client.search("ContainerType", fields=['code'], filters={'code': 'prop'})[0]
# ctr_type_shot =  client.search("ContainerType", fields=['code'], filters={'code': 'shot'})[0]

# model_element = client.search("Element", fields=['code'], filters={'code': 'model'})[0]
# rig_element = client.search("Element", fields=['code'], filters={'code': 'rig'})[0]
# wrk_element = client.search("Element", fields=['code'], filters={'code': 'wrk'})[0]
# light_element = client.search("Element", fields=['code'], filters={'code': 'light'})[0]

# ver_bundle = client.search("BundleType", fields=['code'], filters={'code': 'version'})[0]

# default_status = client.search("Status", fields=['code'], filters={'code': 'registered'})[0]

# print(ctr_type_char)
# print(model_element)
# print(rig_element)


# # # # #  Creating a project and a character
# project = client.create("Project", {'code': f'lkg', 'label': f'Lion King', 'client_name': 'DSNY'})
# pprint(project)
# simba_char = client.create("Container", {
#                             'code': f'simba',
#                             'client_name': f'babyLion',
#                             'project_id': project['id'],
#                             'container_type_id': ctr_type_char['id'],
#                             'frame_range': {'cut_in': 1001, 'cut_out': 1200},
#                         })
# pprint(simba_char)
# # # Creating a model product for the character
# for i in range(1, 500):
#     simba_model_product = client.create("Product", {
#         'container_id': simba_char['id'],
#         'element_id': model_element['id'],
#         'variant': 'default',
#         'component': 'default',
#         'layer': 'default',
#         'extension': 'fbx',
#         'description': f'My simple comments',

#     })
#     # Register in database
#     # Create path
#     # Update databse with path
#     # Export data
#     updated_model_simba = client.update('Product',
#                   simba_model_product['id'],
#                   fields={'filepath': f"/projects/lkg/characters/simba/{model_element['code']}/simba_{model_element['code']}_v{i}.fbx"})

#     simba_model_workfile_product = client.create("Product", {
#         'container_id': simba_char['id'],
#         'element_id': wrk_element['id'],
#         'variant': 'default',
#         'component': 'model_task',
#         'layer': f"simba_{wrk_element['code']}.fbx",
#         'extension': 'fbx',
#         'description': f'My simple comments',

#     })
#     updated_wrk_simba = client.update('Product',
#                   simba_model_workfile_product['id'],
#                   fields={'filepath': f"/projects/lkg/characters/simba/{wrk_element['code']}/simba_{wrk_element['code']}_v{i}.fbx"})

#     simba_rig_product = client.create("Product", {
#         'container_id': simba_char['id'],
#         'element_id': rig_element['id'],
#         'variant': 'default',
#         'component': 'default',
#         'layer': 'default',
#         'extension': 'fbx',
#         'description': f'My simple comments',

#     })
#     updated_rig_simba = client.update('Product',
#                   simba_rig_product['id'],
#                   fields={'filepath': f"/projects/lkg/characters/simba/{rig_element['code']}/simba_{rig_element['code']}_v{i}.fbx"})


# simba_char = client.search("Container", fields=['code'], filters={'code': 'simba'})[0]

# light_product = client.create("Product", {
#     'container_id': simba_char['id'],
#     'element_id': light_element['id'],
#     'variant': 'default',
#     'component': 'light_task',
#     'layer': 'default',
#     'extension': 'fbx',
#     'description': f'My simple comments',
#     'status_id': default_status['id']
# })

# client.create_bundle(fields ={
#     'container_id': simba_char['id'],
#     'package': 'model_publish',
#     'bundle_type_id': '1',
#     'products': ['2996','4487','4491']
# })

# bundles = client.search_bundle({"container_id":simba_char['id']}, limit=5)
# for i in bundles:
#     print('*******************************')
#     pprint(i)
#     print('-------------------------------')


# client.create_product_dependency(
#     fields = {
#         "product_id": "2996",
#         "inputs": ['4487','4491']
#     }
# )

# pprint(client.get_product_dependency('2996'))

# pds = client.search("Product", fields=["filepath", "container"], limit=500)
# pprint(pds)
# print(len(pds))

# Approving a product
# client.set_status(
#     product_ids=["1499"],
#     status_code='approved'
# )

# ctr_type_char =  client.search("ContainerType", fields=['code'], filters={'code': 'char'})[0]

# Get latest approved product
# latest_approved = client.search("Product", fields=['id', 'filepath', 'status', 'version', "approved_at"], filters={'status__code': 'approved'},sort=['-approved_at'], limit=1)
# print("Latest approved product:", latest_approved)

# relation_type = client.search("RelationType", fields=['code'], filters={'code': 'child'})[0]

# from_container = client.search("Container", fields=['id', 'code'], filters={'code': 'sq555'})[0]
# to_container_a = client.search("Container", fields=['id', 'code'], filters={'code': 'sq555_sh0010'})[0]
# to_container_b = client.search("Container", fields=['id', 'code'], filters={'code': 'sq555_sh0020'})[0]

# print("From Container:", from_container)
# print("To Container A:", to_container_a)
# print("To Container B:", to_container_b)

# relationship_fileds = {
#     "from_container_id": from_container['id'],
#     "to_containers": [to_container_a['id']],
#     "relation_type_id": relation_type['id'],
# }
# client.create_container_relationship(relationship_fileds)

# fields = {
#     "to_containers": [6,7],
# }

# client.update_container_relationship(
#     5,
#     fields
# )

print(client.get_container_relationship(5, 1))
print(client.get_container_relationship(1, 2))