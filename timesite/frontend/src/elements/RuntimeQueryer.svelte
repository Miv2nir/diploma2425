<script>
    import { onMount } from 'svelte';
  import {getRequest, postRequest} from "../lib/APICalls.js";
  let {runtime_invoked=$bindable(false),
  runtime_finished=$bindable(false),proj_obj}=$props();
  let status=$state();

  async function queryStatus(){
    status=await getRequest('/api/functions/'+proj_obj.id+'/get_runtime_status/');
    console.log(status);
  }
  onMount(()=>{
      const interval=setInterval(queryStatus,1000);
      return ()=>clearInterval(interval);
  })

</script>

<div>
    <p>Running!</p>
    <br>
    {#each status as i}
        {i.func_name} -
        {#if i.status=='NE'}
        <span>Queued</span>
        {/if}
        {#if i.status=='EX'}
        <span>Executing</span>
        {/if}
        {#if i.status=='OK'}
        <span>Done</span>
        {/if}
        {#if i.status=='ER'}
        <span>Errored</span>
        <!--should query and print the error as well as hault the execution-->
        {/if}
        <br>
    {/each}
</div>