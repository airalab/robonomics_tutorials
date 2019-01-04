import Vue from 'vue'
import Router from 'vue-router'
import Hello from '@/components/Hello'
import Trade from '@/components/Trade'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Hello',
      component: Hello
    },
    {
      path: '/trade',
      name: 'Trade',
      component: Trade
    }
  ]
})
