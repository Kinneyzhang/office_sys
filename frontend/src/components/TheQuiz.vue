<template>
  <v-flex xs12 sm12 fill-height>
    <v-data-table
      expand
      hide-actions
      v-model="selected"
      :headers="headers"
      :items="quizlist"
      class="elevation-0"
      select-all
      item-key="quiz_id"
      :pagination.sync="pagination"
    >
      <template v-slot:items="props">
        <td><v-checkbox
              v-model="props.selected"
              primary
              hide-details
            ></v-checkbox></td>
        <td>{{ props.item.quiz_id }}</td>
        <td class="text-xs-left">
          {{ props.item.quiz_show }}
          <el-popover
            placement="bottom-left"
            width="400"
            trigger="click"
            :content= "props.item.quiz_text">
            <el-button size="mini" type="text" round plain slot="reference">预览</el-button>
          </el-popover>
        </td>
        <td class="text-xs-right">{{ props.item.exer_num }}</td>
        <td class="text-xs-right">{{ props.item.accuracy }}</td>
        <td @click="download(props.item.quiz_id)"><v-icon>{{props.item.icon}}</v-icon></td>
      </template>
    </v-data-table>
    <div class="text-xs-center pt-2">
      <v-pagination v-model="pagination.page" :length="pages"></v-pagination>
    </div>
  </v-flex>
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
       this.$axios.post("api/download/", JSON.stringify({"quiz_id": quizId}), {responseType: 'blob'}).then(res => {
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
     pages () {
       if (this.pagination.rowsPerPage == null ||
           this.pagination.totalItems == null
       ) return 0

       return Math.ceil(this.pagination.totalItems / this.pagination.rowsPerPage)
     }
   }
 }
</script>
