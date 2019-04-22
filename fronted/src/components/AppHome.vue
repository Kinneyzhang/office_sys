<template>
  <div>
    <v-layout row>
      <v-flex xs6 sm6 md3 lg3 style="border-right: 0.1px solid grey;" dark>
        <v-container
          style="max-height: 600px;"
          class="scroll-y"
        >
          <v-layout
            column
            style="height: 1000px"
          >
            <app-scrollbar></app-scrollbar>
          </v-layout>
        </v-container>
      </v-flex>
      <v-spacer></v-spacer>
      <v-flex xs6 sm6 md9 lg9 justify-start>
        <app-body></app-body>
      </v-flex>
    </v-layout>
  </div>
</template>

<script>
 import AppScrollbar from './AppScrollbar.vue'
 import AppBody from './AppBody.vue'
 export default {
   components: {
     AppScrollbar,
     AppBody
   }
 }
</script>

