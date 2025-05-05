<script>
    import {getRequest, postRequest} from "../lib/APICalls.js";
    let {func_obj=$bindable(),form_submitted=$bindable(false),
        pipeline_length=$bindable(0)
    } = $props();
    import Cookies from 'js-cookie';
    let up_visible=$state(true);
    let down_visible=$state(true);
    const csrftoken = Cookies.get('csrftoken');
    function refreshVisibility(){
        if (func_obj.order<=0){
            up_visible=false;
            down_visible=true;
        }
        else if (func_obj.order>0 && func_obj.order<(pipeline_length-1)){
            up_visible=true;
            down_visible=true;
        }
        else {
            up_visible=true;
            down_visible=false;
        }
    }
    refreshVisibility(); //invoke on load
    async function shiftUp(){
        await postRequest('/api/functions/'+func_obj.params_id+'/move_function_down/',csrftoken); //they're ordered in reverse, oops
        form_submitted=!form_submitted;
        if (func_obj.order>0){
            func_obj.order--;
            up_visible=true;
        }
        refreshVisibility();
    }
    async function shiftDown(){
        await postRequest('/api/functions/'+func_obj.params_id+'/move_function_up/',csrftoken); //they're ordered in reverse, oops
        form_submitted=!form_submitted;
        if (func_obj.order<(pipeline_length-1)){
            func_obj.order++;
            down_visible=true;
        }
        refreshVisibility();
    }
    console.log(pipeline_length);
</script>

<div style="display: flex; justify-content:center;">
    {#if up_visible}
    <img src="/backend/static/move_down_up_button.png" class="function-shift-button up" alt="Move Function Up"
    onclick={shiftUp}>
    {:else}
    <div style="width:3rem;"></div>
    {/if}
    <p style="margin-left:2rem; margin-right:2rem;">Order: {func_obj.order}</p>
    {#if down_visible}
    <img src="/backend/static/move_down_up_button.png" class="function-shift-button" alt="Move Function Down"
    onclick={shiftDown}>
    {:else}
    <div style="width:3rem;"></div>
    {/if}
</div>