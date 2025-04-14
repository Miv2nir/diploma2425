<script>
    export let user;
    export let project;
</script>

<div class="project-item">
    <img src="{project.icon}" class="thumb-icon" alt='icon'>
    <div style="text-align: start;">
        <h3 style="margin-bottom: 0; margin-top: 0;">{project.name}</h3>
        By {user.display_name}
    </div>
</div>