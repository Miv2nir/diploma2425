<script>
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {upd_flag=$bindable(false),user,proj_obj} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    var pipeline_list=$state();
    async function getPipeline() {
        pipeline_list=await getRequest('/api/functions/'+proj_obj.id+'/get_pipeline/');
    }
    getPipeline();
    
</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <h2>Pipeline</h2>
    {#key upd_flag}
    {#each pipeline_list as f }
    <div class="project-item center pointer"><b>{f.display_name}</b></div>
    {/each}
    {/key}
    </div>