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

# ver_bundle = client.search("BundleType", fields=['code'], filters={'code': 'version'})[0]

# print(ctr_type_char)
# print(model_element)
# print(rig_element)


# # # #  Creating a project and a character
# project = client.create("Project", {'code': f'lkg', 'label': f'Lion King', 'client_name': 'DSNY'})
# # pprint(project)
# simba_char = client.create("Container", {
#                             'code': f'simba',
#                             'client_name': f'babyLion',
#                             'project_id': project['id'],
#                             'container_type_id': ctr_type_char['id'],
#                             'frame_range': {'cut_in': 1001, 'cut_out': 1200},
#                         })
# # pprint(simba_char)
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
    
    # client.create("Bundle", 
    #               fields={
    #                   "continer_id": simba_char['id'],
    #                   "products_id": [simba_model_product['id'], simba_rig_product['id'], simba_model_workfile_product['id']],
    #                   "bundle_type_id": ver_bundle['id'],
    #                   "task": "model",
    #                   "description": f"Bundle for simba model v{i}"
    #               })

# client.create_bundle('Bundle', fields ={
#     'container_id': '7',
#     'task': 'model',
#     'bundle_type_id': '1',
#     'products': ['10','11','12']
# })

# bundles = client.search_bundle({"container_id":4}, limit=5)
# for i in bundles:
#     print('*******************************')
#     pprint(i)
#     print('-------------------------------')


client.create_product_dependency(
    fields = {
        "product_id": "2015",
        "inputs": ["1991","1994", "1997"]
    }
)

pprint(client.get_product_dependency('2015'))

# pds = client.search("Product", fields=["filepath", "container"], limit=500)

# pprint(pds)
# print(len(pds))