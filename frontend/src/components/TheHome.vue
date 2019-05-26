<template>
  <div>
    <v-card>
      <v-card-title primary-title>
        <div>
          <span class="title mt-0" v-if="!islogin">请登录</span>
          <span class="title mt-0" v-else>欢迎，{{username}}！</span>
        </div>
      </v-card-title>
    </v-card>
    <v-card class="mt-4">
      <div class="px-4 py-4">
        <div class="mt-0">
          <span class="subheading font-weight-bold">已下载试题</span><br>
          <user-download></user-download>
        </div>
        <v-divider></v-divider>
        <div>
          <span class="subheading font-weight-bold">查看批阅结果</span>
          <user-exercise></user-exercise>
        </div>
        <v-divider></v-divider>
        <div>
          <span class="subheading font-weight-bold">推荐您下载</span>
        </div>
      </div>
    </v-card>
  </div>
</template>

<script>
 import UserDownload from '@/components/UserDownload'
 import UserExercise from '@/components/UserExercise'
 export default {
   inject: ['reload'],
   components: {
     UserDownload,
     UserExercise,
   },
   data () {
     return {
       
     }
   },
   computed: {
     username(){
       return this.$store.state.username
     },
     islogin(){
       return this.$store.state.islogin
     },
   },
   methods: {
   },
   created(){
   }
 }
</script>
