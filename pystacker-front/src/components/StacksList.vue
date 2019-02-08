<template>
  <div>
    <stack-card v-for="stack in stacks" v-bind="stack" :key="stack.name"></stack-card>
  </div>
</template>

<script>
  import Vuex from 'vuex'
  import StackCard from './Stack/Card'
  export default {
    name: "StacksList",
    components: {StackCard},
    computed: Vuex.mapState({
      stacks: state => state.stacks.all.sort((x, y) => x.name.localeCompare(y.name))
    }),
    created() {
      this.$store.dispatch('stacks/getAllStacks')
    },
    methods: {
      stackUp(id) {
        this.$store.dispatch('terminal/runCmd', {cmd: 'up', id: id})
      },
      stackDown(id) {
        this.$store.dispatch('terminal/runCmd', {cmd: 'down', id: id})
      },
      deleteStack(id) {
        this.$store.dispatch('stacks/deleteStack', {id: id})
      }
    }
  }
</script>

<style scoped>

</style>
