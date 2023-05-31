<script>
  import { onMount } from "svelte";
  import {writable} from 'svelte/store';

  import * as L from "leaflet";
  import '../node_modules/leaflet/dist/leaflet.css';

  // import svelteLogo from "./assets/svelte.svg";
  // import viteLogo from "/vite.svg";

  let map = null;
  let geo = writable([]);

  onMount(() => {
    getLocation();
  });

  $: if($geo.length > 0){
    // console.log($geo)
    map = L.map('map').setView($geo, 13); //[51.505, -0.09]

    let marker = L.marker($geo).addTo(map);

    marker.bindPopup("<b>Hello world!</b><br>I am a popup.");

    L.tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 20,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);


  }

  function getLocation() {
    const successCallback = (position) => {
      let {latitude, longitude} = position.coords;
      $geo = [latitude, longitude]
    };

    const errorCallback = (error) => {
      console.error(error);
      alert("Please grant browser permissions for geolocation, and reload");
    };

    navigator.geolocation.getCurrentPosition(successCallback, errorCallback);
  }
</script>

<main style="height: 100vh; width: 100%;">
  <div id="map" style="height:100%;width:100%"></div>
</main>

<svelte:head>
  <!-- <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" /> -->

  <!-- <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script> -->

  <!-- <script src="js/leaflet-providers.js"></script> -->
</svelte:head>
