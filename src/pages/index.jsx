import { useEffect, useMemo, useRef, useState } from 'react';
import * as h3 from 'h3-js';
import Datepicker from "react-tailwindcss-datepicker";

export default function Index() {
  const container = useRef(null);
  const map = useRef(null);

  const [coords, setCoords] = useState([44.80718242462311, 37.62550179278068]);
  const [zoom, setZoom] = useState(11);
  const mapState = useMemo(() => ({ center: coords, zoom }), [coords, zoom]);
  const [isInitialized, setIsInitialized] = useState(false);

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
  };

  useEffect(() => {
    ymaps.ready(initMap);
  }, []);

  const [bounds, setBounds] = useState([]);
  // const [polygons, setPolygons] = useState([]);

  useEffect(() => {
    if (!map.current) return;

    // console.log(viewCoords);

    const viewCoords = [
      [44.94645256897698, 37.29703876822711],
      [44.65134306217837, 37.29703876822711],
      [44.65134306217837, 37.94715169000219],
      [44.94645256897698, 37.94715169000219],
      [44.94645256897698, 37.29703876822711],
    ];

    console.log(Math.round(map.current.getZoom() / 23 + 8));
    const cells = h3.polygonToCells(
      viewCoords,
      8,
      // Math.round(map.current.getZoom() / 23 + 8),
      false,
    );

    console.log('Cells:', cells.length);

    for (const cell of cells) {
      const polygon = new ymaps.Polygon(
        [h3.cellToBoundary(cell, false)],
        { id: cell, hintContent: cell },
        {
          hasHint: true,
          openHintOnHover: true,
          openEmptyHint: true,
          fillColor: 'rgba(255,255,255,0)',
          strokeColor: 'rgba(31,169,255,0.5)',
        },
      );

      map.current.geoObjects.add(polygon);
    }
  }, [map, isInitialized]);

  return (
    <>
      <div className="area container grid h-full min-h-full w-full min-w-full grid-flow-row grid-cols-3 grid-rows-3 gap-1">
        <div className="MAP">
          <div id="map" className="h-full w-full" ref={container} />
        </div>
        <div className="TimeGraphs">
          <p> Temp Humidity and Rain graph using Char.js</p>
        </div>
        <div className="CurrentWeather">
          <p>DCurrent Weather widget if we have time</p>
        </div>
        <div className="DataBlock">
          <p>Data goes here:</p>
          <Datepicker asSingle={true} useRange={false}/>
        </div>
      </div>
    </>
  );
}
