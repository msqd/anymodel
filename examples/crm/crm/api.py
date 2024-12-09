import contextlib

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from crm.views.contacts import ContactsViewSet
from crm import services


@contextlib.asynccontextmanager
async def lifespan(app):
    from hdm.storages.sqlalchemy import SqlAlchemyStorage
    from crm.models.contacts import ContactMapper

    storage = SqlAlchemyStorage("postgresql://postgres:postgres@localhost:5432")
    services.set("mappers.contact", ContactMapper(storage))
    storage.setup()

    yield

    storage.engine.dispose()


app = Starlette(
    debug=True,
    routes=[
        *ContactsViewSet().routes("/"),
    ],
    lifespan=lifespan,
    middleware=[
        Middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"]),
    ],
)
