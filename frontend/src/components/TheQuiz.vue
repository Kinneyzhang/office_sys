<template>
  <v-card class="elevation-1">
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
        label="试题"
        min-width="66%"
        align="left"
      >
        <template slot-scope="scope">
          <div class="font-weight-medium" v-html="scope.row.quiz_text"></div>
          <!-- <span><v-btn flat small color="info">预览</v-btn></span> -->
        </template>
      </el-table-column>
      <el-table-column
        label="已练习"
        prop="upload_num"
        min-width="8%"
        align="center"
      ></el-table-column>
      <el-table-column
        label="正确率"
        prop="accuracy"
        min-width="8%"
        align="center"
      ></el-table-column>
      <el-table-column
        label="下载"
        min-width="8%"
        align="center"
      >
        <template slot-scope="scope">
          <v-icon class="pointer" @click="download(scope.row.quiz_id)">{{scope.row.icon}}</v-icon>
        </template>
      </el-table-column>
    </el-table>
  </v-card>
</template>

<script>
 export default {
   data () {
     return {
       search: '',
       pagination: {},
       selected: [],
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
           /* console.log(quizStr[i]) */
         }
         for(var i=0; i<quizId.length; i++){
           knowledge_point = knowledgePoint[i].map(v => v.knowledgePoint)
           this.quizlist.push({
             quiz_id: quizId[i],
             quiz_text: quizStr[i],
             upload_num: uploadNum[i],
             accuracy: accuracy[i]*100 + '%',
             knowledge_point: knowledge_point[i],
             icon: 'get_app'
           })
         }
         /* console.log(res.data) */
       }).catch(err => {
         console.log(err)
       })
     },
     download(quizId){
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
