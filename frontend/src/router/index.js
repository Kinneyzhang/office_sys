import Vue from 'vue'
import Router from 'vue-router'
import TheHome from '@/components/TheHome'
import TheQuiz from '@/components/TheQuiz'
import TheDiscuss from '@/components/TheDiscuss'
import TheLearn from '@/components/TheLearn'

Vue.use(Router)

export default new Router({
    routes: [
	{
	    path: '/',
	    name: 'TheHome',
	    component: TheHome
	},
	{
	    path: '/quiz',
	    name: 'TheQuiz',
	    component: TheQuiz
	},
	{
	    path: '/discuss',
	    name: 'TheDiscuss',
	    component: TheDiscuss
	},
	{
	    path: '/learn',
	    name: 'TheLearn',
	    component: TheLearn
	},
    ]
})
