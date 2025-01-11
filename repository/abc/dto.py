from typing import TYPE_CHECKING, Union

from database import AsyncSession, Base

if TYPE_CHECKING:
    from ..crud import Crud
    from ..user import User

class AbstractDTO:
    crud: 'Crud' 
    session: AsyncSession
    user: Union['User', None]
    obj: Base