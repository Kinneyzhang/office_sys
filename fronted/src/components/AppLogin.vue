<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center style="margin-top: 170px">
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>登陆账号</v-toolbar-title>
                <v-spacer></v-spacer>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    prepend-icon="person"
                    name="username"
                    label="用户名"
                    type="text"
                    v-model="username"
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="lock"
                    name="password"
                    label="密码"
                    type="password"
                    v-model="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary">确定</v-btn>
              </v-card-actions>
            </v-card>
          </v-flex>
        </v-layout>
      </v-container>
    </v-content>
  </v-app>
</template>

<script>
 export default {
   data: () => ({
     username: "",
     password: "",
   }),
   methods: {
     login(){
       this.$axios.post("api/login/", JSON.stringify(
         {"username": this.username, "password": this.password}
       )).then( res => {
         if(res.data.is_login == false){
           this.msg = res.data.msg;
         }else{
           sessionStorage.setItem("username", res.data.username)
           sessionStorage.setItem("userid", res.data.use_id)
           sessionStorage.setItem("islogin", res.data.is_login)
         }
         console.log(this.login_user)
       }).catch( err => {
         console.log(err)
       })
       this.username = ""
       this.password = ""
     }
   },
 }
</script>

<style scoped>
 
</style>
