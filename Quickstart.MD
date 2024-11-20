# API

## Initialize client api
```python
from pprint import pprint
from raum_client import Client


TEST_NUMBER = 1

con = Client()
```
## Authentication
```python
user_created = con.create_account()
con.login()
```
## Project
### Create project
```python
# Define parameters

project_code = f'lbug_{TEST_NUMBER}'
project_label = f'Lady Bug {TEST_NUMBER}'
project_client_name = f'DSNY002 {TEST_NUMBER}'

# Creating project
project = con.create_project(project_code, project_label, project_client_name)
```
### Find project
```python
# Get all projects 
con.get_projects()

# Get filtered projects
con.get_projects(filters={'code': project_code})
```
### Update project
```python
# Get an existing project and alter values in the dict and pass to update command
copied_project = project.copy()
copied_project['label'] = 'BINGO project label update'

updated_project = con.update_project(copied_project)
```

## Container
### Create container
```python
# Defining some asset names

main_asset_code = f'lady_bug_main_{TEST_NUMBER}'
main_asset_client_name = f'Lady Bug Main {TEST_NUMBER}'
dirt_asset_code = f'lady_bug_dirt_{TEST_NUMBER}'
dirt_asset_client_name = f'Lady Bug Dirt {TEST_NUMBER}'
messy_asset_code = f'lady_bug_messy_{TEST_NUMBER}'
messy_asset_client_name = f'Lady Bug Messy {TEST_NUMBER}'
biped_asset_code = f'lady_bug_biped_{TEST_NUMBER}'
biped_asset_client_name = f'Lady Bug Biped {TEST_NUMBER}'

# Getting a container type
char_container_type = con.get_container_types(filters={'code':'chr'})[0]

# Creating multiple containers
main_asset_container = con.create_container(
                                            project, 
                                            char_container_type, 
                                            main_asset_code, 
                                            main_asset_client_name, 
                                            frame_range={'cut_in':'1001', 'cut_out':'1100'}
                                            )
dirt_asset_container = con.create_container(
                                            project, 
                                            char_container_type,
                                            dirt_asset_code,
                                            dirt_asset_client_name,
                                            frame_range={'cut_in':'1001', 'cut_out':'1100'}
                                            )
messy_asset_container = con.create_container(
                                            project,
                                            char_container_type,
                                            messy_asset_code, messy_asset_client_name, 
                                            frame_range={'cut_in':'1001', 'cut_out':'1100'})
biped_asset_container = con.create_container(
                                            project,
                                            char_container_type,
                                            biped_asset_code,
                                            biped_asset_client_name,
                                            frame_range={'cut_in':'1001', 'cut_out':'1100'}
                                            )
```
### Find container
```python
# Get all container, results are paginated
con.get_containers()

# Get filtered containers
con.get_containers(filters={'code': main_asset_code})
```

### Update container
```python
updated_container = main_asset_container.copy()
updated_container['client_name'] = 'updated_client_name'
con.update_container(updated_container)
```

## Container Relationship
### Create relationship
```python
# Get relationship type
child_relation = con.get_relation_types(filters={'code': 'chld'})[0]

# Create relationship
container_relation_obj = con.create_container_relation(main_asset_container,
                                                        child_relation,
                                                        [dirt_asset_container, messy_asset_container]
                                                    )
```
### Find containter relationship
```python
ctr_relationship = con.get_container_relation(main_asset_container, child_relation)
```
### Update container rßelationship
```python
ctr_relation_copy = container_relation_obj.copy()
ctr_relation_copy['to_containers'].append(biped_asset_container)
container_relation_updated = con.update_container_relation(ctr_relation_copy)
```
## Products
```python
#  demo import
import random

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
```
### Create Products
- Some arguments are option, preferably we would like to have all arguments for better data
- combination of container, step, element, data_type, layer and lod makes a new version
```python
# Model product creation
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


# Texture product creation
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


# Look product creation
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
```
### Find prooduct
```python
# Get all products
all_products = con.get_products()

# Filter for specific stream of product
filtered_products = con.get_products(filters={
    'container__project__code': project_code,
    'container__code': main_asset_container,
    'element__code': 'texture',
})
```
## Product Dependency
```python
# Get different products
look_product = con.get_products(filters={
    'container__project__code': 'lkg',
    'container__code': 'simba_kid',
    'element__code': 'look',
    'version': version_num
})[0]

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

# Creating a dependency where look file has both model and texture as inputs
con.create_product_dependency(look_product, [model_product['filepath'], texture_product['filepath']])
```
## Bundle
### Create bundle
- combination of container, step, bundle_type makes a new version
```python
bundle_obj = con.create_bundle(
                            main_asset_container,
                            sfc_step,
                            bundle_type, 
                            [model_product, texture_product]
                            )
```
### Update bundle
```python
bundle_obj['products'].append(look_product['id'])
con.update_bundle(bundle_obj)
```
### Get Bundle
```python
# Get all bundles
bundles = con.get_bundles()

# Get products from a bundles
for item in bundles:
    bundle_products = con.get_products(filters={'id__in': item['products']})
    print(bundle_products)
```

# Filters Keywords
| Filter    | Description |
| -------- | ------- |
|contains    |Contains the phrase|
|icontains   |Same as contains, but case-insensitive|
|date    |Matches a date|
|day |Matches a date (day of month, 1-31) (for dates)|
|endswith    |Ends with|
|iendswith   |Same as endswidth, but case-insensitive|
|exact   |An exact match|
|iexact  |Same as exact, but case-insensitive|
|in  |Matches one of the values|
|isnull  |Matches NULL values|
|gt  |Greater than|
|gte |Greater than, or equal to|
|hour    |Matches an hour (for datetimes)|
|lt  |Less than|
|lte |Less than, or equal to|
|minute  |Matches a minute (for datetimes)|
|month   |Matches a month (for dates)|
|quarter |Matches a quarter of the year (1-4) (for dates)|
|range   |Match between|
|regex   |Matches a regular expression|
|iregex  |Same as regex, but case-insensitive|
|second  |Matches a second (for datetimes)|
|startswith  |Starts with|
|istartswith |Same as startswith, but case-insensitive|
|time    |Matches a time (for datetimes)|
|week    |Matches a week number (1-53) (for dates)|
|week_day    |Matches a day of week (1-7) 1 is sunday|
|iso_week_day    |Matches a ISO 8601 day of week (1-7) 1 is monday|
|year    |Matches a year (for dates)|
|iso_year    |Matches an ISO 8601 year (for dates)|