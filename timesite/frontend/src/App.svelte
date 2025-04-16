<!--script src="/backend/static/front_lib/api_functions.js"></script-->
<script>
  import ProjectThumb from "./elements/ProjectThumb.svelte";
  import {getRequest} from "./lib/APICalls.js";

  import FunctionListPanel from "./panels/FunctionListPanel.svelte";
  import MainPanel from "./panels/MainPanel.svelte";
  import PipelinePanel from "./panels/PipelinePanel.svelte";

  //first things first, retrieve info about the user
  const special_unit_mark=true;
  var user_logged_in = false;
  var project_retrieved = false;
  var user = null;
  var proj_uuid='';
  var proj_obj=null;

  async function pageInit() {
    user = await getRequest("/api/user/data/");
    console.log(user);
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
    console.log(proj_obj);
  }
  pageInit();
</script>

{#if user_logged_in && project_retrieved}
  <span class="home-main-container">
    <FunctionListPanel />
    <MainPanel user={user} proj_obj={proj_obj} />
    <PipelinePanel user={user} />
  </span>
  <script>
    //not part of the svelte component, the code below takes care of the transition animations
    var container_left = document.getElementById("container-side-1");
    var container_main = document.getElementById("container-main");
    var container_right = document.getElementById("container-side-2");
    var animate = false;
    var shrunk = window.innerWidth < 1000;
    function addTransition() {
      container_left.classList.add("transitioning");
      container_right.classList.add("transitioning");
      container_main.classList.add("transitioning");
      console.log("transitions added");
    }
    function removeTransition() {
      container_left.classList.remove("transitioning");
      container_right.classList.remove("transitioning");
      container_main.classList.remove("transitioning");
      animate = false;
      console.log("transitions removed");
    }
    function delayedRemoveTransition() {
      //console.log('aea');
      setTimeout(removeTransition, 100);
    }
    function hider() {
      if (window.innerWidth < 1000) {
        if (animate == false && shrunk == false) {
          animate = true;
          shrunk = true;
          addTransition();
        }
        container_left.classList.add("hidden");
        container_right.classList.add("hidden");
        container_main.classList.add("full-width");
      } else {
        if (animate == false && shrunk == true) {
          animate = true;
          shrunk = false;
          addTransition();
        }
        container_left.classList.remove("hidden");
        container_right.classList.remove("hidden");
        container_main.classList.remove("full-width");
      }
      //window.addEventListener('resize',hider);
    }

    window.onresize = hider;
    //addEventListener('animationstart',(addTransition));
    addEventListener("transitionend", delayedRemoveTransition);
    //fire the function on page load, otherwise it doesnt do anything on mobile unless form fields are interacted with
    hider();
  </script>
{/if}
