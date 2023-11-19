import { useEffect, useMemo, useRef, useState } from 'react';
import Datepicker from 'react-tailwindcss-datepicker';
import axios from 'axios';
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'chartjs-adapter-moment';
import { ru } from 'date-fns/locale';

ChartJS.register(...registerables);

export default function Index() {
  const container = useRef(null);
  const map = useRef(null);

  const [date, setDate] = useState({
    startDate: new Date('2021-05-15'),
    endDate: new Date('2021-05-15'),
  });

  const [coords] = useState([44.80718242462311, 37.62550179278068]);
  const [zoom] = useState(11);
  const mapState = useMemo(() => ({ center: coords, zoom }), [coords, zoom]);
  const [isInitialized, setIsInitialized] = useState(false);

  const [hexagons, setHexagons] = useState([]);
  const [currentHexagon, setCurrentHexagon] = useState({
    center: [0, 0],
    weather: { time: [], temperature_2m: [], rain: [], relative_humidity_2m: [] },
  });

  const [chartData, setChartData] = useState({ labels: [], datasets: [] });

  const fetchData = () => {
    axios
      .get('/polygons', {
        baseURL: 'http://localhost:8080',
        params: {
          now: new Date('2021-05-02').getTime(),
          x1: 44.94645256897698,
          y1: 37.29703876822711,
          x2: 44.65134306217837,
          y2: 37.94715169000219,
        },
      })
      .then((response) => {
        setHexagons(response.data);
      });
  };

  const initMap = () => {
    if (map.current || !container.current) return;

    map.current = new ymaps.Map(container.current, mapState);

    map.current.controls.remove('trafficControl');
    map.current.controls.remove('routeEditor');
    map.current.controls.remove('rulerControl');

    map.current.events.add('boundschange', () => {
      setBounds(map.current.getBounds());
    });

    setIsInitialized(true);

    fetchData();
  };

  useEffect(() => {
    ymaps.ready(initMap);
  }, []);

  useEffect(() => {
    fetchData();
  }, [date]);

  const [, setBounds] = useState([]);

  useEffect(() => {
    if (!map.current) return;

    // const viewCoords = [
    //   [44.94645256897698, 37.29703876822711],
    //   [44.65134306217837, 37.29703876822711],
    //   [44.65134306217837, 37.94715169000219],
    //   [44.94645256897698, 37.94715169000219],
    //   [44.94645256897698, 37.29703876822711],
    // ];

    // console.log(Math.round(map.current.getZoom() / 23 + 8));

    console.log('Cells:', hexagons.length);
    console.log(hexagons);

    for (const hexagon of hexagons) {
      const polygon = new ymaps.Polygon(
        [hexagon.boundary],
        { id: hexagon.cellId, hintContent: hexagon.cellId },
        {
          hasHint: true,
          openHintOnHover: true,
          openEmptyHint: true,
          fillColor: 'rgba(255,255,255,0)',
          strokeColor: 'rgba(31,169,255,0.5)',
        },
      );

      polygon.events.add('click', () => {
        setCurrentHexagon(hexagon);
      });

      map.current.geoObjects.add(polygon);
    }
  }, [map, isInitialized, hexagons]);

  useEffect(() => {
    const dates = currentHexagon.weather.time.map((d) => new Date(d).getTime());
    setChartData({
      labels: dates,
      datasets: [
        {
          type: 'line',
          label: 'Temperature',
          borderColor: 'rgb(255, 99, 132)',
          backgroundColor: 'rgb(255, 99, 132)',
          borderWidth: 2,
          pointStyle: false,
          data: currentHexagon.weather.temperature_2m,
          xAxisId: 'x',
          yAxisID: 'y',
        },
        {
          type: 'bar',
          label: 'Rain',
          backgroundColor: 'rgb(75, 192, 192)',
          borderColor: 'rgb(75, 192, 192)',
          data: currentHexagon.weather.rain,
          borderWidth: 2,
          xAxisId: 'x',
          yAxisID: 'y1',
        },
        {
          type: 'line',
          label: 'Humidity',
          borderColor: 'rgb(53, 162, 235)',
          backgroundColor: 'rgb(53, 162, 235)',
          data: currentHexagon.weather.relative_humidity_2m,
          pointStyle: false,
          xAxisId: 'x',
          yAxisID: 'y2',
        },
      ],
    });
  }, [currentHexagon]);

  return (
    <>
      <div className="area container grid h-full min-h-full w-full min-w-full grid-flow-row grid-cols-3 grid-rows-6 gap-3">
        <div className="MAP shadow-lg">
          <div id="map" className="h-full w-full" ref={container} />
        </div>

        <div className="TimeGraphs p-3 shadow-lg">
          <Chart
            type="bar"
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
                x: {
                  type: 'time',
                  adapters: {
                    date: {
                      locale: ru,
                    },
                  },
                },
                y: {
                  type: 'linear',
                  display: true,
                  position: 'left',
                },
                y1: {
                  type: 'linear',
                  display: true,
                  position: 'right',
                },
                y2: {
                  type: 'linear',
                  display: false,
                  position: 'right',
                },
              },
            }}
          />
        </div>

        {/*<div className="CurrentWeather shadow-lg">*/}
        {/*  <h2 className="text-xl font-bold">Погода в Анапе</h2>*/}
        {/*</div>*/}

        <div className="DataBlock1 p-3 shadow-lg">
          <div className="flew-col flex flex-wrap">
            {/* Таблица показателей */}
            <div className="overflow-x-auto">
              <table className="table table-xs">
                {/* head */}
                <thead>
                  <tr>
                    <th>Заболевание</th>
                    <th>Вероятность</th>
                    <th>Тренд Шанса (?)</th>
                    <th>Через дней (?)</th>
                  </tr>
                </thead>
                <tbody>
                  {/* row 1 */}
                  <tr>
                    <td>Милдью</td>
                    <td>15%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 2 */}
                  <tr>
                    <td>Оидиум</td>
                    <td>0%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 3 */}
                  <tr>
                    <td>Антракноз</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 4 */}
                  <tr>
                    <td>Серая гниль</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 5 */}
                  <tr>
                    <td>Чёрная пятнистость</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 6 */}
                  <tr>
                    <td>Чёрная гниль</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 7 */}
                  <tr>
                    <td>Белая гниль</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 8 */}
                  <tr>
                    <td>Вертициллезное увядание</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 9 */}
                  <tr>
                    <td>Альтернариоз</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 10 */}
                  <tr>
                    <td>Фузариоз</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 11 */}
                  <tr>
                    <td>Краснуха</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                  {/* row 12 */}
                  <tr>
                    <td>Бактериальный рак</td>
                    <td>7%</td>
                    <td>⬆️⬇️</td>
                    <td>3</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <div className="DataBlock2 p-3 shadow-lg">
          <div>
            <p className="text-xl font-bold">Настройки</p>
          </div>
          <div className="flex flex-row justify-start gap-2 py-2">
            <div className="w-1/2">
              <p className="text-md">Сегодня: </p>
            </div>
            <div className="w-1/2">
              <Datepicker
                asSingle={true}
                useRange={false}
                value={date}
                inputClassName="p-2 h-6 rounded bg-gray-200"
                onChange={setDate}
              />
            </div>
          </div>
          <div className="flex flex-row justify-between gap-4">
            <div className="flex w-1/2 flex-col gap-2">
              <p className="text-md">Координаты центра</p>
              <div className="flex flex-col justify-between">
                <span>Lat</span>
                <input
                  className="input input-xs w-3/4 !bg-gray-200"
                  value={currentHexagon?.center[0]}
                  disabled
                />
              </div>
              <div className="flex flex-col justify-between">
                <span>Long</span>
                <input
                  className="input input-xs w-3/4 !bg-gray-200"
                  value={currentHexagon?.center[1]}
                  disabled
                />
              </div>
            </div>
            <div className=" flex w-1/2 flex-col gap-2">
              <p className="text-lg">Веса условий</p>
              <form className="flex flex-col gap-2">
                <div className="flex flex-col justify-between">
                  <span>Оптимальных</span>
                  <input id="opt" className="input input-xs w-3/4 bg-gray-200"></input>
                </div>
                <div className="flex flex-col justify-between">
                  <span>Начальных</span>
                  <input id="beg" className="input input-xs w-3/4 bg-gray-200"></input>
                </div>
                <div className="flex flex-col justify-between">
                  <span>Без условий</span>
                  <input id="no" className="input input-xs w-3/4 bg-gray-200"></input>
                </div>
              </form>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
