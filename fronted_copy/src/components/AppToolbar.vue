<template>
  <v-toolbar
    fixed
    dense
    app
    clipped-left
    color="indigo"
    dark
  >
    <v-toolbar-side-icon @click.stop="drawer = !drawer"></v-toolbar-side-icon>
    <v-toolbar-title class="mr-5 align-center">
      <router-link to="/" tag="span" class="sys_title">
      </router-link>
    </v-toolbar-title>
    
    <v-layout justify-center>
      <router-link to="/">
        <v-btn flat class="subheading font-weight-bold">首页</v-btn>
      </router-link>
      <router-link to="/">
        <v-btn flat class="subheading font-weight-bold">题库</v-btn>
      </router-link>
      <router-link to="/">
        <v-btn flat class="subheading font-weight-bold">讨论</v-btn>
      </router-link>
      <router-link to="/">
        <v-btn flat class="subheading font-weight-bold">学习</v-btn>
      </router-link>
    </v-layout>

    <account-dialog></account-dialog>
    
  </v-toolbar>
</template>

<script>
 import AccountDialog from '@/components/AccountDialog'
 
 export default {
   components: {
     AccountDialog
   }
 }
</script>

<style scoped>
 .active-menu{
   color: green;
 }
</style>
