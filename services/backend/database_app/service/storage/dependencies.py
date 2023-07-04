from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database_app.dependencies import get_db_stub
from . import service
from .schema import EmployeeIn
from .exceptions import EmployeeServiceNumberNotUnique, EmployeeIDDoesntExist


async def employee_id_exist(
        db: Annotated[AsyncSession, Depends(get_db_stub)],
        employee_id: int
) -> int:

    if service.is_employee_id_exist(db, employee_id):
        raise EmployeeIDDoesntExist("Employee service number must exist")
    return employee_id


async def employee_service_number_unique(
        db: Annotated[AsyncSession, Depends(get_db_stub)],
        employee_in: EmployeeIn
) -> EmployeeIn:

    if await service.is_service_number_occupied(db, employee_in.service_number):
        raise EmployeeServiceNumberNotUnique("Employee service number must be unique")
    return employee_in