from enum import Enum, auto

class Role(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

permissions = {
    Role.ADMIN: ['create', 'read', 'update', 'delete'],
    Role.USER: ['create', 'read', 'update'],
    Role.GUEST: ['read'],
}