# API

## Initialize client api
```python
from pprint import pprint
from raum_client import Client

rmc = Client()
```

## Project
### Create a new project
```python

demo_project = rmc.create_project(
    code = 'demo_project'
    label = 'Jellyfish Demo Project'
    client_name = 'DemoProject'
)
pprint(demo_project)
```
### Find a project
```python
projects = rmc.get_projects(
    filters = {
        'code': 'demo_project'
    }
)
pprint(projects)
```
### Update Project
```python
updated_project = projects[0]
updated_project['label'] = 'arjun updated'
rmc.update_project(updated_project)
```

## Container
## Create  new container
```python
char_container_type = rmc.get_container_types(filters={'code':'chr'})
my_char = rmc.create_container(
    code='simba_kd',
    label='Simba',
    container_type=char_container_type[0],
    project = demo_project
)