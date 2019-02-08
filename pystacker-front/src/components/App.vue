<template>
    <section>
        <navbar></navbar>
        <div style="padding:1.5rem 3rem;" class="app_body">
            <breadcrumbs></breadcrumbs>
            <transition name="slide">
                <router-view></router-view>
            </transition>
        </div>
        <!--footer>
            <div class="has-text-grey-light has-text-centered is-size-7">Client:{{ __FRONTEND_VERSION__}}, Backend:</div>
        </footer-->
    </section>
</template>

<script>

    import Navbar from './Navbar'
    import Breadcrumbs from './Breadcrumbs'

    export default {
        name: 'app',
        components: {
            Navbar, Breadcrumbs
        }
    }
</script>

<style lang="scss">

    @import "~bulmaswatch/default/_variables";
    @import "~bulma";
    @import "~bulmaswatch/default/_overrides";
</style>
