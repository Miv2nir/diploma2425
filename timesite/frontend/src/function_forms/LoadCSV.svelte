<script>
    import { get } from "svelte/store";
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('csv_load_form');
      //console.log(form);
    })
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import { onMount } from 'svelte';
    import OrderButtons from "../elements/OrderButtons.svelte";
    import { validateForm } from "../lib/ValidateForm.js";
    let {func_obj=$bindable(),
        form_submitted=$bindable(false),
        is_author=$bindable(false),
        proj_obj,
        pipeline_length=$bindable(0)} = $props();
    //console.log(func_obj);
    var datastore_items = $state();
    var guest_mode_name=$state('');
    var save_var_name=$state('df');
    var error_msg=$state('');
    async function getData(){
        const l = await getRequest('/api/functions/get_csv_files/');
        datastore_items=l;
        //console.log(l);
    }
    getData();
    var selected_data_obj=$state();
    async function guestModeDatasetName(){
        guest_mode_name= await getRequest('/api/functions/'+func_obj.params_id+'/get_foreign_datastore_item/');
    }
    async function getParams(){
        const l = await getRequest('/api/params/'+func_obj.params_id+'/get_params/');
        selected_data_obj=l.info.data_obj;
        //console.log(l.info.data_obj);
        save_var_name=func_obj.produces;
        console.log(func_obj.order);
    }
    if (func_obj.params_id){
        //console.log('Editing!');
        getParams();
        if (!is_author){
            guestModeDatasetName();
        }
    }
    const csrftoken = Cookies.get('csrftoken');
    //const form=document.getElementById('csv_load_form');
    //console.log(form);
    async function sendForm() {
      //console.log(form['csv_files']);
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
    $inspect(func_obj).with(console.trace);
</script>

<div>
    {#if error_msg}
    <p class="error-text">{error_msg}</p>
    {/if}
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
    {/if}

<form action="/api/functions/{proj_obj.id}/accept_csv_load/" method="POST" id="csv_load_form" onsubmit={()=>sendForm()}>
    <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
    <input type="hidden" name="func_name" value="{func_obj.name}">
    {#if func_obj.params_id}
    <input type="hidden" name="update" value="true">
    {/if}
    <p>
        <label for="csv_files_selection">Select CSV Dataset:</label>
        <br>
        <select required name="csv_files" disabled={!is_author} value={selected_data_obj} class="selector" id="csv_files_selection">
            {#if is_author}
            {#each datastore_items as d}
            <option class="selector" value="{d.id}">{d.name}</option>
            {/each}
            {:else}
            <option class="selector" value="{selected_data_obj}">{guest_mode_name}</option>
            {/if}
        </select>
        <br>
        <br>
        <label for="var_name">Store DataFrame as:</label>
        <input required type="text" disabled={!is_author} class="login-input-box small" id="var_name" name="var_name" value={save_var_name}>
        <br>
        <br>
        {#if is_author}
        <button type="button" onclick={()=>sendForm()} class="login-button-primary">Set Loader</button>
        {/if}
        <br>
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}
        <br>
        {#if is_author}
        {#if func_obj.params_id}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
        {/if}
    </p>
</form>    
</div>
