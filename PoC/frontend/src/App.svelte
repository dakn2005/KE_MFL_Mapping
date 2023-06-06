<script>
  import { onMount } from "svelte";
  import { writable } from "svelte/store";

  import * as L from "leaflet";
  import "../node_modules/leaflet/dist/leaflet.css";

  import MapToolbar from "./MapToolbar.svelte";
  import Form from "./SearchForm/Form.svelte";

  // import svelteLogo from "./assets/svelte.svg";
  // import viteLogo from "/vite.svg";

  let map = null;
  let geo = writable([]);
  let allFacilities = writable([]);
  let overlay = false;

  onMount(() => {
    getLocation();
  });

  function createMap(geo) {
    // reset map container
    if (map) {
      // map.off();
      map.remove();
      document.getElementById("map").innerHTML = "";
      document.getElementById("map").innerHTML =
        '<span class="text-5xl">Loading Maps...</span>';
    }

    map = L.map("map").setView(geo, 13);

    let userIcon = L.icon({
      iconUrl: "./user.png",
      iconSize: [45, 45], // size of the icon
      // shadowSize: [50, 64], // size of the shadow
      iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
      popupAnchor: [-3, -76], // point from which the popup should open relative to the iconAnchor
    });

    L.marker(geo, { icon: userIcon }).addTo(map);

    L.tileLayer("https://tile.openstreetmap.de/{z}/{x}/{y}.png", {
      maxZoom: 20,
      attribution:
        '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);

    let toolbar = L.control({ position: "topright" });

    let toolbarComponent;
    toolbar.onAdd = (map) => {
      let div = L.DomUtil.create("div");
      toolbarComponent = new MapToolbar({
        target: div,
        props: {},
      });

      toolbarComponent.$on("click-over", ({ detail }) => (overlay = detail));

      return div;
    };

    toolbar.addTo(map);
  }

  function mapFacilities(facArr) {
    createMap($geo);
    
    facArr.forEach((f) => {

      let returnHIcon = (ownerType) => {
        let theicon = "./hosi-public.png";

        if (ownerType == "Private Practice") theicon = "./hosi-private.png";
        if (ownerType == "Faith Based Organization") theicon = "./hosi-fbo.png";

        return theicon;
      };

      let hosiIcon = L.icon({
        iconUrl: returnHIcon(f.owner_type_name),
        iconSize: [32, 32], // size of the icon
        // shadowSize: [50, 64], // size of the shadow
        iconAnchor: [22, 94], // point of the icon which will correspond to marker's location
        popupAnchor: [-3, -76], // point from which the popup should open relative to the iconAnchor
      });

      let marker = L.marker([f.lat, f.long], { icon: hosiIcon }).addTo(map);

      let html = `<ul>
        <li>${f.name}</li>
        <li>${f.owner_type_name}</li>
        <li><b>Approx distance: ${f.distance.toFixed(2)} km</b></li>
        <li>Services: ${f.service_names}</li>
        `;
      marker.bindPopup(html);
    });
  }

  $: if ($allFacilities.length > 0) {
    console.log("All Facs...", $allFacilities.length);
    mapFacilities([...$allFacilities]);
  }

  // TODO: weird, getting previous position from navigator.geolocation !important
  // Different browsers render location differently e.g. chrome vs edge
  function getLocation() {
    const successCallback = async (position) => {
      let { latitude, longitude } = position.coords;
      console.info("lat: ", latitude, "long: ", longitude);
      $geo = [latitude, longitude];
      let latlong = $geo.join(",");

      fetch(`http://127.0.0.1:5000/init/${latlong}`, {
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json;charset=UTF-8",
          "Access-Control-Allow-Origin": "*",
        },
      })
        .then((r) => r.json())
        .then((r) => {
          $allFacilities = JSON.parse(r.data);
          // createMap($geo);
        });

    };

    const errorCallback = (error) => {
      alert(showError(error));
    };

    let options = {
      enableHighAccuracy: true,
      // timeout: 5000,
      maximumAge: 0,
    };

    navigator.geolocation.getCurrentPosition(
      successCallback,
      errorCallback,
      options
    );
  }

  function showError(error) {
    let msg = "";

    switch (error.code) {
      case error.PERMISSION_DENIED:
        msg = "User denied the request for Geolocation.";
        break;
      case error.POSITION_UNAVAILABLE:
        msg = "Location information is unavailable.";
        break;
      case error.TIMEOUT:
        msg = "The request to get user location timed out.";
        break;
      case error.UNKNOWN_ERROR:
        msg = "An unknown error occurred.";
        break;
    }

    return msg;
  }
</script>

<div class="w-full bg-gray-200 flex justify-center items-center">
  <!-- <div id="map" style="height: 80vh; width: 100%;"></div> -->

  <div class="bg-gray-400 w-full h-screen relative z-0">
    <!-- map -->
    <div id="map" style="height: 100vh; width: 100%; z-index: 0;">
      <span class="text-5xl">Loading Maps...</span>
    </div>

    <!-- overlay -->
    <div
      class="{overlay
        ? 'flex'
        : 'hidden'} bg-sky-50 bg-opacity-40 absolute inset-0 z-10"
    >
      <!-- <div class="flex flex-col w-full"> -->

      <div class="min-h-fit m-4 md:mt-4 md:ml-4 w-full md:w-1/5">
        <!-- <p class="text-2xl font-bold">This should be on top of the map</p> -->
        <Form bind:overlay {mapFacilities} allFacilities={$allFacilities} />
      </div>
      <!-- </div> -->
    </div>
  </div>
</div>
