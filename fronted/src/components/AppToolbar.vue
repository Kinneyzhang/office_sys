<template>
    <v-toolbar color="light-blue darken-4" dark fixed>
      <v-toolbar-side-icon @click="drawer = !drawer"></v-toolbar-side-icon>
      <v-toolbar-title>Office操作题测试与批阅</v-toolbar-title>
      <v-spacer></v-spacer>
      <div class="hidden-sm-and-down">
        <router-link to="/login">
          <v-btn flat>
            <v-icon>person</v-icon>登陆
          </v-btn>
        </router-link>
        <router-link to="/register">
          <v-btn flat @click>注册</v-btn>        
        </router-link>
      </div>
    </v-toolbar>
</template>

<script>
 export default {
   data () {
     return {
       items: [
         { title: 'Home', icon: 'dashboard' },
         { title: 'About', icon: 'question_answer' }
       ],
       right: null,
       drawer: null
     }
   }
 }
</script>
