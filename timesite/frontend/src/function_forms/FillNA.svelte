<script>
    let {func_obj=$bindable(),
      form_submitted=$bindable(false),
      is_author=$bindable(false),
      proj_obj,
      pipeline_length=$bindable(0)} = $props();
    import { onMount } from 'svelte';
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import OrderButtons from "../elements/OrderButtons.svelte";
    const csrftoken = Cookies.get('csrftoken');
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('processor_form');
      //console.log(form);
    })
    var func_params=$state();
    var mode_selection=$state('');
    var value_number=$state(0.0);
    //var is_value=$state()
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
        mode_selection=func_params['fill_mode'];
        if (mode_selection=='value'){
            value_number=parseFloat(func_params['value']);
        }
    }
    if (func_obj.params_id){
        //console.log('Editing!');
        getParams();
    }
    console.log(func_obj);
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
        <form action="/api/functions/{proj_obj.id}/accept_processor/" method="POST" id="processor_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <input type="hidden" name="func_name" value="{func_obj.name}">
        {#if func_obj.params_id}
        <input type="hidden" name="update" value="true">
        {/if}
        <label for="fill_mode">Select fill mode:</label>
        <br>
        <select name="fill_mode" class="selector" bind:value={mode_selection} disabled={!is_author}>
            <option class='selector' value='average'>Average Fill (based on column values)</option>
            <option class='selector' value='value'>Fill with set value</option>
            <option class='selector' value='ffill'>Propagate valid values forward</option>
            <option class='selector' value='bfill'>Propagate valid values backward</option>
        </select>
        {#if mode_selection=='value'}
        <br>
        <br>
        <label for='value_definition'>Define the value to set in the NaN fields:</label>
        <input type='number' name='fill_value' value={value_number} class="login-input-box" step='0.001' id='value_definition'>
        {/if}
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Renderer</button>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}

    </form>
    {#if func_obj.params_id}
    <br>
    {#if is_author}
    <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
    {/if}
    <br>
    <br>
    {/if}
</div>