from abc import ABC, abstractmethod


class FormRepository(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def find_project_by_id(self, project_id: str):
        pass

    @abstractmethod
    async def find_by_id(self, form_id: str):
        pass

    @abstractmethod
    async def find_by_id_with_project(self, form_id: str):
        pass

    @abstractmethod
    async def find_by_id_with_project_and_submissions(self, form_id: str):
        pass

    @abstractmethod
    async def list_by_project(self, project_id: str):
        pass

    @abstractmethod
    async def list_public(self):
        pass

    @abstractmethod
    async def update(self, form_id: str, data: dict):
        pass

    @abstractmethod
    async def delete_permanent(self, form_id: str):
        pass

    @abstractmethod
    async def delete_submissions_by_form(self, form_id: str):
        pass

    @abstractmethod
    async def list_submissions_by_form(self, form_id: str):
        pass