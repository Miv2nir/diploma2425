<script>
    import { run } from "svelte/legacy";
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {upd_flag=$bindable(false),
        func_obj=$bindable(),
        proj_obj,
        runtime_invoked=$bindable(false),
        runtime_finished=$bindable(false),
        pipeline_length=$bindable(0)} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import {writable} from 'svelte/store';
    import PipelineFuncVarDisplay from "../elements/PipelineFuncVarDisplay.svelte";
    const csrftoken = Cookies.get('csrftoken');
    var pipeline_list=$state();
    var renderer_present=$state(false);
    var warning=$state('');
    //var pipeline_length=writable(0);
    //var pipeline_length=$state();
    function validatePipeline(){ //called from getPipeline btw
        //this function goes over the constructed pipeline, checking the variable names
        //if some function accepts the wrong variable (like if it doesn't exist)
        //block the run function

        //for the time being, this will only check for the presence of requested values
        var var_store=new Set();
        console.log('validating');
        console.log(pipeline_list);
        for (var i in pipeline_list){
            console.log(var_store);
            //verify if consumed variables exist
            for (var j in pipeline_list[i].accepts){
                const accepted_var = pipeline_list[i].accepts[j]
                if (!(var_store.has(accepted_var))){
                    warning+=('['+
                    pipeline_list[i].name+
                    ', pos.'+
                    String(i)+
                    ']: '+
                    accepted_var+
                    ' is not defined!<br>')
                    console.log(warning);
                }
            }
            //append all created variables
            const produces = new Set(pipeline_list[i].produces);
            var_store=var_store.union(produces);
        }
    }
    async function getPipeline() { //gets called upon pipeline update essentially
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
        validatePipeline();
    }
    getPipeline();

    async function invokeRuntime(){
        //the runtime order should already be on the server side at this point
        //shouldn't be awaited actually
        //await postRequest('/api/functions/'+proj_obj.id+'/execute/',csrftoken);
        var runtime_promise=postRequest('/api/functions/'+proj_obj.id+'/execute/',csrftoken);
        runtime_invoked=true; //sets the main panel to render the waiting parts
        const runtime_result= await runtime_promise;
        if (runtime_result instanceof Error){
            console.log(runtime_result.message);
            if(runtime_result.message.search('500') != -1){
                //500 error on this api endpoint should indicate runtime failure
                //the cause is logged in function statuses
                console.log('handling 500');
            }
        }
        runtime_finished=true; //sets the main panel to render results
    }
    async function getLastResult(){
        //similar in behavior to that of invokeRuntime but instead it just goes for the last results
        runtime_invoked=true;
        runtime_finished=true;
    }
</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <div class="underlying-container">

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
        };console.log(f.accepts);}}>
        <div>
            
            <b>{f.display_name}</b>
            <PipelineFuncVarDisplay f={f} />
        </div>
        </div>
    {/each}
    {/key}
    {#if renderer_present==true}
        {#if warning}
        <p>{@html warning}</p>
        {:else}
            {#if runtime_invoked}
            <button type="button" onclick={()=>{runtime_invoked=false; runtime_finished=false;}} class="login-button-secondary">Reset</button>
            {:else}
            <button type="button" onclick={invokeRuntime} class="login-button-primary">Run</button>
            <br>
            <br>
            <button type="button" onclick={getLastResult} class="login-button-secondary">Show Last Result</button>
        {/if}
        {/if}
    {:else}
    <p>Add a renderer to run the pipeline.</p>
    {/if}
</div>
    </div>