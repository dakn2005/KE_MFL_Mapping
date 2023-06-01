<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import * as L from "leaflet";
  import "../node_modules/leaflet/dist/leaflet.css";

  // import svelteLogo from "./assets/svelte.svg";
  // import viteLogo from "/vite.svg";

  let map = null;
  let geo = writable([]);

  onMount(() => {
    getLocation();
  });

  $: if ($geo.length > 0) {
    // console.log($geo)
    map = L.map("map").setView($geo, 13); //[51.505, -0.09]

    let marker = L.marker($geo).addTo(map);

    marker.bindPopup("<b>Hello world!</b><br>I am a popup.");

    L.tileLayer("https://tile.openstreetmap.de/{z}/{x}/{y}.png", {
      maxZoom: 20,
      attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
  }

  // TODO: wierd, getting previous position from navigator.geolocation !important
  // Different browsers render location differently e.g. chrome vs edge

  function getLocation() {
    const successCallback = (position) => {
      let { latitude, longitude } = position.coords;
      console.info(latitude, longitude)
      $geo = [latitude, longitude];
    };

    const errorCallback = (error) => {
      console.error(error);
      alert("Please grant browser permissions for geolocation, and reload");
    };

    let options = {
      enableHighAccuracy: true,
      timeout: 5000,
      maximumAge: 0,
    };

    navigator.geolocation.getCurrentPosition(successCallback, errorCallback, options);
  }
</script>

<main class="w-full h-screen bg-gray-200 flex justify-center items-center">
  <!-- <div id="map" style="height: 80vh; width: 100%;"></div> -->

  <div class="bg-gray-400 w-full h-screen relative z-0">
    <!-- <p class="italic text-bold bd-red-100 font-serif">Map</p> -->
    <div id="map" style="height: 100vh; width: 100%; z-index: 0;"></div>

    <!-- <div class="flex ml-12 w-11/12 absolute inset-0 z-10 border-2 border-amber-600" style="height: 90%;">
        
        <div class="flex flex-col w-full">
          <div class="w-full h-14 mt-4 md:ml-10">
            <div class="p-4 space-y-2 bg-gray-600 rounded shadow w-16 float-right mr-4">
              <span class="block w-8 h-0.5 bg-gray-100"></span>
              <span class="block w-6 h-0.5 bg-gray-100"></span>
              <span class="block w-4 h-0.5 bg-gray-100"></span>
            </div>
          </div>

          <div class=" w-full h-screen flex justify-center items-center ">
            <p class="text-2xl font-bold">This should be on top of the map</p>
          </div>
        </div>
      </div> -->
  </div>
</main>
