<template>
  <!-- 帖子标题内容板块 -->
  <div>
    <v-card class="elevation-1">
      <div class="px-4 py-4">
        <p class="overflow headline font-weight-bold">{{postTitle}}</p>
        <!-- px-3 pt-4 -->
        <div class="grey--text text--darken-2">
          <span class="font-weight-medium">{{postTag}} ●</span>
          <span class="font-weight-medium">{{postPerson}} ●</span>
          <span class="font-weight-medium">发布时间: {{postCreateTime}}</span>
        </div>
        <v-divider></v-divider>
        <div class="pl-3 pr-3">
          <v-layout row justify-center>
            <v-flex md12 sm12>
              <p class="overflow subheading">{{postContent}}</p> <!-- pl-3 pr-2 -->
            </v-flex>
          </v-layout>
          <v-layout row justify-center>
            <v-flex md3 sm3>
              <v-bottom-sheet
                v-model="post_sheet"
                inset>
                <template v-slot:activator>
                  <v-btn flat small class="body-2 font-weight-bold" color="primary">
                    <v-icon small>reply</v-icon>回复
                  </v-btn>
                </template>
                <v-list class="pa-2">
                  <div class="font-weight-bold body-2"><v-icon>reply</v-icon>&nbsp;&nbsp;添加一条新回复</div><br>
                  <v-textarea
                    v-model="reply_content"
                    label="回复楼主"
                    auto-grow
                    required
                    flat
                    outline
                    placeholder="输入回复的内容"
                    rows=6>
                  </v-textarea>
                  <v-btn small flat color="primary" @click="create_post_reply" class="body-2 btn-style">回复</v-btn>
                  <v-btn small flat color="primary" @click="cancle_post_sheet" class="body-2 btn-style">取消</v-btn>
                </v-list>
              </v-bottom-sheet>
            </v-flex>
            <v-flex md3 sm3>
              <v-btn flat small @click="collect_post" color="purple" v-if="true" class="body-2 font-weight-bold">
                <v-icon small>favorite</v-icon>加入收藏
              </v-btn>
              <v-btn flat small @click="collect_post" v-else>
                <v-icon small class="black--text">favorite</v-icon>取消收藏
              </v-btn>
            </v-flex>
          </v-layout>
        </div>
      </div>
    </v-card>
    <!-- 回复板块 -->
    <v-card class="mt-4">
      <div>
        <div v-for="(item, index) in replyList" :key="index" class="reply_box">
          <v-layout row justify-center align-center>
            <v-flex md10 sm10>
              <div class="pl-5 pt-3">
                <span class="grey--text text--darken-1 font-weight-medium">{{item.reply_from}}</span>
                <span class="caption grey--text text--darken-1 font-weight-medium">&nbsp;&nbsp;{{timeFormat(item.reply_time)}}</span>
                <p class="overflow mt-2 subheading">
                  <span v-show="isShow(item.reply_to)" class="grey--text">@{{item.reply_to}}&nbsp;&nbsp;</span>
                  {{item.reply_content}}
                </p>
              </div>
            </v-flex>
            <!-- 弹出输入框 -->
            <v-flex md2 sm2>
              <v-bottom-sheet v-model="item.reply_sheet" inset>
                <template v-slot:activator>
                  <v-btn flat small @click="reply_reply(item.reply_from)" color="primary" class="body-2 font-weight-bold">
                    <v-icon small>{{item.reply_icon}}</v-icon>回复
                  </v-btn>
                </template>
                <v-list class="pa-2">
                  <div class="font-weight-bold body-2"><v-icon>reply</v-icon>&nbsp;&nbsp;添加一条新回复</div><br>
                  <v-textarea
                    v-model="reply_content"
                    :label= "reply_other"
                    auto-grow
                    flat
                    outline
                    placeholder="输入回复的内容"
                    rows=6>
                  </v-textarea>
                  <v-btn small flat color="primary" @click="create_reply_reply(item.reply_from, index)" class="body-2 btn-style">回复</v-btn>
                  <v-btn small flat color="primary" @click="cancle_reply_sheet(index)" class="body-2 btn-style">取消</v-btn>
                </v-list>
              </v-bottom-sheet>
            </v-flex>
          </v-layout>
          <!-- <v-divider v-if="index + 1 < replyList.length" :key="`divider-${index}`"></v-divider> -->
        </div>
      </div>
    </v-card>
  </div>
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
       postId: 0,
       postCreateTime: null,
       postViewNum: null,
     }
   },
   methods: {
     collect_post(){
       this.$axios.post("api/collect_post/", JSON.stringify({
         "post_id": sessionStorage.getItem("post_id"),
         "user_id": this.$store.state.userid,
       })).then(res => {
         console.log(res.data)
         this.$message({
           message: res.data.msg
         })
       }).catch(err => {
         console.log(err.data)
       })
     },
     get_reply(){
       this.$axios.post("api/get_reply/", JSON.stringify(
         {"post_id": this.$route.params.id}
       )).then(res => {
         console.log(res.data)
         var res = JSON.parse(res.data)
         
         this.postTitle = res[0].post_title
         this.postTag = res[0].post_tag
         this.postPerson = res[0].poster
         this.postContent = res[0].post_content
         this.postCreateTime = res[0].post_create_time
         this.postViewNum = res[0].view_num

         sessionStorage.setItem("post_id", this.$route.params.id)
         sessionStorage.setItem("post_person", this.postPerson)
         sessionStorage.setItem("post_tag", this.postTag)
         sessionStorage.setItem("post_title", this.postTitle)
         sessionStorage.setItem("post_content", this.postContent)
         
         var replyFrom = res.slice(1).map(v => v.reply_from)
         var replyTo = res.slice(1).map(v => v.reply_to)
         var replyContent = res.slice(1).map(v => v.reply_content)
         var replyTime = res.slice(1).map(v => v.reply_time)
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
         if(!this.$store.state.islogin){
           this.$message({
             message: '登录后才能进行回复！',
           });
           this.post_sheet = false
           this.reply_content = ""
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
       }
     },
     create_reply_reply(reply_to, index){
       if(!this.reply_content){
         this.$message({
           message: '输入不能为空！',
         });
       }else{
         if(!this.$store.state.islogin){
           this.$message({
             message: '登录后才能进行回复！',
           });
           this.replyList[index].reply_sheet = false;
           this.reply_content = ""
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
   border-bottom: 0.1px solid #E0E0E0;
 }
</style>
