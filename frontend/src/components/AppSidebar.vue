<template>
  <v-card>
    <v-card-title>
      <div v-if="!isLogin">
        <h3 class="subheading font-weight-bold mt-0">Office 操作题练习与测试</h3>
        <span class="grey--text">用户未登陆</span>
      </div>
      <router-link v-else :to="userinfo" class="font-weight-medium subheading pointer">欢迎，{{userName}}!</router-link>
    </v-card-title>
    <v-list>
      <v-list-tile>
        <router-link to="/">
          <v-icon>create</v-icon>&nbsp;创建新主题
        </router-link>
      </v-list-tile>
      <v-list-tile>
        <router-link to="/">
          <v-icon>cloud_upload</v-icon>&nbsp;上传答案
        </router-link>
      </v-list-tile>
    </v-list>
    
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
     userinfo(){
       return "/user/" + this.userName
     }
   },
   methods: {
   },
 }
</script>
