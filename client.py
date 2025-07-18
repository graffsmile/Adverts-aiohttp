import asyncio

import aiohttp


async def main():

    client = aiohttp.ClientSession()

    response = await client.post(
        "http://localhost:8080/users",
        json={
            "name": "John",
            "password": "123",
            "email": "john@ya.ru",
        }
    )
    print(response.status)
    print(await response.json())

    # response = await client.patch(
    #     'http://localhost:8080/users/2',
    #     json={"name": "new_name"}
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.delete(
    #     'http://localhost:8080/users/4',
    # )
    # print(response.status)
    # print(await response.json())

    response = await client.get(
        "http://localhost:8080/users/3",
    )
    print(response.status)
    print(await response.json())


    # response = await client.post(
    #     "http://localhost:8080/adverts",
    #     json={
    #         "title": "Lada 2103",
    #         "description": "Sedan, Baklszhan",
    #         "owner": 7,
    #     }
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.patch(
    #     'http://localhost:8080/adverts/2',
    #     json={"name": "new_name"}
    # )
    # print(response.status)
    # print(await response.json())
    #
    # response = await client.delete(
    #     'http://localhost:8080/adverts/4',
    # )
    # print(response.status)
    # print(await response.json())

    # response = await client.get(
    #     "http://localhost:8080/adverts/4",
    # )
    # print(response.status)
    # print(await response.json())


    await client.close()



asyncio.run(main())




