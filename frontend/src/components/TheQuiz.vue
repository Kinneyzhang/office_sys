<template>
  <v-card class="elevation-1">
    <v-container fluid>
      <v-layout row>
        <v-flex sm3 md1>
          <v-menu offset-y z-index="1">
            <template v-slot:activator="{ on }">
              <v-btn small flat color="primary" v-on="on" class="btn-style subheading">试题分类<v-icon>arrow_drop_down</v-icon></v-btn>
            </template>
            <v-list dense>
              <v-list-tile
                v-for="(item, index) in typeList"
                :key="index"
                @click="typeLink(item)"
              >
                <span>{{item}}练习</span>
              </v-list-tile>
            </v-list>
          </v-menu>
        </v-flex>
        <v-flex sm3 md1 offset-md1 offset-sm1>
          <div>
            <v-btn small flat color="primary" class="btn-style subheading" @click="latestQuiz">最新发布</v-btn>
          </div>
        </v-flex>
      </v-layout>
      <v-layout>
        <router-view></router-view>
      </v-layout>
    </v-container>
  </v-card>
</template>

<script>
 export default {
   data () {
     return {
       typeList: [],
     }
   },
   methods: {
     typeLink(type){
       this.$router.push({path:'/quiz/' + type})
     },
     latestQuiz(){
       this.$router.push({path:'/quiz/'})
     },
     get_type_list(){
       this.$axios.get("api/get_type_list/").then(res => {
         console.log(res.data)
         this.typeList = JSON.parse(res.data)
       }).catch(err => {
         console.log(err.data)
       })
     },
   },
   created(){
     this.get_type_list()
   }
 }
</script>
