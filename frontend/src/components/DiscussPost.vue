<template>
  <v-layout row>
    <v-flex md8 sm8 mr-2>
      <!-- 帖子标题内容板块 -->
      <v-card class="elevation-1">
        <v-breadcrumbs :items="breadcrumbs" divider=">"></v-breadcrumbs>
        <p class="overflow headline font-weight-bold px-3">{{postTitle}}</p>
        <span class="grey--text font-weight-medium ml-3">{{postPerson}}</span>
        <v-divider></v-divider>
        <div class="pl-3 pr-3">
          <v-layout row justify-center>
            <v-flex md12 sm12>
              <p class="overflow pl-3 pr-2">{{postContent}}</p>
            </v-flex>
          </v-layout>
          <v-layout row justify-center>
            <v-flex md6 sm6>
              <v-bottom-sheet
                v-model="post_sheet"
                inset>
                <template v-slot:activator>
                  <v-btn flat small class="grey--text">
                    <v-icon>reply</v-icon>回复
                  </v-btn>
                </template>
                <v-list class="pa-2">
                  <div><v-icon>reply</v-icon>&nbsp;&nbsp;添加一条新回复</div><br>
                  <v-textarea
                    v-model="reply_content"
                    :rules="[() => !!reply_content || '输入不能为空!']"
                    label="回复楼主"
                    required
                    flat
                    outline
                    placeholder="输入回复的内容"
                    rows=6>
                  </v-textarea>
                  <v-btn small @click="create_post_reply" class="font-weight-bold">回复</v-btn>
                  <v-btn small @click="cancle_post_sheet" class="font-weight-bold">取消</v-btn>
                </v-list>
              </v-bottom-sheet>
            </v-flex>
          </v-layout>
        </div>
      </v-card>
      <!-- 回复板块 -->
      <v-card class="mt-4">
        <div v-for="(item, index) in replyList" class="reply_box">
          <v-layout row justify-center>
            <v-flex md10 sm10>
              <div class="pl-5 pt-3">
                <span class="grey--text font-weight-medium">{{item.reply_from}}</span>
                <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{timeFormat(item.reply_time)}}</span>
                <p class="overflow mt-2">
                  <span v-show="isShow(item.reply_to)" class="grey--text">@{{item.reply_to}}&nbsp;&nbsp;</span>
                  {{item.reply_content}}
                </p>
              </div>
            </v-flex>
            <!-- 弹出输入框 -->
            <v-flex md2 sm2>
              <v-bottom-sheet v-model="item.reply_sheet" inset>
                <template v-slot:activator>
                  <v-btn flat small class="grey--text" @click="reply_reply(item.reply_from)">
                    <v-icon>{{item.reply_icon}}</v-icon>回复
                  </v-btn>
                </template>
                <v-list class="pa-2">
                  <div><v-icon>reply</v-icon>&nbsp;&nbsp;添加一条新回复</div><br>
                  <v-textarea
                    v-model="reply_content"
                    :rules="[() => !!reply_content || '输入不能为空!']"
                    :label= "reply_other"
                    flat
                    outline
                    placeholder="输入回复的内容"
                    rows=6>
                  </v-textarea>
                  <v-btn small @click="create_reply_reply(item.reply_from, index)" class="font-weight-bold">回复</v-btn>
                  <v-btn small @click="cancle_reply_sheet(index)" class="font-weight-bold">取消</v-btn>
                </v-list>
              </v-bottom-sheet>
            </v-flex>
          </v-layout>
          <!-- <v-divider v-if="index + 1 < replyList.length" :key="`divider-${index}`"></v-divider> -->
        </div>
      </v-card>
    </v-flex>
    <v-flex md4 sm4>
      <v-card>
        2222222222
      </v-card>
    </v-flex>
  </v-layout>
</template>

