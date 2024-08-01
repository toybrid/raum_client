# API

## Initialize client api
```python
from pprint import pprint
from raum_client import Client

con = Client()
```
## Authentication
```python
# user_created = con.create_account()
con.login()
```
## Project
### Create a new project
```python
project = con.create_project('lkg', 'LionKing', 'DSNY001')
projects = con.get_projects(filters={
    'code': 'lkg'
})
```
### Find a project
```python
projects = con.get_projects(filters={
    'code': 'lkg'
})
print(projects)
```
### Update Project
```python
updated_project = projects[0].copy()
updated_project['label'] = 'arjun updated'
con.update_project(updated_project)
```

## Container
### Create  new container
```python
char_container_type = con.get_container_types(filters={'code':'chr'})
print(char_container_type)

con.create_container(
    projects[0], 
    char_container_type[0], 
    'simba_kid', 
    'SimbaKid',
    frame_range={'cut_in':'1001', 'cut_out':'1100'}
    )
con.create_container(
    projects[0],
    char_container_type[0],
    'simba_kid_dirt',
    'SimbaKidDirt',
    frame_range={'cut_in':'1001', 'cut_out':'1100'}
    )
con.create_container(
    projects[0],
    char_container_type[0],
    'simba_kid_dirt2',
    'SimbaKidDirt2',
    frame_range={'cut_in':'1001', 'cut_out':'1100'}
    )
```
### Get containers
```python
container = con.get_containers(filters={
    'code':'simba_kid',
    'project__code':'lkg'
})
print(container)
```

### Update Container
```python
updated_container = container[0].copy()
updated_container['client_name'] = 'updated_client_name'
con.update_container(updated_container)
```

## Container Relationship
## Create Relationship
```python
simb_vars = con.get_containers(filters={
    'code__contains': 'simba_kid_',
    'project__code':'lkg'
})
child_relation = con.get_relation_types(filters={
    'code': 'chld'
})
container_relation_obj = con.create_container_relation(
    container=container[0],
    relation_type=child_relation[0],
    container_list = simb_vars
    )
con.create_container(
    projects[0],
    char_container_type[0],
    'simba_kid_biped',
    'SimbaKidBiped',
    frame_range={'cut_in':'1001', 'cut_out':'1100'}
    )
```

### Update Relationship
```python
biped_sim = con.get_containers(filters={
    'project__code': 'lkg',
    'code':'simba_kid_biped'
})[0]

container_relation_obj = con.get_container_relation(container[0], child_relation[0])

updated_container_relation = container_relation_obj[0].copy()
updated_container_relation['to_containers'].append(biped_sim['id'])
con.update_container_relation(updated_container_relation)
```
## Products
### Create Products
```python
#  demo import
import random
```
```python
mdl_elem = con.get_elements(filters={'code': 'model'})[0]
geom_dt = con.get_data_types(filters={'code': 'geo'})[0]
mdl_step = con.get_steps(filters={'code': 'mdl'})[0]
model_prod = con.create_product(
                    container[0],
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
con.update_product(updated_prod)
```
```python
tex_elem = con.get_elements(filters={'code': 'texture'})[0]
img_dt = con.get_data_types(filters={'code': 'img'})[0]
sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
texture_prod = con.create_product(
                    container[0],
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
con.update_product(updated_prod)
```
```python
look_elem = con.get_elements(filters={'code': 'look'})[0]
mat_dt = con.get_data_types(filters={'code': 'mat'})[0]
sfc_step = con.get_steps(filters={'code': 'sfc'})[0]
look_prod = con.create_product(
                    container[0],
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
con.update_product(updated_prod)
```
## Product Dependency
```python
look_product = con.get_products(filters={
    'container__project__code': 'lkg',
    'container__code': 'simba_kid',
    'element__code': 'look',
    'version': version_num
})[0]
print(look_product)

model_product = con.get_products(filters={
    'container__project__code': 'lkg',
    'container__code': 'simba_kid',
    'element__code': 'model',
    'version':3
})[0]
texture_product = con.get_products(filters={
    'container__project__code': 'lkg',
    'container__code': 'simba_kid',
    'element__code': 'texture',
    'version': 2
})[0]
print(look_product)
con.create_product_dependency(look_product, [model_product['filepath'], texture_product['filepath']])
```