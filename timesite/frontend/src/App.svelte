<script>
  import ProjectThumb from "./lib/ProjectThumb.svelte";
  /*
  import { onMount } from "svelte";

  */
  //const response = fetch('/api/user/data/');
  //var obj;
  //fetch('/api/user/data/').then(x=>x.json()).then(data=> {obj = data}).then(()=>{console.log(obj)});

  /*
  var userdata_promise;
  var user_logged_in = false;
  userdata_promise = fetch('/api/user/data').then(x=>x.json());
  console.log(userdata_promise);
  userdata_promise.then(
    function(value) {
      console.log(value);
      if (value.pk == null) {
        //user not logged in. redirect to the login page
        window.location.href = '/login?next=/edit/';
        }
        else {
          user_logged_in = true;
      }
      },
      function(error) {console.log(error);}
      )*/
  //first things first, retrieve info about the user
  var user_logged_in = false;
  var user = null;
  async function getRequest(url) {
    //moving to async otherwise this will be way too overcomplicated
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
      const json = await response.json();
      console.log(json);
      return json;
    } catch (error) {
      console.error(error.message);
      return null;
    }
  }

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
    //enable animations for the ui (cant situate it outside the function due to async await)
  }
  pageInit();
</script>

{#if user_logged_in}
  <span class="home-main-container">
    <div class="home-container" id="container-side-1">
      <h2>Recent projects</h2>
      <div class="project-item"></div>
    </div>
    <div class="home-container center" id="container-main">
      <div class="underlying-container">
        <h1>Welcome back, {user.display_name}</h1>
        
      </div>
    </div>
    <div class="home-container" id="container-side-2">
      {#if user.has_pfp}
        <p class="profile-shorthand">
          <img src="/backend/media/{user.pfp_path}" alt="pfp" class="pfp" /><b
            >{user.display_name}</b
          >
        </p>
      {:else}
        <p class="profile-shorthand">
          <img
            src="/backend/static/icon_placeholder.png"
            alt="pfp"
            class="pfp"
          /><b>{user.display_name}</b>
        </p>
      {/if}
      <a href="/" class="fancy-underline underlined">Home Page</a><br />
      <a href="/profile/" class="fancy-underline">Profile Page</a><br />
      <a href="/projects/" class="fancy-underline">Projects</a><br />
      <a href="/logout/" class="fancy-underline">Log Out</a><br />
    </div>
  </span>
  <script>
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
