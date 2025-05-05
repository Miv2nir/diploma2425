<script>
    let {func_obj=$bindable(),form_submitted=$bindable(false),proj_obj} = $props();
    import { onMount } from 'svelte';
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    const csrftoken = Cookies.get('csrftoken');
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('renderer_form');
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
  <p>Order: {func_obj.order}</p>
  {/if}
    <form action="/api/functions/{proj_obj.id}/accept_renderer/" method="POST" id="renderer_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Renderer</button>
    </form>
    {#if func_obj.params_id}
    <br>
    <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
    {/if}
</div>