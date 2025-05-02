<script>
    import { get } from "svelte/store";
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('csv_load_form');
      console.log(form);
    })
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import { onMount } from 'svelte';
    let {func_obj=$bindable(),form_submitted=$bindable(false),proj_obj} = $props();
    console.log(func_obj);
    var datastore_items = $state();
    async function getData(){
        const l = await getRequest('/api/functions/get_csv_files/');
        datastore_items=l;
        console.log(l);
    }
    getData();
    var selected_data_obj=$state();
    async function getParams(){
        const l = await getRequest('/api/params/'+func_obj.params_id+'/get_params/');
        selected_data_obj=l.info.data_obj;
        console.log(l.info.data_obj);
    }
    if (func_obj.params_id){
        console.log('Editing!');
        getParams();
    }
    const csrftoken = Cookies.get('csrftoken');
    //const form=document.getElementById('csv_load_form');
    //console.log(form);
    async function sendForm() {
      console.log('sending form');
      await fetch(form.action, {method:'post',
       body: new FormData(form)});
      //discard this component for it has been used
      func_obj=undefined;
      form_submitted=true;
    }
    async function removeFunction(){
        await postRequest('/api/params/'+func_obj.params_id+'/delete_params/',csrftoken);
        func_obj=undefined;
        form_submitted=true;
    }
    

</script>

<div>
<form action="/api/functions/{proj_obj.id}/accept_csv_load/" method="POST" id="csv_load_form" onsubmit={()=>sendForm()}>
    <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
    {#if selected_data_obj}
    <input type="hidden" name="update" value="true">
    {/if}
    <p>
        <label for="csv_files_selection">Select CSV Dataset:</label>
        <br>
        <select name="csv_files" value={selected_data_obj} class="selector" id="csv_files_selection">
            {#each datastore_items as d}
            <option class="selector" value="{d.id}">{d.name}</option>
            {/each}
        </select>
        <br>
        <br>
        <button type="button" onclick={()=>sendForm()} class="login-button-primary">Save Parameters</button>
        <br>
        <br>
        {#if selected_data_obj}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
    </p>
</form>
</div>