<template>
  <div>
    <div class="level">
    <h1 class="title">Select template</h1>
    <a class="button is-text level-right" @click="show_all_templates=!show_all_templates">
      <template v-if="show_all_templates">hide</template>
      <template v-else>show</template>
      deprecated
    </a>
    </div>



    <router-link class="box" v-for="t in templates" :to="'/stack/new/' + t.name " :key="t.name">
      <article class="media">
        <div class="media-left">

          <figure class="image is-64x64">
                    <span :class="'icon image' + (t.meta.deprecated ? ' has-text-grey' : '')">
                      <i v-bind:class="' fa-4x ' + t.meta.icon" aria-hidden="true"></i>
                    </span>
          </figure>
        </div>
        <div class="media-content">
          <div class="content">
            <p>
              <strong>{{ t.meta.label }}</strong>
              <br>
              {{ t.meta.description }}
            </p>
          </div>
        </div>
      </article>
    </router-link>

  </div>
</template>

<script>
  export default {
    name: "New",
    data(){
      return {
        show_all_templates : false
      }
    },
    computed: {
      templates() {
        let all = this.$store.state.templates.all.slice()
                .sort((a, b) => {return a.name   >  b.name})
        if(this.show_all_templates){
          return all
        }
        return all.filter(a => !a.meta.deprecated)
      },
    },

    created() {
      this.$store.dispatch('templates/getAll')
    },
  }
</script>

<style scoped>

</style>
