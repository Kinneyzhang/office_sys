<template>
  <div>
    <input type="file" class="uploadHide" ref="file" multiple accept=".zip, .rar" @change="getFile($event)">
    <v-expansion-panel
      class="elevation-0"
      expand
    >
      <v-expansion-panel-content
        v-for="(item, index) in count_list"
        :key="index"
      >
        <template v-slot:actions>
          <v-icon small color="warning" v-if="!item.upload_status">info</v-icon>
          <v-icon small color="primary" v-else>check_circle</v-icon>
        </template>
        <template v-slot:header>
          <div>
            <span class="font-weight-medium">{{item.quiz_id}}</span>
            <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{item.download_time}}&nbsp;下载</span>
            <form v-if="!item.upload_status" class="d-inline">
              <v-btn small flat class="font-italic" @click.stop="popWindow"><u>选择答案文件</u></v-btn>
              <v-btn small color="primary" flat @click.stop="upload($event,item.record_id)">
                <v-icon color="primary">publish</v-icon>
                <span class="font-weight-black body-2">上传</span>
              </v-btn>
            </form>
            <v-btn v-else small flat class="grey--text text--darken-3">答案已提交</v-btn>
          </div>
        </template>
        <div class="px-4">
          <p class="" v-html="item.quiz_text"></p>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <div class="text-xs-center">
      <v-pagination
        v-model="page"
        :length="count_length"
        prev-icon="mdi-menu-left"
        next-icon="mdi-menu-right"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
 export default{
   inject: ['reload'],
   data(){
     return {
       download_list: [],
       file: "",
       page: 1,
     }
   },
   computed: {
     count_list(){
       return this.download_list.slice(eval(this.page*6-6),this.page*6)
     },
     count_length(){
       return eval(this.download_list.length/6+1)
     }
   },
   methods: {
     //获取下载记录和练习记录
     get_quiz_record(){
       this.$axios.post("api/get_quiz_record/", JSON.stringify({
         "username": this.$store.state.username,
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
         var recordId = res.map(v => v.record_id)
         var quizStr = []
         var correct_sheet = []
         
         for(var i=0; i<quizId.length; i++){
           quizStr.push(quizText[i].split('；').join('；<br>'))
           this.download_list.unshift({
             quiz_id: quizId[i],
             quiz_text: quizStr[i],
             quiz_type: quizType[i],
             download_time: downloadTime[i],
             upload_status: uploadStatus[i],
             record_id: recordId[i],
           })
         }
       }).catch(err => {
         console.log(err.data)
       }) 
     },
     getFile(event) {
       this.file = event.target.files[0];
       console.log(this.file);
       this.$message({
         message: "即将上传的文件为"+this.file.name 
       })
     },
     popWindow(){
       /* var file = "file"+index */
       let uploadBtn = this.$refs.file
       uploadBtn.click()
     },
     upload(event, record_id){
       if(!this.file){
         this.$message({
           message: "请先选择上传的文件！"
         })
       }else{
         event.preventDefault();
         let formData = new FormData();
         formData.append('file', this.file)
         formData.append('userId', this.userId)
         formData.append('recordId', record_id)
         console.log(this.userId)
         console.log(record_id)
         let config = {
           headers: {'Content-Type': 'multipart/form-data'}
         }
         this.$axios.post('api/upload/', formData, config).then(res => {
           console.log(res)
           this.reload()
         }).catch(err => {
           console.log(err)
         }) 
       }
     },
   },
   created(){
     this.get_quiz_record()
     /* this.get_post_record() */
   },
 }
</script>

<style scoped>
 .downloadBox{
   border-bottom: 0.1px solid #E0E0E0;
 }
 .uploadHide{
   height: 0;
   width: 0;
   visibility: hidden;
 }
</style>
