<template>
  <v-flex xs12 sm12 fill-height>
    <div class="text-xs-left" style="display:inline;">
      <v-menu offset-y z-index="2">
        <template v-slot:activator="{ on }">
          <v-btn color="primary" dark v-on="on" class="font-weight-bold">所有分类</v-btn>
        </template>
        <v-list dense>
          <v-list-tile
            v-for="(item, index) in topic"
            :key="index"
            @click=""
          >
            <v-list-tile-title>{{ item.title }}</v-list-tile-title>
          </v-list-tile>
        </v-list>
      </v-menu>
    </div>
    
  </v-flex>
</template>


<script>
 export default {
   data () {
     return {
       topic: [
         { title: 'word讨论 x 22' },
         { title: 'excel讨论 x 12' },
         { title: 'ppt讨论 x 31' },
         { title: '等级考试 x 56' },
         { title: '办公技巧 x 4' },
         { title: '闲聊灌水 x 104' },
         { title: '网站反馈 x 13' },
       ],
     }
   }
 }
</script>

<style scoped>
</style>
