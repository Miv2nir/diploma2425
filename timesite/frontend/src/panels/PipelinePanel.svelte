<script>
    import UserThumb from "../elements/UserThumb.svelte";
    let {user} = $props();

</script>
<div class="home-container" id="container-side-2">
    <UserThumb user={user} />
    </div>