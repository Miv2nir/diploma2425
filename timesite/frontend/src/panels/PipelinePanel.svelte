<script>
    import { nonpassive, run, stopImmediatePropagation } from "svelte/legacy";
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {upd_flag=$bindable(false),
        func_obj=$bindable(),
        is_author=$bindable(),
        proj_obj,
        runtime_invoked=$bindable(false),
        runtime_error=$bindable({}),
        runtime_errored=$bindable(false),
        runtime_finished=$bindable(false),
        pipeline_length=$bindable(0)} = $props();
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
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
            console.log(pipeline_list[i]);
            const accepted_var = pipeline_list[i].accepts
            console.log(accepted_var);
            if (!(var_store.has(accepted_var)) && (accepted_var.length!=0)){
                warning+=('['+
                pipeline_list[i].name+
                ', pos.'+
                String(parseInt(i)+1)+
                ']: '+
                accepted_var+
                ' is not defined!<br>')
                console.log(warning);
            }
            //if mergedf or floatpointevolmodelforecast, do it again on another parameter
            if (pipeline_list[i].name==='MergeDF' || pipeline_list[i].name==='FloatPointEvolModelForecast'){
                const accepted_var_second=pipeline_list[i].accepts_second
                console.log(accepted_var_second);
                if (!(var_store.has(accepted_var_second)) && (accepted_var_second.length!=0)){
                    warning+=('['+
                    pipeline_list[i].name+
                    ', pos.'+
                    String(parseInt(i)+1)+
                    ']: '+
                    accepted_var_second+
                    ' is not defined!<br>')
                    console.log(warning);
                }
            }
            //append all created variables
            const produces = pipeline_list[i].produces;
            console.log(produces);
            var_store=var_store.add(produces);

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
                //get pipeline status
                var status=await getRequest('/api/functions/'+proj_obj.id+'/get_runtime_status/');
                for (var i in status){
                    if (status[i].status=="ER"){
                        runtime_error={
                            'func_name':status[i].func_name,
                            'error':status[i].info.error,
                            'position':parseInt(i)+1
                        }
                        console.log(status[i].info.error);
                        runtime_errored=true;
                        runtime_finished=true;
                        break;
                    }
                }
            }
        }else{
                runtime_finished=true; //sets the main panel to render results
            }
    }
    async function getLastResult(){
        //similar in behavior to that of invokeRuntime but instead it just goes for the last results
        runtime_invoked=true;
        runtime_finished=true;
    }
    async function stopExecution(){
        var stop_signal=postRequest('/api/functions/'+proj_obj.id+'/stop_runtime/',csrftoken);
        await stop_signal;
        runtime_invoked=false;
        runtime_finished=false;
        runtime_error={};
        runtime_errored=false;
    }
</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <div class="underlying-container">

    <h2>Pipeline</h2>
    {#key upd_flag}
    {#each pipeline_list as f,i }
    <div class="function-item center pointer" onclick={() =>{
            func_obj={
                'name':f.name,
                'display_name':f.display_name,
                'description':f.description,
                'params_id':f.params_id,
                'order':i,
                'accepts':f.accepts,
                'produces':f.produces
            };console.log(f.accepts);
        }}>
            
            <b class="function-item-text">{f.display_name}</b>
            <PipelineFuncVarDisplay f={f} />
        </div>
    {/each}
    {/key}
    {#if renderer_present==true}
        {#if warning}
        <p>{@html warning}</p>
        {:else}
            {#if runtime_invoked}
            <button type="button" onclick={stopExecution} class="login-button-secondary">Reset</button>
            {:else}
            {#if is_author}
            <button type="button" onclick={invokeRuntime} class="login-button-primary">Run</button>
            <br>
            <br>
            {/if}
            <button type="button" onclick={getLastResult} class="login-button-secondary">Show Last Result</button>
        {/if}
        {/if}
    {:else}
    <p>Add a renderer to run the pipeline.</p>
    {/if}
    <br>
    <br>
</div>
    </div>