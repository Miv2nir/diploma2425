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
    var save_var_name=$state('df');
    var load_var_name=$state('df');
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
        //console.log(l.info.params);
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
    <form action="/api/functions/{proj_obj.id}/accept_processor/" method="POST" id="processor_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <input type="hidden" name="func_name" value="{func_obj.name}">
        {#if func_obj.params_id}
        <input type="hidden" name="update" value="true">
        {/if}
        <p>
        <label for="var_name">Load DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="var_name">Store changes as:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="save_var_name" value={save_var_name}>
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Processor</button>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}
        {#if func_obj.params_id}
        <br>
        <br>
        {#if is_author}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
        {/if}
      </p>
    </form>
</div>