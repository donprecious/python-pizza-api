import uuid
from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import CustomerInfo


class CustomerRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get(self, customer_id: uuid.UUID) -> Optional[CustomerInfo]:
        return await self._session.get(CustomerInfo, customer_id)

    async def get_by_unique_identifier(self, unique_identifier: str) -> Optional[CustomerInfo]:
        stmt = select(CustomerInfo).where(CustomerInfo.uniqueIdentifier == unique_identifier)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, customer: CustomerInfo) -> CustomerInfo:
        self._session.add(customer)
        await self._session.flush()
        await self._session.refresh(customer)
        return customer

    async def update(self, customer: CustomerInfo) -> CustomerInfo:
        await self._session.flush()
        await self._session.refresh(customer)
        return customer

    async def find_or_create(self, unique_identifier: str, fullname: str, full_address: str) -> CustomerInfo:
        """Find existing customer by uniqueIdentifier or create a new one."""
        if existing_customer := await self.get_by_unique_identifier(unique_identifier):
            # Update existing customer info if provided data is different
            if existing_customer.fullname != fullname:
                existing_customer.fullname = fullname
            if existing_customer.full_address != full_address:
                existing_customer.full_address = full_address
            return await self.update(existing_customer)

        # Create new customer
        new_customer = CustomerInfo(
            uniqueIdentifier=unique_identifier,
            fullname=fullname,
            full_address=full_address,
        )
        return await self.create(new_customer)