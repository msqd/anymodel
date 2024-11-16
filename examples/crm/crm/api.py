import contextlib

from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

mappers = {}


@contextlib.asynccontextmanager
async def lifespan(app):
    from hdm.storage import SqlAlchemyStorage
    from crm.models.contacts import ContactMapper

    storage = SqlAlchemyStorage("postgresql://postgres:postgres@localhost:5432")
    mappers["contacts"] = ContactMapper(storage)
    storage.upgrade()

    yield

    storage.engine.dispose()


async def homepage(request):
    output = []
    for contact in mappers["contacts"].find_all():
        output.append(contact.model_dump(exclude_none=True))
    return JSONResponse(output)


middleware = [Middleware(CORSMiddleware, allow_origins=["*"])]


app = Starlette(
    debug=True,
    routes=[
        Route("/", homepage),
    ],
    lifespan=lifespan,
    middleware=middleware,
)
