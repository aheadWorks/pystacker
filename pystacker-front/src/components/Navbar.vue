<template>
    <nav class="navbar has-shadow is-spaced" role="navigation" aria-label="main navigation">
  <div class="navbar-brand">
    <router-link to="/" class="navbar-item is-size-3" href="/"   >
      STACKER
    </router-link>

    <a role="button" @click="isActive = !isActive" :class="'navbar-burger burger' + (isActive ? ' is-active':'')" aria-label="menu" aria-expanded="false" data-target="navbarBasicExample">
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
      <span aria-hidden="true"></span>
    </a>
  </div>
  <div id="navbarBasicExample" :class="'navbar-menu' + (isActive ? ' is-active':'')">
    <div class="navbar-start">
        <router-link class="navbar-item" to="/">Stacks</router-link>

      <div class="navbar-item has-dropdown is-hoverable">
        <a class="navbar-link">
          More
        </a>

        <div class="navbar-dropdown">
          <router-link class="navbar-item" to="/more/workers">
            Workers
          </router-link>
        </div>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <div class="buttons">
          <router-link to="/stack/new" class="button is-primary">
            <strong>Create new stack</strong>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</nav>
</template>

<script>
    export default {
        name: "Navbar",
        data(){
            return {
                isActive: false
            }
        },
    }
</script>

<style scoped>

</style>
