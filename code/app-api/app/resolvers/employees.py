import asyncio
import time
from typing import AsyncGenerator, List
import strawberry
import uuid
import logging
from .. import couchbase as cb, env
from ..auth import IsAuthenticated

logger = logging.getLogger(__name__)

@strawberry.type
class Employee:
    id: str
    name: str
    availability: List[str]  # List of availability values for each day of the week

@strawberry.input
class EmployeeCreateInput:
    name: str
    availability: List[str]

def list_employees() -> List[Employee]:
    result = cb.exec(
        env.get_couchbase_conf(),
        f"SELECT name, availability, META().id FROM {env.get_couchbase_bucket()}._default.employees"
    )
    #return [Employee(**r) for r in result]
    return [Employee(**r) for r in result]

@strawberry.type
class Query:
    @strawberry.field
    def employees(self) -> List[Employee]:
        return list_employees()

@strawberry.type
class Mutation:
    @strawberry.field(permission_classes=[IsAuthenticated])
    async def employees_create(self, employees: List[EmployeeCreateInput]) -> List[Employee]:
        created_employees = []
        for employee in employees:
            id = str(uuid.uuid1())
            cb.insert(env.get_couchbase_conf(),
                      cb.DocSpec(bucket=env.get_couchbase_bucket(),
                                 collection='employees',
                                 key=id,
                                 data={'name': employee.name, 'availability': employee.availability}))
            created_employee = Employee(id=id, name=employee.name, availability=employee.availability)
            created_employees.append(created_employee)
        return created_employees

    @strawberry.field(permission_classes=[IsAuthenticated])
    async def employees_remove(self, ids: List[str]) -> List[str]:
        for id in ids:
            cb.remove(env.get_couchbase_conf(),
                      cb.DocRef(bucket=env.get_couchbase_bucket(),
                                collection='employees',
                                key=id))
        return ids

@strawberry.type
class Subscription:
    @strawberry.subscription(permission_classes=[IsAuthenticated])
    async def employees_created(self, info: strawberry.types.Info) -> AsyncGenerator[Employee, None]:
        seen = set(e.id for e in list_employees())
        while True:
            current_time = int(time.time())
            for e in list_employees():
                if e.id not in seen:
                    seen.add(e.id)
                    yield e
            await asyncio.sleep(0.5)
