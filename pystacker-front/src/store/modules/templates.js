import templates_api from '../../api/template'

// initial state
const state = {
  all: []
};

// getters
const getters = {
    getById: (state) => (id) => {
        let i = state.all.findIndex(x => x.name === id)
        if(i >= 0){
            return state.all[i]
        }
        return {vars:{}}
    },
};

// actions
const actions = {

    getAll({ commit }) {
        templates_api.all()
            .then((templates => {
            commit('SET_ALL', templates)
        }))
    },
    getOne({ commit }, {name}) {
        templates_api.one(name)
            .then((template => {
            commit('SET_ONE', template)
        }))
    }

}


// mutations
const mutations = {
    SET_ONE (state, template){
        let foundIndex = state.all.findIndex(x => x.name === template.name) || 0;
            state.all.splice(foundIndex, 1, template)
    },

    SET_ALL (state, templates) {
        state.all = templates
    },
};

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}
