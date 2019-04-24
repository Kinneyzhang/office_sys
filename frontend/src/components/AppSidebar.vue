<template>
  <v-navigation-drawer
    v-model="drawer"
    app
    clipped
    floating
    width="250"
  >
    <v-layout
      class="fill-height"
      tag="v-list"
      column
    > 
      <v-subheader class="mt-3 grey--text text--darken-1">系统选项</v-subheader> 
      <v-list-tile v-for="item in items" :key="item.text" @click="">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-content>
          <v-list-tile-title>
            {{ item.text }}
          </v-list-tile-title>
        </v-list-tile-content>
      </v-list-tile>
      <v-subheader class="mt-3 grey--text text--darken-1">综合练习</v-subheader>
      <v-list>
        <v-list-tile v-for="item in items2" :key="item.text" avatar @click="">
          <v-list-tile-action>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-tile-action>
          <v-list-tile-title v-text="item.text"></v-list-tile-title>
        </v-list-tile>
      </v-list>
      <v-subheader class="mt-3 grey--text text--darken-1">专项练习</v-subheader>
      <v-list-tile v-for="item in items3" :key="item.text" avatar @click="">
        <v-list-tile-action>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-tile-action>
        <v-list-tile-title v-text="item.text"></v-list-tile-title>
      </v-list-tile>
    </v-layout>
  </v-navigation-drawer>
</template>

<script>
 export default {
   data: () => ({
     items: [
       { icon: 'list_alt', text: '练习题库' }, 
       { icon: 'publish', text: '讨论交流' },  //展示最近下载的题目，以及对应的上传接口
       { icon: 'search', text: '考试真题' },  //智能推荐在这推荐
     ],
     items2: [
       { icon: 'trending_up', text: '练习记录' },
       { icon: 'watch_later', text: '下载记录' },
       { icon: 'subscriptions', text: '查看结果' },
     ],
     items3: [
       { icon: 'trending_up', text: 'Word专项' },
       { icon: 'watch_later', text: 'Excel专项' },
       { icon: 'subscriptions', text: 'PPT专项' },
     ]
   }),
   computed: {
     drawer(){
       return this.$store.state.drawer
     }
   }
 }
</script>
