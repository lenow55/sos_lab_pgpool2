from typing import Any, Set
from abc import ABC, abstractmethod



class ABCCacheBackend(ABC):
    @abstractmethod
    async def set(
            self, key: str, value,
            expire: int = 0, pexpire: int = 0,
            exists=False):
        """Set Key to Value"""

    @abstractmethod
    async def get(self, key: str):
        """Get Value from Key"""

    @abstractmethod
    async def pttl(self, key: str) -> int:
        """Get PTTL from a Key"""

    @abstractmethod
    async def ttl(self, key: str) -> int:
        """Get TTL from a Key"""

    @abstractmethod
    async def pexpire(self, key: str, pexpire: int) -> bool:
        """Sets and PTTL for a Key"""

    @abstractmethod
    async def expire(self, key: str, expire: int) -> bool:
        """Sets and TTL for a Key"""

    @abstractmethod
    async def incr(self, key: str) -> int:
        """Increases an Int Key"""

    @abstractmethod
    async def decr(self, key: str) -> int:
        """Decreases an Int Key"""

    @abstractmethod
    async def delete(self, key: str):
        """Delete value of a Key"""

    @abstractmethod
    async def smembers(self, key: str) -> Set:
        """Gets Set Members"""

    @abstractmethod
    async def sadd(self, key: str, value: Any) -> bool:
        """Adds a Member to a Set"""

    @abstractmethod
    async def srem(self, key: str, member: Any) -> bool:
        """Removes a Member from a Set"""

    @abstractmethod
    async def exists(self, key: str) -> bool:
        """Checks if a Key exists"""
