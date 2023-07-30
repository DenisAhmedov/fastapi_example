import aiohttp

from app.config import CLEARBIT_API_KEY


async def get_data_from_clearbit(email):
    async with aiohttp.ClientSession(headers={'Authorization': f'Bearer {CLEARBIT_API_KEY}'}) as session:
        query = {
            'email': email
        }
        response = await session.get('https://person-stream.clearbit.com/v2/combined/find', params=query)

        result = None
        if response.status == 200:
            json = await response.json()
            if json.get('id'):
                result = {
                    'first_name': json['name']['givenName'],
                    'last_name': json['name']['MacCaw'],
                    'location': json['location']
                }

        return result


