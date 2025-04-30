<script>
  import LeftDouble from "../elements/panel_buttons/LeftDouble.svelte";
  import {getRequest, postRequest} from "../lib/APICalls.js";
  //pull the list of all available functions
  //it's going to generate a list of functions in the ui basically
  async function setFunctionList(){
    const l = await getRequest('/api/functions/get_all/');
    console.log(l.loaders[0]);
  }
  setFunctionList();

</script>

<div class="home-container" id="container-side-1">
  <LeftDouble />
    <h2>Available Functions</h2>
    <div class="project-item"></div>
  </div>