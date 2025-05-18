<script>
    import { onMount } from "svelte";
import {getRequest, postRequest} from "../lib/APICalls.js";
//upon invoking this component, request runtime results from the database
let {
    runtime_invoked=$bindable(false),
    proj_obj
    } = $props();
    var selected_render=$state('');
    var render=$state([]);
    var tabs=$state([]);
    var request;
    async function queryResults() {
        request=await getRequest('/api/functions/'+proj_obj.id+'/get_results/');
        //the above code will wait for the end of the query process
        //also it doesn't represent the actual end of the execution!!!!!
        //for now check if there is at least one renderer who has finished
        //console.log(request);
        if (request){
            for (var i in request){
                console.log(request[i]);
                render.push({
                    'name':request[i].name,
                    'output':request[i].resulting_html,
                    'order':i
                });
                //tabs.push('<div class="tab" id="'+request[i].name+'_'+String(i)+'">\
                //    '+request[i].name+'@'+String(i)+'</div>');
                tabs.push({
                    'div_id':request[i].name+'_'+String(i),
                    'text':request[i].name+' @ '+String(parseInt(i)+1),
                    'target':i
                });
            }
        }
        //set selection on the first item in tabs
        selected_render=tabs[0].target;
        //document.getElementById(tabs[0].div_id).classList.add('pressed');
        //if (request) {
        //    //not empty
        //    render=request;
        //}
        //it's gonna be over only when all the representative functions report on their completion
        //check whether it got the results back, if not, wait 1 second and query again
        //if the result is obtained, update render state and hault
    }
    async function doStuff(){
        //idk fsr i cant seem to work with tabs if i dont do it
        //or mb im just dumb
        //probably the latter lmao
        await queryResults();
        console.log(tabs);
    }
    onMount(()=>{
        doStuff();
    })

    //tabs thingy
    /*const onload=el=>{
        console.log('hi');
        //consdocument.getElementById('separator');
        if (el.offsetWidth<el.scrollWidth){
            document.getElementById('separator').style.display='none';
        }
        else{
            document.getElementById('separator').style.display='block';
        }
    }*/

</script>

<div>
    {#if !render}
<p>Running!</p>
{:else}
<p>Execution has finished!</p>
<br>
<div class="tab-array" id="tab_array">
    {#each tabs as item}
    <div class={{'tab pressed':(item.target==selected_render),'tab':(item.target!=selected_render)}} id={item.div_id} onclick={()=>{
        selected_render=item.target;
        console.log(selected_render);
        //logic for handling the pressed button visuals
        /*for (var i in tabs){
            if (tabs[i]==item){
                document.getElementById(tabs[i].div_id).classList.add('pressed');
            }
            else{
                document.getElementById(tabs[i].div_id).classList.remove('pressed');
            }
        }*/
    }}>{item.text}</div>
    {/each}
    <div class="hr" id="separator" style="position:absolute;bottom:0; width:100%;"></div>
</div>
{#each render as i}
    {#if i.order==selected_render}
        
    <div style="display:flex;justify-content:center;flex-direction:column;align-items:center;">
        {#if i.name==='DownloadDF'}
        <div>
            <p>Your file is ready to download!</p>
            <a href="/{i.output}"><button type="button" class="login-button-primary">Download file</button></a>
        </div>
        {:else if i.name==='RenderDF'}
        <div style="max-width:100%;">
            {@html i.output}
        </div>
        {:else}
        <div>
            {@html i.output}
        </div>
        {/if}
    </div>
    {/if}
{/each}
{/if}
</div>