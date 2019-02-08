<template>
  <div>
    <card :stack_id="stack_id" :service_name="s.name" v-for="s in services" :key="s.name"></card>

  </div>
</template>

<script>
  import Card from './Service/Card'
  export default {
    name: "ServicesList",
    components: {Card},
    props: {
      services: Array,
      stack_id: Number,
    },
  }
</script>

<style scoped>
</style>
