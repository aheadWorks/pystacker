<template>
  <div class="box level" v-if="dataReady">

    <div class="level-left">
      <span class="icon"><i :class="iconClass(status)"></i></span><strong>{{ service_name }}</strong> <span
      class="tag is-light" v-if="image">{{ image }}</span>

      <pull-status :stack_id="stack_id" :service_name="service_name" v-if="isPulling"></pull-status>
    </div>

    <div v-if="!!status" class="level-right field is-grouped">
      <p class="control">
        <router-link :to="'/stack/'+stack_id+'/'+service_name+'/exec'" class="button" v-if="status > 0">Exec</router-link>
      </p>
      <p class="control">
        <router-link :to="'/stack/'+stack_id+'/'+service_name+'/logs'" class="button" v-if="status">Logs</router-link>
      </p>
    </div>
  </div>
</template>

<script>
  import PullStatus from './PullStatus'

  export default {
    name: "Card",
    components: {PullStatus},
    computed: {
      service() {
        return this.$store.getters['stacks/getService'](this.stack_id, this.service_name)
      },
      dataReady() {
        return !!this.service
      },
      status() {
        return this.service.status
      },
      image() {
        return this.service.image
      },
      isPulling() {
        return this.$store.getters['cmd/isPulling'](this.stack_id)
      }
    },
    methods: {
      iconClass(status) {
        if (this.isPulling) return 'fas has-text-info fa-spinner fa-spin'
        return this.icons[status + '']
      }
    },
    data() {
      return {
        icons: {
          "0": 'fas has-text-grey-light fa-circle',
          "1": 'fas has-text-success fa-circle',
          "-1": 'fas has-text-warning fa-circle'
        }
      }
    },
    props: {
      service_name: String,
      stack_id: Number
    },
  }
</script>

<style scoped>

</style>
