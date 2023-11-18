import { useEffect, useMemo, useRef, useState } from 'react';
import Datepicker from 'react-tailwindcss-datepicker';
import axios from 'axios';
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, registerables } from 'chart.js';

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
        setChartData({
          labels: hexagon.weather.time,
          datasets: [
            {
              type: 'line',
              label: 'Temperature',
              borderColor: 'rgb(255, 99, 132)',
              backgroundColor: 'rgb(255, 99, 132)',
              borderWidth: 2,
              pointStyle: false,
              data: hexagon.weather.temperature_2m,
              yAxisID: 'y',
            },
            {
              type: 'bar',
              label: 'Rain',
              backgroundColor: 'rgb(75, 192, 192)',
              borderColor: 'rgb(75, 192, 192)',
              data: hexagon.weather.rain,
              borderWidth: 2,
              yAxisID: 'y1',
            },
            {
              type: 'line',
              label: 'Humidity',
              borderColor: 'rgb(53, 162, 235)',
              backgroundColor: 'rgb(53, 162, 235)',
              data: hexagon.weather.relative_humidity_2m,
              pointStyle: false,
              yAxisID: 'y2',
            },
          ],
        });
      });

      map.current.geoObjects.add(polygon);
    }
  }, [map, isInitialized, hexagons]);

  return (
    <>
      <div className="area container grid h-full min-h-full w-full min-w-full grid-flow-row grid-cols-3 grid-rows-3 gap-4">
        <div className="MAP">
          <div id="map" className="h-full w-full" ref={container} />
        </div>
        <div className="TimeGraphs">
          <Chart
            type="bar"
            data={chartData}
            options={{
              responsive: true,
              maintainAspectRatio: false,
              scales: {
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
        <div className="CurrentWeather">
          <p>DCurrent Weather widget if we have time</p>
        </div>
        <div className="DataBlock">
          <Datepicker asSingle={true} useRange={false} value={date} onChange={setDate} />
        </div>
      </div>
    </>
  );
}
