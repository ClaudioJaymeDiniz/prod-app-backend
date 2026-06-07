from abc import ABC, abstractmethod


class InvitationRepository(ABC):

    @abstractmethod
    async def create(self, data: dict):
        pass

    @abstractmethod
    async def find_project_by_id(self, project_id: str):
        pass

    @abstractmethod
    async def find_invitation_by_id(self, invitation_id: str):
        pass

    @abstractmethod
    async def find_user_by_email(self, email: str):
        pass

    @abstractmethod
    async def upsert_project_member(
        self,
        user_id: str,
        project_id: str,
        role: str
    ):
        pass

    @abstractmethod
    async def list_pending_by_email(self, email: str):
        pass

    @abstractmethod
    async def update_invitation_status(
        self,
        invitation_id: str,
        status: str,
        user_id: str | None = None,
    ):
        pass

    @abstractmethod
    async def find_accepted_by_project_and_email(
        self,
        project_id: str,
        email: str
    ):
        pass

    @abstractmethod
    async def list_pending_by_project(self, project_id: str):
        pass