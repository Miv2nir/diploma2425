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
    //var is_value=$state()
    var numeric_only=$state(false);
    var save_var_name=$state('df_new');
    var load_var_name=$state('df');
    var second_df=$state('df2');
    var how=$state('inner');
    var left_on=$state('');
    var right_on=$state('');
    var left_index=$state(false);
    var right_index=$state(false);

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
        second_df=func_params['second_df'];
        how=func_params['how'];
        left_on=func_params['left_on'];
        right_on=func_params['right_on'];
        left_index=func_params['left_index'];
        right_index=func_params['right_index'];
        save_var_name=func_obj.produces;
        load_var_name=func_obj.accepts;
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
        <label for="load_var_name">Load DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="second_df">Load Second DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" name="second_df" value={second_df}>
        <br>
        <br>
        <label for="how">How:</label>
        <br>
        <select name='how' id="how" disabled={!is_author} value={how} class="selector">
            <option class="selector" value="inner">inner</option>
            <option class="selector" value="left">left</option>
            <option class="selector" value="right">right</option>
            <option class="selector" value="outer">outer</option>
            <option class="selector" value="inner">inner</option>
            <option class="selector" value="cross">cross</option>
        </select>
        <br>
        <br>
        <label for="left_on">Left On:</label>
        <input type="text" disabled={!is_author} class="login-input-box small"name="left_on" value={left_on}>
        <br>
        <br>
        <label for="right_on">Right On:</label>
        <input type="text" disabled={!is_author} class="login-input-box small"name="right_on" value={right_on}>
        <br>
        <br>
        <label for="left_index">Left Index:</label>
        <input type="checkbox" disabled={!is_author} style="transform:scale(1.5);" name="left_index" checked={left_index}>
        <br>
        <br>
        <label for="right_index">Right Index:</label>
        <input type="checkbox" disabled={!is_author} style="transform:scale(1.5);" name="right_index" checked={right_index}>
        <br>
        <br>
        <label for="var_name">Store changes as:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="save_var_name" value={save_var_name}>
        {#if is_author}
        <br>
        <br>
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