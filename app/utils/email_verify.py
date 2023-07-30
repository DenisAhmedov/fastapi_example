import aiohttp

from app.config import EMAIL_HUNTER_API_KEY


async def email_verify(email):
    async with aiohttp.ClientSession() as session:
        query = {
            'email': email,
            'api_key': EMAIL_HUNTER_API_KEY
        }
        response = await session.get('https://api.hunter.io/v2/email-verifier', params=query)

        while response.status == 202:
            response = await session.get('https://api.hunter.io/v2/email-verifier', params=query)

        json = await response.json()
        if ('errors' in json) or (json['data']['status'] == 'invalid'):
            return False
        else:
            return True


