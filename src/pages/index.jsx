import { useEffect, useMemo, useRef, useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import axios from 'axios';
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';
import 'chartjs-adapter-moment';
import { ru } from 'date-fns/locale';
import * as h3 from 'h3-js';
import throttle from 'lodash.throttle';

ChartJS.register(...registerables);

export default function Index() {
  const container = useRef(null);
  const map = useRef(null);

  const [date, setDate] = useState(new Date('2021-08-13'));

  const [coords] = useState([44.80718242462311, 37.62550179278068]);
  const [zoom] = useState(11);
  const mapState = useMemo(() => ({ center: coords, zoom }), [coords, zoom]);
  const [isInitialized, setIsInitialized] = useState(false);

  const [isSelectingMode, setSelectingMode] = useState(false);

  const [selectedHexagons, setSelectedHexagons] = useState(
    localStorage.getItem('selectedHexagons')
      ? JSON.parse(localStorage.getItem('selectedHexagons'))
      : {},
  );

  const throttledAPICall = throttle(() => {
    fetchData();
  }, 1000);

  const [hexagons, setHexagons] = useState([]);
  const [currentHexagon, setCurrentHexagon] = useState({
    center: [0, 0],
    weather: { time: [], temperature_2m: [], rain: [], relative_humidity_2m: [] },
    illnesses: [],
  });

  const [chartData, setChartData] = useState({ labels: [], datasets: [] });

  const fetchData = () => {
    if (!Object.keys(selectedHexagons).length) return;

    axios
      .get('/polygons', {
        baseURL: 'http://localhost:8080',
        params: {
          now: date.getTime(),
          ids: Object.keys(selectedHexagons),
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

    throttledAPICall();
  };

  useEffect(() => {
    ymaps.ready(initMap);
  }, []);

  useEffect(() => {
    throttledAPICall();
  }, [date]);

  useEffect(() => {
    if (isSelectingMode) return;

    throttledAPICall();
  }, [isSelectingMode]);

  useEffect(() => {
    localStorage.setItem('selectedHexagons', JSON.stringify(selectedHexagons));
  }, [selectedHexagons]);

  const [bounds, setBounds] = useState([]);

  const getColor = (hex) => {
    let color = 'rgba(31,169,255,0.5)';

    if (hex) {
      for (const illnessKey of Object.keys(hex.illnesses)) {
        if (hex.illnesses[illnessKey].probs[hex.illnesses[illnessKey].probs.length - 1] > 0.5) {
          color = 'rgba(203,51,51,0.76)';
          break;
        }
      }
    }

    return color;
  };

  useEffect(() => {
    if (!map.current) return;

    map.current.geoObjects.removeAll();

    const cells = [];
    if (isSelectingMode) {
      const localBounds = map.current.getBounds();

      const viewCoords = [
        localBounds[0],
        [localBounds[0][0], localBounds[1][1]],
        localBounds[1],
        [localBounds[1][0], localBounds[0][1]],
      ];

      console.log(Math.round((map.current.getZoom() / 23) * 8 + 2));

      cells.push(
        ...h3.polygonToCells(
          viewCoords,
          8,
          // Math.round((map.current.getZoom() / 23) * 8 + 2),
          false,
        ),
      );
    } else {
      cells.push(...Object.keys(selectedHexagons));
    }

    console.log('Cells:', cells.length);
    console.log(cells);

    for (const cell of cells) {
      // const isBreak = map.current.geoObjects.each((o) => {
      //   if (cell.cellId === o.properties.get('id')) {
      //     return false;
      //   }
      // });
      //
      // if (!isBreak) {
      //   continue;
      // }

      const boundary = h3.cellToBoundary(cell);

      const hex = hexagons.find((h) => h.cellId === cell);

      let color = getColor(hex);
      if (currentHexagon.cellId === cell) {
        color = '#80FF60C7';
      }

      const polygon = new ymaps.Polygon(
        [boundary],
        { id: cell, hintContent: cell },
        {
          hasHint: true,
          openHintOnHover: true,
          openEmptyHint: false,
          fillColor: color,
          strokeColor: 'rgba(31,169,255,0.5)',
        },
      );

      // polygon.events.add('mouseleave', (e) => {
      //   const color = e.originalEvent.target.properties.get('id') in selectedHexagons
      //   if (!()) {
      //     e.originalEvent.target.options.set('fillColor', 'rgba(255,255,255, 0)');
      //   }
      // });
      // polygon.events.add('hover', (e) => {
      //   e.originalEvent.target.options.set('fillColor', 'rgba(140,255,110,0.42)');
      // });

      polygon.events.add('click', (e) => {
        const cellId = e.originalEvent.target.properties.get('id');

        if (isSelectingMode) {
          if (cellId in selectedHexagons) {
            delete selectedHexagons[cellId];

            e.originalEvent.target.options.set('fillColor', 'rgba(255,255,255, 0)');
          } else {
            selectedHexagons[cellId] = true;

            e.originalEvent.target.options.set('fillColor', '#80FF60C7');
          }

          setSelectedHexagons({ ...selectedHexagons });

          console.log(selectedHexagons);
        } else {
          const hex = hexagons.find((h) => h.cellId === cellId);
          map.current.geoObjects.each((e) => {
            console.log(e.properties.get('id'), currentHexagon.cellId);
            if (e.properties.get('id') === currentHexagon.cellId) {
              e.options.set('fillColor', 'rgba(31,169,255,0.5)');
            }
          });
          e.originalEvent.target.options.set('fillColor', '#80FF60C7');

          setCurrentHexagon(hex);
          console.log(currentHexagon);
        }
      });

      map.current.geoObjects.add(polygon);
    }
  }, [map, isInitialized, hexagons, isSelectingMode]);

  useEffect(() => {
    if (!currentHexagon) return;

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
        // {
        //   type: 'line',
        //   label: 'Black gnil',
        //   borderColor: 'rgb(5, 5, 4)',
        //   backgroundColor: 'rgb(5, 5, 4)',
        //   data: currentHexagon.probs,
        //   pointStyle: false,
        //   xAxisId: 'x',
        //   yAxisID: 'y3',
        // },
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
                y3: {
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
                    <th>Тренд</th>
                  </tr>
                </thead>
                <tbody>
                  {/* row 1 */}
                  <tr>
                    <td>Милдью</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['MILDEW']?.probs &&
                      currentHexagon?.illnesses['MILDEW']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['MILDEW'].probs[
                              currentHexagon?.illnesses['MILDEW'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['MILDEW']?.probs &&
                      currentHexagon?.illnesses['MILDEW']?.probs.length
                        ? currentHexagon?.illnesses['MILDEW'].probs[
                            currentHexagon?.illnesses['MILDEW'].probs.length - 1
                          ] > currentHexagon?.illnesses['MILDEW'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                      ️️
                    </td>
                  </tr>
                  {/* row 2 */}
                  <tr>
                    <td>Оидиум</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['OIDIUM']?.probs &&
                      currentHexagon?.illnesses['OIDIUM']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['OIDIUM'].probs[
                              currentHexagon?.illnesses['OIDIUM'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['OIDIUM']?.probs &&
                      currentHexagon?.illnesses['OIDIUM']?.probs.length
                        ? currentHexagon?.illnesses['OIDIUM'].probs[
                            currentHexagon?.illnesses['OIDIUM'].probs.length - 1
                          ] > currentHexagon?.illnesses['OIDIUM'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 3 */}
                  <tr>
                    <td>Антракноз</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['ANTRACNOS']?.probs &&
                      currentHexagon?.illnesses['ANTRACNOS']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['ANTRACNOS'].probs[
                              currentHexagon?.illnesses['ANTRACNOS'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['ANTRACNOS']?.probs &&
                      currentHexagon?.illnesses['ANTRACNOS']?.probs.length
                        ? currentHexagon?.illnesses['ANTRACNOS'].probs[
                            currentHexagon?.illnesses['ANTRACNOS'].probs.length - 1
                          ] > currentHexagon?.illnesses['ANTRACNOS'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 4 */}
                  <tr>
                    <td>Серая гниль</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['GRAY_GNILL']?.probs &&
                      currentHexagon?.illnesses['GRAY_GNILL']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['GRAY_GNILL'].probs[
                              currentHexagon?.illnesses['GRAY_GNILL'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['GRAY_GNILL']?.probs &&
                      currentHexagon?.illnesses['GRAY_GNILL']?.probs.length
                        ? currentHexagon?.illnesses['GRAY_GNILL'].probs[
                            currentHexagon?.illnesses['GRAY_GNILL'].probs.length - 1
                          ] > currentHexagon?.illnesses['GRAY_GNILL'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 5 */}
                  <tr>
                    <td>Чёрная пятнистость</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BLACK_PYATNISTS']?.probs &&
                      currentHexagon?.illnesses['BLACK_PYATNISTS']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['BLACK_PYATNISTS'].probs[
                              currentHexagon?.illnesses['BLACK_PYATNISTS'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BLACK_PYATNISTS']?.probs &&
                      currentHexagon?.illnesses['BLACK_PYATNISTS']?.probs.length
                        ? currentHexagon?.illnesses['BLACK_PYATNISTS'].probs[
                            currentHexagon?.illnesses['BLACK_PYATNISTS'].probs.length - 1
                          ] > currentHexagon?.illnesses['BLACK_PYATNISTS'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 6 */}
                  <tr>
                    <td>Чёрная гниль</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BLACK_GNILL']?.probs &&
                      currentHexagon?.illnesses['BLACK_GNILL']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['BLACK_GNILL'].probs[
                              currentHexagon?.illnesses['BLACK_GNILL'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BLACK_GNILL']?.probs &&
                      currentHexagon?.illnesses['BLACK_GNILL']?.probs.length
                        ? currentHexagon?.illnesses['BLACK_GNILL'].probs[
                            currentHexagon?.illnesses['BLACK_GNILL'].probs.length - 1
                          ] > currentHexagon?.illnesses['BLACK_GNILL'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 7 */}
                  <tr>
                    <td>Белая гниль</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['WHITE_GNILL']?.probs &&
                      currentHexagon?.illnesses['WHITE_GNILL']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['WHITE_GNILL'].probs[
                              currentHexagon?.illnesses['WHITE_GNILL'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['WHITE_GNILL']?.probs &&
                      currentHexagon?.illnesses['WHITE_GNILL']?.probs.length
                        ? currentHexagon?.illnesses['WHITE_GNILL'].probs[
                            currentHexagon?.illnesses['WHITE_GNILL'].probs.length - 1
                          ] > currentHexagon?.illnesses['WHITE_GNILL'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 8 */}
                  <tr>
                    <td>Вертициллезное увядание</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['VILT']?.probs &&
                      currentHexagon?.illnesses['VILT']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['VILT'].probs[
                              currentHexagon?.illnesses['VILT'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['VILT']?.probs &&
                      currentHexagon?.illnesses['VILT']?.probs.length
                        ? currentHexagon?.illnesses['VILT'].probs[
                            currentHexagon?.illnesses['VILT'].probs.length - 1
                          ] > currentHexagon?.illnesses['VILT'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 9 */}
                  <tr>
                    <td>Альтернариоз</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['ALTERNARIOZ']?.probs &&
                      currentHexagon?.illnesses['ALTERNARIOZ']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['ALTERNARIOZ'].probs[
                              currentHexagon?.illnesses['ALTERNARIOZ'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['ALTERNARIOZ']?.probs &&
                      currentHexagon?.illnesses['ALTERNARIOZ']?.probs.length
                        ? currentHexagon?.illnesses['ALTERNARIOZ'].probs[
                            currentHexagon?.illnesses['ALTERNARIOZ'].probs.length - 1
                          ] > currentHexagon?.illnesses['ALTERNARIOZ'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 10 */}
                  <tr>
                    <td>Фузариоз</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['FUZARIOZ']?.probs &&
                      currentHexagon?.illnesses['FUZARIOZ']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['FUZARIOZ'].probs[
                              currentHexagon?.illnesses['FUZARIOZ'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['FUZARIOZ']?.probs &&
                      currentHexagon?.illnesses['FUZARIOZ']?.probs.length
                        ? currentHexagon?.illnesses['FUZARIOZ'].probs[
                            currentHexagon?.illnesses['FUZARIOZ'].probs.length - 1
                          ] > currentHexagon?.illnesses['FUZARIOZ'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 11 */}
                  <tr>
                    <td>Краснуха</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['KRASNUHA']?.probs &&
                      currentHexagon?.illnesses['KRASNUHA']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['KRASNUHA'].probs[
                              currentHexagon?.illnesses['KRASNUHA'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['KRASNUHA']?.probs &&
                      currentHexagon?.illnesses['KRASNUHA']?.probs.length
                        ? currentHexagon?.illnesses['KRASNUHA'].probs[
                            currentHexagon?.illnesses['KRASNUHA'].probs.length - 1
                          ] > currentHexagon?.illnesses['KRASNUHA'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
                  </tr>
                  {/* row 12 */}
                  <tr>
                    <td>Бактериальный рак</td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BACT_CANCER']?.probs &&
                      currentHexagon?.illnesses['BACT_CANCER']?.probs.length
                        ? Math.round(
                            currentHexagon?.illnesses['BACT_CANCER'].probs[
                              currentHexagon?.illnesses['BACT_CANCER'].probs.length - 1
                            ] * 100,
                          )
                        : 0}
                      %
                    </td>
                    <td>
                      {currentHexagon?.illnesses &&
                      currentHexagon?.illnesses['BACT_CANCER']?.probs &&
                      currentHexagon?.illnesses['BACT_CANCER']?.probs.length
                        ? currentHexagon?.illnesses['BACT_CANCER'].probs[
                            currentHexagon?.illnesses['BACT_CANCER'].probs.length - 1
                          ] > currentHexagon?.illnesses['BACT_CANCER'].probs[0]
                          ? '⬆'
                          : '⬇'
                        : '-'}
                    </td>
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
          <div>
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => setSelectingMode(!isSelectingMode)}
            >
              {!isSelectingMode ? 'Выбрать территорию' : 'Подтвердить выбор'}
            </button>
          </div>
          <div className="flex flex-row justify-start gap-2 py-2">
            <div className="w-1/2">
              <p className="text-md">Сегодня: </p>
            </div>
            <div className="w-1/2">
              <DatePicker selected={date} onChange={(date) => setDate(date)} />
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
