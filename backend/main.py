import datetime
import json

import aiohttp
import h3
from aiohttp import web

url = "https://archive-api.open-meteo.com/v1/archive"

app = web.Application()


async def get_polygons(request: web.Request):
    now = round(int(request.query.get('now')) / 1000)

    x1 = float(request.query.get('x1'))
    y1 = float(request.query.get('y1'))

    x2 = float(request.query.get('x2'))
    y2 = float(request.query.get('y2'))

    view_coords = [
        [x1, y1],
        [x1, y2],
        [x2, y2],
        [x2, y1],
    ]

    cells = h3.polygon_to_cells(h3.Polygon(view_coords), 7)

    map = []
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

            hexagon['weather'] = data['hourly']

        map.append(hexagon)

    return web.Response(text=json.dumps(map))


app.add_routes([web.get('/polygons', get_polygons)])

if __name__ == '__main__':
    web.run_app(app)