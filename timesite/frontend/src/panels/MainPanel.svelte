<script>
    import Left from "../elements/panel_buttons/Left.svelte";
    import Right from "../elements/panel_buttons/Right.svelte";
    import ProjectThumb from "../elements/ProjectThumb.svelte";
    import ServerSideResultRender from "../elements/ServerSideResultRender.svelte";
    import LoadCSV from "../function_forms/LoadCSV.svelte";
    import DropColumns from "../function_forms/DropColumns.svelte";
    import RenderDf from "../function_forms/RenderDF.svelte";
    import DownloadDf from "../function_forms/DownloadDF.svelte";
    import RuntimeQueryer from "../elements/RuntimeQueryer.svelte";
    import FillNa from "../function_forms/FillNA.svelte";
    import DropNa from "../function_forms/DropNA.svelte";
    import GetQuantile from "../function_forms/GetQuantile.svelte";
    import FloatPointEvolModelFit from "../function_forms/FloatPointEvolModelFit.svelte";
    import ArchModelFit from "../function_forms/ArchModelFit.svelte";
    import LinePlotDf from "../function_forms/LinePlotDF.svelte";
    import ArimaModelFit from "../function_forms/ARIMAModelFit.svelte";
    let {author,
      proj_obj,
      func_obj=$bindable(),
      form_submitted=$bindable(false),
      runtime_invoked=$bindable(false),
      runtime_error=$bindable({}),
      runtime_errored=$bindable(false),
      is_author=$bindable(false),
      runtime_finished=$bindable(false),
      pipeline_length=$bindable(0)} = $props();
</script>
<div style="display:flex; flex-direction:column; justify-content: space-around; height:90.3vh;" id='container-main-spacer'>
    <div class="home-container center" id="container-main" style="margin-bottom:1rem;">
      <Left />
      <Right />
      <div class="underlying-container" style="height:80vh;">
      {#if runtime_invoked}
        {#if runtime_finished}
          {#if !runtime_errored}
          <ServerSideResultRender bind:runtime_invoked={runtime_invoked} 
          proj_obj={proj_obj}/>
          {:else}
          <div>
            <br>
            Error in function {runtime_error.func_name} at position {runtime_error.position}!<br><br>
            {runtime_error.error}<br><br>
            Consider changing the function parameters to remedy this issue.
          </div>
          {/if}
        {:else}
        <RuntimeQueryer 
        bind:runtime_invoked={runtime_invoked}
        bind:runtime_finished={runtime_finished}
        proj_obj={proj_obj}/>
        {/if}
      {:else}
      {#if is_author}
        <h1 style="padding-left: 3rem; padding-right:3rem;">Select a function to view from the side panels...</h1>
        {:else}
        <h1 style="padding-left: 3rem; padding-right:3rem;">Select a function from the right panel to examine...</h1>
        {/if}
        {#if func_obj}
        <div class="function-item center"><b>{func_obj.display_name}</b><span class="subtitle">{func_obj.name}</span></div>
        <!--function forms invokation (should probably rewrite into a separate component)-->
        <p>{func_obj.description}</p>
        {#key func_obj}
        {#if func_obj.name=='LoadCSV'}
        <LoadCSV bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='DropColumns'}
        <DropColumns bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='FillNA'}
        <FillNa bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='DropNA'}
        <DropNa bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='GetQuantile'}
        <GetQuantile bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='RenderDF'}
        <RenderDf bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='DownloadDF'}
        <DownloadDf bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='FloatPointEvolModelFit'}
        <FloatPointEvolModelFit bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='ArchModelFit'}
        <ArchModelFit bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='LinePlotDF'}
        <LinePlotDf bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {#if func_obj.name=='ARIMAModelFit'}
        <ArimaModelFit bind:func_obj={func_obj}
         bind:form_submitted={form_submitted}
          proj_obj={proj_obj}
          bind:pipeline_length={pipeline_length}
          bind:is_author={is_author}/>
        {/if}
        {/key}
        {/if}
        {/if}
        </div>
    </div>
    <ProjectThumb author={author} project={proj_obj}/>
  </div>