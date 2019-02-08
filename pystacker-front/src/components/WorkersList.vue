<template>
  <div>
    <div v-for="w in workers" :key="w.name">
      <strong>{{w.name}}</strong>
      <button @click="force(w.name)">Force</button>
    </div>
  </div>
</template>

<script>
  export default {
    name: "WorkersList",
    computed: {
      workers() {
        return this.$store.state.workers.all
      }
    },
    created() {
      this.$store.dispatch('workers/getAll')
    },
    methods: {
      force(name) {
        this.$store.dispatch('workers/force', {name: name})
      }
    }
  }
</script>

<style scoped>

</style>
