<template>
  <v-app
    id="inspire"
  >
    <app-nav-drawer></app-nav-drawer>
    
    <app-toolbar></app-toolbar>
    
    <v-content>
      <v-container fill-height>
        <v-layout justify-center>
          <router-view/>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
 import AppToolbar from '@/components/AppToolbar'
 import AppNavDrawer from '@/components/AppNavDrawer'
 
 export default {
   components: {
     AppToolbar,
     AppNavDrawer
   },
 }
</script>
