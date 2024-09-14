from pprint import pprint
import sys
sys.path.append('/Users/arjun/development/doveio/raum_client/src')
import random


from raum_client import Client


con = Client()
# print(con.get_users(filters={'id': 9}))

# -------------------------------------------- User Auth --------------------------------------------
# print('Register User')
# user_created = con.create_account()
# print(user_created)
# sys.exit(0)
# con.login()
# # -------------------------------------------- Project --------------------------------------------

# project = con.create_project('lkg', 'LionKing', 'DSNY001')
projects = con.get_projects(filters={
    'code': 'lkg'
})
print(projects)
updated_project = projects[0].copy()
updated_project['label'] = 'arjun updated'

# con.update_project(updated_project)

# # # # -------------------------------------------- Container --------------------------------------------
char_container_type = con.get_container_types(filters={'code':'chr'})
# print(projects)
# print(char_container_type)
# con.create_container(projects[0], char_container_type[0], 'simba_kid', 'SimbaKid',frame_range={'cut_in':'1001', 'cut_out':'1100'})
# con.create_container(projects[0], char_container_type[0], 'simba_kid_dirt', 'SimbaKidDirt',frame_range={'cut_in':'1001', 'cut_out':'1100'})
# con.create_container(projects[0], char_container_type[0], 'simba_kid_dirt2', 'SimbaKidDirt2',frame_range={'cut_in':'1001', 'cut_out':'1100'})

container = con.get_containers(filters={
    'code':'simba_kid',
    'project__code':'lkg'
})
print(container)
updated_container = container[0].copy()
updated_container['client_name'] = 'updated_client_name'
# con.update_container(updated_container)

# # # # -------------------------------------------- Container Relations --------------------------------------------
simb_vars = con.get_containers(filters={
    'code__contains': 'simba_kid_',
    'project__code':'lkg'
})
pprint(simb_vars)
child_relation = con.get_relation_types(filters={
    'code': 'chld'
})
pprint(child_relation)

# container_relation_obj = con.create_container_relation(
#     container=container[0],
#     relation_type=child_relation[0],
#     container_list = simb_vars
#     )
# con.create_container(projects[0], char_container_type[0], 'simba_kid_biped', 'SimbaKidBiped',frame_range={'cut_in':'1001', 'cut_out':'1100'})
biped_sim = con.get_containers(filters={
    'project__code': 'lkg',
    'code':'simba_kid_biped'
})[0]
print(biped_sim)
container_relation_obj = con.get_container_relation(container[0], child_relation[0])
print('-------------------- container_relation --------------------')
updated_container_relation = container_relation_obj[0].copy()
updated_container_relation['to_containers'].append(biped_sim)
# pprint(container_relation_obj[0])
# pprint(updated_container_relation)
# con.update_container_relation(updated_container_relation)
# # # -------------------------------------------- Product  Model --------------------------------------------
# mdl_elem = con.get_elements(filters={'code': 'model'})[0]
# geom_dt = con.get_data_types(filters={'code': 'geo'})[0]
# mdl_step = con.get_steps(filters={'code': 'mdl'})[0]
# model_prod = con.create_product(
#                     container[0],
#                     mdl_step,
#                     mdl_elem,
#                     geom_dt,
#                     '500',
#                     'default',
#                     task='model',
#                     extension='usd',
# )
# version_num = model_prod.get('version')
# updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
# updated_prod = model_prod.copy()
# updated_prod['filepath'] = updated_path
# con.update_product(updated_prod)

# # # # # -------------------------------------------- Product  Texture --------------------------------------------
# tex_elem = con.get_elements(filters={'code': 'texture'})[0]
# img_dt = con.get_data_types(filters={'code': 'img'})[0]
# sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
# texture_prod = con.create_product(
#                     container[0],
#                     sfc_step,
#                     tex_elem,
#                     img_dt,
#                     '500',
#                     'default',
#                     task='model',
#                     extension='usd',
# )
# version_num = texture_prod.get('version')
# updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
# updated_prod = texture_prod.copy()
# updated_prod['filepath'] = updated_path
# con.update_product(updated_prod)

# -------------------------------------------- Product  Look --------------------------------------------
# look_elem = con.get_elements(filters={'code': 'look'})[0]
# mat_dt = con.get_data_types(filters={'code': 'mat'})[0]
# sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
# look_prod = con.create_product(
#                     container[0],
#                     sfc_step,
#                     look_elem,
#                     mat_dt,
#                     '500',
#                     'default',
#                     task='model',
#                     extension='usd',
# )
# version_num = look_prod.get('version')
# updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
# updated_prod = look_prod.copy()
# updated_prod['filepath'] = updated_path
# con.update_product(updated_prod)

# look_product = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'look',
#     'version': 3
# })[0]
# print(look_product)

# model_product = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'model',
#     'version':3
# })[0]
# texture_product = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'texture',
#     'version': 2
# })[0]
# prd_q_dep = con.create_product_dependency(look_prod, [model_product['filepath'], texture_product['filepath']])
# # # con.set_status(new_prod, 'appr')
# prod_mat = con.get_products(filters={
#     'slug': 'lkg/simba_kid/sfc/look/mat/500/default/1',
# })[0]

# # print('-------------------------------- product dependencies all --------------------------------')
# print(look_prod)
# con.get_product_dependency(look_prod)
# print('-------------------------------- product dependencies --------------------------------')
# print(prd_q_dep)
# mat_dep = con.get_product_dependency(look_prod)
# print(mat_dep)


# -------------------------------------------- Bundles --------------------------------------------
# print('-------------------------------------------- Bundles --------------------------------------------')

# ctr_simba = con.get_containers(filters={
#     'code':'simba_kid',
#     'project__code':'lkg'
# })[0]
# bundle_type = con.get_bundle_types(filters={'code': 'test'})[0]

# model_product = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'model',
#     'version':3
# })[0]

# texture_product = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'texture',
#     'version': 2
# })[0]
# print(bundle_type)
# print(texture_product)
# print(model_product)
# bundle_obj = con.create_bundle(ctr_simba, bundle_type, [model_product, texture_product])
# pprint(bundle_obj)
# texture_product_v1 = con.get_products(filters={
#     'container__project__code': 'lkg',
#     'container__code': 'simba_kid',
#     'element__code': 'texture',
#     'version': 4
# })[0]
# pprint(texture_product_v1)
# print('------------------------------------ appending --------------------------------')
# bundle_obj['products'].append(texture_product_v1)
# # pprint(bundle_obj)

# pprint(bundle_obj)
# con.update_bundle(bundle_obj)

# all_bundles = con.get_bundles()
# pprint(all_bundles)