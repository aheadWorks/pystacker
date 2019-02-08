<template>
  <nav class="breadcrumb" aria-label="breadcrumbs">
    <ul>
        <li :class="idx === sitems.length - 1 ? 'is-active' : ''" v-for="(item, idx) in sitems" :key="idx">
          <a v-if="!item.link">{{item.name}}</a>
          <span v-else>
                    <router-link :to="item.link" v-if="item.link || ''" class="is-active">{{ item.name }}</router-link>
                </span>
        </li>
    </ul>
  </nav>
</template>

<script>
  export default {
    name: "Breadcrumbs",
    computed: {
      sitems() {
        return this.items.map((_breadcrumb) => {
          let breadcrumb = {..._breadcrumb}
          for (let i in this.params) {
            if (this.params.hasOwnProperty(i)) {
              breadcrumb.name = breadcrumb.name.replace("{" + i + "}", this.params[i])
              if (breadcrumb.link) breadcrumb.link = breadcrumb.link.replace("{" + i + "}", this.params[i])
            }
          }
          return breadcrumb
        })
      },
      params() {
        return this.$route.params || {}
      }
    },

    data: () => {
      return {items: []}
    },
    mounted() {
      this.items = this.$route.meta.breadcrumb || []
    },
    watch: {
      '$route'() {
        this.items = this.$route.meta.breadcrumb || []
      }
    },
  }
</script>

<style scoped>
</style>
