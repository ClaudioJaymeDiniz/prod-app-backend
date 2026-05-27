from abc import ABC, abstractmethod


class ProjectRepository(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def find_by_id(self, project_id: str):
        pass

    @abstractmethod
    async def find_full_by_id(self, project_id: str):
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str):
        pass

    @abstractmethod
    async def list_archived_by_owner(self, owner_id: str):
        pass

    @abstractmethod
    async def update(self, project_id: str, data: dict):
        pass

    @abstractmethod
    async def delete_permanent(self, project_id: str):
        pass

    @abstractmethod
    async def delete_project_dependencies(self, project_id: str):
        pass