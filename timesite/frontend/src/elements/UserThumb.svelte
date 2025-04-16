<script>
    let {user} = $props();
</script>
<div>
    {#if user.has_pfp}
    <p class="profile-shorthand">
      <img src="/backend/media/{user.pfp_path}" alt="pfp" class="pfp" /><b
        >{user.display_name}</b
      >
    </p>
  {:else}
    <p class="profile-shorthand">
      <img
        src="/backend/static/pfp_placeholder.png"
        alt="pfp"
        class="pfp"
      /><b>{user.display_name}</b>
    </p>
  {/if}
</div>