<template>
  <v-toolbar
    fixed
    dense
    app
    clipped-left
    color="indigo"
    dark
  >
    <v-toolbar-side-icon @click.stop="drawer_status"></v-toolbar-side-icon>
    <v-toolbar-title class="mr-5 align-center">
      <router-link to="/" tag="span" class="sys_title">
      </router-link>
    </v-toolbar-title>
    
    <v-layout justify-center>
      <router-link to="/">
        <v-btn flat class="subheading font-weight-bold">首页</v-btn>
      </router-link>
      <router-link to="/quiz">
        <v-btn flat class="subheading font-weight-bold">题库</v-btn>
      </router-link>
      <router-link to="/post">
        <v-btn flat class="subheading font-weight-bold">讨论</v-btn>
      </router-link>
      <router-link to="/learn">
        <v-btn flat class="subheading font-weight-bold">学习</v-btn>
      </router-link>
    </v-layout>

    <app-login></app-login>
    
  </v-toolbar>
</template>

<script>
 import AppLogin from '@/components/AppLogin'
 
 export default {
   data(){
     return{
       /* drawer: false */
     }
   },
   components: {
     AppLogin
   },
   methods: {
     drawer_status(){
       this.$store.commit({type: 'drawer', drawer: !this.$store.state.drawer})
     }
   }
 }
</script>

<style scoped>
 .active-menu{
   color: green;
 }
</style>
