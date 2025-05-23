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
    var x=$state('');
    var y=$state('');
    var x_label=$state('');
    var y_label=$state('');
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
        x=func_params['x'];
        y=func_params['y'];
        x_label=func_params['x_label'];
        y_label=func_params['y_label'];
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
        <label for="x">Name the column for the x axis (leave empty for index):</label>
        <input type='text' disabled={!is_author} name='x' value={x} class="login-input-box" >
        <br>
        <br>
        <label for="y">Name the columns for the y axis (separated by comma):</label>
        <input type='text' disabled={!is_author} name='y' value={y} class="login-input-box" >
        <br>
        <br>
        <label for="x_label">Set label for the x axis:</label>
                <br>
        <input type='text' disabled={!is_author} name='x_label' value={x_label} class="login-input-box" >
        <br>
        <br>
        <label for="y">Set label for the y axis:</label>
                <br>
        <input type='text' disabled={!is_author} name='y_label' value={y_label} class="login-input-box" >
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