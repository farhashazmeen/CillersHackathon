import uuid
import strawberry
from . import couchbase as cb, env
from typing import List, Optional


@strawberry.type
class Item:
    id: str
    name: str

def create_item(name: str) -> Item:
    id = str(uuid.uuid1())
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='items',
                         key=id,
                         data={'name': name}))
    return Item(id=id, name=name)
#
def get_item(id: str) -> Item | None:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='items',
                               key=id)):
        return Item(id=id, name=doc['name'])

def delete_item(id: str) -> None:
    cb.remove(env.get_couchbase_conf(),
              cb.DocRef(bucket=env.get_couchbase_bucket(),
                        collection='items',
                        key=id))

def list_items() -> list[Item]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, META().id FROM {env.get_couchbase_bucket()}._default.items"
    )
    return [Item(**r) for r in result]
#Employee collection
@strawberry.type
class Employee:
    id: str
    name: str
    availability: List[str]  # List of availability values for each day of the week

def create_employee(name: str, availability: List[str]) -> Employee:
    id = str(uuid.uuid1())
    cb.insert(env.get_couchbase_conf(),
              cb.DocSpec(bucket=env.get_couchbase_bucket(),
                         collection='employees',
                         key=id,
                         data={'name': name, 'availability': availability}))
    return Employee(id=id, name=name, availability=availability)

def get_employee(id: str) -> Optional[Employee]:
    if doc := cb.get(env.get_couchbase_conf(),
                     cb.DocRef(bucket=env.get_couchbase_bucket(),
                               collection='employees',
                               key=id)):
        data = doc.value
        return Employee(id=id, name=data['name'], availability=data['availability'])
    return None

def delete_employee(id: str) -> None:
    cb.remove(env.get_couchbase_conf(),
              cb.DocRef(bucket=env.get_couchbase_bucket(),
                        collection='employees',
                        key=id))

def list_employees() -> List[Employee]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, availability, META().id FROM {env.get_couchbase_bucket()}._default.employees"
    )
    #return [Employee(id=r['id'], name=r['name'], availability=r['availability']) for r in result]
    return [Employee(**r) for r in result]
    #return [Employee(id=r['META']['id'], name=r['name'], availability=r['availability']) for r in result]

