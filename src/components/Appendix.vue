<template>
  <div class="container-fluid">
      <div class="row justify-content-center">
          <VueShowdown
                    :markdown="paragraphText"
                    flavor="github"
                    :options="{ emoji: true }"
                    class="textRow"
                    :style="cssVars"
                  />

      </div>
      <div class="row justify-content-center">
        <button v-on:click="toggleTextExpansion()" class="expansionButton">
          <b-icon icon="arrow-down-circle" :style="cssVars" class="expansionIcon" scale="2"/>
        </button></div>
      <b-container fluid>
      <b-row class="d-flex justify-content-center">
        <b-col id="component-graph" 
               v-for="field in fields" 
               v-on:graphDelete="onGraphDelete"
               v-on:graphToggleSize="onGraphDelete"
               v-bind:is="field.type" 
               :key="field.id" 
               :parentData="reportData"
               :parentID="field.id"
               class='borderclass d-flex justify-content-center'>
        </b-col>
        <b-col class=" borderclass d-flex justify-content-center">
          <button v-on:click="addGraph" class="addgraphbtn"><b-icon icon="plus-square" scale="2" class="addgraphicon"></b-icon></button>
        </b-col>
      </b-row>
      <b-row class="d-flex justify-content-center">
        
      </b-row>
    </b-container>
  </div>
</template>

<script>
//import Vue from 'vue'
import Graph from '../components/Graph';
import Multiselect from 'vue-multiselect'
import { VueShowdown } from 'vue-showdown';
//import $ from 'jquery'

export default {
  name: 'Appendix',
  components: {
    Graph, Multiselect, VueShowdown
  },
  props: ["paragraphText", "reportData"],
  data: () => ({
    NoFile: true,
    contact: String,
    reference: String,
    textExpanded: false,
    options: [{text: '0', value: 0},
              {text: '1', value: 1},
              {text: '2', value: 2},
              {text: '3', value: 3},
              {text: '4', value: 4},
              {text: '5', value: 5},
              {text: '6', value: 6}],
    numberOfGraphs: 0,
    count: 0,
    fields: [],
  }),
  computed: {
    cssVars() {
      let th = "100px"
      let expandButtonRotation = "0deg"
      if (this.textExpanded) {
        th="1000px"
        expandButtonRotation = "180deg"
      } else {
        th="100px"
        expandButtonRotation = "0deg"
      }
      return {'--textHeight': th, '--expandButtonRotation': expandButtonRotation}
    },
    buttonRotation(){
      if (this.textExpanded) {
        return 180
      }
      else {
        return 0
      }
    }
  },
  methods: {
    setNumberOfGraphs(type) {
      if (this.count < this.numberOfGraphs) {
        this.fields.push({
        'type': type,
        id: this.count++})}
      else if (this.count - this.numberOfGraphs == 1) {
        this.fields.pop()
        this.count--}
      else if (this.count - this.numberOfGraphs == 2) {
        this.fields.pop()
        this.fields.pop()
        this.count--
        this.count--} 
      },
      onGraphDelete (data) {
        for (var i=0 ; i < this.fields.length; i++){
          console.log("popping graph "+data)
          if (this.fields[i].id==data){this.fields.splice(i, 1)}
        }
      },
      addGraph(){
        this.fields.push({
        'type': "Graph",
        id: this.count++})
    },
    paragraphServer(){
      return this.paragraphText
    },
    toggleTextExpansion(){
      this.textExpanded = !this.textExpanded
    }
    },
    mounted(){
    if (this.$route.path == "/datafile"){
      console.log(this.$route.query.path)
    }
  }
}


  
</script>

<style>
.addgraphbtn{
  width: 600px;
  height: 400px;
  background-color: transparent;
  border-radius: 10px;
  border: 0px;
  outline: none;
  transition-timing-function: ease-out;
  transition: 0.4s;
  border: 2px dashed #0927a2;
}

.addgraphbtn:hover{
  background-color: #e5eef2;
}

.addgraphbtn:focus{
  outline: none;
}

.addgraphicon{
  color: #0927a2ff;
}

.borderclass{
  border:0px dashed red;
}
.borderclass2{
  border: 0px solid blue;
}

h1 {
  color: #0927a2ff;
  font-family: Helvetica, Arial, sans-serif;
}

h2 {
  color: #0927a2ff;
  font-family: Helvetica, Arial, sans-serif;
}

h3 {
  color: black;
  font-family: Helvetica, Arial, sans-serif;
  font-weight: bold;
}

.logos_footer {
  width: 200px;
}

.textRow {
  max-width: 600px;
  transition: all 0.8s ease-out;
  max-height: var(--textHeight);
  overflow: hidden;
  border-bottom: 2px solid #0927a2;
  
}

.expansionIcon{
  transition: all 1s ease-out;
  color: #0927a2;
  transform: rotate(var(--expandButtonRotation));
}

.expansionButton{
  background-color: transparent;
  border-radius: 10px;
  border: 0px;
  margin-top: 10px;
  margin-bottom: 10px;
  outline: none;
  transition-timing-function: ease-out;
  transition: 0.8s;
  border: 0px dashed #0927a2;
}

.expansionButton:focus{
  outline: none;
}

.expansionButton:hover{
  background-color: #e5eef2;
}


.footer {
  background-color: white;
  box-shadow:0px 0px 10px 0px rgba(0,0,0,0.25);
}

.caption {
  font-size: 12px; 
}

</style>
