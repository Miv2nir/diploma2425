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
    import { validateForm } from "../lib/ValidateForm.js";
    const csrftoken = Cookies.get('csrftoken');
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('model_form');
      //console.log(form);
    })
    //get order
    var func_params=$state();
    var load_var_name=$state('df');
    var save_var_name=$state('modelsparams');
    //var dist=$state('Normal');
    var chosen_column=$state('');
    var p=$state(1);
    var q=$state(1);
    var jump_threshold=$state(3);
    var error_msg=$state('');
 async function sendForm() {
      var values_missing=validateForm(form);
      if (values_missing){
        error_msg='Please fill all of the missing values!';
        return false;
      }
      else{
        error_msg='';
      }
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
        chosen_column=func_params['chosen_column'];
        p=parseInt(func_params['p']);
        q=parseInt(func_params['q']);
        jump_threshold=func_params['jump_threshold'];

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
        <label for="load_var_name">Load DataFrame from:</label>
        <input required type="text" disabled={!is_author} class="login-input-box small" id="load_var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="tenor_definition">Write the tenor name (column name):</label>
        <br>
        <input required type="text" disabled={!is_author} name="chosen_column" value={chosen_column} class="login-input-box" id="tenor_definition">
        <br>
        <br>
        <label for="p">p:</label>
        <input required type="text" disabled={!is_author} class="login-input-box smaller" name="p" id="p" value={p}>
        <label for="q" style="margin-left:1rem;">q:</label>
        <input required type="text" disabled={!is_author} class="login-input-box smaller" name="q" id="q" value={q}>
        <br>
        <br>
        <label for="jump_threshold">Jump Threshold:</label>
        <input required type="text" disabled={!is_author} class="login-input-box smaller" name="jump_threshold" id="jump_threshold" value={jump_threshold}>
        <br>
        <br>
        <label for="save_var_name">Store parameters as:</label>
        <input required type="text" disabled={!is_author}  class="login-input-box small" id="save_var_name" name="save_var_name" value={save_var_name}>
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Model</button>
        <br>
        <br>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {#if is_author}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
        <br>
        <br>
        {/if}
        </p>
    </form>

</div>