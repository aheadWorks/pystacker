<template>
  <div class="columns" v-if="Object.keys(all_vars).length">
    <div class="column">
      <b-field label="Name">
        <b-input v-model="name" required></b-input>
      </b-field>
      <b-field v-for="(v,k) in visible_vars" :key="k" :label="v.label || k">
        <template v-if="v.type === 'select'">
          <b-select v-bind:value="defaults[k]" v-on:input="payload[k] = $event">
            <option v-for="(o,ov) in v.options" :key="ov">{{o}}</option>
          </b-select>
        </template>

        <template v-if="v.type === 'textarea'">
          <b-input type="textarea" v-bind:value="defaults[k]" v-on:input="payload[k] = $event">
          </b-input>
        </template>

        <template v-if="!v.type">
          <b-input v-bind:value="defaults[k]" v-on:input="payload[k] = $event" :required="v.required"></b-input>
        </template>

      </b-field>
      <button class="button is-primary" @click="createAndLeave">Create</button>
    </div>
  </div>
</template>

<script>
  export default {
    name: "Create",
    components: {},
    created() {
      this.$store.dispatch('templates/getOne', {name: this.id})
    },

    computed: {
      all_vars() {
        return this.$store.getters['templates/getById'](this.id).vars || {}
      },
      visible_vars() {
        return Object.keys(this.all_vars)
                .reduce((acc, idx) => {
                  if(this.all_vars[idx].type !== 'system') acc[idx] = this.all_vars[idx]
                  return acc
                }, {})
      },
      defaults() {
        let defaults = {}
        Object.keys(this.all_vars).forEach(k => (defaults[k] = this.all_vars[k].default))
        return defaults
      },
      id() {
        return this.$route.params.id
      }

    },
    methods: {

      collectVars() {
        return Object.assign({}, this.defaults, this.payload)
      },
      send() {
        this.$store.dispatch('stacks/templatePreview', {id: this.id, vars: this.collectVars()})
      },
      create() {
        this.$store.dispatch('stacks/createStack', {id: this.id, vars: this.collectVars(), name: this.name})
      },
      createAndLeave() {
        this.$store.dispatch('stacks/createStack', {id: this.id, vars: this.collectVars(), name: this.name})
          .then((r) => this.$router.push("/stack/" + r['id']))
          .catch(r => this.$buefy.toast.open({
            duration: 5000,
            message: `Error creating stack: ${r}`,
            position: 'is-top',
            type: 'is-danger'
          }))
      }
    },
    data() {
      return {
        name: '',
        payload: {},
      }
    },
  }
</script>

<style scoped>

</style>
