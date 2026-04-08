from app.dependencies import SessionDep
from app.models.listing import Listing
from app.repositories.base_repository import BaseRepository


class ListingRepository(BaseRepository[Listing]):
    def __init__(self, db: SessionDep):
        super().__init__(Listing, db)