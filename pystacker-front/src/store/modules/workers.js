import Vue from 'vue'

import api from '../../api/workers'

// initial state
const state = {
    all: []
};

// getters
const getters = {
    getByName: (state) => (name) => {
        let w = state.workers.find((v) => v.name === name)
        if(w) return w;
        return {}
    }

};

// actions
const actions = {
    getAll({commit}){
        return api.all()
            .then(l => commit('SET_WORKERS', {list:l}))
    },
    force({commit}, {name}){
        return api.force(name).then(worker => commit('SET_ONE', {worker:worker}))
    }
};

// mutations
const mutations = {
    SET_WORKERS (state, {list}){
        Vue.set(state, 'all', list)
    },
    SET_ONE(state, {worker}){
        let index = state.all.findIndex(v => v.name === worker.name)
        state.all.splice(index, 1, worker)
    }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
