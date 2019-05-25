<template>
  <div style="width:100%">
    <div class="py-4">
      <span class="font-weight-medium title"><v-icon>subtitles</v-icon>&nbsp;{{quizType}}&nbsp;操作题</span><hr>
      <span class="ml-2 body-2 font-weight-bold">知识点专项</span>
      <v-btn class="ma-2 font-weight-bold" small round flat color="primary" v-for="(item, index) in knowledgelist" :key="index" @click="pointLink(item)">
        {{item}}
      </v-btn>
    </div>
    <div>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
 export default {
   data () {
     return {
       knowledgelist: [],
     }
   },
   methods: {
     get_knowledge_point(){
       this.$axios.post("api/get_knowledge_point/", JSON.stringify({
         "quiz_type": this.quizType,
       })).then(res => {
         console.log(res.data)
         this.knowledgelist = JSON.parse(res.data)
       }).catch(err => {
         console.log(err.data)
       })
     },
     pointLink(point){
       this.$router.push({path: '/quiz/' + this.quizType + '/' + point})
     },
   },
   created(){
     this.get_knowledge_point()
   },
   watch: {
     '$route': 'get_type_quiz',
     '$route': 'get_knowledge_point',
   },
   computed: {
     userid(){
       return this.$store.state.userid
     },
     quizType(){
       return this.$route.params.quizType
     }
   },
 }
</script>
