<template>

  <div  id="Main">
    <b-navbar toggleable="lg" sticky type="light" variant="light">
      <b-navbar-brand href="#"><img src="./assets/logo_deltares.png" alt="DeltaresLogo" class="logo"></b-navbar-brand>
<b-navbar-toggle target="nav-collapse"></b-navbar-toggle>
<b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <!--<b-nav-item to="/" :active="path == '/'">Home</b-nav-item>
          <b-nav-item to="/search" :active="path == '/search'">Search</b-nav-item>
        -->
        <b-nav-item v-for="appendix in Appendices" :key="appendix.name" v-on:click="SetAppendix(appendix.index)"> {{ appendix.name }}</b-nav-item>
        <b-nav-item href="#" v-b-modal.modal-1>About</b-nav-item>
        <b-nav-item href="https://deltares.nl" target="_blank">Bezoek Deltares.nl</b-nav-item>
        </b-navbar-nav>
        <b-modal id="modal-1" 
                 title="About this app">
        <p class="my-4">Hi! Great you are here :) </p><p>Please be advised that this web-app is currently in an experimental state. Functionality may change, and input files may not longer be accepted after an update. </p><p>We hope you enjoy your visit and tell us your experiences!</p>
        <p>To get in touch, reach us at <a href="mailto:koen.berends@deltares.nl">koen.berends@deltares.nl</a></p>

      </b-modal>
      </b-collapse>
    </b-navbar>
    <!-- Figure Header -->
    <div class="row d-flex justify-content-center header align-items-center">
    </div>
    <div class="row d-flex align-content-right author align-items-center">
      Foto: Beeldbank Rijkswaterstaat
    </div>
    <div v-if="NoFile"><DropFile v-on:childToParent="onFileDrop"></DropFile></div>
    <div v-else>

     <Appendix
        v-bind:paragraphText="currentAppendix.paragraphText"
        v-bind:reportData="currentAppendix.reportData"
        v-bind:appendixType="currentAppendix.appendixType"
        v-bind:deleteAll="triggerToDeleteAll"

     ></Appendix>
    </div>
    
    

  
    <img src="./assets/Deltares_pay-off_D-blauw_RGB.svg" alt="DeltaresLogo" class="payoff">
  </div>

</template>

<script>

import DropFile from './components/DropFile'  
import Appendix from './components/Appendix.vue';

export default {
    name: 'App',
    components: {
       Appendix, DropFile
    },
    data: () => ({
      NoFile: true,
      Appendices: [],
      triggerToDeleteAll: 0,
      currentAppendix: {"name": "koen", "paragraphText": "*be* **bold**"}
    }),
    mounted(){
      console.log(this.$route)
    },
    methods: {
    SetAppendix (index) {
      this.currentAppendix = this.Appendices[index]
      this.triggerToDeleteAll ++

    },
    onFileDrop (data) {
        this.NoFile = false
        for (let i=0; i< data.appendices.length ; i++){
          let reportData = null
          if (data.appendices[i].type == "graphs") {
            reportData =  data.appendices[i].graphs
          } else if (data.appendices[i].type == "tables"){
            reportData =  data.appendices[i].tables
          } else {
            reportData = data.appendices[i].graphs
          }
          console.log(data.appendices[i].type)

          this.Appendices.push({
            "name": data.appendices[i].name,
            "index": i,
            "paragraphText": data.appendices[i].paragraphs,
            "appendixType": data.appendices[i].type,
            "reportData": reportData
          })
        }
        this.reference = data.reference
        this.contact = data.contact
        this.SetAppendix(0)
      },
    }
}

</script>

<style>

#modal-1 h5{
  color: #0927a2;
  font-family: Helvetica, Arial, sans-serif;
}


#modal-1 header, footer{
  background-color: #e5eef2;
}


.logo {
  max-width: 150px;
}

.payoff{
  position: fixed;
  right: 20px;
  bottom: 10px;
  width: 15%;
}

#Main {
  font-family: Helvetica, Arial, sans-serif;
}

b-navbar{
    background-color: white;

}


.header {
  background-color: white;
  background-image: url(./assets/header.png);
  height: 200px;
  color: white;
  background-size: cover;
  background-repeat: no-repeat;
  box-shadow: 0px 2px 8px 0px rgba(0,0,0,0.75);
}


.author {
  background-color: white;
  box-shadow:0px 10px 10px 0px rgba(0,0,0,0.25);
  margin-bottom: 30px;
  font-size: 10px;
  padding-left: 20px;
}

</style>