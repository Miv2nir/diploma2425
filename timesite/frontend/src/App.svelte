<script>
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
 var username = 'user';
  async function getRequest(url) { //moving to async otherwise this will be way too overcomplicated
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
    var user = await getRequest('/api/user/data/');
    console.log(user);
    if (user.pk == null) 
    {
      //user not logged in. redirect to the login page
      window.location.href = '/login?next=/edit/';
    }
    else {
      user_logged_in = true;
      username = user.username;
    }
    //pull the project information
    }

  pageInit();
 /*
 onMount(async function() {
  const response = await fetch('/api/user/data/');
  const data = await response.json();
  console.log(data.username);
  userdata=data;
  console.log(userdata.username);
 })*/

</script>
{#if user_logged_in}
<span class="home-main-container">
  <div class="home-container" id="container-side-1">
      <h2>Recent projects</h2>
      <div class="project-item"></div>
  </div>
  <div class="home-container center" id="container-main">
      <div class="underlying-container">
      <h1>Welcome back, {username}</h1>
      <p class="text-containered">Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
      </p>
      </div> 
  </div>
  <div class="home-container" id="container-side-2">
      
      <p class="profile-shorthand"><img src="/backend/static/icon_placeholder.png" alt='pfp' class="pfp"><b></b></p>
      <a href='/' class="fancy-underline underlined">Home Page</a><br>
      <a href='/profile/' class="fancy-underline">Profile Page</a><br>
      <a href='/projects/' class="fancy-underline">Projects</a><br>
      <a href='/logout/' class="fancy-underline">Log Out</a><br>
  </div>
</span>
{/if}