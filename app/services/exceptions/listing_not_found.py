from uuid import UUID


class ListingNotFound(Exception):
    def __init__(self, listing_id: UUID):
        self.listing_id = listing_id
