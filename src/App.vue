<template>
  <div>
    <div>
      <ul id="App">
        <TreeItem
          class="item"
          :item="treeData"
          @make-folder="makeFolder"
        ></TreeItem>
      </ul>
      <span>Selected entities: {{ checkedEntities }}</span>
    </div>
    <div>
      <button>Cosine Similarity</button>
      <button>Path Length</button>
      <button>Semantic Content Similarity</button>
      <button>Clear</button>
    </div>
  </div>
</template>

<script>
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
    };
  },
  methods: {
    makeFolder(item) {
      this.set(item, "children", []);
      this.addItem(item);
    },
  },
};
</script>

<style>
li {
  list-style-type: none;
}
</style>
