<template>
  <v-app
    id="inspire"
  >
    <app-sidebar></app-sidebar>
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
 import AppSidebar from '@/components/AppSidebar'
 
 export default {
   components: {
     AppToolbar,
     AppSidebar
   },
 }
</script>
