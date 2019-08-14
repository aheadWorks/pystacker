<template>
    <div v-if="name">
        <div class="card">
            <header class="card-header">
                <p class="card-header-title">
                <span class="icon">
                                <i :class="'fas '+progress" aria-hidden="true"></i>
                            </span>
                    {{ name }}
                </p>

                <b-dropdown class="card-header-icon" position="is-bottom-left">
                  <span class="icon " slot="trigger"><i class="fas fa-cog"></i></span>
                  <b-dropdown-item :disabled="!cmd_results.length" @click="isCardModalActive = true">Show run logs</b-dropdown-item>
                  <b-dropdown-item :disabled="!is_stopped" @click="del()">Delete</b-dropdown-item>
                </b-dropdown>
            </header>
            <div class="card-content level">
                <div class="level-left">
                    <template v-for="k in links">
                        <span v-for="v in k" :key="v.url">
                            <a v-bind:href="v.url" target="_blank">{{v.name}}</a>&nbsp;
                        </span>
                    </template>
                </div>
                <div v-if="!isLoading" class="level-right">
                    <a v-if="is_paused || is_stopped" @click="up()" class=" is-light"><i
                            class="fas fa-2x fa-play-circle"></i></a>
                    <a v-if="!is_paused && !is_stopped" @click="pause()" class=""><i
                            class="fas fa-2x fa-pause-circle"></i></a>
                    <a v-if="!is_stopped" @click="down()" class=""><i class="fas fa-2x fa-stop-circle"></i></a>
                </div>
            </div>
        </div>
        <br/>
        <b-modal :active.sync="isCardModalActive" :width="640" scroll="keep">
            <section v-if="cmd_results.length">
                <console :lines="cmd_results"></console>
            </section>
        </b-modal>
        <section>
            <services :services="stack.services" :stack_id="parseInt(id)"></services>
        </section>

    </div>
</template>

<script>

    import Services from './ServicesList'
    import Console from '../Console'

    export default {
        name: "ViewStack",
        components: {Services, Console},
        mounted() {
            this.$store.dispatch('stacks/getStack', {id: this.id})
        },
        data() {
            return {
                isCardModalActive: false
            }
        },

        computed: {

            cmd_results() {
                return this.$store.getters['cmd/getResultById'](this.id)
            },

            stack() {
                return this.$store.getters['stacks/getStackById'](this.id)
            },


            name() {
                return this.stack.name
            },

            links() {
                if (this.stack.links) {
                    return this.stack.links
                }
                return []
            },

            vars() {
                if (this.stack.vars) {
                    return this.stack.vars
                }
                return {}
            },

            services() {
                return this.stack.services
            },

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
                return this.id
            }

        },
        props: {
            id: String,
            action: String
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


                        this.$store.dispatch('cmd/run', {cmd: 'destroy', stack_id: this.stack_id})
                            .then(() => this.$router.push("/"))
                    }
                })
            }
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
