import Vue from 'vue'
import Router from 'vue-router'
import AppHome from '@/components/AppHome'
import AppRegister from '@/components/AppRegister'
import AppLogin from '@/components/AppLogin'

Vue.use(Router)

export default new Router({
    routes: [
	{
	    path: '/',
	    name: 'AppHome',
	    component: AppHome
	},
	{
	    path: '/register',
	    name: 'AppRegister',
	    component: AppRegister
	},
	{
	    path: '/login',
	    name: 'AppLogin',
	    component: AppLogin
	}
    ]
})
