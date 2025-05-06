<script>
    import { run } from "svelte/legacy";
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {upd_flag=$bindable(false),
        func_obj=$bindable(),
        proj_obj,
        runtime_invoked=$bindable(false),
        pipeline_length=$bindable(0)} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import {writable} from 'svelte/store';
    const csrftoken = Cookies.get('csrftoken');
    var pipeline_list=$state();
    var renderer_present=$state(false);
    //var pipeline_length=writable(0);
    //var pipeline_length=$state();
    async function getPipeline() {
        pipeline_list=await getRequest('/api/functions/'+proj_obj.id+'/get_pipeline/');
        //console.log(pipeline_list);
        //console.log(pipeline_list);
        //pipeline_length.set(pipeline_list.length);
        pipeline_length=pipeline_list.length;
        for (var i in pipeline_list){
            if (pipeline_list[i].type=='renderer'){
                //console.log(pipeline_list[i].type);
                renderer_present=true;
                break;
            }
        }
        //console.log(renderer_present);
    }
    getPipeline();
    async function invokeRuntime(){
        //the runtime order should already be on the server side at this point
        //shouldn't be awaited actually
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
        'order':i,
        'accepts':f.accepts,
        'produces':f.produces
        }}}><b>{f.display_name}</b>

        </div>
    {/each}
    {/key}
    {#if renderer_present==true}
    {#if runtime_invoked}
    <button type="button" onclick={()=>{runtime_invoked=false;}} class="login-button-secondary">Reset</button>
    {:else}
    <button type="button" onclick={invokeRuntime} class="login-button-primary">Run</button>
    {/if}
    {:else}
    <p>Add a renderer to run the pipeline.</p>
    {/if}
    </div>