<template>
  <div>
    <div class="hidden-sm-and-down" v-show="islogin">
      <router-link :to="userinfo" tag="span" class="pointer">{{login_usrname}}</router-link>
      <router-link to="/"><v-btn flat @click="logout" outline small>退出登陆</v-btn></router-link>
    </div>
    
    <div class="hidden-sm-and-down" v-show="!islogin">
      <v-dialog v-model="login_dialog" persistent max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn flat outline small v-on="on">
            <v-icon>person</v-icon>
            登陆
          </v-btn>
        </template>
        <v-card>
          <v-toolbar class="elevation-1 white" dense>
            <v-toolbar-title>
              登陆账号
            </v-toolbar-title>
          </v-toolbar>
          <!-- <v-card-title class="title">
               </v-card-title> -->
          <v-card-text>
            <v-form>
              <v-text-field
                prepend-icon="person"
                name="username"
                label="用户名"
                type="text"
                v-model="username"
                @click="msg=''"
              ></v-text-field>
              <v-text-field
                prepend-icon="lock"
                name="password"
                label="密码"
                type="password"
                v-model="password"
                @click="msg=''"
                @keyup.enter="login"
              ></v-text-field>
            </v-form>
            <div class="red--text ml-2" style="height: 10px; font-size: 10px;">{{msg}}</div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <el-button type="primary" :plain="true" color="" @click="login_dialog = false">取消</el-button>
            <el-button type="primary" :plain="true" @click="login">确定</el-button>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <v-dialog v-model="register_dialog" persistent max-width="400px">
        <template v-slot:activator="{ on }">
          <v-btn flat outline small v-on="on">注册</v-btn>
        </template>
        <v-card>
          <v-toolbar class="elevation-1 white" dense>
            <v-toolbar-title>
              注册账号
            </v-toolbar-title>
          </v-toolbar>
          <!-- <v-card-title color="indigo">
               <span class="headline">注册账号</span>
               </v-card-title> -->
          <v-card-text>
            <v-form>
              <v-text-field
                prepend-icon="person"
                name="username"
                label="用户名"
                type="text"
                v-model="username"
                @click="msg=''"
              ></v-text-field>
              <v-text-field
                prepend-icon="lock"
                name="password1"
                label="密码"
                type="password"
                v-model="password1"
                @click="msg=''"
              ></v-text-field>
              <v-text-field
                prepend-icon="lock"
                name="password2"
                label="重复密码"
                type="password"
                v-model="password2"
                @click="msg=''"
                @keyup.enter="register"
              ></v-text-field>
            </v-form>
            <div class="red--text ml-2" style="height: 10px; font-size: 10px;">{{msg}}</div>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <el-button type="primary" :plain="true" @click="register_dialog = false">取消</el-button>
            <el-button type="primary" :plain="true" @click="register">确定</el-button>
            <!-- <v-btn color="indigo" dark @click="register_dialog = false">取消</v-btn>
                 <v-btn color="indigo" dark @click="register">确定</v-btn> -->
          </v-card-actions>
        </v-card>
      </v-dialog>
    </div>
  </div>
</template>

<script>
 export default{
   inject: ['reload'],
   data: () => ({
     login_dialog: false,
     register_dialog: false,
     username: "",
     password: "",
     password1: "",
     password2: "",
     msg: ""
   }),
   methods: {
     register(){
       this.$axios.post("api/register/", JSON.stringify(
         {"new_username": this.username,
          "new_password1": this.password1,
          "new_password2": this.password2
         })).then(res => {
           if(res.data.msg=='账号注册成功!'){
             this.register_dialog = false
             this.$message({
               message: '账号注册成功，请登陆！',
             });
             this.username = ""
             this.password1 = ""
             this.password2 = ""
           }else{
             this.msg = res.data.msg
             this.username = ""
             this.password1 = ""
             this.password2 = ""
           }
           this.reload()
         }).catch(err => {
           console.log(err)
         })
     },
     login(){
       this.$axios.post("api/login/", JSON.stringify(
         {"username": this.username, "password": this.password}
       )).then( res => {
         if(res.data.is_login == false){
           this.msg = "*" + res.data.msg;
           this.username = "";
           this.password = "";
         }else{
           this.login_dialog = false
           sessionStorage.setItem("islogin", res.data.is_login)
           sessionStorage.setItem("username", res.data.user_name)
           sessionStorage.setItem("userid", res.data.user_id)
           sessionStorage.setItem("registertime", res.data.register_time)
           this.$store.commit({
             type: 'login',
             islogin: sessionStorage.getItem("islogin"),
             username: sessionStorage.getItem("username"),
             userid: sessionStorage.getItem("userid"),
             registertime: sessionStorage.getItem("registertime")
           })
         }
         console.log(res.data)
         /* this.reload() */
       }).catch( err => {
         console.log(err)
       })
     },
     logout(){
       sessionStorage.clear()
       this.$store.commit({
         type: 'login',
         islogin: false,
         username: null,
       })
       this.username = "";
       this.password = "";
       this.password1 = "";
       this.password2 = "";
       this.msg = "";
       this.reload()
     },
   },
   computed: {
     islogin(){ // 很重要！！通过登陆状态的计算属性，每次刷新时commit用户信息。保证随时可以获取。为什么要用vuex，直接用sessionStorage行不行？？？
       if(sessionStorage.getItem("username") && sessionStorage.getItem("islogin")){
         this.$store.commit({
           type: 'login',
           islogin: sessionStorage.getItem("islogin"),
           username: sessionStorage.getItem("username"),
           userid: sessionStorage.getItem("userid"),
           registertime: sessionStorage.getItem("registertime")
         })
       }else{
         this.$store.commit({
           type: 'login',
           islogin: false
         })
       }
       this.login_dialog = false
       return this.$store.state.islogin
     },
     login_usrname(){
       return this.$store.state.username
       /* return sessionStorage.getItem("username") */
     },
     login_usrid(){
       return this.$store.state.userid
     },
     userinfo(){
       return "/user/" + this.login_usrname
     }
   },
 }
</script>

<style scoped>
</style>
