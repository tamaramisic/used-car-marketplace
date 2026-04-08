from typing import List, Protocol, TypeVar

T = TypeVar("T")

class BaseRepositoryProtocol(Protocol[T]):
    async def find_all(self) -> List[T]:
        ...

    async def find_by(self, obj_id: int) -> T | None:
        ...

    async def save_or_update(self, model: T) -> T | None:
        ...

    async def delete_by_id(self, obj_id: int):
        ...


