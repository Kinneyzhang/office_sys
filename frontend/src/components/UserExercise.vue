<template>
  <div>
    <v-expansion-panel
      class="elevation-0"
      expand
    >
      <v-expansion-panel-content
        v-for="(item, index) in count_list"
        :key="index"
      >
        <template v-slot:actions>
          <v-icon small color="warning" v-if="!item.correct_status">info</v-icon>
          <v-icon small color="primary" v-else>check_circle</v-icon>
        </template>
        <template v-slot:header>
          <div>
            <span class="font-weight-medium">{{item.quiz_id}}</span>
            <span class="caption grey--text font-weight-medium">&nbsp;&nbsp;{{item.upload_time}}&nbsp;提交答案</span>
          </div>
        </template>
        <div class="px-4 pb-3">
          <div v-if="!item.correct_status">
            <span class="grey--text darken-3">该试题尚未批阅</span>

            <v-bottom-sheet v-model="item.correct_sheet" inset>
              <template v-slot:activator>
                <v-btn small flat color="primary" class="btn-style">模拟批阅</v-btn>
              </template>
              <v-list class="pa-2">
                <div class="mb-2"><v-icon>reply</v-icon>&nbsp;&nbsp;模拟批阅</div><br>
                <v-textarea
                  v-model="quiz_score"
                  label="得分"
                  flat
                  outline
                  auto-grow
                  autofocus
                  rows=1>
                </v-textarea>
                <v-textarea
                  v-model="correct_info"
                  label="批阅反馈"
                  flat
                  outline
                  rows=3>
                </v-textarea>
                <v-btn small flat color="primary" class="btn-style body-2" @click="correct_quiz(item.record_id)">批阅</v-btn>
                <v-btn small flat color="primary" class="btn-style body-2" @click="cancle_sheet(index)">取消</v-btn>
              </v-list>
            </v-bottom-sheet>
          </div>
          <div v-else>
            <span>得分：{{item.quiz_score}}</span><br>
            <span>提示信息：{{item.result_info}}</span>
          </div>
        </div>
      </v-expansion-panel-content>
    </v-expansion-panel>
    <div class="text-xs-center">
      <v-pagination
        v-model="page"
        :length="count_length"
        prev-icon="mdi-menu-left"
        next-icon="mdi-menu-right"
      ></v-pagination>
    </div>
  </div>
</template>

<script>
 export default {
   inject: ['reload'],
   data(){
     return {
       quiz_score: null,
       correct_info: "",
       exer_list: [],
       page: 1,
     }
   },
   computed: {
     count_list(){
       return this.exer_list.slice(eval(this.page*6-6),this.page*6)
     },
     count_length(){
       return Number(this.exer_list.length/6+1)
     }
   },
   methods: {
     get_quiz_record(){
       this.$axios.post("api/get_quiz_record/", JSON.stringify({
         "username": this.$store.state.username,
       })).then(res => {
         /* console.log(res.data) */
         res = JSON.parse(res.data)
         var quizId = res.map(v => v.quiz_id)
         var quizText = res.map(v => v.quiz_text)
         var quizType = res.map(v => v.quiz_type)
         var uploadStatus = res.map(v => v.upload_status)
         var uploadTime = res.map(v => v.upload_time)
         var correctStatus = res.map(v => v.correct_status)
         var quizScore = res.map(v => v.quiz_score)
         var resultInfo = res.map(v => v.result_info)
         var recordId = res.map(v => v.record_id)
         var correct_sheet = []
         
         for(var i=0; i<quizId.length; i++){
           if(uploadStatus[i] == true){
             correct_sheet.push(false)
             this.exer_list.unshift({
               quiz_id: quizId[i],
               quiz_text: quizText[i],
               upload_time: uploadTime[i],
               quiz_score: quizScore[i],
               result_info: resultInfo[i],
               correct_status: correctStatus[i],
               record_id: recordId[i],
               correct_sheet: correct_sheet[i],
             }) 
           }
         }
       }).catch(err => {
         console.log(err.data)
       })
     },
     //模拟批阅相关方法
     cancle_sheet(i){
       this.exer_list[i].correct_sheet = false
     },
     correct_quiz(record_id){
       if(!this.quiz_score || !this.correct_info){
         this.$message({
           message: "输入不能为空！"
         })
       }else{
         this.$axios.post("api/correct_quiz/", JSON.stringify({
           "record_id": record_id,
           "quiz_score": this.quiz_score,
           "correct_info": this.correct_info,
         })).then(res => {
           console.log(res.data)
           this.correct_sheet = false
           this.quiz_score = null
           this.correct_info = null
           this.reload()
         }).catch(err =>{
           console.log(err.data)
         })
       }
     },
   },
   created(){
     this.get_quiz_record()
   }
 }
</script>
