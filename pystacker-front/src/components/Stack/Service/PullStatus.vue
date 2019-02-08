<template>
    <span>
                    {{status.status}} <progress v-if="status.progressDetail.total"
                                                :value="status.progressDetail.current"
                                                :max="status.progressDetail.total"></progress>
                </span>
</template>

<script>
  export default {
    name: "PullStatus",
    computed: {
      status() {
        return this.$store.getters['cmd/getPullImageStatus'](this.stack_id + '/' + this.service_name)[0]
      },
    },
    props: {
      stack_id: Number,
      service_name: String
    },
  }
</script>

<style scoped>
</style>
