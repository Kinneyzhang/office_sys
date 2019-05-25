
<template>
  <!-- <post-list :data="postList"></post-list> -->
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
          :to="tagLink(scope.row.tag)"
          tag="span"
          class="font-weight-bold pointer grey--text grey lighten-3"
          style="font-size:13px;"
        >{{scope.row.tag}}</router-link>
        <span v-html="scope.row.divider" class="grey--text caption"></span>
        <router-link
          to = "/discuss"
          tag="span"
          class="font-weight-bold pointer"
          style="font-size:13px;"
        >{{scope.row.poster}}</router-link>
        <span v-html="scope.row.divider" class="grey--text caption"></span>
        <router-link
          to = "/discuss"
          tag="span"
          class="font-weight-bold grey--text"
          style="font-size:10px;"
        >创建于&nbsp;{{timeFormat(scope.row.create)}}</router-link>
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
      label="活动"
      align="center"
      min-width="10%">
      <template slot-scope="scope">
        <span>{{timeFormat(scope.row.active)}}</span>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
 export default {
   data() {
     return{
       postList: []
     }
   },
   computed: {
     link(){
       return function(post_id){
         return "/post/" + post_id
       }
     },
     tagLink(){
       return function(post_tag){
         return "/post/tag/" + post_tag
       }
     },
     timeFormat(){
       return (time) => {
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
     get_tag_post(){
       this.$axios.post("api/get_tag_post/", JSON.stringify({
         "tag_name": this.$route.params.tagName,
       })).then(res => {
         this.postList = []
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
         var createTime = res.map(v => v.post_create_time)
         
         for(var i=0; i<postPerson.length; i++){
           this.postList.unshift({
             id: postId[i],
             poster: postPerson[i],
             title: postTitle[i],
             tag: postTag[i],
             reply: replyNum[i],
             view: viewNum[i],
             active: modifyTime[i],
             create: createTime[i],
             divider: "&nbsp;●&nbsp;"
           })
         }
       }).catch(err => {
         console.log(err.data)
       })
     },
   },
   created(){
     this.get_tag_post()
   },
   watch:{
     '$route': 'get_tag_post'
   }
 }
</script>
