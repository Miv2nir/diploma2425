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
    let {func_name=$bindable(''),form_submitted=$bindable(false),proj_obj} = $props();
    var datastore_items = $state();
    async function getData(){
        const l = await getRequest('/api/functions/get_csv_files/');
        datastore_items=l;
        console.log(l);
    }
    getData();
    const csrftoken = Cookies.get('csrftoken');
    //const form=document.getElementById('csv_load_form');
    //console.log(form);
    async function sendForm() {
      console.log('sending form');
      await fetch(form.action, {method:'post', body: new FormData(form)});
      //discard this component for it has been used
      func_name='';
      form_submitted=true;
    }
    

</script>

<div>
<form action="/api/functions/{proj_obj.id}/accept_csv_load/" method="POST" id="csv_load_form" onsubmit={()=>sendForm()}>
    <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
    <p>
        <label for="csv_files_selection">Select CSV Dataset:</label>
        <br>
        <select name="csv_files" class="selector" id="csv_files_selection">
            {#each datastore_items as d}
            <option class="selector" value="{d.id}">{d.name}</option>
            {/each}
        </select>
        <br>
        <br>
        <button type="button" onclick={()=>sendForm()} class="login-button-primary">Save Parameters</button>
    </p>
</form>
</div>