<script>
 export default{
   inject: ['reload'],
   data(){
     return {
       replyList: [],
       post_sheet: false,
       reply_content: "",
       reply_other: "",
       
       postPerson: "",
       postTitle: "",
       postTag: "",
       postContent: "",
       postId: 5,

       /* rules: {
        *   required: (value) => !!value || 'Required',
        * }, */
       
       breadcrumbs: [
         {
           text: 'Post',
           disabled: false,
           href: '/#/discuss'
         },
         {
           text: '闲聊灌水',
           disabled: false,
           href: '/#/discuss'
         }
       ]
     }
   },
   methods: {
     get_reply(){
       this.$axios.post("api/get_reply/", JSON.stringify(
         {"post_id": this.$route.params.id}
       )).then(res => {
         console.log(res.data)
         res = JSON.parse(res.data)
         var last = res.length
         
         this.postTitle = res[0].post_title
         this.postTag = res[0].post_tag
         this.postPerson = res[0].poster
         this.postContent = res[0].post_content

         sessionStorage.setItem("post_id", this.$route.params.id)
         sessionStorage.setItem("post_person", this.postPerson)
         sessionStorage.setItem("post_tag", this.postTag)
         sessionStorage.setItem("post_title", this.postTitle)
         sessionStorage.setItem("post_content", this.postContent)
         
         var replyFrom = res.slice(1,last).map(v => v.reply_from)
         var replyTo = res.slice(1,last).map(v => v.reply_to)
         var replyContent = res.slice(1,last).map(v => v.reply_content)
         var replyTime = res.slice(1,last).map(v => v.reply_time)
         var sheet = []
         for(var i=0; i<replyFrom.length; i++){
           sheet[i] = false
           this.replyList.push({
             reply_from: replyFrom[i],
             reply_to: replyTo[i],
             reply_content: replyContent[i],
             reply_time: replyTime[i],
             reply_icon: "reply",
             reply_sheet: sheet[i]
           })
         }
       }).catch(err => {
         console.log(err.data)
       })
     },
     create_post_reply(){
       if(!this.reply_content){
         this.$message({
           message: '输入不能为空！',
         });
       }else{
         this.$axios.post("api/create_post_reply/", JSON.stringify({
           "reply_content": this.reply_content,
           "reply_from": this.$store.state.userid,
           "reply_to": sessionStorage.getItem("post_person"),
           "reply_post": sessionStorage.getItem("post_id")
         })).then(res => {
           this.post_sheet = false
           this.reply_content = ""
           console.log(res.data)
           this.reload()
         }).catch(err => {
           console.log(err.data)
         })
       }
     },
     create_reply_reply(reply_to, index){
       if(!this.reply_content){
         this.$message({
           message: '输入不能为空！',
         });
       }else{
         this.$axios.post("api/create_reply_reply/", JSON.stringify({
           "reply_content": this.reply_content,
           "reply_from": this.$store.state.userid,
           "reply_to": reply_to,
           "reply_post": sessionStorage.getItem("post_id")
         })).then(res => {
           this.replyList[index].reply_sheet = false
           this.reply_content = ""
           console.log(res.data)
           this.reload()
         }).catch(err => {
           console.log(err.data)
         }) 
       }
     },
     cancle_post_sheet(){
       this.post_sheet = false;
     },
     cancle_reply_sheet(index){
       this.replyList[index].reply_sheet = false;
     },
     reply_reply(other){
       this.reply_other = "@" + other
     },
   },
   computed: {
     isShow(){
       return function(to){
         if(to == sessionStorage.getItem("post_person"))
           return false;
         else
           return true;
       }
     },
     timeFormat(){
       return function(reply_time) {
         //如果时间格式是正确的，那下面这一步转化时间格式就可以不用了
         /* var dateBegin = new Date(reply_time.replace(/-/g, "/")); *///将-转化为/，使用new Date
         var dateBegin = new Date(reply_time)
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
           timeString = dayDiff + " 天 "
         if(hours>0)
           timeString += hours + " 小时 "
         if(minutes>0)
           timeString += minutes + " 分钟前"
         else
           timeString += "刚刚"

         return timeString
       }
     }
   },
   /* watch: {
    *   '$route.path': function(newVal, oldVal){
    *     sessionStorage.removeItem("post_id")
    *     sessionStorage.removeItem("post_person")
    *     sessionStorage.removeItem("post_tag")
    *     sessionStorage.removeItem("post_title")
    *     sessionStorage.removeItem("post_content")
    *   }
    * }, */
   created(){
     this.get_reply()
   }
 }
</script>

<style scoped>
 .list_tile{
   border-bottom: 0.2px solid grey;
 }
 .overflow{
   word-wrap:break-word;
   word-break:break-all;
 }
 .reply_box{
   border-top: 0.1px solid #E0E0E0;
 }
</style>
