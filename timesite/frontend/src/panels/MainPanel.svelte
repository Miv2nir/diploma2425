<script>
    import Left from "../elements/panel_buttons/Left.svelte";
    import Right from "../elements/panel_buttons/Right.svelte";
    import ProjectThumb from "../elements/ProjectThumb.svelte";
    import LoadCSV from "../function_forms/LoadCSV.svelte";
    import RenderDf from "../function_forms/RenderDF.svelte";
    let {user,proj_obj,func_obj=$bindable(),form_submitted=$bindable(false)} = $props();
    const special_unit_mark=true;
</script>
<div style="display:flex; flex-direction:column; justify-content: space-around; height:90.3vh;" id='container-main-spacer'>
    <div class="home-container center" id="container-main" style="margin-bottom:1rem;">
      <Left />
      <Right />
      <div class="underlying-container">
        <h1>Select a function from the left panel...</h1>
        {#if func_obj}
        <div class="project-item center"><b>{func_obj.display_name}</b></div>
        <p>{func_obj.description}</p>
        {#if func_obj.name=='LoadCSV'}
        <LoadCSV bind:func_obj={func_obj} bind:form_submitted={form_submitted} proj_obj={proj_obj}/>
        {/if}
        {#if func_obj.name=='RenderDF'}
        <RenderDf bind:func_obj={func_obj} bind:form_submitted={form_submitted} proj_obj={proj_obj}/>
        {/if}
        {/if}
      </div>
    </div>
    <ProjectThumb user={user} project={proj_obj} is_special={special_unit_mark}/>
  </div>