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
    var save_var_name=$state('df_res');
     var modelsparams=$state('modelsparams');
    //var dist=$state('Normal');
    var chosen_column=$state('');
    var n_simulations=$state(10);
    var n_steps=$state(100);
    var dt=$state(250);
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
        modelsparams=func_params['modelsparams'];
        n_simulations=parseInt(func_params['n_simulations']);
        n_steps=parseInt(func_params['n_steps']);
        dt=parseInt(func_params['dt']);

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
        <label for="second_df">Load model parameters from:</label>
        <input required type="text" disabled={!is_author} class="login-input-box small" name="modelsparams" id="second_df" value={modelsparams}>
        <br>
        <br>
        <label for="tenor_definition">Write the tenor name (column name) for estimation:</label>
        <br>
        <input required type="text" disabled={!is_author} name="chosen_column" value={chosen_column} class="login-input-box" id="tenor_definition">
        <br>
        <br>
        <label for="n_simulations">n_simulatins:</label>
        <input required type="number" disabled={!is_author} class="login-input-box smaller" name="n_simulations" id="n_simulations" value={n_simulations}>
        <label for="n_steps" style="margin-left:1rem;">n_steps:</label>
        <input required type="number" disabled={!is_author} class="login-input-box smaller" name="n_steps" id="n_steps" value={n_steps}>
        <br>
        <br>
        <label for="dt">dt:</label>
        <input required type="number" disabled={!is_author} class="login-input-box smaller" name="dt" id="dt" value={dt}>
        <br>
        <br>
        <label for="save_var_name">Store result as:</label>
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
        {/if}
        </p>
    </form>
</div>