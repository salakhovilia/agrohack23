import datetime
import json

import aiohttp
import aiohttp_cors
import h3
from aiohttp import web

from algo_client import get_illness_prob_for_each_timeunit, map_hums
from illness_cases_spec import IllnessCase

url = "https://archive-api.open-meteo.com/v1/archive"

app = web.Application()


async def get_polygons(request: web.Request):
    now = round(int(request.query.get('now')) / 1000)

    cells = request.query.getall('ids[]')
    
    map = []

    print('hexagons:', len(cells))

    for cell in cells:
        hexagon = {
            'cellId': cell,
            'center': h3.cell_to_latlng(cell),
            'boundary': h3.cell_to_boundary(cell, geo_json=False),
            'weather': []
        }

        end_date = datetime.datetime.fromtimestamp(now).date().isoformat()
        if datetime.datetime.now().timestamp() - now > 24 * 60 * 60:
            end_date = datetime.datetime.fromtimestamp(now + 7 * 24 * 60 * 60).date().isoformat()
        else:
            forecast_start = now
            forecast_end = now + 7 * 24 * 60 * 60

        params = {
            "latitude": hexagon['center'][0],
            "longitude": hexagon['center'][1],
            "start_date": datetime.datetime.fromtimestamp(now - 7 * 24 * 60 * 60).date().isoformat(),
            "end_date": end_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "rain"],
            "timezone": "Europe/Moscow",
            "models": "best_match"
        }

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            response = await session.get(url, params=params)
            data = await response.json()

            if not data:
                print('skip', json.dumps(params))
                continue
            hexagon['weather'] = data['hourly']

            temps = data['hourly']["temperature_2m"]
            hums = data['hourly']["relative_humidity_2m"]

            probs = get_illness_prob_for_each_timeunit(
                none_satisf_weight=0.5,
                partially_satisf_weight=1.0,
                optimally_satisf_weight=3.0,
                exp_growth_weight=0.1,
                temps=temps,
                hums=map_hums(hums),
                illness_name=IllnessCase.BLACK_GNILL.name
            )
            hexagon['probs'] = probs

        map.append(hexagon)

    return web.Response(text=json.dumps(map))


app.add_routes([web.get('/polygons', get_polygons)])

cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

if __name__ == '__main__':
    web.run_app(app)
