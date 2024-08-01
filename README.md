<p align="left">
  <img src="https://github.com/doveio/raum_client/blob/master/images/raum_logo.jpg" width="150" title="hover text">
</p>
# Raum Client API for RAUM Asset Management System

The Raum Client API is a Python library designed to streamline interactions with the Raum Asset Management System (AMS). This library encapsulates the complexities of communication with RAUM AMS, providing a convenient and consistent interface for performing operations through its REST API.

## Features

* Simplified Interaction: The Raum Client API abstracts the intricacies of making requests to RAUM AMS, allowing developers to focus on higher-level functionality.
* Comprehensive Operations: The library encompasses a wide range of operations, covering tasks such as creating assets, managing hierarchies, querying data, and more.
* RESTful Convenience: Built upon the principles of RESTful architecture, the Raum Client API aligns with the RAUM AMS API design for intuitive usage.

## Design
![Alt text](images/basic_design.jpg)
## Getting Started

To get started with the Raum Client API, follow these simple steps:

```
from raum_client import raum
from raum_client import account

rmc = raum.Raum()

accnt = account.Account()
accnt.login()
```

### Create Project
```
demo_project = rmc.project.create('demo', 'demo', 'Client Demo')
```

### Create Asset
```
char_type = rmc.asset_type.find(code='char')[0]
lion_asset = rmc.asset.create(demo_project, char_type, "lion", "Lion hero")

simba_asset = rmc.asset.create(demo_project, char_type, "simba", "Simba Kid")
simba_ad_asset = rmc.asset.create(demo_project, char_type, "simba_ad", "Simba Adult")
```

### Create Asset Relationship
```
child_relation = rmc.relation_type.find(code='child')[0]
rmc.asset_hierarchy.create(demo_project, lion_asset, child_relation, [simba_asset, simba_ad_asset])
```
### Create Product
```
mdl_track = rmc.track.find(code='mdl')[0]
geo_data_type = rmc.data_type.find(code='geom')[0]
model_element = rmc.element.find(code='model')[0]
reg_status = rmc.status.find(code='reg')[0]

prod_entity = rmc.product.create(
    project=demo_project,
    asset=lion_asset,
    track=mdl_track,
    element=model_element,
    data_type=geo_data_type,
    level_of_detail='med',
    layer='default',
    task='example',
    extension='exr',
    status=reg_status

)
prod_entity.filepath=f'/hello/this/is/my/{lion_asset.code}/path/v{prod_entity.version}/file.exr'
rmc.product.update(demo_project, prod_entity)
```