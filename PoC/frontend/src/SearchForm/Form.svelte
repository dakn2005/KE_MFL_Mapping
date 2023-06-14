<script>
  import { onMount } from "svelte";
  import Select from "svelte-select";
  // import Select from 'svelte-select/no-styles/Select.svelte'

  import orderBy from "lodash/orderBy";
  import capitalize from "lodash/capitalize";
  import flattenDeep from "lodash/flattenDeep";
  import filter from "lodash/filter";
  import includes from "lodash/includes";

  export let overlay = false,
    allFacilities,
    mapFacilities,
    services,
    service_categories;

  let selectedLevel,
    selectedFacilityType,
    selectedPage,
    selectedServices = [],
    selectedServiceCategories = [];

  let facilityType = [
    "Private Practice",
    "Faith Based Organization",
    "Ministry of Health",
  ];
  let facLevel = [2, 3, 4, 5, 6].map((n) => "Level " + n);
  let pages = [5, 20, 50, 100];

  let serviceOptions = [],
    serviceCategoryOptions = [];

  $: if (services.length > 0) {
    serviceOptions = services.map((s) => ({
      value: s.id,
      label: capitalize(s.name),
    }));
  }

  $: if (service_categories.length > 0) {
    serviceCategoryOptions = service_categories.map((s) => ({
      value: s.id,
      label: capitalize(s.name),
    }));
  }

  function search() {
    let filteredFacilities = [...allFacilities];

    //level
    if (selectedLevel && selectedLevel != "")
      filteredFacilities = filteredFacilities.filter(
        (f) => f.keph_level_name == selectedLevel.value
      );

    //facility type
    if (selectedFacilityType && selectedFacilityType != "")
      filteredFacilities = filteredFacilities.filter(
        (f) => f.owner_type_name == selectedFacilityType.value
      );

    //service categories
    if (selectedServiceCategories && selectedServiceCategories.length > 0) {
      let filteredSCatIdsArr = [];

      selectedServiceCategories.forEach((s) => {
        let filteredIds = filteredFacilities
          .filter((f) =>
            f.categories.includes(s.value)
          )
          .map((f) => f.id);
          filteredSCatIdsArr = [...filteredIds];
      });

      //get search unique ids
      let uniqSCatIds = Array.from(new Set(filteredSCatIdsArr));

      //filter by ids
      filteredFacilities = filter(filteredFacilities, (fac) =>
        includes(uniqSCatIds, fac.id)
      );
    }

    //services
    if (selectedServices && selectedServices.length > 0) {
      let filteredIdsArr = [];

      selectedServices.forEach((s) => {
        let filteredIds = filteredFacilities
          .filter((f) =>
            f.service_names.toLowerCase().includes(s.label.toLowerCase())
          )
          .map((f) => f.id);
        filteredIdsArr = [...filteredIds];
      });


      //get search unique ids
      let uniqIds = Array.from(new Set(filteredIdsArr));

      //filter by ids
      filteredFacilities = filter(filteredFacilities, (fac) =>
        includes(uniqIds, fac.id)
      );
    }

    //paging
    if (selectedPage) {
      let ordered = orderBy(filteredFacilities, ["distance", "asc"]);
      filteredFacilities = ordered.slice(0, selectedPage.value);
    }

    // console.log(filteredFacilities)
    mapFacilities(filteredFacilities);
    // closeForm();
  }

  function clearFilters() {
    mapFacilities(allFacilities);
    closeForm();
  }

  function closeForm() {
    overlay = !overlay;
  }
</script>

<form class="bg-white opacity-90 shadow-md rounded px-8 pt-6 pb-8 mb-4">
  <div class="mb-4 text-right">
    <span class="text-red-600 text-xl cursor-pointer" on:click={closeForm}>
      &#x2716;
    </span>
  </div>

  <div class="mb-2">
    <label for="username">Services Categories</label>

    <!--  -->
    <Select
      items={serviceCategoryOptions}
      multiple={true}
      bind:value={selectedServiceCategories}
    />
  </div>

  <div class="mb-2">
    <label for="username">Services</label>
    <!--  -->
    <Select
      items={serviceOptions}
      multiple={true}
      bind:value={selectedServices}
    />
  </div>

  <div class="mb-2">
    <label>Level</label>
    <Select
      inputStyles="text-align: left; text-align-last: left;"
      items={facLevel}
      bind:value={selectedLevel}
    />
    <!--  -->
  </div>

  <div class="mb-2">
    <label>Facility type</label>
    <!--  -->
    <Select
      --input-left="left"
      items={facilityType}
      bind:value={selectedFacilityType}
    />
  </div>
  <!-- <div class="mb-6">
    <label > Operating Hours </label>
    
  </div> -->
  <!-- <div class="mb-6">
    <label > Has Cots </label>
    
  </div> -->
  <div class="mb-2">
    <label>Facilities displayed: </label>
    <Select items={pages} bind:value={selectedPage} />
    <!--  -->
  </div>

  <div class="flex flex-col">
    <button
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold text-sm focus:outline-none focus:shadow-outline"
      type="button"
      on:click|preventDefault={search}
    >
      Search
    </button>
    <!-- href="#" -->
    <button
      class="bg-orange-800 font-bold text-sm text-white border-none hover:bg-orange-500 mt-2 focus:shadow-outline"
      on:click|preventDefault={clearFilters}
    >
      Clear Filters
    </button>
  </div>
</form>

<style>
  label {
    @apply block text-gray-700 text-sm font-bold mb-1 text-left;
  }

  option {
    text-align: left;
  }
</style>
