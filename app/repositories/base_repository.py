from typing import Generic, Type, List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base_repository_protocol import T, BaseRepositoryProtocol


class BaseRepository(Generic[T], BaseRepositoryProtocol[T]):
    def __init__(self, model: Type[T], db: AsyncSession):
        self.model = model
        self.db = db

    async def find_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def find_by(self, obj_id: UUID) -> T | None:
        return await self.db.get(self.model, obj_id)

    async def create(self, model: T) -> T:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model

    async def update(self, obj_id: UUID, update_data: dict) -> T | None:
        db_obj = await self.db.get(self.model, obj_id)
        if not db_obj:
            return None

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def delete_by_id(self, obj_id: UUID) -> bool:
        obj = await self.db.get(self.model, obj_id)
        if not obj:
            return False
        else:
            await self.db.delete(obj)
            await self.db.commit()
            return True
