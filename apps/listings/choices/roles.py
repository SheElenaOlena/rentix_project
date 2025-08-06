from enum import Enum


class Role(Enum):
    TENANT = "tenant"
    LANDLORD = "landlord"
    MODERATOR = "moderator"
    ADMIN = "admin"


    @classmethod
    def choices(cls):
        return [(attr.name, attr.value) for attr in cls]