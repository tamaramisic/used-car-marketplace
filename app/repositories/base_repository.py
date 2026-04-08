from typing import Generic, Type, List
from uuid import UUID
from sqlalchemy import select
from .base_repository_protocol import T
from ..dependencies import SessionDep


class BaseRepository(Generic[T]):
    def __init__(self, model: Type[T], db: SessionDep):
        self.model = model
        self.db = db

    async def find_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def find_by(self, obj_id: UUID) -> T | None:
        return await self.db.get(self.model, obj_id)

    async def save_or_update(self, entity: T) -> T | None:
        self.db.add(entity)
        await self.db.commit()
        await self.db.refresh(entity)
        return entity

    async def delete_by_id(self, obj_id: UUID):
        obj = await self.db.get(self.model, obj_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
