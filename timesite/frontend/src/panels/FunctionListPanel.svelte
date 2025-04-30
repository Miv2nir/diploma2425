<script>
    import { render } from "svelte/server";
  import LeftDouble from "../elements/panel_buttons/LeftDouble.svelte";
  import {getRequest, postRequest} from "../lib/APICalls.js";
  //pull the list of all available functions
  //it's going to generate a list of functions in the ui basically
  var loaders=$state([]);
  var renderers=$state([]);
  async function setFunctionList(){
    const l = await getRequest('/api/functions/get_all/');
    loaders=l.loaders;
    renderers=l.renderers;
  }
  setFunctionList();
  //allow for selection of functions for the main panel to update
  let {func_name=$bindable('')} = $props();
  function setSelect(){

  }
</script>

<div class="home-container" id="container-side-1">
  <LeftDouble />
    <h2>Available Functions</h2>
    {#each loaders as f}
    <div class="project-item center"><b>{f.display_name}</b></div>
    {/each}
    {#each renderers as f}
    <div class="project-item center"><b>{f.display_name}</b></div>
    {/each}
  </div>