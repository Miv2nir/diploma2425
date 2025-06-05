<!--script src="/backend/static/front_lib/api_functions.js"></script-->
<svelte:head>
  <script src="https://cdn.plot.ly/plotly-latest.min.js" type="text/javascript"></script>
</svelte:head>
<script>
  //get csrf token
  const csrftoken = Cookies.get('csrftoken');
  
  import Cookies from 'js-cookie';
  import ProjectThumb from "./elements/ProjectThumb.svelte";
  import {getRequest, postRequest} from "./lib/APICalls.js";

  import FunctionListPanel from "./panels/FunctionListPanel.svelte";
  import MainPanel from "./panels/MainPanel.svelte";
  import PipelinePanel from "./panels/PipelinePanel.svelte";

  //first things first, retrieve info about the user
  //const special_unit_mark=true;
  var user_logged_in = $state(false);
  var project_retrieved = $state(false);
  var user = $state(null);
  var author = $state(null);
  var is_author = $state(false);
  var proj_uuid=$state('');
  var proj_obj=$state(null);
  var upd_flag=$state(false);
  var pipeline_length=$state(0);

  async function pageInit() {
    user = await getRequest("/api/user/data/");
    //console.log($state.snapshot(user));
    if (user.pk == null) {
      //user not logged in. redirect to the login page
      window.location.href = "/login?next=/edit/";
    } else {
      user_logged_in = true;
      //username = user.display_name;
    }
    //pull the project information
    // TODO: Pass project uuid to the app (likely as query)
    const query_string= $state(new URLSearchParams(window.location.search));
    if (query_string.has('project_id'))
    {
      proj_uuid=query_string.get('project_id');
    }
    else 
    {
      window.location.href = "/projects/";
    }
    
    //retrieve project info
    proj_obj = await getRequest('/api/project/'+proj_uuid+'/');
    //get author information
    author=await getRequest('/api/user/data/'+proj_obj.user+'/');
    console.log(author);
    if (proj_obj!=null) {
      project_retrieved=true;
    }
    is_author=(user.pk===author.pk);
    console.log(is_author);
    //console.log($state.snapshot(proj_obj));
    //assuming things went successful, update the last_edited value of the project
    await postRequest('/api/project/'+proj_uuid+'/upd_date/',csrftoken);
  }
  pageInit();
  //stuff for components to update each other
  let func_obj= $state();
  let form_submitted=$state(false);
  let runtime_invoked=$state(false);
  let runtime_error=$state({});
  let runtime_errored=$state(false);
  let runtime_finished=$state(false);
</script>

{#if user_logged_in}
  {#if project_retrieved}
    <span class="home-main-container">
      {#key form_submitted}
      <FunctionListPanel bind:func_obj={func_obj} 
      is_author={is_author}
      proj_obj={proj_obj}/>
      {/key}
      <MainPanel author={author}
      is_author={is_author}
      proj_obj={proj_obj}
        bind:func_obj={func_obj}
        bind:form_submitted={form_submitted}
        bind:runtime_invoked={runtime_invoked}
        bind:runtime_error={runtime_error}
        bind:runtime_errored={runtime_errored}
        bind:runtime_finished={runtime_finished}
        bind:pipeline_length={pipeline_length}/>
      {#key form_submitted}
      <PipelinePanel bind:upd_flag={upd_flag}
      is_author={is_author}
      bind:func_obj={func_obj}
        proj_obj={proj_obj} 
        bind:runtime_invoked={runtime_invoked}
        bind:runtime_error={runtime_error}
        bind:runtime_errored={runtime_errored}
        bind:runtime_finished={runtime_finished}
        bind:pipeline_length={pipeline_length}/>
      {/key}
    </span>
    {#key form_submitted}
    <script src="/backend/static/three_panel_animator.js"></script>
    {/key}
  {:else}
    <div style="
      height: 100svh;
      display: flex;
      align-items: center;
      flex-direction: column;
      justify-content: center;">
      <div style="font-size: 2rem;">Loading...</div>
    </div>
  {/if}
  {:else}
    <div style="
      height: 100svh;
      display: flex;
      align-items: center;
      flex-direction: column;
      justify-content: center;">
      <div style="font-size: 2rem;">Verifying user session...</div>
    </div>
{/if}
