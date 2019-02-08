import api from '../../api/stack'
import Vue from 'vue'


// initial state
const state = {
    cmd_results: {},
    pullImagesResults: {},
    logs: {},
    status: {}
}

// getters
const getters = {

    getResultById: (state) => (id) => {
        if(state.cmd_results.hasOwnProperty(id)){
            return state.cmd_results[id]
        }
        return []
    },
    getLogsById: (state) => (id) => {
        if(state.logs.hasOwnProperty(id)){
            return state.logs[id]
        }
        return []
    },
    getLogsByService: (state) => (id, service) => {
        if(state.logs.hasOwnProperty(id)){
            return state.logs[id].filter(l => l.startsWith(service + '_'))
        }
        return []
    },
    getPullImageStatus: (state) => (path) => {

        if(state.pullImagesResults.hasOwnProperty(path))
            return [{...state.pullImagesResults[path], path: path}]

        let matchingStatuses = Object.keys(state.pullImagesResults)
            .filter(key => key.startsWith(path))
            .map((v) =>   {return {...state.pullImagesResults[v], path: v}})

        if (matchingStatuses.length)
            return matchingStatuses

        return [{status: 'Unknown', progressDetail: {current:0, total:0}, path: path}]
    },

    isPulling: (state) => (stack_id) => !!state.status['pull_in_progress/'+stack_id],

    isCmdRunning: (state) => (stack_id,  cmd) => {
        if(cmd) return !!state.status[ 'cmd_' + cmd + '_in_progress' + '/' + stack_id]
        let re = RegExp('cmd_[a-z]+_in_progress/'+stack_id)
        return !!Object.keys(state.status).filter((v) => v.match(re) && state.status[v]).length
    }

};

// actions
const actions = {
    run({commit}, {cmd, stack_id}){
        commit('SET_STATUS', {stack_id:stack_id, namespace: 'cmd_' + cmd + '_in_progress', value:true})
        return new Promise((resolve, reject) => {
            api.cmd(lines => {
                commit('SET_RESULT', {obj: cmd === 'logs' ? 'logs' : 'cmd_results', lines: lines.split('\n'), id: stack_id})
            }, cmd, stack_id)
                .then(() => {
                    resolve(stack_id)}
                    )
                .catch(reject)
                .finally(() => commit('SET_STATUS', {stack_id:stack_id, namespace: 'cmd_' + cmd + '_in_progress', value:false})
)
        })
    },
    pullImages({commit}, {stack_id}){
        commit('SET_STATUS', {stack_id:stack_id, namespace:'pull_in_progress', value:true})
        return api.pullImages(statusObj => commit('UPDATE_PULL_IMAGES', statusObj), stack_id)
            .finally(() => commit('SET_STATUS', {stack_id:stack_id, namespace:'pull_in_progress', value:false}))
    }
};


// mutations
const mutations = {
    SET_RESULT (state, {obj, lines, id}){
        Vue.set(state[obj], id, lines)
    },

    UPDATE_PULL_IMAGES (state, data){
        let path = data['stack_id'] + '/' + data['service']
        let obj = {
            status: data['status'],
            progressDetail: data['progressDetail']
        };
        Vue.set(state.pullImagesResults, path, obj)
    },

    SET_STATUS (state, {stack_id, namespace, value}){
        Vue.set(state.status, namespace + '/' + stack_id, value)
    }


};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
