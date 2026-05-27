from abc import ABC, abstractmethod


class SubmissionRepository(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def update(self, submission_id: str, data: dict):
        pass

    @abstractmethod
    async def find_by_id(self, submission_id: str):
        pass

    @abstractmethod
    async def find_form_by_id(self, form_id: str):
        pass

    @abstractmethod
    async def find_form_with_project_owner(self, form_id: str):
        pass

    @abstractmethod
    async def list_by_user(self, user_id: str):
        pass

    @abstractmethod
    async def list_by_form(self, form_id: str):
        pass

    @abstractmethod
    async def list_by_form_and_user(self, form_id: str, user_id: str):
        pass

    @abstractmethod
    async def find_by_id_with_form(self, submission_id: str):
        pass