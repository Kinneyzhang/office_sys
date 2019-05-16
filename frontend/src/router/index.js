import Vue from 'vue'
import Router from 'vue-router'
import TheHome from '@/components/TheHome'
import TheQuiz from '@/components/TheQuiz'
import TheDiscuss from '@/components/TheDiscuss'
import TheLearn from '@/components/TheLearn'
import DiscussPost from '@/components/DiscussPost'
import UserInfo from '@/components/UserInfo'
import UserDownload from '@/components/UserDownload'
import UserExercise from '@/components/UserExercise'
import UserPost from '@/components/UserPost'

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
	    component: TheDiscuss,
	},
	{
	    path: '/post/:id',
	    name: 'discussPost',
	    component: DiscussPost
	},
	{
	    path: '/learn',
	    name: 'TheLearn',
	    component: TheLearn
	},
	{
	    path: '/user/:username',
	    component: UserInfo,
	    children: [
		{
		    path: 'download',
		    component: UserDownload
		},
		{
		    path: 'exercise',
		    component: UserExercise
		},
		{
		    path: 'post',
		    component: UserPost
		}
	    ]
	},
    ]
})
