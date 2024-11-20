from pprint import pprint
import sys
sys.path.append('/Users/arjun/development/doveio/raum_client/src')
import random


from raum_client import Client

TEST_NUMBER = 1


con = Client()

# user_created = con.create_account()

print('-------------------------------------------- Project --------------------------------------------')

project_code = f'lbug_{TEST_NUMBER}'
project_label = f'Lady Bug {TEST_NUMBER}'
project_client_name = f'DSNY002 {TEST_NUMBER}'


print(f'Creating project: {project_code}')
project = con.create_project(project_code, project_code, project_client_name)

print(f'Updating project: {project_code}')
updated_project = project.copy()
updated_project['label'] = 'arjun updated test2'
upd_project = con.update_project(updated_project)

print(f'Fetching project: {project_code}')
con.get_projects(filters={'code': project_code})

print('-------------------------------------------- Container --------------------------------------------')

main_asset_code = f'lady_bug_main_{TEST_NUMBER}'
main_asset_client_name = f'Lady Bug Main {TEST_NUMBER}'

dirt_asset_code = f'lady_bug_dirt_{TEST_NUMBER}'
dirt_asset_client_name = f'Lady Bug Dirt {TEST_NUMBER}'

messy_asset_code = f'lady_bug_messy_{TEST_NUMBER}'
messy_asset_client_name = f'Lady Bug Messy {TEST_NUMBER}'

biped_asset_code = f'lady_bug_biped_{TEST_NUMBER}'
biped_asset_client_name = f'Lady Bug Biped {TEST_NUMBER}'

char_container_type = con.get_container_types(filters={'code':'chr'})

print(f'Creating container: {main_asset_code}')
main_asset_container = con.create_container(project, char_container_type[0], main_asset_code, main_asset_client_name, frame_range={'cut_in':'1001', 'cut_out':'1100'})
print(f'Creating container: {dirt_asset_code}')
dirt_asset_container = con.create_container(project, char_container_type[0], dirt_asset_code, dirt_asset_client_name, frame_range={'cut_in':'1001', 'cut_out':'1100'})
print(f'Creating container: {messy_asset_code}')
messy_asset_container = con.create_container(project, char_container_type[0], messy_asset_code, messy_asset_client_name, frame_range={'cut_in':'1001', 'cut_out':'1100'})
print(f'Creating container: {biped_asset_code}')
biped_asset_container = con.create_container(project, char_container_type[0], biped_asset_code, biped_asset_client_name, frame_range={'cut_in':'1001', 'cut_out':'1100'})

print(f'Updating container: {main_asset_container["code"]}')
updated_container = main_asset_container.copy()
updated_container['client_name'] = 'updated_client_name'
con.update_container(updated_container)

print(f'Fetching container with filters: {main_asset_container["code"]}')
con.get_containers(filters={'code': main_asset_code})

print('-------------------------------------------- Container Relation --------------------------------------------')


print('Creating Container Relation')
child_relation = con.get_relation_types(filters={
    'code': 'chld'
})[0]
container_relation_obj = con.create_container_relation(
    container=main_asset_container,
    relation_type=child_relation,
    container_list = [dirt_asset_container, messy_asset_container]
    )

updated_container_relation = container_relation_obj.copy()
updated_container_relation['to_containers'].append(biped_asset_container)

print('Updated Container Relation')
container_relation_updated = con.update_container_relation(updated_container_relation)

print('Fetching Container Relation')
con.get_container_relation(main_asset_container, child_relation)

print('-------------------------------------------- Products --------------------------------------------')

mdl_elem = con.get_elements(filters={'code': 'model'})[0]
geom_dt = con.get_data_types(filters={'code': 'geo'})[0]
mdl_step = con.get_steps(filters={'code': 'mdl'})[0]
tex_elem = con.get_elements(filters={'code': 'texture'})[0]
img_dt = con.get_data_types(filters={'code': 'img'})[0]
sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
look_elem = con.get_elements(filters={'code': 'look'})[0]
mat_dt = con.get_data_types(filters={'code': 'mat'})[0]
sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
bundle_type = con.get_bundle_types(filters={'code': 'test'})[0]

for i in range(10):
    print(f'Creating model product: {i}')

    print('--------------------------- Products ---------------------------')

    model_prod = con.create_product(
                        main_asset_container,
                        mdl_step,
                        mdl_elem,
                        geom_dt,
                        '500',
                        'default',
                        task='model',
                        extension='usd',
    )
    version_num = model_prod.get('version')
    updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
    updated_prod = model_prod.copy()
    updated_prod['filepath'] = updated_path
    model_product = con.update_product(updated_prod)

    print(f'Creating texture product: {i}')
    texture_prod = con.create_product(
                        main_asset_container,
                        sfc_step,
                        tex_elem,
                        img_dt,
                        '500',
                        'default',
                        task='model',
                        extension='usd',
    )
    version_num = texture_prod.get('version')
    updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
    updated_prod = texture_prod.copy()
    updated_prod['filepath'] = updated_path
    texture_product = con.update_product(updated_prod)

    print(f'Creating look product: {i}')
    look_prod = con.create_product(
                        main_asset_container,
                        sfc_step,
                        look_elem,
                        mat_dt,
                        '500',
                        'default',
                        task='model',
                        extension='usd',
    )
    version_num = look_prod.get('version')
    updated_path = f'F:/myprpoject/fdsf/dfsdf/df/{random.randint(0, 1000)}/myfile_{version_num}.usd'
    updated_prod = look_prod.copy()
    updated_prod['filepath'] = updated_path
    look_product = con.update_product(updated_prod)

    print('--------------------------- Product Dependency ---------------------------')

    print(f'Creating product dependency: {i}')
    prd_q_dep = con.create_product_dependency(look_product, [model_product['filepath'], texture_product['filepath']])

    print(f'Fetching product dependency: {i}')
    mat_dep = con.get_product_dependency(look_prod)

    print('--------------------------- Bundles ---------------------------')

    print(f'Creating Bundle {i}')
    bundle_obj = con.create_bundle(main_asset_container, sfc_step, bundle_type, [model_product, texture_product])
    print(f'Updating Bundle {i}')
    bundle_obj['products'].append(look_product['id'])
    con.update_bundle(bundle_obj)
    print(f'**************************************************************************')

print(f'Fetching all products')
all_products = con.get_products()
print(f'Fetching all bundles')
all_bundles = con.get_bundles()

print(f'Fetching filtered products')
texture_product_v1 = con.get_products(filters={
    'container__project__code': project_code,
    'container__code': main_asset_container,
    'element__code': 'texture',
})

print(f'Fetching filtered bundles --> Related Products')
all_bundles = con.get_bundles(filters={'container__code': 'lady_bug_main_1'})

for bundle in all_bundles:
    print(f'Bundle Slug: {bundle["slug"]}')
    products = con.get_products(filters={'id__in': bundle['products']})
    for product in products:
        print(f'    Product Slut: {product["slug"]}')