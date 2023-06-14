<script>
  import { createEventDispatcher } from "svelte";
  let overlay = false;
  const dispatch = createEventDispatcher();

  function handleClick(e) {
    overlay = !overlay;
    dispatch("click-over", overlay);
  }
</script>

<div class="flex flex-col items-center w-full h-screen mt-2 mr-2" >

  <img class="p-2" src="logo-white.png" alt="test img" width="100" height="100" />

  <div class="mt-5 mr-4 p-4 space-y-2 bg-white rounded hover:cursor-pointer shadow-slate-300 shadow-md focus:shadow-2xl" on:click="{handleClick}">
    <span class="block w-8 h-0.5 bg-black" />
    <span class="block w-6 h-0.5 bg-black" />
    <span class="block w-4 h-0.5 bg-black" />
  </div>

  <button class="mt-5 mr-4 p-4 border-none shadow-slate-3s00 shadow-md">
    About
  </button>
  
</div>
