<script>
    //export let user;
    //export let project;
    let {user,project,is_special=false} = $props();
    var special_class=$state('');
    if (is_special)
    {
        special_class='special';
    }
</script>

<div class="project-item {special_class}" style="position:relative;">
    {#if project.icon}
    <img src="{project.icon}" class="thumb-icon" alt='icon'>
    {:else}
    <img src="/backend/static/icon_placeholder.png" class="thumb-icon" alt='icon'>
    {/if}
    <div style="text-align: start;">
        <h3 style="margin-bottom: 0; margin-top: 0;">{project.name}</h3>
        By {user.display_name}
    </div>
    {#if is_special}
    <!--p style="position:absolute; right:5%;">Exit</p-->
    <a href="/projects/{project.id}/" style="position:absolute;right:2%; max-width:10rem;">
        <button type="button" class="login-button-secondary" style="width: 10rem;">Exit</button>
    </a>
    {/if}
</div>