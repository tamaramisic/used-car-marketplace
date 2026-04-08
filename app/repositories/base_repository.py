from typing import Type, List

from .base_repository_protocol import BaseRepositoryProtocol
from .base_repository_protocol import T
from ..dependencies import SessionDep


class BaseRepository(BaseRepositoryProtocol[T]):
    def __init__(self, model: Type[T], db: SessionDep):
        self.model = model
        self.db = db

    async def find_all(self) -> List[T]:
        result = await self.db.execute.select(self.model)
        return result.scalars().all()

    async def find_by(self, id: int) -> T | None:
        return await self.db.get(self.model, id)

    async def save_or_update(self) -> T | None:
        self.db.add(T)
        await self.db.commit()
        await self.db.refresh()
        return T

    async def delete_by_id(self, id: int):
        await self.db.delete(self.db.get(self.db.model, id))
        await self.db.commit()









