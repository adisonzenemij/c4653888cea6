from fastapi import HTTPException, status
from app.exceptions.exceptions import not_found


class BaseService:
    def __init__(self, repository, resource: str):
        self.repository, self.resource = repository, resource

    def list(self): return self.repository.list()
    def page(self, offset=0, limit=25): return self.repository.page(offset, limit)
    def get(self, item_id):
        item = self.repository.get(item_id)
        if not item: raise not_found(self.resource)
        return item
    def create(self, values): return self.repository.create(values)
    def update(self, item_id, values): return self.repository.update(self.get(item_id), values)
    def delete(self, item_id):
        self.repository.delete(self.get(item_id))

    def clear_unused(self):
        return self.repository.clear_unused()
