from ninja import NinjaAPI

from blogs.api import router as blogs_router
from events.api import router as events_router
from news.api import router as news_router
from proposals.api import router as proposal_router

api = NinjaAPI(urls_namespace="newspaper")

api.add_router("/events/", events_router)
api.add_router("/news/", news_router)
api.add_router("/blogs/", blogs_router)


api.add_router("/proposals/", proposal_router)
