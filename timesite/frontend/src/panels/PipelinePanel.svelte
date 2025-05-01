<script>
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {user,proj_obj} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    var pipeline_list=$state();
    async function getPipeline() {
        pipeline_list=await getRequest('/api/functions/'+proj_obj.id+'/get_pipeline/');
        console.log(pipeline_list);        
    }
    getPipeline();
</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <h2>Pipeline</h2>
    {#each pipeline_list as f }
    <div class="project-item center pointer"><b>{f.display_name}</b></div>
    {/each}
    </div>