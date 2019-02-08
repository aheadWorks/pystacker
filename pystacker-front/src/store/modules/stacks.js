import stacks_api from '../../api/stack'
import templates_api from '../../api/template'
import Vue from 'vue'


// initial state
const state = {
  all: [],
  templates: [],
  preview: {},
  logs: {},
  cmd_results: {}
};

// getters
const getters = {
    getStackById: (state) => (id) => {
        let i = state.all.findIndex(x => x.id === parseInt(id))
        if(i >= 0){
            return state.all[i]
        }
        return {}
    },

    getService: (state) => (stack_id, service_name) => {
        let stack = state.all.find(x => x.id === parseInt(stack_id))
        if(!stack) return
        return stack.services.find(v => v.name === service_name)
    },

    getLogs: (state)=> (stack_id, service_name) => {
        let sn = stack_id + '/' + service_name
        if(!state.logs.hasOwnProperty(sn)) {
            return []
        }
        return state.logs[sn]
    },
    getServiceCmdResults: (state)=> (stack_id, service_name) => {
        let sn = stack_id + '/' + service_name
        if(!state.cmd_results.hasOwnProperty(sn)) {
            return ''
        }
        return state.cmd_results[sn]
    }
};

// actions
const actions = {
    getAllStacks({ commit }) {
        stacks_api.all(stacks => {
            commit('setStacks', stacks)
        })
    },
    getStack({commit}, {id}){
        stacks_api.one(stack => {
            commit('setStack', stack)
        }, id)
    },
    getTemplates({ commit }) {
        templates_api.all()
            .then((templates => {
            commit('setTemplates', templates)
        }))
    },
    getTemplate({ commit }, {name}) {
        templates_api.one(name)
            .then((template => {
            commit('setTemplate', template)
        }))
    },


    createStack({ dispatch }, {id, vars, name}) {
        return stacks_api.create(id, name, vars)
            .then((r) => {dispatch('getAllStacks'); return r})
    },

    deleteStack({ commit, dispatch }, {id}) {
        commit('deleteStack', id)
        return stacks_api.delete(id).catch(() => dispatch('getAllStacks'))
    },

    destroyStack({ commit, dispatch }, {id}) {
        commit('deleteStack', id)
        return stacks_api.destroy(id).catch(() => dispatch('getAllStacks'))
    },

    getLogs({commit}, {stack_id, service_name}) {
         commit('CLEAR_LOG_RECORDS', {stack_id, service_name})
         stacks_api.logs((r) => commit('ADD_LOG_RECORD', {stack_id: stack_id, service_name: service_name, record: r}), stack_id, service_name)
    },
    execServiceCmd({commit}, {stack_id, service_name, cmd}) {
         commit('CLEAR_CMD_RECORDS', {stack_id, service_name})
         stacks_api.exec((r) => commit('ADD_CMD_RECORD', {stack_id: stack_id, service_name: service_name, record: r}), stack_id, service_name, cmd)
    },

};


// mutations
const mutations = {
    setStack (state, stack){
        let foundIndex = state.all.findIndex(x => x.id === stack.id) || 0;
        state.all.splice(foundIndex, 1, stack)
    },

    deleteStack (state, stack){
        let foundIndex = state.all.findIndex(x => x.id === stack.id);
        state.all.splice(foundIndex, 1)
    },

    setStacks (state, stacks) {
        state.all = stacks
    },
    setTemplates (state, templates) {
        state.templates = templates
    },
    setTemplate (state, template){
        let foundIndex = state.templates.findIndex(x => x.name === template.name);
        state.templates.splice(foundIndex, 1, template)
    },
    setPreview (state, preview) {
        state.preview = preview
    },

    CLEAR_LOG_RECORDS (state, {stack_id, service_name}){
        Vue.set(state.logs, stack_id + '/' + service_name, [])
    },
    ADD_LOG_RECORD (state, {stack_id, service_name, record}){
        let sn = stack_id + '/' + service_name
        if(!state.logs.hasOwnProperty(sn)){
            Vue.set(state.logs, sn, [])
        }
        state.logs[sn].push(record)
    },

    CLEAR_CMD_RECORDS (state, {stack_id, service_name}){
        Vue.set(state.cmd_results, stack_id + '/' + service_name, '')
    },
    ADD_CMD_RECORD (state, {stack_id, service_name, record}){
        let sn = stack_id + '/' + service_name
        Vue.set(state.cmd_results, sn, record)
    }
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
