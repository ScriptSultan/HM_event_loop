import asyncio
from datetime import datetime
from http.client import InvalidURL
from pprint import pprint
import requests
import aiohttp

from models import StarWars, async_session

base_url = 'https://swapi.dev/api/'


async def request(url):
    client = aiohttp.ClientSession()
    request_people = await client.get(url + 'people')
    count_people = await request_people.json()
    await client.close()
    return count_people['count']


async def info_people(url, id_people):
    client = aiohttp.ClientSession()
    response = await client.get(url + 'people/' + f'{id_people}')
    response_json = await response.json()
    await client.close()
    return response_json


async def insert_db(lst_info):
    async with async_session() as session:
        model = StarWars(
            birth_year=lst_info['birth_year'],
            eye_color=lst_info['eye_color'],
            films=lst_info['films'],
            gender=lst_info['gender'],
            hair_color=lst_info['hair_color'],
            height=lst_info['height'],
            homeworld=lst_info['homeworld'],
            mass=lst_info['mass'],
            name=lst_info['name'],
            skin_color=lst_info['skin_color'],
            species=lst_info['species'],
            starships=lst_info['starships'],
            vehicles=lst_info['vehicles'])
        session.add_all(model)
        await session.commit()


async def take_lst_films(session, films):
    films_titles = []
    for film_url in films:
        async with session.get(film_url) as response:
            try:
                film_data = await response.json()
                film_title = film_data.get('title')
                if film_title:
                    films_titles.append(film_title)
            except InvalidURL as e:
                print(f"Error fetching film data: {e}")
    return ", ".join(films_titles)


async def take_lst_other(session, other):
    other_names = []
    for other_url in other:
        try:
            async with session.get(other_url) as response:
                data = await response.json()
                other_name = data.get('name')
                if other_name:
                    other_names.append(other_name)
        except aiohttp.ClientConnectorError as e:
            pass
        except aiohttp.client_exceptions.InvalidURL as e:
            pass
    return ", ".join(other_names)

async def main():
    count_person = await request(base_url)
    info_people_lst = []
    async with aiohttp.ClientSession() as session:
        tasks = [info_people(base_url, i) for i in range(1, count_person + 1)]
        results = await asyncio.gather(*tasks)
        for person in results:
            if len(person) > 1:
                person['films'] = await take_lst_films(session, person['films'])
                person['homeworld'] = await take_lst_other(session, person['homeworld'])
                person['species'] = await take_lst_other(session, person['species'])
                person['vehicles'] = await take_lst_other(session, person['vehicles'])
                person['starships'] = await take_lst_other(session, person['starships'])
    insert = asyncio.create_task(insert_db(person))

if __name__ == '__main__':
    start = datetime.now()
    asyncio.run(main())
    end = datetime.now()
    print(end - start)