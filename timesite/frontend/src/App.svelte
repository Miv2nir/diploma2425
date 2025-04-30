<!--script src="/backend/static/front_lib/api_functions.js"></script-->
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
  const special_unit_mark=true;
  var user_logged_in = $state(false);
  var project_retrieved = $state(false);
  var user = $state(null);
  var proj_uuid=$state('');
  var proj_obj=$state(null);

  async function pageInit() {
    user = await getRequest("/api/user/data/");
    console.log($state.snapshot(user));
    if (user.pk == null) {
      //user not logged in. redirect to the login page
      window.location.href = "/login?next=/edit/";
    } else {
      user_logged_in = true;
      //username = user.display_name;
    }
    //pull the project information
    // TODO: Pass project uuid to the app (likely as query)
    const query_string= new URLSearchParams(window.location.search)
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
    if (proj_obj!=null) {
      project_retrieved=true;
    }
    console.log($state.snapshot(proj_obj));
    //assuming things went successful, update the last_edited value of the project
    await postRequest('/api/project/'+proj_uuid+'/upd_date/',csrftoken);
  }
  pageInit();
  //for the matter of selecting functions
  let func_name= $state('');
</script>

{#if user_logged_in && project_retrieved}
  <span class="home-main-container">
    <FunctionListPanel bind:func_name={func_name} />
    <MainPanel user={user} proj_obj={proj_obj} func_name={func_name} />
    <PipelinePanel user={user} />
  </span>
  <script src="/backend/static/three_panel_animator.js"></script>
{/if}
