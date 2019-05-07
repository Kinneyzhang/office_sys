<template>
  <v-card>
    <v-card-title>
      <div v-if="!isLogin">
        <h3 class="subheading font-weight-bold mt-0">Office 操作题练习与测试</h3>
        <span class="grey--text">用户未登陆</span>
      </div>
      <span v-else class="font-weight-medium subheading">欢迎，{{userName}}!</span>
    </v-card-title>
  </v-card>
</template>

<script>
 export default {
   data(){
     return{
       
     }
   },
   computed: {
     isLogin(){
       return this.$store.state.islogin
     },
     userName(){
       return this.$store.state.username
     },
   },
 }
</script>
