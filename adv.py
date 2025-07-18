import asyncio
import aiohttp



async def main():

    client = aiohttp.ClientSession()


    response = await client.post(
        "http://localhost:8080/adverts",
        json={
            "title": "Lada 2103",
            "description": "Sedan, Baklszhan",
            "owner": 3,
        }
    )
    print(response.status)
    print(await response.json())

    # response = await client.patch(
    #         'http://localhost:8080/adverts/1',
    #         json={"title": "Lada"}
    #     )
    # print(response.status)
    # print(await response.json())

    # response = await client.delete(
    #         'http://localhost:8080/adverts/2',
    #     )
    # print(response.status)
    # print(await response.json())

    response = await client.get("http://localhost:8080/adverts/1")
    print(response.status)
    print(await response.json())

    await client.close()

asyncio.run(main())
