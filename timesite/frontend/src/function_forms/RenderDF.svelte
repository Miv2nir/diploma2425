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
    //get order
    var load_var_name=$state('df');
    var func_params=$state();
    var order = $state(func_obj.order+1);
    var render_full_dataset = $state(false);
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
        load_var_name=func_obj.accepts;
        func_params=l.info.params;
        render_full_dataset=func_params['render_full_dataset'];
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
        <p>
        <label for="var_name">Load DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="render_full_dataset">Render Full Dataset:</label>
        <input type="checkbox" disabled={!is_author} style="transform:scale(1.5);" name="render_full_dataset" id='render_full_dataset' checked={render_full_dataset}>
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Renderer</button>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}
        {#if func_obj.params_id}
        <br>
        {#if is_author}
        <br>
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
        {/if}
      </p>
    </form>
</div>