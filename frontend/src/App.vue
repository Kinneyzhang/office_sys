<template>
  <v-app
    id="app"
  >
    <!-- <app-sidebar></app-sidebar> -->
    <app-toolbar></app-toolbar>
    
    <v-content>
      <v-container fill-height>
        <v-layout fluid row>
          <v-flex xs9 sm9 md9 mr-4 fill-height>
            <router-view v-if="isRouterAlive"></router-view>
          </v-flex>
          <v-flex xs3 sm3 md3 fill-height>
            <app-sidebar></app-sidebar>
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
   components: {
     AppToolbar,
     AppSidebar
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
   /* watch: {
    *   '$route' (to, from) {
    *     const toDepth = to.path.split('/').length
    *     const fromDepth = from.path.split('/').length
    *     this.transitionName = toDepth < fromDepth ? 'slide-right' : 'slide-left'
    *   }
    * }, */
 }
</script>

<style>
 .pointer{
   cursor: pointer;
 }
 .overflow2{
   overflow: hidden;
   -webkit-line-clamp: 2;
   text-overflow: ellipsis;
   display: -webkit-box;
   -webkit-box-orient: vertical;
 }
 .overflow1{
   white-space: nowrap;
   text-overflow:ellipsis;
   overflow:hidden;
 }
 .v-progress-circular{
   margin: 1rem
 }
 .btn-style{
   border: 2px solid #E0E0E0;
   font-weight: bold;
 }
</style>
