<script>
    import { get } from "svelte/store";
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    var datastore_items = $state();
    async function getData(){
        const l = await getRequest('/api/functions/get_csv_files/');
        datastore_items=l;
        console.log(l);
    }
    getData();
    const csrftoken = Cookies.get('csrftoken');
</script>

<div>
<form action="/api/functions/accept_csv_load/" method="POST" onsubmit={()=>{return false}}>
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
        <button type="submit" class="login-button-primary">Save Parameters</button>
    </p>
</form>
</div>