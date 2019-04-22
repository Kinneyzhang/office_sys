<template>
  <div id="app">
    <app-toolbar></app-toolbar>
    <div class="router">
      <router-view/>
    </div>
    <app-footer></app-footer>
  </div>
</template>

<script>
 import AppToolbar from '@/components/AppToolbar'
 import AppFooter from '@/components/AppFooter'
 export default {
   name: 'App',
   components: {
     AppToolbar,
     AppFooter,
   }
 }
</script>

<style>
 #app {
   font-family: 'Avenir', Helvetica, Arial, sans-serif;
   -webkit-font-smoothing: antialiased;
   -moz-osx-font-smoothing: grayscale;
   text-align: center;
   color: #2c3e50;
 }
 body{
   overflow: hidden;
 }
 .router{
   margin-top: 64px;
   background-color: #f9f9f9;
 }
</style>
