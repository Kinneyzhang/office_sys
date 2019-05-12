import Vue from 'vue'
import Vuex from 'vuex'
import 'es6-promise/auto'
Vue.use(Vuex)

const store = new Vuex.Store({
    state: {
	islogin: false,
	username: null,
	userid: null,
	registertime: null,
	drawer: true,
	fileInput: null,
    },
    mutations: {
	login(state, payload) {
	    state.registertime = payload.registertime,
            state.islogin = payload.islogin,
	    state.username = payload.username,
	    state.userid = payload.userid
	}
    }
})

export default store
