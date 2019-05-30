<template>
  <div>
    <div v-if="!islogin">
      <v-card>
        <v-img
          class="white--text"
          height="600px"
          aspect-ratio="4"
          src="http://pic.rmb.bdstatic.com/5d1bf2db27cd808776a6bbcb9cfc68ac.jpeg"
        ></v-img>
      </v-card>
    </div>
    <div v-else>
      <v-card>
        <v-card-title primary-title>
          <div>
            <span class="title mt-0">欢迎，{{username}}！</span>
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
