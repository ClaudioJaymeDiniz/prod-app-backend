from abc import ABC, abstractmethod


class UserRepository(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def find_by_email(self, email: str):
        pass

    @abstractmethod
    async def find_by_id(self, user_id: str):
        pass

    @abstractmethod
    async def update(self, user_id: str, data: dict):
        pass

    @abstractmethod
    async def find_by_reset_token(self, token: str):
        pass

    @abstractmethod
    async def search(self, query: str):
        pass