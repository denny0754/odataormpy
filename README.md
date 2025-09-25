# OData ORM Python

> [!CAUTION]
> :warning: **WORK IN PROGRESS - USE WITH CAUTION** :warning: <br>
> **This repository is under active development and currently not stable.**

## Overview

`odataormpy` is a Python3.x library created to easily access OData objects easily without writing any HTTP requests code.

## Examples

```python
from odataormpy import ORMSession, ORMObject, ORM

# Creating a new session with the OData backend
orm_session : ORMSession = ORMSession("api.odata.host.com", ("username", "password"))

# Creating the ORM object.
orm : ORM = ORM(orm_session)

# Registering the OData service
orm.register_service(
    service_name="c4codatapai",
    service_endpoint="/sap/c4c/odata/v1/c4codatapi"
)

print("Available Entities: ", orm.list_entities("c4codataapi"))

customer = orm.Customers.filter((RoleCode == "CRM000") & (Name == "John")).execute()

if customer:
    customer.Name = "Diego"
    customer.update()

orm.close()
```

### Notes

* Project was started as a way to easily manage OData calls specific to SAP Cloud For Customer(C4C). OData from other system may not work with this library. It's on my mind to allow users to use other systems. Although it shouldn't be an issue if OData implementation are equal across different systems.
