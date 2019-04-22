<template>
  <div class="thebody">
    <table class="table table-striped table-hover table-condensed">
      <thead>
        <tr align="center">
          <td></td>
          <td><h4>试题</h4></td>
          <td><h4>下载</h4></td></tr>
      </thead>
      <tbody> 
        <tr v-for="item in itemlist" :key="item.id">
          <td width="5%" align="center"><input type="checkbox"></td>
          <td width="80%">{{ item.quizText }}</td>
          <td width="10%" align="center"><span class="glyphicon glyphicon-download-alt" aria-hidden="true" @click="download(item.quizFilename)"></span></td>
        </tr>
      </tbody>
    </table>
    
  </div>
</template>

<script>
 export default{
   data(){
     return{
       itemlist: [
         {quizFilename: "", quizText: ""}
       ]
     }
   },
   methods: {
     show_quiz(){
       this.$axios.get("api/show_quiz/").then(res => {
         this.itemlist = JSON.parse(res.data)
         console.log(res.data)
       }).catch(err => {
         console.log(err)
       })
     },
     download(filename){
       this.$axios.post("api/download/", JSON.stringify({"filename": filename}), {responseType: 'blob'}).then(res => {
         var blob = res.data
         let url = window.URL.createObjectURL(blob)
         let link = document.createElement('a')
         link.style.display = 'none'
         link.href = url
         link.setAttribute('download', filename)
         document.body.appendChild(link)
         link.click()
       }).catch(err => {
         console.log(err)
       })
     }
   },
   created(){
     this.show_quiz()
   }
 }
</script>

<style scoped>
 .thebody{
   /* background-color: #f6f8fa; */
 }
 .glyphicon{
   cursor: pointer;
 }
</style>
