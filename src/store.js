import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    checkedEntities: [],
  },
  mutations: {
    add(state, entity) {
        state.checkedEntities.push(entity)
    },
    remove(state, entity) {
        let index = state.checkedEntities.indexOf(entity);
        state.checkedEntities.splice(index, 1);
    }
  },
});

export default store;
