import Vue from 'vue'
import Router from 'vue-router'

import TheHome from '@/components/TheHome'

import TheQuiz from '@/components/TheQuiz'
import QuizList from '@/components/QuizList'
import QuizType from '@/components/QuizType'
import SinglePoint from '@/components/SinglePoint'
import ManyPoint from '@/components/ManyPoint'

import TheDiscuss from '@/components/TheDiscuss'
import PostList from '@/components/PostList'
import PostTag from '@/components/PostTag'
import DiscussPost from '@/components/DiscussPost'

import TheLearn from '@/components/TheLearn'

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
	    redirect: '/quiz/latest',
	    component: TheQuiz,
	    children: [
		{
		    path: 'latest',
		    component: QuizList
		},
		{
		    path: ':quizType',
		    redirect: ':quizType/many',
		    component: QuizType,
		    children: [
			{
			    path: 'many',
			    component: ManyPoint
			},
			{
			    path: ':point',
			    component: SinglePoint
			}
		    ]
		}
	    ]
	},
	{
	    path: '/post',
	    redirect: '/post/latest',
	    component: TheDiscuss,
	    children: [
		{
		    path: 'latest',
		    component: PostList
		},
		{
		    path: 'tag/:tagName',
		    name: 'tagList',
		    component: PostTag
		},
	    ]
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
	    redirect: '/user/:username/download',
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
