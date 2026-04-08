from typing import Type, List

from sqlalchemy import select

from .base_repository_protocol import BaseRepositoryProtocol
from .base_repository_protocol import T
from ..dependencies import SessionDep


class BaseRepository(BaseRepositoryProtocol[T]):
    def __init__(self, model: Type[T], db: SessionDep):
        self.model = model
        self.db = db

    async def find_all(self) -> List[T]:
        result = await self.db.execute(select(self.model))
        return list(result.scalars().all())

    async def find_by(self, obj_id: int) -> T | None:
        return await self.db.get(self.model, obj_id)

    async def save_or_update(self, model: T) -> T | None:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return T

    async def delete_by_id(self, obj_id: int):
        obj = await self.db.get(self.model, obj_id)
        if obj:
            await self.db.delete(obj)
            await self.db.commit()
