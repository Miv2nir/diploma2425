<script>
    let {func_obj=$bindable(),
    form_submitted=$bindable(false),
    proj_obj,
    is_author=$bindable(false),
    pipeline_length=$bindable(0)} = $props();
    import { onMount } from 'svelte';
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import OrderButtons from "../elements/OrderButtons.svelte";
    const csrftoken = Cookies.get('csrftoken');
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('model_form');
      //console.log(form);
    })
    var func_params=$state();
    var load_var_name=$state('am');
    var save_var_name=$state('df');
    var horizon=$state(1);
    var forecast_type=$state('mean');
 async function sendForm() {
      console.log('sending form');
      await fetch(form.action, {method:'post',
       body: new FormData(form)});
      //discard this component for it has been used
      func_obj=undefined;
      form_submitted=!form_submitted;
    }
    async function removeFunction(){
        await postRequest('/api/params/'+func_obj.params_id+'/delete_params/',csrftoken);
        func_obj=undefined;
        form_submitted=!form_submitted;
    }
    async function getParams(){
        const l = await getRequest('/api/params/'+func_obj.params_id+'/get_params/');
        console.log(l.info.params);
        func_params=l.info.params;
        horizon=parseInt(func_params['horizon']);
        forecast_type=func_params['forecast_type'];

        save_var_name=func_obj.produces;
        load_var_name=func_obj.accepts;
    }
    if (func_obj.params_id){
        //console.log('Editing!');
        getParams();
    }
</script>

<div>
    {#if func_obj.params_id}
    <p>
        {#if func_obj.accepts.length!=0}
        <span>Accepts: {func_obj.accepts}</span>
        {/if}
        {#if func_obj.produces.length!=0}
        {#if func_obj.accepts.length!=0}
        <span>;</span>
        {/if}
        <span>Produces: {func_obj.produces}</span>
        {/if}
    </p>
    {#if is_author}
    <OrderButtons bind:func_obj={func_obj}
    bind:form_submitted={form_submitted}
    bind:pipeline_length={pipeline_length}/>
    {/if}
    <br>
    {/if}
    <form action="/api/functions/{proj_obj.id}/accept_model/" method="POST" id="model_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <input type="hidden" name="func_name" value="{func_obj.name}">
        {#if func_obj.params_id}
        <input type="hidden" name="update" value="true">
        {/if}    
        <p>
        <label for="var_name">Load model from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="load_var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="horizon">Horizon:</label>
        <input type="number" disabled={!is_author} class="login-input-box smaller" name="horizon" value={horizon}>
        <br>
        <br>
        <label for="forecast_type">Forecast Type:</label>
        <br>
        <select name='forecast_type' id="forecast_type" disabled={!is_author} value={forecast_type} class="selector">
            <option class="selector" value="mean">mean</option>
            <option class="selector" value="residual_variance">residual_variance</option>
            <option class="selector" value="variance">variance</option>
        </select>
        <br>
        <br>
        <label for="var_name">Store resulting DataFrame as:</label>
        <input type="text" disabled={!is_author}  class="login-input-box small" name="save_var_name" value={save_var_name}>
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Model</button>
        <br>
        <br>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}
        {#if is_author}
        {#if func_obj.params_id}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        <br>
        <br>
        {/if}
        {/if}
        </p>
    </form>
</div>