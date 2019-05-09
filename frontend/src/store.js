import Vue from 'vue'
import Vuex from 'vuex'
import 'es6-promise/auto'
Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
	islogin: false,
	username: null,
	userid: null,
	drawer: true,
	fileInput: null,
    },
    mutations: {
	login(state, payload) {
            state.islogin = payload.islogin,
	    state.username = payload.username,
	    state.userid = payload.userid
	},
	drawer(state, payload) {
	    state.drawer = payload.drawer
	},
	fileInput(state, payload) {
	    state.fileInput = payload.fileInput
	},
    },
    getters: {
	drawer: (state) => {
	    return state.drawer
	},
    }
})

export default store
