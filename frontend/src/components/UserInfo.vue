<template>
  <div>
    <v-card class="elevation-1">
      <v-card-title>
        <span class="display-1 font-weight-bold">{{userName}}</span>
        <input type="file" id="upload" ref="upload" multiple accept=".zip, .rar">
      </v-card-title>
      <v-card-text>
        <span class="subheading grey--text">本站第 1 位用户，注册时间：2019-05-07</span>
      </v-card-text>
    </v-card>
    <v-card class="elevation-1 mt-4">
      <v-tabs
        v-model="active"
        slider-color="blue"
      >
        <v-tab
          v-for="(menu, index) in personal_menu"
          :key="index"
          ripple
        >
          {{menu}}
        </v-tab>
        <v-tab-item
          v-for="(menu, index) in personal_menu"
          :key="index"
        >
          <div v-if="index == 0">
            <div v-for="(item, index) in download_list" class="downloadBox">
              <v-layout row justify-center align-center>
                <v-flex md10 sm10>
                  <div class="pl-5 pt-3">
                    <span class="font-weight-medium">{{item.quiz_id}}</span>
                    <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{item.download_time}}&nbsp;下载</span>
                    <p class="mt-2 overflow2">{{item.quiz_text}}</p>
                  </div>
                </v-flex>
                <v-flex md2 sm2 align-center>
                  <v-btn small color="info" flat v-if="!item.upload_status" @click="popWindow">
                    <v-icon color="info">publish</v-icon>提交答案
                  </v-btn>
                  <span v-else>答案已提交</span>
                </v-flex>
              </v-layout>
            </div>
          </div>
          
          <div v-if="index == 1">
            <div v-for="(item, index) in exer_list" class="downloadBox">
              <v-layout row justify-center align-center>
                <v-flex md10 sm10>
                  <div class="pl-5 pt-3">
                    <span class="font-weight-medium">{{item.quiz_id}}</span>
                    <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{item.upload_time}}&nbsp;下载</span>
                    <p class="mt-2 overflow2">{{item.quiz_text}}</p>
                  </div>
                </v-flex>
                <v-flex md2 sm2 align-center>
                  <v-btn small color="info" flat v-if="!item.upload_status" @click="popWindow">
                    <v-icon color="info">publish</v-icon>提交答案
                  </v-btn>
                  <span v-else>答案已提交</span>
                </v-flex>
              </v-layout>
            </div>
          </div>
          
          <div v-if="index == 2">
          </div>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
 export default {
   data(){
     return {
       active: null,
       personal_menu: [
         '下载记录',
         '练习记录',
         '创建的帖子',
       ],
       download_list: [],
       exer_list: [],
     }
   },
   computed: {
     userName(){
       return this.$store.state.username
     },
   },
   methods: {
     get_record(){
       this.$axios.post("api/get_record/", JSON.stringify({
         "username": this.userName,
       })).then(res => {
         /* console.log(res.data) */
         res = JSON.parse(res.data)
         var quizId = res.map(v => v.quiz_id)
         var quizText = res.map(v => v.quiz_text)
         var quizType = res.map(v => v.quiz_type)
         var downloadTime = res.map(v => v.download_time)
         var uploadStatus = res.map(v => v.upload_status)
         var uploadTime = res.map(v => v.upload_time)
         var correctStatus = res.map(v => v.correct_status)
         var quizScore = res.map(v => v.quiz_score)
         var resultInfo = res.map(v => v.result_info)
         
         for(var i=0; i<quizId.length; i++){
           this.download_list.unshift({
             quiz_id: quizId[i],
             quiz_text: quizText[i],
             quiz_type: quizType[i],
             download_time: downloadTime[i],
             upload_status: uploadStatus[i],
           })
         }
         for(var i=0; i<quizId.length; i++){
           this.exer_list.unshift({
             quiz_id: quizId[i],
             quiz_text: quizText[i],
             upload_time: uploadTime[i],
             quiz_score: quizScore[i],
             result_info: resultInfo[i],
           })
         }
       }).catch(err => {
         console.log(err.data)
       }) 
     },
     popWindow(){
       let uploadBtn = this.$refs.upload
       uploadBtn.click()
     },
     upload(){
       this.userid = sessionStorage.getItem("userid")
       let formData = new FormData();
       formData.append('file', this.$refs.file.files[0])
       formData.append('')
       this.$axios.post('/api/upload/', formData, config).then(res => {
         console.log(res)
       }).catch(err => {
         console.log(err)
       })
     }
   },
   created(){
     this.get_record()
   }
 }
</script>

<style scoped>
 .downloadBox{
   border-bottom: 0.1px solid #E0E0E0;
 }
 #upload{
   height: 0;
   width: 0;
   visibility: hidden;
 }
</style>
