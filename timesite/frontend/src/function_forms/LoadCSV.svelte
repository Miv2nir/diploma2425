<script>
    import { get } from "svelte/store";
    import {getRequest, postRequest} from "../lib/APICalls.js";
    var datastore_items = $state();
    async function getData(){
        const l = await getRequest('/api/functions/get_csv_files/');
        datastore_items=l;
        console.log(l);
    }
    getData();
</script>

<div>
<form action="/api/functions/set_dataset/" onsubmit={()=>{return false}}>
    <p>
        <label for="csv_files_selection">Select CSV Dataset:</label>
        <br>
        <select name="csv files" class="selector" id="csv_files_selection">
            {#each datastore_items as d}
            <option class="selector">{d.name}</option>
            {/each}
        </select>
        <br>
        <br>
        <button type="submit" class="login-button-primary">Set Parameters</button>
    </p>
</form>
</div>