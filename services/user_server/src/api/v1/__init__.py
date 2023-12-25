from fastapi import APIRouter

from .users import router as users_router
from .base_configs import router as base_config_router
from .login import router as login_router
#from .logout import router as logout_router
#from .posts import router as posts_router
#from .tasks import router as tasks_router
#from .tiers import router as tiers_router
#from .rate_limits import router as rate_limits_router


router: APIRouter = APIRouter(prefix="/v1")
router.include_router(router=users_router)
router.include_router(router=base_config_router)
router.include_router(router=login_router)
#router.include_router(logout_router)
#router.include_router(posts_router)
#router.include_router(tasks_router)
#router.include_router(tiers_router)
#router.include_router(rate_limits_router)
