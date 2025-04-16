<script>
    import ProjectThumb from "../elements/ProjectThumb.svelte";
    let {user,proj_obj} = $props();
    const special_unit_mark=true;
</script>
<div style="display:flex; flex-direction:column; justify-content: space-around; height:90.3vh;" id='container-main-spacer'>
    <div class="home-container center" id="container-main" style="margin-bottom:1rem;">
      <div class="underlying-container">
        <h1>Working Field</h1>
      </div>
    </div>
    <ProjectThumb user={user} project={proj_obj} is_special={special_unit_mark}/>
  </div>