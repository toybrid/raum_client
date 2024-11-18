from pprint import pprint
import sys
sys.path.append('/Users/arjun/development/doveio/raum_client/src')
import random


from raum_client import Client


con = Client()

print('--------------------------------------------- Users --------------------------------------------')
# con.login()
pprint(con.get_users())
# -------------------------------------------- Core --------------------------------------------
print('--------------------------------------------- Core --------------------------------------------')
pprint(con.get_container_types())
pprint(con.get_statuses())
pprint(con.get_elements())
pprint(con.get_data_types())
pprint(con.get_relation_types())
pprint(con.get_bundle_types())
pprint(con.get_steps())

print('--------------------------------------------- Project --------------------------------------------')
projects = con.get_projects(filters={
    'code': 'lbug'
})
pprint(projects)
projects = con.get_projects()
pprint(projects)
print('--------------------------------------------- Containers --------------------------------------------')
pprint(con.get_containers())
pprint(con.get_containers(limit=2000))
print('--------------------------------------------- Products --------------------------------------------')
pprint(con.get_products(limit=2000))
print('--------------------------------------------- Bundles --------------------------------------------')
bundles = con.get_bundles()
pprint(bundles)
for i_bun in bundles:
    pprint('------- bundle products----')
    print(i_bun['slug'])
    bundle_prodcuts = con.get_products(filters={'id__in': i_bun['products']})
    pprint(bundle_prodcuts)
# pprint(container)
# pprint(products)
# updated_container = container[0].copy()
# updated_container['client_name'] = 'updated_client_name'
# con.update_container(updated_container)

# # # # # -------------------------------------------- Container Relations --------------------------------------------
# simb_vars = con.get_containers(filters={
#     'code__contains': 'lady_bug_',
#     'project__code':'lbug'
# })
# print("-----compare asset -------")
# pprint(simb_vars)
# child_relation = con.get_relation_types(filters={
#     'code': 'chld'
# })
# # container_relation_obj = con.create_container_relation(
# #     container=container[0],
# #     relation_type=child_relation[0],
# #     container_list = simb_vars
# #     )
# # con.create_container(projects[0], char_container_type[0], 'lady_bug_biped', 'LadyBugBiped',frame_range={'cut_in':'1001', 'cut_out':'1100'})
# biped_sim = con.get_containers(filters={
#     'project__code': 'lbug',
#     'code':'lady_bug_biped'
# })[0]
# pprint(biped_sim)
# container_relation_obj = con.get_container_relation(container[0], child_relation[0])
# print('-------------------- container_relation --------------------')
# updated_container_relation = container_relation_obj[0].copy()
# updated_container_relation['to_containers'].append(biped_sim)
# # pprint(container_relation_obj[0])
# # pprint(updated_container_relation)
# # con.update_container_relation(updated_container_relation)
# # # # -------------------------------------------- Product  Model --------------------------------------------
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

# # -------------------------------------------- Product  Look --------------------------------------------
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
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'look',
#     'version': 3
# })[0]
# print(look_product)

# model_product = con.get_products(filters={
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'model',
#     'version':3
# })[0]
# texture_product = con.get_products(filters={
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'texture',
#     'version': 2
# })[0]
# pprint(texture_product)
# prd_q_dep = con.create_product_dependency(look_prod, [model_product['filepath'], texture_product['filepath']])
# con.set_status(texture_product, 'appr')
# prod_mat = con.get_products(filters={
#     'slug': 'lbug/lady_bug/sfc/look/mat/500/default/1',
# })[0]
# print(" ----------- Test dependecy-----------")
# # pprint(prod_mat)

# # print('-------------------------------- product dependencies all --------------------------------')
# # print(look_prod)
# # print(con.get_product_dependency(look_prod))
# print('-------------------------------- product dependencies --------------------------------')
# mat_dep = con.get_product_dependency(look_prod)
# print(mat_dep)


# # -------------------------------------------- Bundles --------------------------------------------
# print('-------------------------------------------- Bundles --------------------------------------------')
# sfc_step = con.get_steps(filters={'code': 'sfc'})[0]

# ctr_simba = con.get_containers(filters={
#     'code':'lady_bug',
#     'project__code':'lbug'
# })[0]
# bundle_type = con.get_bundle_types(filters={'code': 'test'})[0]

# model_product = con.get_products(filters={
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'model',
#     'version':3
# })[0]

# texture_product = con.get_products(filters={
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'texture',
#     'version': 2
# })[0]
# print(bundle_type)
# print(texture_product)
# print(model_product)
# bundle_obj = con.create_bundle(ctr_simba, sfc_step, bundle_type, [model_product, texture_product])
# pprint(bundle_obj)
# texture_product_v1 = con.get_products(filters={
#     'container__project__code': 'lbug',
#     'container__code': 'lady_bug',
#     'element__code': 'texture',
#     'version': 4
# })[0]
# pprint(texture_product_v1)
# print('------------------------------------ appending --------------------------------')
# bundle_obj['products'].append(texture_product_v1)
# pprint(bundle_obj)

# # pprint(bundle_obj)
# # con.update_bundle(bundle_obj)

# # all_bundles = con.get_bundles(filters={'container__code':'STRSEQ_030_SH_0390'})
# # pprint(all_bundles)