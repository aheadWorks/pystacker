import stacks from './modules/stacks'
import templates from './modules/templates'
import cmd from './modules/cmd'
import workers from './modules/workers'

import Vuex from 'vuex'
import Vue from "vue";

Vue.use(Vuex);


export default new Vuex.Store({
  modules: {
    stacks, cmd, templates, workers
  }
})
