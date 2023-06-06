<script>
    import { createEventDispatcher } from 'svelte';

    let overlay= false
    const dispatch = createEventDispatcher();

    function handleClick(e){
        overlay = !overlay;
        dispatch('click-over', overlay);
    }

</script>

<div class="w-full h-14 mt-2 mr-2" on:click={handleClick}>
    <div class="p-4 space-y-2 bg-gray-600 rounded shadow w-16 float-right mr-4">
      <span class="block w-8 h-0.5 bg-gray-100"></span>
      <span class="block w-6 h-0.5 bg-gray-100"></span>
      <span class="block w-4 h-0.5 bg-gray-100"></span>
    </div>
  </div>