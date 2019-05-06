<template>
  <v-app
    id="app"
  >
    <!-- <app-sidebar></app-sidebar> -->
    <app-toolbar></app-toolbar>
    <v-content>
      <v-container fill-height>
        <v-layout fluid>
          <v-flex xs12 sm12 md12 fill-height>
            <router-view v-if="isRouterAlive"></router-view>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
 import AppToolbar from '@/components/AppToolbar'
 import AppSidebar from '@/components/AppSidebar'
 
 export default {
   name: 'app',
   provide(){
     return{
       reload: this.reload
     }
   },
   data(){
     return {
       isRouterAlive: true
     }
   },
   methods: {
     reload(){
       this.isRouterAlive = false
       this.$nextTick(function(){
         this.isRouterAlive = true
       })
     }
   },
   components: {
     AppToolbar,
     AppSidebar
   },
 }
</script>
