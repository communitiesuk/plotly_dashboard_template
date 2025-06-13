"""LocalAuthority class"""

from dataclasses import dataclass


@dataclass(eq=True)
class LocalAuthority:
    """
    A data class representing a Local Authority

    Args:
        ons_code (str): The ONS code of the Local Authority.
        name (str): The display name of the Local Authority.
        tier (str, optional): The tier of the local authority.
    """

    ons_code: str
    name: str
    tier: str = None

    def __eq__(self, other):
        if isinstance(other, LocalAuthority):
            return self.ons_code == other.ons_code
        return False

    def __hash__(self):
        """define hash function so can compare two objects on ons code"""
        return hash((self.ons_code))
