<script>
    //export let user;
    //export let project;
    let {user,project} = $props();
</script>

<div class="project-item">
    {#if project.icon}
    <img src="{project.icon}" class="thumb-icon" alt='icon'>
    {:else}
    <img src="/backend/static/icon_placeholder.png" class="thumb-icon" alt='icon'>
    {/if}
    <div style="text-align: start;">
        <h3 style="margin-bottom: 0; margin-top: 0;">{project.name}</h3>
        By {user.display_name}
    </div>
</div>