<script>
    import RightDouble from "../elements/panel_buttons/RightDouble.svelte";
    import UserThumb from "../elements/UserThumb.svelte";
    let {user} = $props();

</script>
<div class="home-container" id="container-side-2">
    <RightDouble />
    <UserThumb user={user} />
    </div>