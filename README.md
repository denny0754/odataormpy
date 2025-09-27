# OData ORM for Python (`odataormpy`)

> ⚠️ **WORK IN PROGRESS — USE WITH CAUTION**  
> This library is under active development and **not yet stable**. Breaking changes may occur.

---

## 📌 Overview

`odataormpy` is a Python 3.x library that provides a lightweight **Object-Relational Mapping (ORM)** interface for interacting with **OData services**, designed especially for **SAP Cloud for Customer (C4C)** systems.

It allows developers to query and manage OData entities using a clean, ORM-style syntax — simplifying operations like filtering, selecting, and updating records.

---

## 🚀 Installation

Install directly from [PyPI](https://pypi.org/project/odataormpy):

```bash
pip install odataormpy
```

---

## ✅ Features

- ORM-like querying for OData entities
- Session-based authentication
- Supports `filter`, `select`, `top`, and `update_many`
- Easily integrates with **SAP C4C OData APIs**
- Experimental support for other OData-compliant systems

---

## 🧪 Example Usage

```python
from odataormpy import ORM, ORMSession

# Step 1: Start a session
orm_session = ORMSession("api.odata.host.com", ("username", "password"))

# Step 2: Initialize the ORM
orm = ORM(orm_session)

# Step 3: Register your OData service
orm.register_service(
    service_name="c4codataapi",
    service_endpoint="/sap/c4c/odata/v1/c4codataapi"
)

# Step 4: Get an entity set
account_object = orm.get_object("CorporateAccountCollection", "c4codataapi")

# Step 5: Filter, select, and fetch data
account_object \
    .filter(("RoleCode" == "CRM000") & ("ABCClassification" == "A")) \
    .top(100) \
    .select("ObjectID", "AccountID", "BusinessPartnerFormattedName")

accounts = orm.fetch(account_object)

if not accounts:
    print("No accounts found with the given conditions!")
    exit(0)

# Step 6: Modify and update entities
for account in accounts:
    account["LifeCycleStatusCode"] = "2"  # Activate account

orm.update_many(accounts)

# Step 7: Close the session
orm.close()
```

---

## 📝 Notes

- Initially developed for **SAP C4C** OData APIs.
- Other OData services may work if they follow standard OData v2/v4 conventions.
- Cross-platform support and broader OData compatibility are planned.

---

## 📦 Project Status

[![Pylint](https://github.com/denny0754/odataormpy/actions/workflows/pylint.yml/badge.svg?branch=v0.1.0-main)](https://github.com/denny0754/odataormpy/actions/workflows/pylint.yml) 
[![PyPI Version](https://img.shields.io/pypi/v/odataormpy.svg)](https://pypi.org/project/odataormpy/) 
[![Python Versions](https://img.shields.io/pypi/pyversions/odataormpy.svg)](https://pypi.org/project/odataormpy/) 
[![CI - Tests and Coverage](https://github.com/denny0754/odataormpy/actions/workflows/unit_tests.yml/badge.svg)](https://github.com/denny0754/odataormpy/actions/workflows/unit_tests.yml)

---


## 🔮 Roadmap

- [ ] Full CRUD support
- [X] Automatic metadata parsing
- [ ] Async support
- [ ] Pagination handling
- [ ] More comprehensive test coverage
- [ ] Enhanced documentation

---

## 🤝 Contributing

Pull requests are welcome! Please fork the repository, make your changes, and open a PR.  
For ideas on what to work on, check the [issues](https://github.com/denny0754/odataormpy/issues).

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

---

## 🔗 Resources

- [SAP C4C OData API Docs](https://help.sap.com/viewer/product/SAP_CLOUD_FOR_CUSTOMER)
- [OData Official Site](https://www.odata.org/)
- [odataormpy on PyPI](https://pypi.org/project/odataormpy)
