<template>
  <v-flex xs12 sm12 fill-height>
    <v-card class="elevation-0">
      <v-container fluid>
        <div class="pa-3" style="background-color:#d1f0ff;">
          <p class="subheading">各位 Emacs 道友，大家好。</p>
          <p>在通过电邮、新闻组或者聊天室提出技术问题前，请检查你有没有做到：</p>
          <p class="ml-3">1. 阅读手册，试着自己找答案。（C-h C-h， 有问题，问 Emacs）；</p>
          <p class="ml-3">2. 在网上搜索；</p>
          <p class="ml-3">3. 使用 Emacs China 站内搜索（本论坛的站内搜索做的相当不错，中英文都支持）。</p>
          <p>关于提问的艺术，完整版本请参考：https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way/blob/master/README-zh_CN.md</p>
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
                  <v-btn color="purple" dark><v-icon>add</v-icon>发表主题</v-btn>
                </template>
                <v-list class="pa-2">
                  <v-subheader>创建新的主题</v-subheader>
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
                    rows=8>
                  </v-textarea>
                  <v-btn @click="create_post" class="font-weight-bold">创建主题</v-btn>
                  <v-btn @click="cancle" class="font-weight-bold">取消</v-btn>
                </v-list>
              </v-bottom-sheet>
            </div>
          </v-flex>
        </v-layout>
        
        <v-layout>
          <el-table
            :data="postInfo"
            style="width: 100%">
            <el-table-column
              label="主题"
              min-width="70%">
              <template slot-scope="scope">
                <span v-html="scope.row.author"></span><br>
                <span v-html="scope.row.title"></span><br>
                <span v-html="scope.row.reply"></span>
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
  </v-flex>
</template>


<script>
 export default {
   data () {
     return {
       tagList: [],
       postInfo: [
         /* {
          *   title: '',
          *   reply: '20',
          *   view: '122',
          *   active: '10'
          * } */
       ],
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
     }
   },
   methods: {
     create_post(){
       this.$axios.post("api/create_post/", JSON.stringify({
         "postTitle": this.postTitle,
         "postTag": this.postTag,
         "postContent": this.postContent,
         "postUser": this.$store.state.username
       })).then( res => {
         console.log(res.data)
         this.sheet = false;
       }).catch( err => {
         console.log(err.data)
       })
     },
     cancle(){
       this.sheet = false;
     },
     get_post(){
       this.$axios.get("api/get_post/").then(res => {
         console.log(res.data)
       }).catch(err => {
         console.log(err.data)
       })
     },
     get_tagNum(){
       this.$axios.get("api/get_tagNum/").then(res => {
         res = JSON.parse(res.data)
         this.tagList = res
       }).catch(err => {
         console.log(err.data)
       })
     }
   },
   created(){
     this.get_post()
     this.get_tagNum()
   }
 }
</script>

<style scoped>
</style>
