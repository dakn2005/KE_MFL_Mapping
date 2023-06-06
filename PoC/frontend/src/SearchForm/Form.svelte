<script>
  import Select from "svelte-select";
  import orderBy from "lodash/orderBy";


  export let overlay=false, allFacilities, mapFacilities;

  let selectedLevel, selectedFacilityType, selectedPage;

  let facilityType = [
    "Private Practice",
    "Faith Based Organization",
    "Ministry of Health",
  ];
  let facLevel = [2, 3, 4, 5, 6].map((n) => "Level " + n);
  let pages = [1, 5, 20, 50, 100];

  function search(){
    let filteredFacilities=[...allFacilities];

    if (selectedLevel && selectedLevel != "")
        filteredFacilities = filteredFacilities.filter(f => f.keph_level_name == selectedLevel.value)

    if (selectedFacilityType && selectedFacilityType != "")
        filteredFacilities = filteredFacilities.filter(f => f.owner_type_name == selectedFacilityType.value)

    if (selectedPage){
        let ordered = orderBy(filteredFacilities, ['distance','asc'])
        filteredFacilities =ordered.slice(0, selectedPage.value);
    }

    console.log(filteredFacilities)
    mapFacilities(filteredFacilities);
    closeForm();
}

function clearFilters(){
    mapFacilities(allFacilities);
    closeForm();
  }

  function closeForm(){
    overlay = !overlay
  }

</script>

<form class="bg-white opacity-90 shadow-md rounded px-8 pt-6 pb-8 mb-4">
  <div class="mb-4 text-right">
    <span class="text-red-600 text-xl cursor-pointer" on:click={closeForm}> &#x2716; </span>
  </div>
  <div class="mb-4">
    <label for="username"> Services </label>
    <!--  -->
  </div>

  <div class="mb-6">
    <label for="password"> Level </label>
    <Select items={facLevel} bind:value={selectedLevel} />
    <!--  -->
  </div>
  <div class="mb-6">
    <label for="password"> Facility type </label>
    <!--  -->
    <Select items={facilityType} bind:value={selectedFacilityType} />
  </div>
  <div class="mb-6">
    <label for="password"> Operating Hours </label>
    <!--  -->
  </div>
  <div class="mb-6">
    <label for="password"> Has Cots </label>
    <!--  -->
  </div>
  <div class="mb-6">
    <label for="password"> Output Numbers </label>
    <Select items={pages} bind:value={selectedPage} />
    <!--  -->
  </div>
  <div class="flex flex-col">
    <button
      class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
      type="button"
      on:click|preventDefault={search}
    >
      Search
    </button>
    <!-- href="#" -->
    <button
      class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
      on:click|preventDefault={clearFilters}
    >
      Clear Filters
    </button>
  </div>
</form>

<style>
  label {
    @apply block text-gray-700 text-sm font-bold mb-2 text-left;
  }
</style>
