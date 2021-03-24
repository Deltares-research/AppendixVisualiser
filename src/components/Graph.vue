<template>
  <b-col>
    <div :style="graphStyle" class='graphContainer blackborder'>
      <b-row class="d-flex justify-content-between toolbar">
        <multiselect v-model="showGraph" :options="getMultiSelectOptions()" placeholder="Choose from available graphs" class="multiselector">tt</multiselect>  
        <span>
        <button class="btn sizegraphbtn" v-on:click="toggleSize"> <b-icon icon="arrows-angle-expand" scale="1"></b-icon></button>
        <button class="btn deletegraphbtn" v-on:click="deleteMe"> <b-icon icon="x" scale="2" variant="danger"></b-icon></button>
      </span>
      </b-row>
      
        <Plotly :data="data" :layout="layout"></Plotly>

    </div>
  </b-col>
</template>

<script>
import { Plotly } from 'vue-plotly'
import Multiselect from 'vue-multiselect'

export default {
  name: "Graph",
  components: {
    Plotly,
    Multiselect
  },
  props: {
    parentID: Number,
    parentData: Array,
  },
  data: () => ({
      data: [{x: [1, 2, 3, 4],
              y: [0, 0, 0, 0],
              type:"scatter"
            }],
      layout: {title: {text: "dummy"}, 
               xaxis: {title: "x Axis", 
                       linecolor: "#000000",
                       linewidth: 2,
                       font : {family: 'helvetica, arial'}},
              legend: {bgcolor: "#e5eef2"}
            },
      count: 0,
      fields: [],
      value: null,
      ToggleGraphStyle: 0,
      maxgraphwidth: "900px",
      options:  ['list', 'of', 'options']      
    }),
    computed: {
      showGraph: {
      get(){return this.value},
      set(selectedVal){
        this.value=selectedVal;
        for (let item in this.parentData) {
          if (this.parentData[item].title == selectedVal){
            this.changeData(this.parentData[item])
          }
        }
      }
    },
    graphStyle(){
      if (this.ToggleGraphStyle%2 == 0) {
        return this.graphDynamicStyle
      } else {
        return this.graphFocusStyle
      }
    },
    graphDynamicStyle(){
      return {
        '--graph-width': "100%",
        '--graph-maxwidth': this.maxgraphwidth,
        '--graph-minwidth': "600px"}
    },
    graphFocusStyle(){
      return {
        '--graph-width': "100%",
        '--graph-maxwidth': "1200px",
        '--graph-minwidth': "1200px"}
    }
  },
    methods: {
    getMultiSelectOptions(){
      let array = [];
      for (let item in this.parentData) {
        array.push(this.parentData[item].title)
      }
      return array
    },
    deleteMe(){
        console.log('emitting from graphy')
        this.$emit('graphDelete', this.parentID)
    },
    changeData(item) {
      
      this.data = item.data
      this.layout = {title: item.title,
                     titlefont: {color: '#0927a2ff', 
                                 family: 'helvetica, arial'},
                     xaxis: {title: item.xlabel,
                             linewidth: 4,
                             hoverformat: " .2f", 
                             range: item.xlim},
                     yaxis: {title: item.ylabel,
                             linewidth: 4,
                             hoverformat: " .2f",
                             range:item.ylim},
                     showlegend: false,
                     legend: {bgcolor: "#e5eef2", 
                              orientation: "h",
                              y:-0.5,
                              x: 0
                            },
                     font : {family: 'helvetica, arial', size: 18},
                     annotations: item.annotations}

    },
    toggleSize(){
      this.ToggleGraphStyle ++ 
    }
  }
}

</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style>

.toolbar{
  padding: 10px 10px 10px 20px;
  width: 100%;
  border-radius: 5px;
  background-color: #e5eef2;
}

.graphContainer{
  transition: all ease-in 0.4s;
  width: var(--graph-width);
  max-width: var(--graph-maxwidth);
  min-width: var(--graph-minwidth);
}

.sizegraphbtn{
  border: none; /* Remove borders */
  color: black; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
}

.deletegraphbtn {
  border: none; /* Remove borders */
  color: white; /* White text */
  padding: 12px 16px; /* Some padding */
  font-size: 16px; /* Set a font size */
  cursor: pointer; /* Mouse pointer on hover */
}

/* Darker background on mouse-over */
.deletegraphbtn:hover {
  border: 1px dashed black;
}


.redborder{
  border: 1px solid red;
}
.blackborder{
  border: 0px dashed black;
}



.multiselector{
  width: 400px;
}

.logos_footer {
  width: 200px;
}

.header {
  background-color: red;
  background-image: url(../assets/header.png);
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

.footer {
  background-color: white;
  box-shadow:0px 0px 10px 0px rgba(0,0,0,0.25);
}

.caption {
  font-size: 12px; 
}

</style>
