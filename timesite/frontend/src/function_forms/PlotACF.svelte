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
      form=document.getElementById('renderer_form');
      //console.log(form);
    })
    var func_params=$state();
    var load_var_name=$state('df');
    var chosen_column=$state('');
    var lags=$state(40);
    async function sendForm() {
      console.log('sending form');
      await fetch(form.action, {method:'post',
       body: new FormData(form)});
      //discard this component for it has been used
      func_obj=undefined;
      form_submitted=!form_submitted;
    }
    async function getParams(){
        const l = await getRequest('/api/params/'+func_obj.params_id+'/get_params/');
        //console.log(l.info.data_obj);
        func_params=l.info.params;
        load_var_name=func_obj.accepts;
        chosen_column=func_params['chosen_column'];
        lags=parseInt(func_params['lags']);
    }
        if (func_obj.params_id){
        //console.log('Editing!');
        getParams();
      }
    async function removeFunction(){
        await postRequest('/api/params/'+func_obj.params_id+'/delete_params/',csrftoken);
        func_obj=undefined;
        form_submitted=!form_submitted;
    }
</script>
<div>
  {#if func_obj.params_id}
  {#if func_obj.accepts.length!=0}
  <p>Accepts: {func_obj.accepts}</p>
  {/if}
  {#if func_obj.produces.length!=0}
  <p>Produces: {func_obj.produces}</p>
  {/if}
  {#if is_author}
  <OrderButtons bind:func_obj={func_obj}
  bind:form_submitted={form_submitted}
  bind:pipeline_length={pipeline_length}/>
  {/if}
  <br>
  {/if}
      <form action="/api/functions/{proj_obj.id}/accept_renderer/" method="POST" id="renderer_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <input type="hidden" name="func_name" value="{func_obj.name}">
        {#if func_obj.params_id}
        <input type="hidden" name="update" value="true">
        {/if}
        <label for="var_name">Load DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="chosen_column">Name of the column of interest:</label>
        <input type='text' disabled={!is_author} name='chosen_column' value={chosen_column} class="login-input-box" >
        <br>
        <br>
        <label for="var_name">Lags:</label>
        <input type="number" disabled={!is_author} class="login-input-box smaller" name="lags" value={lags}>
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
    {/if}
</div>