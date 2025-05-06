<script>
    let {func_obj=$bindable(),form_submitted=$bindable(false),proj_obj,pipeline_length=$bindable(0)} = $props();
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
    //get order
    var order = $state(func_obj.order+1);
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
    console.log(func_obj);
</script>

<div>
  {#if func_obj.params_id}
  {#if func_obj.accepts.length!=0}
  <p>Accepts: {func_obj.accepts}</p>
  {/if}
  {#if func_obj.produces.length!=0}
  <p>Produces: {func_obj.produces}</p>
  {/if}
  <OrderButtons bind:func_obj={func_obj}
  bind:form_submitted={form_submitted}
  bind:pipeline_length={pipeline_length}/>
  <br>
  {/if}
    <form action="/api/functions/{proj_obj.id}/accept_processor/" method="POST" id="processor_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <label for="csv_files_selection">Define column names, separated by comma:</label>
        <br>
        <input type="text" name="columns" class="login-input-box" id="text_columns_definitions">
        <br>
        <br>
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Renderer</button>
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}

    </form>
    {#if func_obj.params_id}
    <br>
    <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
    {/if}
</div>