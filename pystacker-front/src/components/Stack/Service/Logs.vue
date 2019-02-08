<template>
  <console :lines="lines"></console>
</template>
<script>
  import Console from '../../Console'

  export default {
    name: "Logs",
    components: {Console},
    computed: {
      lines() {
        return this.$store.getters['stacks/getLogs'](this.stack_id, this.service_name)
      }
    },
    mounted() {
      this.$store.dispatch('stacks/getLogs', {stack_id: this.stack_id, service_name: this.service_name})
    },
    props: {
      stack_id: String,
      service_name: String
    },
  }
</script>
