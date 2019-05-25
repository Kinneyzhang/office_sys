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
        <v-flex xs1 sm3 md1>
          <v-menu offset-y z-index="1">
            <template v-slot:activator="{ on }">
              <v-btn small flat color="primary" v-on="on" class="btn-style body-2">主题分类<v-icon small>arrow_drop_down</v-icon></v-btn>
            </template>
            <v-list dense>
              <v-list-tile
                v-for="(item, index) in tagList"
                :key="index"
                @click="tagLink(item.tagName)"
              >
                <span> {{ item.tagName }} x {{ item.tagNum }}</span>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
        <v-flex sm3 md1 offset-sm1>
          <v-btn flat small color="primary" class="btn-style body-2" @click="latestPost">最近活动</v-btn>
        </v-flex>
        <v-flex xs1 sm3 md1 offset-sm1>
          <div class="text-xs-center">
            <v-bottom-sheet v-model="sheet" inset>
              <template v-slot:activator>
                <v-btn small flat color="purple" class="btn-style body-2"><v-icon>add</v-icon>创建主题</v-btn>
              </template>
              <v-list class="px-3">
                <div class="mt-2 font-weight-bold body-2"><v-icon>reply</v-icon>&nbsp;&nbsp;创建新的主题</div><br>
                <v-textarea
                  v-model="postTitle"
                  label="主题标题"
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
                  label="主题内容"
                  flat
                  outline
                  placeholder="在输入内容前，请先选择合适的标签类型"
                  rows=6>
                </v-textarea>
                <div id="editor"></div>
                <v-btn small flat color="primary" @click="create_post" class="btn-style body-2">创建主题</v-btn>
                <v-btn small flat color="primary" @click="cancle" class="btn-style body-2">取消</v-btn>
              </v-list>
            </v-bottom-sheet>
          </div>
        </v-flex>
      </v-layout>
      <v-layout>
        <router-view></router-view>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
 export default {
   inject: ['reload'],
   data () {
     return {
       tagList: [],
       sheet: false,
       postTitle: "",
       postTag: "",
       postContent: "",
       isShow: true,
     }
   },
   computed: {
     computedTag(){
       var tag = this.tagList.map(v => v.tagName);
       return tag;
     },
     userName(){
       return this.$store.state.username
     }
   },
   methods: {
     latestPost(){
       this.$router.push({path: '/post/latest'})
     },
     tagLink(tag){
       this.$router.push({name:'tagList', params: {tagName: tag}});
     },
     create_post(){
       if(!this.$store.state.username){
         this.$message({
           message: '请登录后再发帖！',
         })
       }else if(!this.postTitle || !this.postTag || !this.postContent){
         this.$message({
           message: '输入不能为空！',
         })
       }else{
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
       }
     },
     cancle(){
       this.sheet = false;
       this.postTitle = "";
       this.postTag = "";
       this.postContent = "";
     },
     closeBox(){
       this.isShow = false;
     },
     get_tag_list(){
       this.$axios.get("api/get_tag_list/").then(res => {
         console.log(res.data)
         this.tagList = JSON.parse(res.data)
       }).catch(err => {
         console.log(err.data)
       })
     },
   },
   created(){
     this.get_tag_list()
   }
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
