<script>
    import Left from "../elements/panel_buttons/Left.svelte";
    import Right from "../elements/panel_buttons/Right.svelte";
    import ProjectThumb from "../elements/ProjectThumb.svelte";
    import LoadCsv from "../function_forms/LoadCSV.svelte";
    let {user,proj_obj,func_name,form_submitted=$bindable(false)} = $props();
    const special_unit_mark=true;
</script>
<div style="display:flex; flex-direction:column; justify-content: space-around; height:90.3vh;" id='container-main-spacer'>
    <div class="home-container center" id="container-main" style="margin-bottom:1rem;">
      <Left />
      <Right />
      <div class="underlying-container">
        <h1>Select a function from the left panel...</h1>
        {#if func_name}
        <div class="project-item center"><b>{func_name}</b></div>
        {/if}
        {#if func_name=='LoadCSV'}
          <LoadCsv bind:func_name={func_name} bind:form_submitted={form_submitted} proj_obj={proj_obj}/>
        {/if}
      </div>
    </div>
    <ProjectThumb user={user} project={proj_obj} is_special={special_unit_mark}/>
  </div>