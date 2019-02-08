<template>
  <div>
    <b-field>
      <b-input v-model="cmd" placeholder="ls -la | grep php" v-on:keyup.enter.native="exec()"></b-input>
      <p class="control">
        <button class="button is-primary" @click="exec()" :disabled="!cmd.length">Run</button>
      </p>
    </b-field>

    <console :lines="lines"></console>
  </div>
</template>

<script>
  import Console from '../../Console'


  export default {
    name: "Exec",
    components: {Console},
    computed: {
      lines() {
        let res = this.$store.getters['stacks/getServiceCmdResults'](this.stack_id, this.service_name) || ''
        return res.split(/\n/)
      }
    },
    methods: {
      exec() {
        if (!this.cmd.length) return;
        this.$store.dispatch('stacks/execServiceCmd', {
          stack_id: this.stack_id,
          service_name: this.service_name,
          cmd: this.cmd
        })
      },
    },
    data() {
      return {
        cmd: ''
      }
    },
    props: {
      stack_id: String,
      service_name: String
    },
  }
</script>

<style scoped>

</style>
