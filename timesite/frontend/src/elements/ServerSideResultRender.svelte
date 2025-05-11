<script>
    import { onMount } from "svelte";
import {getRequest, postRequest} from "../lib/APICalls.js";
//upon invoking this component, request runtime results from the database
let {
    runtime_invoked=$bindable(false),
    proj_obj
    } = $props();
    var render=$state([]);
    var tabs=$state([]);
    var request;
    async function queryResults() {
        request=await getRequest('/api/functions/'+proj_obj.id+'/get_results/');
        //the above code will wait for the end of the query process
        //also it doesn't represent the actual end of the execution!!!!!
        //for now check if there is at least one renderer who has finished
        console.log(request);
        if (request){
            for (var i in request){
                console.log(request[i].resulting_html);
                render.push(request[i].resulting_html);
                tabs.push('<div class="tab" id="'+request[i].name+'_'+String(i)+'">\
                    '+request[i].name+'@'+String(i)+'</div>');
            }
        }
        //if (request) {
        //    //not empty
        //    render=request;
        //}
        //it's gonna be over only when all the representative functions report on their completion
        //check whether it got the results back, if not, wait 1 second and query again
        //if the result is obtained, update render state and hault
    }
    onMount(()=>{
        queryResults();
    });

</script>

<div>
    {#if !render}
<p>Running!</p>
{:else}
<p>Execution has finished!</p>
<br>
<div class="tab-array">
    {#each tabs as item}
        {@html item}
    {/each}

</div>
<div class="hr"></div>
{#each render as i}
    <div style="display:flex;justify-content:center;flex-direction:column;align-items:center;">
        <div>
            {@html i}
        </div>
    </div>
{/each}
{/if}
</div>