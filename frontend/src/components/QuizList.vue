<template>
  <el-table
    :data="quizlist"
    style="width:100%"
  >
    <el-table-column
      label="编号"
      prop="quiz_id"
      min-width="10%"
      align="center"
    ></el-table-column>
    <el-table-column
      label="知识点"
      min-width="30%"
      align="center"
      prop="knowledge_point"
    ></el-table-column>
    <el-table-column
      label="题目预览"
      min-width="30%"
      align="center"
    >
      <template slot-scope="scope">
        <v-menu bottom offset-y z-index="10">
          <template v-slot:activator="{ on }">
            <v-btn small flat v-on="on" color="primary">点击预览</v-btn>
          </template>
          <div class="quiz_text pa-3" v-html="scope.row.quiz_text"></div>
        </v-menu>
      </template>
    </el-table-column>
    <el-table-column
      label="已练习"
      prop="upload_num"
      min-width="10%"
      align="center"
    ></el-table-column>
    <el-table-column
      label="正确率"
      prop="accuracy"
      min-width="10%"
      align="center"
    ></el-table-column>
    <el-table-column
      label="下载"
      min-width="10%"
      align="center"
    >
      <template slot-scope="scope">
        <v-icon class="pointer" @click="download(scope.row.quiz_id)">{{scope.row.icon}}</v-icon>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
 export default {
   data () {
     return {
       quizlist: []
     }
   },
   methods: {
     get_quiz(){
       this.$axios.get("api/get_quiz/").then(res => {
         console.log(res.data)
         res = JSON.parse(res.data)
         var quizId = res.map(v => v.quizId)
         var quizText = res.map(v => v.quizText)
         var uploadNum = res.map(v => v.uploadNum)
         var accuracy = res.map(v => v.accuracy)
         var knowledgePoint = res.map(v => v.knowledgePoint)

         var knowledge_point = []
         var quizStr = []
         for(var i=0; i<quizId.length; i++){
           quizStr.push(quizText[i].split('；').join('；<br>'))
           console.log(accuracy[i])
         }
         for(var i=0; i<quizId.length; i++){
           knowledge_point.push(knowledgePoint[i].map(v => v.knowledgePoint))
           this.quizlist.unshift({
             quiz_id: quizId[i],
             quiz_text: quizStr[i],
             upload_num: uploadNum[i],
             accuracy: Number(accuracy[i]*100).toFixed(2) + '%',
             knowledge_point: knowledge_point[i].join('/'),
             icon: 'get_app'
           })
         }
         /* console.log(res.data) */
       }).catch(err => {
         console.log(err)
       })
     },
     download(quizId){
       if(!this.$store.state.islogin){
         this.$message({
           message: '登录后才能下载试题！',
         });
       }else{
         this.$axios.post("api/download/", JSON.stringify({
           "quiz_id": quizId,
           "user_id": this.userid,
         }),{
           responseType: 'blob'
         }).then(res => {
           var blob = res.data
           let url = window.URL.createObjectURL(blob)
           let link = document.createElement('a')
           link.style.display = 'none'
           link.href = url
           link.setAttribute('download', quizId+'.zip')
           document.body.appendChild(link)
           link.click()
         }).catch(err => {
           console.log(err)
         }) 
       }
     },
   },
   created(){
     this.get_quiz()
   },
   computed: {
     userid(){
       return this.$store.state.userid
     }
   },
 }
</script>

<style>
 .quiz_text{
   width: 400px;
   background-color: white;
 }
</style>
