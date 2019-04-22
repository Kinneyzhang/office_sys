<template>
  <v-flex xs12 sm12 fill-height>
    <v-card>
      <v-img
        src= "https://cn.bing.com/th?id=OHR.Paepalanthus_ZH-CN2626725103_1920x1080.jpg&rf=LaDigue_1920x1080.jpg&pid=hp"
        aspect-ratio="2"
      >
      </v-img>
      
      <v-card-title primary-title>
        <div>
          <span class="title mt-0">{{ card_title }}</span>
        </div>
      </v-card-title>

      <v-card-actions>
      </v-card-actions>
    </v-card>
  </v-flex>
</template>

<script>
 export default {
   data () {
     return {
       card_title: '欢迎，Kinney',
     }
   },
   methods: {
     getBingImage(){
       var instance = this.$axios.create({
         baseUrl: '',
         headers: {
           'Access-Control-Allow-Origin': '*'
         }
       })
       instance.get('https://cn.bing.com/').then(res => {
         console.log(res.data)
       }).catch(err => {
         console.log(err)
       })
     }
   },
   created(){
     /* this.getBingImage() */
   }
 }
</script>
