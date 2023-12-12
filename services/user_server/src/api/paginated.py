from typing import Annotated, Generic, List, TypeVar, ClassVar
from tortoise.contrib.pydantic.base import PydanticModel
from pydantic import BaseModel, Field, ConfigDict

SchemaModelType = TypeVar(
    "SchemaModelType", bound=PydanticModel)


class ListResponse(BaseModel, Generic[SchemaModelType]):
    data: List[SchemaModelType]
    total_count: Annotated[
        int,
        Field(
            description="Total count of records"
        )
    ]


class PaginatedListResponse(ListResponse[SchemaModelType]):
    model_config: ClassVar[ConfigDict] = ConfigDict(
        extra='forbid')
    has_more: bool
    page: int | None = None
    items_per_page: int | None = None


def compute_offset(page: int, items_per_page: int) -> int:
    """
    Calculate the offset for pagination based on the given page number and items per page.

    The offset represents the starting point in a dataset for the items on a given page.
    For example, if each page displays 10 items and you want to display page 3, the offset will be 20,
    meaning the display should start with the 21st item.

    Parameters
    ----------
    page : int
        The current page number. Page numbers should start from 1.
    items_per_page : int
        The number of items to be displayed on each page.

    Returns
    -------
    int
        The calculated offset.

    Examples
    --------
    >>> offset(1, 10)
    0
    >>> offset(3, 10)
    20
    """
    return (page - 1) * items_per_page
