<script>
    import { render } from "svelte/server";
  import LeftDouble from "../elements/panel_buttons/LeftDouble.svelte";
  import {getRequest, postRequest} from "../lib/APICalls.js";
  let {func_obj=$bindable(),
    is_author=$bindable(false),
    proj_obj
  } = $props();
  //pull the list of all available functions
  //it's going to generate a list of functions in the ui basically
  var loaders=$state([]);
  var processors=$state([]);
  var renderers=$state([]);
  var models=$state([]);
  async function setFunctionList(){
    const l = await getRequest('/api/functions/get_all/');
    loaders=l.loaders;
    processors=l.processors;
    renderers=l.renderers;
    models=l.models;
  }
  setFunctionList();
  //allow for selection of functions for the main panel to update

</script>

<div class="home-container" id="container-side-1">
  <LeftDouble />
  <div class="underlying-container">
    {#if is_author}
    <h2>Available Functions</h2>
    {#snippet funclist(l)}
    {#each l as f}
    <div class="function-item center pointer" onclick={() =>{func_obj={
      'name':f.name,
      'display_name':f.display_name,
      'description':f.description,
      'params_id':''
      }}}><b class="function-item-text">{f.display_name}</b>
      <span class="function-item-text subtitle">{f.name}</span></div>
    {/each}
    {/snippet}
    {@render funclist(loaders)}
    {@render funclist(processors)}
    {@render funclist(renderers)}
    {@render funclist(models)}
    {:else}
    <h1>Description</h1>
    <p>{proj_obj.description}</p>
    {/if}
  </div>
</div>