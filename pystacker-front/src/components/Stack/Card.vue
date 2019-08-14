<template>
  <div class="box">
    <article class="media">
      <div class="media-left">

        <figure class="image is-48x48">
                        <span class="icon image">
                            <i v-bind:class="'fa-3x ' + meta.icon" aria-hidden="true"></i>
                        </span>
        </figure>
      </div>
      <div class="media-content">
        <div class="content">
          <p>
                            <span class="icon">
                                <i v-bind:class="'fas '+progress" aria-hidden="true"></i>
                            </span>
            <strong>
              <router-link :to="'/stack/'+stack_id" :key="name">{{ name }}</router-link>
              <span class="has-text-grey-lighter">&nbsp;#{{ stack_id }}</span> </strong>
            <br>
            <template v-for="k in links">
                                <span v-for="v in k" :key="v.url">

                                    <a v-bind:href="v.url" target="_blank">{{v.name}}</a>&nbsp;
                                </span>
            </template>
          </p>
        </div>

      </div>
      <div class="media-right">

        <template v-if="!isLoading">

          <a v-if="is_paused || is_stopped" @click="up()" class=" "><i class="fas fa-2x fa-play-circle"></i></a>
          <a v-if="!is_paused && !is_stopped" @click="pause()" class=""><i class="fas fa-2x fa-pause-circle"></i></a>
          <a v-if="!is_stopped" @click="down()" class=""><i class="fas fa-2x fa-stop-circle"></i></a>

        </template>
        <template v-else>
          <a class="has-text-grey-light"><span class=""><i class="fas fa-2x fa-play-circle"></i></span></a>
          <a class="has-text-grey-light"><span class=""><i class="fas fa-2x fa-pause-circle"></i></span></a>
        </template>

      </div>
    </article>

  </div>
</template>

<script>

  export default {
    name: "Card",
    components: {},
    computed: {
      progress() {

        let icons = {
          'on': 'has-text-success fa-circle',
          'pending': 'has-text-info fa-spinner fa-spin',
          'off': 'has-text-grey-light fa-circle',
          'paused': 'has-text-warning fa-circle',
          'broken': 'has-text-danger fa-circle'
        }
        if (this.isLoading) return icons['pending']
        if (this.is_ok) return icons['on']
        if (this.is_stopped) return icons['off']
        if (this.is_paused) return icons['paused']
        return icons['broken']

      },
      is_paused() {
        // If any is paused
        return this.services.findIndex((v) => v.status === -1) !== -1
      },
      is_stopped() {
        // If all are stopped
        return this.services.findIndex((v) => v.status !== 0) === -1
      },
      is_ok() {
        // all services are running
        return this.services.findIndex((v) => v.status !== 1) === -1
      },

      isLoading() {
        return this.$store.getters['cmd/isCmdRunning'](this.stack_id) || this.$store.getters['cmd/isPulling'](this.stack_id)
      },
      stack_id() {
        // TODO: Refactor to use stack_id instead of id
        return this.id
      }

    },
    props: {
      id: Number,
      name: String,
      from_template: String,
      services: Array,
      meta: Object,
      links: Object
    },
    methods: {
      up() {
        let cmd_name = this.is_paused ? 'unpause' : 'up'

        if (cmd_name === 'unpause') {
          this.$store.dispatch('cmd/run', {cmd: 'unpause', stack_id: this.stack_id})
            .then(() => {
              this.$store.dispatch('stacks/getStack', {id: this.stack_id})
            })
          return
        }

        this.$store.dispatch('cmd/pullImages', {stack_id: this.stack_id})
          .then(() => {
            this.$store.dispatch('cmd/run', {cmd: 'up', stack_id: this.stack_id})
              .then(() => {
                this.$store.dispatch('stacks/getStack', {id: this.stack_id})
              })

              .then(() => {
                this.$store.dispatch('cmd/run', {cmd: 'logs', stack_id: this.stack_id})
              })
          })


      },
      down() {
        this.$store.dispatch('cmd/run', {cmd: 'down', stack_id: this.stack_id})
          .then(() => {
            this.$store.dispatch('stacks/getStack', {id: this.stack_id})
          })
      },
      pause() {
        this.$store.dispatch('cmd/run', {cmd: 'pause', stack_id: this.stack_id})
          .then(() => {
            this.$store.dispatch('stacks/getStack', {id: this.stack_id})
          })
      },
      del() {
        this.$buefy.dialog.confirm({
          title: 'Deleting stack',
          message: 'Are you sure you want to <b>delete</b> stack? This action cannot be undone.',
          confirmText: 'Delete stack',
          type: 'is-danger',
          hasIcon: true,
          onConfirm: () => {
            this.$store.dispatch('stacks/deleteStack', {id: this.id})
          }
        })
      },
    },
    filters: {
      limit: (v) => {
        if (!v) return ''
        v = v.toString()
        return v.length > 20 ? v.substring(0, 20) + '...' : v;
      }
    },
  }
</script>

<style scoped>

</style>
