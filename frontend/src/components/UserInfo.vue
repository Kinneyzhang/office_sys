<template>
  <div>
    <v-card class="elevation-1">
      <v-card-title>
        <span class="display-1 font-weight-bold">{{userName}}</span>
        <input type="file" id="upload" ref="file" multiple accept=".zip, .rar" @change="getFile($event)">
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
                <v-flex md2 sm2 align-center justify-center>
                  <div v-if="!item.upload_status">
                    <form>
                      <v-btn small flat class="grey--text" @click="popWindow"><u>选择文件</u></v-btn>
                      <v-btn small color="info" flat @click="upload($event,item.record_id)">
                        <v-icon color="info">publish</v-icon>上传
                      </v-btn>
                    </form>
                  </div>
                  <div v-else>
                    <span class="grey--text mr-2">答案已提交</span>
                  </div>
                </v-flex>
              </v-layout>
            </div>
          </div>
          
          <div v-if="index == 1">
            <div v-for="(item, index) in exer_list" class="downloadBox">
              <v-layout row justify-center align-center>
                <v-flex md12 sm12>
                  <div class="pl-5 pt-3">
                    <span class="font-weight-medium">{{item.quiz_id}}</span>
                    <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{item.upload_time}}&nbsp;提交答案</span>
                    <div v-if="!item.correct_status">
                      <span class="grey--text darken-3">该试题尚未批阅</span>
                    </div>
                    <div v-else>
                      <span>得分：{{item.quiz_score}}</span><br>
                      <span>提示信息：{{item.result_info}}</span>
                    </div>
                  </div>
                </v-flex>
              </v-layout>
            </div>
          </div>
          
          <div v-if="index == 2">
            <el-table
              :data="postList"
              style="width: 100%">
              <el-table-column
                label="主题"
                min-width="70%">
                <template slot-scope="scope">
                  <router-link
                    tag="span"
                    :to="link(scope.row.id)"
                    class="pointer subheading font-weight-medium"
                    v-html="scope.row.title"
                  ></router-link>
                  <br>
                  <router-link
                    to = "/discuss"
                    tag="span"
                    class="font-weight-bold pointer"
                    style="font-size:10px;"
                    v-html="scope.row.tag"
                  ></router-link>
                </template>
              </el-table-column>
              <el-table-column
                prop="reply"
                label="回复"
                align="center"
                min-width="10%">
              </el-table-column>
              <el-table-column
                prop="view"
                label="浏览"
                align="center"
                min-width="10%">
              </el-table-column>
              <el-table-column
                prop="active"
                label="活动"
                align="center"
                min-width="10%">
              </el-table-column>
            </el-table>
          </div>
        </v-tab-item>
      </v-tabs>
    </v-card>
  </div>
</template>

<script>
 export default {
   inject: ['reload'],
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
       postList: [],
       file: "",
     }
   },
   computed: {
     userName(){
       return this.$store.state.username
     },
     userId(){
       return this.$store.state.userid
     },
     link(){
       return function(post_id){
         return "/post/" + post_id
       }
     },
     timeFormat(){
       return function(time){
         //如果时间格式是正确的，那下面这一步转化时间格式就可以不用了
         var dateBegin = new Date(time.replace(/-/g, "/"));//将-转化为/，使用new Date
         var dateEnd = new Date();//获取当前时间
         var dateDiff = dateEnd.getTime() - dateBegin.getTime();//时间差的毫秒数
         var dayDiff = Math.floor(dateDiff / (24 * 3600 * 1000));//计算出相差天数
         var leave1=dateDiff%(24*3600*1000)    //计算天数后剩余的毫秒数
         var hours=Math.floor(leave1/(3600*1000))//计算出小时数
         //计算相差分钟数
         var leave2=leave1%(3600*1000)    //计算小时数后剩余的毫秒数
         var minutes=Math.floor(leave2/(60*1000))//计算相差分钟数
         //计算相差秒数
         var leave3=leave2%(60*1000)      //计算分钟数后剩余的毫秒数
         var seconds=Math.round(leave3/1000)
         var timeString = ""
         
         if(dayDiff>0)
           timeString = dayDiff + " 天前 "
         else if(hours>0)
           timeString += hours + " 小时前 "
         else if(minutes>0)
           timeString += minutes + " 分钟前"
         else
           timeString += "刚刚"

         return timeString
       }
     },
   },
   methods: {
     get_quiz_record(){
       this.$axios.post("api/get_quiz_record/", JSON.stringify({
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
         var recordId = res.map(v => v.record_id)
         
         for(var i=0; i<quizId.length; i++){
           this.download_list.unshift({
             quiz_id: quizId[i],
             quiz_text: quizText[i],
             quiz_type: quizType[i],
             download_time: downloadTime[i],
             upload_status: uploadStatus[i],
             record_id: recordId[i],
           })
         }
         for(var i=0; i<quizId.length; i++){
           if(uploadStatus[i] == true){
             this.exer_list.unshift({
               quiz_id: quizId[i],
               quiz_text: quizText[i],
               upload_time: uploadTime[i],
               quiz_score: quizScore[i],
               result_info: resultInfo[i],
               correct_status: correctStatus[i],
               record_id: recordId[i],
             }) 
           }
         }
       }).catch(err => {
         console.log(err.data)
       }) 
     },
     getFile(event) {
       this.file = event.target.files[0];
       console.log(this.file);
     },
     popWindow(){
       let uploadBtn = this.$refs.file
       uploadBtn.click()
     },
     upload(event, record_id){
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
     },
     get_post_record(){
       this.$axios.post("api/get_post_record/", JSON.stringify({
         "username": this.userName,
       })).then(res => {
         console.log(res.data)
         res = JSON.parse(res.data)

         var postId = res.map(v => v.post_id)
         var postPerson = res.map(v => v.poster)
         var postTitle = res.map(v => v.post_title)
         var postTag = res.map(v => v.post_tag)
         var postContent = res.map(v => v.post_content)
         var replyNum = res.map(v => v.reply_num)
         var viewNum = res.map(v => v.view_num)
         var modifyTime = res.map(v => v.post_modify_time)
         var activeTime = []
         for(var i=0; i<postPerson.length; i++){
           activeTime.push(this.timeFormat(modifyTime[i]))
         }
         for(var i=0; i<postPerson.length; i++){
           this.postList.unshift({
             id: postId[i],
             poster: postPerson[i],
             title: postTitle[i],
             tag: postTag[i],
             reply: replyNum[i],
             view: viewNum[i],
             active: activeTime[i],
           })
         }
       }).catch(err => {
         console.log(err.data)
       })
     },
   },
   created(){
     this.get_quiz_record()
     this.get_post_record()
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
 .border_right{
   border-right: 0.5px solid grey;
 }
</style>
