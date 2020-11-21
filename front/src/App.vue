<template>
  <div class="columns my-1 mx-6">
    <div class="column is-two-fifths">
      <ul id="App">
        <TreeItem
          class="item"
          :item="treeData"
          @make-folder="makeFolder"
        ></TreeItem>
      </ul>
      <span>Selected entities: {{ checkedEntities }}</span>
    </div>
    <div class="column">
      <button class="button is-primary m-1" @click="cosineSimilarity">
        Cosine Similarity
      </button>
      <button class="button is-primary m-1">Path Length</button>
      <button class="button is-primary m-1">Semantic Content Similarity</button>
      <button class="button is-light m-1">Clear</button>
      <div>
        {{ results }}
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import TreeItem from "./components/TreeItem.vue";
import treeData from "./data/ontology.json";
import store from "./store";

export default {
  name: "App",
  store,
  components: {
    TreeItem,
  },
  data() {
    return {
      treeData: treeData,
      checkedEntities: store.state.checkedEntities,
      results: "results",
    };
  },
  methods: {
    makeFolder(item) {
      this.set(item, "children", []);
      this.addItem(item);
    },
    cosineSimilarity() {
      let myJSON = JSON.stringify(this.checkedEntities);
      console.log(myJSON);
      axios
        .post("http://localhost:5000/cosine-similarity", {
          entities: this.checkedEntities
        })
        .then((response) => {
          this.results = response.data;
        })
        .catch((e) => {
          this.errors.push(e);
        });
    },
  },
};
</script>

<style>
li {
  list-style-type: none;
}
</style>
