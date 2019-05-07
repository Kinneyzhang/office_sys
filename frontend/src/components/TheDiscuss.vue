<template>
  <v-card class="elevation-1">
    <v-container fluid>
      <div class="pa-3 disscussInfo" style="background-color:#d1f0ff;" v-show="false">
        <v-icon class="cursor" @click="closeBox">close</v-icon>
        <p class="subheading">{{userName}}, 你好</p>
        <p>此为讨论交流板块。在这里你可以分享自己的观点，提出做题过程中的疑惑，积极讨论和office操作题及相关话题。</p>
        <p>我们欢迎您积极发帖，也欢迎积极解答其他用户的疑惑，营造一个良好的讨论氛围。</p>
        <p>在提问之前，请检查自己是否已经做到如下两点：</p>
        <p class="ml-3">1. 在网上搜索，试着自己找答案；</p>
        <p class="ml-3">2. 在本站内搜索，是否有类似问题；</p>
        <p>关于提问的艺术，请参考：https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md</p>
      </div>
      <v-layout row>
        <v-flex xs1 sm1>
          <v-menu offset-y z-index="2">
            <template v-slot:activator="{ on }">
              <v-btn color="primary" dark v-on="on" class="font-weight-bold">所有分类</v-btn>
            </template>
            <v-list dense>
              <v-list-tile
                v-for="(item, index) in tagList"
                :key="index"
                @click=""
              >
                <v-list-tile-title>{{ item.tagName }} x {{ item.tagNum }}</v-list-tile-title>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
        <v-flex xs1 sm1 md1 offset-xs9>
          <div class="text-xs-center">
            <v-bottom-sheet v-model="sheet" inset>
              <template v-slot:activator>
                <v-btn color="purple" dark><v-icon>add</v-icon>发表帖子</v-btn>
              </template>
              <v-list class="pa-2">
                <div class="mb-2"><v-icon>reply</v-icon>&nbsp;&nbsp;创建新的帖子</div><br>
                <v-textarea
                  v-model="postTitle"
                  label="帖子标题"
                  flat
                  outline
                  auto-grow
                  autofocus
                  rows=1>
                </v-textarea>
                <v-select
                  v-model="postTag"
                  label="选择标签"
                  :items="computedTag"
                  outline
                  flat
                  single-line
                ></v-select>
                <v-textarea
                  v-model="postContent"
                  label="帖子内容"
                  flat
                  outline
                  placeholder="在输入内容前，请先选择合适的标签类型"
                  rows=6>
                </v-textarea>
                <div id="editor"></div>
                <v-btn small @click="create_post" class="font-weight-bold">创建主题</v-btn>
                <v-btn small @click="cancle" class="font-weight-bold">取消</v-btn>
              </v-list>
            </v-bottom-sheet>
          </div>
        </v-flex>
      </v-layout>
      
      <v-layout>
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
      </v-layout>
    </v-container>
  </v-card>
</template>


<script>
 export default {
   inject: ['reload'],
   data () {
     return {
       postList: [],
       userName: this.$store.state.username,
       isShow: true,
       tagList: [],
       sheet: false,
       postTitle: "",
       postTag: "",
       postContent: ""
     }
   },
   computed: {
     computedTag(){
       var tag = this.tagList.map(v => v.tagName);
       return tag;
     },
     link(){
       return function(post_id){
         return "/post/" + post_id
       }
     },
   },
   methods: {
     timeFormat(time){
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
     },
     create_post(){
       this.$axios.post("api/create_post/", JSON.stringify({
         "postTitle": this.postTitle,
         "postTag": this.postTag,
         "postContent": this.postContent,
         "postUser": this.$store.state.username
       })).then( res => {
         console.log(res.data)
         this.sheet = false;
         this.reload()
       }).catch( err => {
         console.log(err.data)
       })
     },
     cancle(){
       this.sheet = false;
     },
     closeBox(){
       this.isShow = false;
     },
     get_post_list(){
       this.$axios.get("api/get_post_list/").then(res => {
         console.log(res.data)
         res = JSON.parse(res.data)
         
         var tagArray = res.tag_list
         this.tagList = tagArray
         
         var postArray = res.post_list
         var postId = postArray.map(v => v.post_id)
         var postPerson = postArray.map(v => v.poster)
         var postTitle = postArray.map(v => v.post_title)
         var postTag = postArray.map(v => v.post_tag)
         var postContent = postArray.map(v => v.post_content)
         var replyNum = postArray.map(v => v.reply_num)
         var viewNum = postArray.map(v => v.view_num)
         var modifyTime = postArray.map(v => v.post_modify_time)
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
     /* expandPost(thisId){
      *   this.reload()
      *   this.$router.push({ name: 'discussPost', params: {'id': thisId}})
      * }, */
   },
   created(){
     this.get_post_list()
   },
 }
</script>

<style scoped>
 .disscussInfo{
   position: relative;
 }
 .cursor{
   cursor: pointer;
   position: absolute;
   right: 10px;
   top: 8px;
 }
</style>
