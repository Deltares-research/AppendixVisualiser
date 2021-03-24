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
      <b-row class="justify-content-center"><h2>{{tabledata.title}}</h2></b-row>
      <vue-table-dynamic :params="tabledata" ref="table"></vue-table-dynamic>
        <!--Plotly :data="data" :layout="layout"></Plotly>-->

    </div>
  </b-col>
</template>

<script>
import VueTableDynamic from 'vue-table-dynamic'
import Multiselect from 'vue-multiselect'

export default {
  name: "Graph",
  components: {
    VueTableDynamic ,
    Multiselect
  },
  props: {
    parentID: Number,
    parentData: Array,
  },
  data: () => ({
      "tabledata": {
                "data": [
                    ['Index', 'Data1', 'Data2', 'Data3'],
                    [1, 'b3ba90', '7c95f7', '9a3853'],
                    [2, 'ec0b78', 'ba045d', 'ecf03c'],
                    [3, '63788d', 'a8c325', 'aab418']
                  ],
                "header": 'row',
                "border": true
        }
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
    onlyUnique(value, index, self){
      return self.indexOf(value) === index;
    },
    changeData(item) {
      let filter = []
      // get number of columns and rows
      let nrows = item.data[0].length
      let array = item.data  
      array = array[0].map((_, colIndex) => array.map(row => row[colIndex]));
      let ncols = array[0].length

      // get unique values in column
      for (let icol=0;icol<ncols-1;icol++){

        var unique = array[icol].slice(1, ncols).filter(this.onlyUnique)

        if (unique.length < 7){
          console.log('adding filter to column')
          let content = []
          for (let i=0;i<=unique.length-1;i++){
            content.push({"text": unique[i], 
                          "value": unique[i]})
          }
          console.log(content)
          filter.push({"column": icol,
                       "content": content,
                       "method": (value, tableCell) => {return tableCell.data == value}
                      })
      
      }
      
      this.tabledata = {"title": item.title,
                        "data": item.data, 
                        "header": 'row',
                        "stripe": true,
                        "highlight": { "row": [0] },
                        "highlightedColor": '#e5eef2',
                        "enableSearch": true,
                        "pagination": true,
                        "sort": Array.from(Array(nrows).keys()),
                        "filter": filter,
                        "border": false
                      }
      }

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
