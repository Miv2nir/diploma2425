<script>
    let {f}=$props();
    //console.log(f);
</script>

<br>
{#if f.produces.length!=0}
    <span>↳ {f.produces}
        {#if f.accepts.length!=0}
        ;
        {/if}
    </span>
    {/if}
{#if f.accepts.length!=0}
    <span>⎆ {f.accepts}</span>
{/if}
