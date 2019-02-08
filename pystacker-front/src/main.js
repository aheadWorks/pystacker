import Vue from 'vue'
import VueRouter from 'vue-router'

import Buefy from 'buefy'

import store from './store/index'

import App from './components/App.vue'

import StacksList from "./components/StacksList";

Vue.use(Buefy)

const NewStack = () => import(/* webpackChunkName: "stack" */ "./components/Stack/New")
const CreateStack = () => import(/* webpackChunkName: "stack" */ "./components/Stack/Create")
const ViewStack = () => import(/* webpackChunkName: "stack" */ "./components/Stack/ViewStack")
const WorkersList = () => import(/* webpackChunkName: "stack" */ "./components/WorkersList.vue")
const ServiceExec = () => import(/* webpackChunkName: "stack" */ "./components/Stack/Service/Exec")
const ServiceLogs = () => import(/* webpackChunkName: "stack" */ "./components/Stack/Service/Logs")

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    component: StacksList,
    meta: {
      breadcrumb: [
        {name: 'Stacks'},
      ]
    }
  },
  {
    path: '/stack/new/:id',
    component: CreateStack,
    meta: {
      breadcrumb: [
        {name: 'Stacks', link: '/'},
        {name: 'Create new stack', link: '/stack/new'},
        {name: '{id}'}
      ]
    }
  },
  {
    path: '/stack/new',
    component: NewStack,
    meta: {
      breadcrumb: [
        {name: 'Stacks', link: '/'},
        {name: 'Create new stack'}
      ]
    }
  },
  {
    path: '/stack/:id',
    component: ViewStack,
    props: true,
    meta: {
      breadcrumb: [
        {name: 'Stacks', link: '/'},
        {name: 'ID #{id}'}
      ]
    }
  },
{
        path: '/stack/:stack_id(\\d+)/:service_name/logs',
        component: ServiceLogs,
        props: true,
        meta: {
            breadcrumb: [
                {name: 'Stacks', link:'/'},
                {name: 'ID #{stack_id}', link: '/stack/{stack_id}'},
                {name: '{service_name}', link: '/stack/{stack_id}/{service_name}'},
                {name: 'Logs'}

            ]
        }
    },{
        path: '/stack/:stack_id(\\d+)/:service_name/exec',
        component: ServiceExec,
        props: true,
        meta: {
            breadcrumb: [
                {name: 'Stacks', link:'/'},
                {name: 'ID #{stack_id}', link: '/stack/{stack_id}'},
                {name: '{service_name}', link: '/stack/{stack_id}/{service_name}'},
                {name: 'Exec'}

            ]
        }
    },
  {
    path: '/more/workers',
    component: WorkersList,
    meta: {
      breadcrumb: [
        {name: 'Workers'},
      ]
    }
  },
]

const router = new VueRouter({routes, mode: 'history'})

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
