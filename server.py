import json

from aiohttp import web
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth import hash_password
from models import Session, User, Adverts, close_orm, init_orm


async def orm_context(app: web.Application):
    print("START")
    await init_orm()
    yield
    print("FINISH")
    await close_orm()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


app = web.Application()
app.cleanup_ctx.append(orm_context)
app.middlewares.append(session_middleware)


def get_http_error(err_cls, message: str | dict | list):
    response_json = json.dumps({"error": message})
    return err_cls(text=response_json, content_type="application/json")


async def get_user_by_id(user_id: int, session: AsyncSession):
    user = await session.get(User, user_id)
    if user is None:
        raise get_http_error(web.HTTPNotFound, "user not found")
    return user


async def add_user(user: User, session: AsyncSession):
    try:
        session.add(user)
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, "user already exists")


async def get_advert_by_id(advert_id: int, session: AsyncSession):
    advert = await session.get(Adverts, advert_id)
    if advert is None:
        raise get_http_error(web.HTTPNotFound, "advert not found")
    return advert

async def add_advert(advert: Adverts, session: AsyncSession):
    user = await session.get(User, advert.owner)
    if user is None:
        raise get_http_error(web.HTTPConflict, "owner(user) does`t exists")
    try:
        session.add(advert)
        await session.commit()
    except IntegrityError:
        raise get_http_error(web.HTTPConflict, "advert already exists")


class UserView(web.View):

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    @property
    def user_id(self) -> int:
        return int(self.request.match_info["user_id"])

    async def get_user(self):
        return await get_user_by_id(self.user_id, self.session)

    async def get(self):
        user = await self.get_user()
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        user = User(
            name=json_data["name"],
            password=hash_password(json_data["password"]),
            email=json_data["email"],
        )
        await add_user(user, self.session)
        return web.json_response(user.id_dict)

    async def patch(self):
        user = await self.get_user()
        json_data = await self.request.json()
        if "name" in json_data:
            user.name = json_data["name"]
        if "password" in json_data:
            user.password = hash_password(json_data["password"])
        if "email" in json_data:
            user.name = json_data["email"]
        await add_user(user, self.session)
        return web.json_response(user.id_dict)

    async def delete(self):
        user = await self.get_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "ok", "message": "user deleted"})





class AdvView(web.View):

    @property
    def session(self) -> AsyncSession:
        return self.request.session

    @property
    def advert_id(self) -> int:
        return int(self.request.match_info["advert_id"])

    async def get_advert(self):
        return await get_advert_by_id(self.advert_id, self.session)

    async def get(self):
        advert = await self.get_advert()
        return web.json_response(advert.dict)

    async def post(self):
        json_data = await self.request.json()
        advert = Adverts(
            title=json_data["title"],
            description=json_data["description"],
            owner=json_data["owner"],
        )
        await add_advert(advert, self.session)
        return web.json_response(advert.id_dict)

    async def patch(self):
        advert = await self.get_advert()
        json_data = await self.request.json()
        if "title" in json_data:
            advert.title = json_data["title"]
        if "description" in json_data:
            advert.description = json_data["description"]
        await add_advert(advert, self.session)
        return web.json_response(advert.id_dict)

    async def delete(self):
        advert = await self.get_advert()
        await self.session.delete(advert)
        await self.session.commit()
        return web.json_response({"status": "ok", "message": "advert deleted"})


app.add_routes(
    [
        web.post("/adverts", AdvView),
        web.get("/adverts/{advert_id:[0-9]+}", AdvView),
        web.patch("/adverts/{advert_id:[0-9]+}", AdvView),
        web.delete("/adverts/{advert_id:[0-9]+}", AdvView),
        web.post("/users", UserView),
        web.get("/users/{user_id:[0-9]+}", UserView),
        web.patch("/users/{user_id:[0-9]+}", UserView),
        web.delete("/users/{user_id:[0-9]+}", UserView),
    ]
)

web.run_app(app)
