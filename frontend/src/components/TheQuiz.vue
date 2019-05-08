<template>
  <v-card class="elevation-1">
    <el-table
      :data="quizlist"
      style="width:100%"
    >
      <el-table-column
        label="编号"
        prop="quiz_id"
        min-width="8%"
        align="center"
      ></el-table-column>
      <el-table-column
        label="试题"
        min-width="68%"
        align="center"
      >
        <template slot-scope="scope">
          <div class="font-weight-medium">
            {{scope.row.quiz_show}}
            <span><v-btn flat small color="info">预览</v-btn></span>
          </div>
        </template>
      </el-table-column>
      <el-table-column
        label="练习"
        prop="exer_num"
        min-width="8%"
        align="center"
      ></el-table-column>
      <el-table-column
        label="AC%"
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
       headers: [
         { text: '编号', align: 'left', value: 'quiz_id' },
         { text: '试题', align: 'center', sortable: false, value: 'quiz_show' },
         { text: '练习', align: 'left', value: 'exer_num' },
         { text: 'AC%', align: 'left', value: 'accuracy' },
         { text: '下载', align: 'left', sortable: false, value: 'icon'},
       ],
       quizlist: []
     }
   },
   methods: {
     show_quiz(){
       this.$axios.get("api/show_quiz/").then(res => {
         console.log(res.data)
         res = JSON.parse(res.data)
         var quizId = res.map(v => v.quizId)
         var quizText = res.map(v => v.quizText)
         var temp = ""
         var quizStr = []
         var quizShow = []
         for(var i=0; i<quizId.length; i++){
           temp = quizText[i].slice(0,75) + " . . . . . ."
           quizShow.push(temp)
         }
         for(var i=0; i<quizId.length; i++){
           temp = quizText[i].split('；').join('\n')
           quizStr.push(temp)
           console.log(quizStr[i])
         }
         for(var i=0; i<quizId.length; i++){
           this.quizlist.push(
             {quiz_id: quizId[i], quiz_show: quizShow[i], quiz_text: quizStr[i], exer_num: 5, accuracy: '80%', icon: 'get_app'})
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
     this.show_quiz()
   },
   computed: {
     userid(){
       return this.$store.state.userid
     }
   },
 }
</script>
