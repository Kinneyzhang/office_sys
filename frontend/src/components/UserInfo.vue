<template>
  <div>
    <v-card class="elevation-1">
      <v-card-title>
        <span class="display-1 font-weight-bold">{{userName}}</span>
      </v-card-title>
      <v-card-text>
        <span class="subheading grey--text">本站第 {{userId}} 位用户，加入时间：{{registerTime}}</span>
      </v-card-text>
    </v-card>
    
    <v-card class="elevation-1 mt-4">
      <div class="pt-2" style="border-bottom: 1px solid #E0E0E0;">
        <router-link :to="download_link" tag="span">
          <v-btn flat color="primary" class="font-weight-bold subheading">下载记录</v-btn> 
        </router-link>
        <router-link :to="exercise_link" tag="span">
          <v-btn small flat color="primary" class="font-weight-bold subheading">练习记录</v-btn>
        </router-link>
        <router-link :to="post_link" tag="span">
          <v-btn small flat color="primary" class="font-weight-bold subheading">发帖记录</v-btn>
        </router-link>
        <router-link :to="collect_link" tag="span">
          <v-btn small flat color="primary" class="font-weight-bold subheading">帖子收藏</v-btn>
        </router-link>
      </div>
      
      <router-view></router-view>
      
    </v-card>
  </div>
</template>

<script>
 export default {
   inject: ['reload'],
   computed: {
     registerTime(){
       console.log(this.$store.state.registertime)
       return this.$store.state.registertime
     },
     userName(){
       return this.$store.state.username
     },
     userId(){
       return this.$store.state.userid
     },
     download_link(){
       return "/user/" + this.userName + "/download"
     },
     exercise_link(){
       return "/user/" + this.userName + "/exercise"
     },
     post_link (){
       return "/user/" + this.userName + "/post"
     },
     collect_link (){
       return "/user/" + this.userName + "/collect"
     }
   },
 }
</script>

<style scoped>
</style>
