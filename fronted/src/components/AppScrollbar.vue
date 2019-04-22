<template>
  <ul class="list-group">
    <li class="list-group-item title" style="font-size: 14px;">个人信息</li>
    <li class="list-group-item title">专项练习</li>
    <li class="list-group-item sub-title" @click="show('word')">&nbsp;&nbsp;&nbsp;◎ Word</li>
    <li class="list-group-item content" v-show="isShowWord" v-for="item in wordlist" :key="item">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;● {{item}}</li>
    
    <li class="list-group-item sub-title" @click="show('excel')">&nbsp;&nbsp;&nbsp;◎ Excel</li>
    <li class="list-group-item content" v-show="isShowExcel" v-for="item in excellist">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;● {{item}}</li>
    
    <li class="list-group-item title">综合练习</li>
    <li class="list-group-item sub-title">&nbsp;&nbsp;&nbsp;◎ Word</li>
    <li class="list-group-item sub-title">&nbsp;&nbsp;&nbsp;◎ Excel</li>
  </ul>

</template>

<script>
 export default{
   data(){
     return{
       wordlist: [
         '字体', '段落', '页面', '图片', '表格', '分栏', '查找替换', '页眉页脚'
       ],
       excellist: [
         '单元格', '行列', '公式计算', '筛选排序'
       ],
       isShowWord: false,
       isShowExcel: false
     }
   },
   methods: {
     show(type){
       if(type == 'word')
         this.isShowWord = !this.isShowWord
       else
         this.isShowExcel = !this.isShowExcel
     }
   }
 }
</script>

<style scoped>
 div{ /* 文字不可被选中 */
   -webkit-user-select:none;
   -moz-user-select:none;
   -ms-user-select:none;
   user-select:none;
 }
 ul{
   padding: 0;
   margin: 0;
   list-style: none;
 }

 .title{
   font-weight: bold;
   font-size: 13px;
 }
 
 .sub-title{
   color: #0062d9;
   cursor: pointer;
   font-size: 12px;
   font-weight: normal;
 }
 .sub-title:hover{
   -webkit-filter:brightness(1); /* 兼容不同浏览器 */
   -o-filter:brightness(1);
   -moz-filter:brightness(1);
   filter:brightness(0.9); /* 设置亮度值，范围：0-1 */
 }
 
 .content{
   color: #0062d9;
   cursor: pointer;
   font-size: 12px;
   font-weight: normal;
 }
 .content:hover{
   -webkit-filter:brightness(1); /* 兼容不同浏览器 */
   -o-filter:brightness(1);
   -moz-filter:brightness(1);
   filter:brightness(0.9); /* 设置亮度值，范围：0-1 */
 }
</style>
