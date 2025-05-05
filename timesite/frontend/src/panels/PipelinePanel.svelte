<script>
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {upd_flag=$bindable(false),
        func_obj=$bindable(),
        proj_obj,
        runtime_invoked=$bindable(false)} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    const csrftoken = Cookies.get('csrftoken');
    var pipeline_list=$state();
    async function getPipeline() {
        pipeline_list=await getRequest('/api/functions/'+proj_obj.id+'/get_pipeline/');
    }
    getPipeline();
    async function invokeRuntime(){
        //the runtime order should already be on the server side at this point
        await postRequest('/api/functions/'+proj_obj.id+'/execute/',csrftoken);
        runtime_invoked=true;
    }
</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <h2>Pipeline</h2>
    {#key upd_flag}
    {#each pipeline_list as f,i }
    <div class="project-item center pointer" onclick={() =>{func_obj={
        'name':f.name,
        'display_name':f.display_name,
        'description':f.description,
        'params_id':f.params_id,
        'order':i
        }}}><b>{f.display_name}</b></div>
    {/each}
    {/key}
    {#if pipeline_list != {}}
    <button type="button" onclick={invokeRuntime} class="login-button-primary">Run</button>
    {/if}
    </div>