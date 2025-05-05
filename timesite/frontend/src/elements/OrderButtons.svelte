<script>
    import {getRequest, postRequest} from "../lib/APICalls.js";
    let {func_obj=$bindable(),form_submitted=$bindable(false),
        pipeline_length=$bindable(0)
    } = $props();
    import Cookies from 'js-cookie';
    const csrftoken = Cookies.get('csrftoken');
    async function shiftDown(){
        await postRequest('/api/functions/'+func_obj.params_id+'/move_function_up/',csrftoken); //they're ordered in reverse, oops
        form_submitted=!form_submitted;
        if (func_obj.order<(pipeline_length-1)){
            func_obj.order++;
        }
    }
    async function shiftUp(){
        await postRequest('/api/functions/'+func_obj.params_id+'/move_function_down/',csrftoken); //they're ordered in reverse, oops
        form_submitted=!form_submitted;
        if (func_obj.order>0){
            func_obj.order--;
        }
    }
    console.log(pipeline_length);
</script>

<div style="display: flex; justify-content:center;">
    <img src="/backend/static/move_down_up_button.png" class="function-shift-button up" alt="Move Function Up"
    onclick={shiftUp}>
    <p style="margin-left:2rem; margin-right:2rem;">Order: {func_obj.order}</p>
    <img src="/backend/static/move_down_up_button.png" class="function-shift-button" alt="Move Function Down"
    onclick={shiftDown}>
</div>