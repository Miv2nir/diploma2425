<script>
    let {f}=$props();
    //console.log(f);
</script>

<span class="function-item-text">
{#if f.accepts.length!=0}
    <span>↳ {f.accepts}
        {#if f.produces.length!=0}
        ;
        {/if}
    </span>
    {/if}
{#if f.produces.length!=0}
    <span>⎆ {f.produces}</span>
{/if}
</span>
