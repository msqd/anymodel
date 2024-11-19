from functools import cached_property

from starlette.responses import JSONResponse
from starlette.routing import Route

from crm import services


class ContactsViewSet:
    @cached_property
    def mapper(self):
        return services.get("mappers.contact")

    def routes(self, prefix):
        return [
            Route(prefix, self.list, methods=["GET"]),
            Route(prefix, self.create, methods=["POST"]),
            Route(prefix + "{id:int}", self.get, methods=["GET"]),
            Route(prefix + "{id:int}", self.update, methods=["PUT"]),
        ]

    async def get(self, request):
        contact = self.mapper.find_one(request.path_params["id"])
        if contact is None:
            return JSONResponse({"error": "Not found."}, status_code=404)
        return JSONResponse(contact.model_dump(exclude_none=True))

    async def list(self, request):
        output = []
        for contact in self.mapper.find():
            output.append(contact.model_dump(exclude_none=True))
        return JSONResponse(output)

    async def create(self, request):
        data = await request.json()
        contact = self.mapper.save(self.mapper.__type__(**data))
        return JSONResponse(contact.model_dump(exclude_none=True))

    async def update(self, request):
        data = await request.json()
        contact = self.mapper.get(request.path_params["id"])
        if contact is None:
            return JSONResponse({"error": "Not found."}, status_code=404)
        contact = contact.model_copy(update=data)
        contact = self.mapper.save(contact)
        return JSONResponse(contact.model_dump(exclude_none=True))
