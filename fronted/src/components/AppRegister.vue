<template>
  <v-app id="inspire">
    <v-content>
      <v-container fluid fill-height>
        <v-layout justify-center style="margin-top: 170px">
          <v-flex xs12 sm8 md4>
            <v-card class="elevation-12">
              <v-toolbar dark color="primary">
                <v-toolbar-title>注册账号</v-toolbar-title>
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
                    name="password1"
                    label="密码"
                    type="password"
                    v-model="password1"
                  ></v-text-field>
                  <v-text-field
                    prepend-icon="lock"
                    name="password2"
                    label="重复密码"
                    type="password"
                    v-model="password2"
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
     password1: "",
     password2: ""
   }),
   methods: {
     register(){
       this.$axios.post("api/register/", JSON.stringify(
         {"new_username": this.username,
          "new_password1": this.password1,
          "new_password2": this.password2
         })).then(res => {
           this.msg = res.data.msg
         }).catch(err => {
           console.log(err)
         })
       this.username = ""
       this.password1 = ""
       this.password2 = ""
     },
   },
 }
</script>

<style scoped>
 
</style>
