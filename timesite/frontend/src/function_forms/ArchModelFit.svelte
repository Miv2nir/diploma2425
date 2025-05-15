<script>
    let {func_obj=$bindable(),
    form_submitted=$bindable(false),
    proj_obj,
    is_author=$bindable(false),
    pipeline_length=$bindable(0)} = $props();
    import { onMount } from 'svelte';
    import {getRequest, postRequest} from "../lib/APICalls.js";
    import Cookies from 'js-cookie';
    import OrderButtons from "../elements/OrderButtons.svelte";
    import { parse } from 'svelte/compiler';
    const csrftoken = Cookies.get('csrftoken');
    var form=undefined;
    onMount(()=>{
      form=document.getElementById('model_form');
      //console.log(form);
    })
    var func_params=$state();
    var load_var_name=$state('df');
    var save_var_name=$state('am');
    var chosen_column=$state('');
    var mean=$state('Constant');
    var lags=$state(0);
    var vol=$state('GARCH');
    var p=$state(1);
    var o=$state(0);
    var q=$state(1);
    var power=$state(2.0);
    var dist=$state('normal');
    var rescale=$state(false);
 async function sendForm() {
      console.log('sending form');
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
    async function getParams(){
        const l = await getRequest('/api/params/'+func_obj.params_id+'/get_params/');
        console.log(l.info.params);
        func_params=l.info.params;
        chosen_column=func_params['chosen_column'];
        mean=func_params['mean'];
        lags=parseInt(func_params['lags']);
        vol=func_params['GARCH'];
        p=parseInt(func_params['p']);
        o=parseInt(func_params['o']);
        q=parseInt(func_params['q']);
        power=parseFloat(func_params['power']);
        rescale=func_params['rescale'];

        save_var_name=func_obj.produces;
        load_var_name=func_obj.accepts;
    }
    if (func_obj.params_id){
        //console.log('Editing!');
        getParams();
    }
</script>

<div>
    {#if func_obj.params_id}
    <p>
        {#if func_obj.accepts.length!=0}
        <span>Accepts: {func_obj.accepts}</span>
        {/if}
        {#if func_obj.produces.length!=0}
        {#if func_obj.accepts.length!=0}
        <span>;</span>
        {/if}
        <span>Produces: {func_obj.produces}</span>
        {/if}
    </p>
    {#if is_author}
    <OrderButtons bind:func_obj={func_obj}
    bind:form_submitted={form_submitted}
    bind:pipeline_length={pipeline_length}/>
    {/if}
    <br>
    {/if}
    <form action="/api/functions/{proj_obj.id}/accept_model/" method="POST" id="model_form" onsubmit={()=>sendForm()}>
        <input type="hidden" name="csrfmiddlewaretoken" value="{csrftoken}">
        <input type="hidden" name="func_name" value="{func_obj.name}">
        {#if func_obj.params_id}
        <input type="hidden" name="update" value="true">
        {/if}    
        <label for="var_name">Load DataFrame from:</label>
        <input type="text" disabled={!is_author} class="login-input-box small" id="load_var_name" name="load_var_name" value={load_var_name}>
        <br>
        <br>
        <label for="text_columns_definitions">Write the tenor name (column name):</label>
        <br>
        <input type="text" disabled={!is_author} name="chosen_column" value={chosen_column} class="login-input-box" id="tenor_definition">
        <br>
        <br>
        <label for="mean">Mean:</label>
        <br>
        <select name='mean' id="mean" disabled={!is_author} value={mean} class="selector">
            <option class="selector" value="Constant">Constant</option>
            <option class="selector" value="Zero">Zero</option>
            <option class="selector" value="LS">LS</option>
            <option class="selector" value="AR">AR</option>
            <option class="selector" value="ARX">ARX</option>
            <option class="selector" value="HAR">HAR</option>
            <option class="selector" value="HARX">HARX</option>
        </select>
        <br>
        <br>
        <label for="vol">Volatility:</label>
        <br>
        <select name='vol' id="vol" disabled={!is_author} value={vol} class="selector">
            <option class="selector" value="GARCH">GARCH</option>
            <option class="selector" value="ARCH">ARCH</option>
            <option class="selector" value="EGARCH">EGARCH</option>
            <option class="selector" value="FIGARCH">FIGARCH</option>
            <option class="selector" value="APGARCH">APGARCH</option>
            <option class="selector" value="HARCH">HARCH</option>
        </select>
        <br>
        <br>
        <label for="var_name">p:</label>
        <input type="text" disabled={!is_author} class="login-input-box smaller" name="p" value={p}>
        <label for="var_name" style="margin-left:1rem;">o:</label>
        <input type="text" disabled={!is_author} class="login-input-box smaller" name="o" value={o}>
        <label for="var_name" style="margin-left:1rem;">q:</label>
        <input type="text" disabled={!is_author} class="login-input-box smaller" name="q" value={q}>
        <label for="var_name" style="margin-left:1rem;">Power:</label>
        <input type="text" disabled={!is_author} class="login-input-box smaller" name="power" value={power}>
        
        <br>
        <br>
        <label for="dist">Distribution:</label>
        <br>
        <select name='dist' id="dist" disabled={!is_author} value={dist} class="selector">
            <option class="selector" value="normal">normal</option>
            <option class="selector" value="gaussian">gaussian</option>
            <option class="selector" value="t">t</option>
            <option class="selector" value="studentst">studentst</option>
            <option class="selector" value="skewstudent">skewstudent</option>
            <option class="selector" value="skewt">skewt</option>
            <option class="selector" value="ged">ged</option>
            <option class="selector" value="generalized error">generalized error</option>
        </select>
        <br>
        <br>
        <label for="index_toggle">Rescale:</label>
        <input type="checkbox" disabled={!is_author} style="transform:scale(1.5);" name="rescale" checked={rescale}>
        <br>
        <br>
        <label for="var_name">Store result model as:</label>
        <input type="text" disabled={!is_author}  class="login-input-box small" name="save_var_name" value={save_var_name}>
        <br>
        <br>
        {#if is_author}
        <button type="button" class="login-button-primary" onclick={()=>sendForm()}>Set Model</button>
        <br>
        <br>
        {/if}
        {#if func_obj.params_id}
        <input type="hidden" name="order" value={func_obj.order}>
        {/if}
        {#if is_author}
        {#if func_obj.params_id}
        <button type="button" onclick={()=>removeFunction()} class="login-button-delete">Remove Function</button>
        {/if}
        {/if}
    </form>
</div>