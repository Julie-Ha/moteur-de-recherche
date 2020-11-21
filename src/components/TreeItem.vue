<template>
  <li>
    <input type="checkbox" v-model='checked' @change="updateEntities">
    <span :class="{ bold: isFolder }" @click="toggle" @dblclick="makeFolder">
      
      {{ item.name }}
      <span v-if="isFolder">[{{ isOpen ? "-" : "+" }}]</span>
    </span>
    <ul v-show="isOpen" v-if="isFolder">
      <TreeItem
        class="item"
        v-for="(child, index) in item.children"
        :key="index"
        :item="child"
        @make-folder="$emit('make-folder', $event)"
      ></TreeItem>
    </ul>
  </li>
</template>

<script>
import store from "../store";

export default {
  name: "TreeItem",
  store,
  props: {
    item: Object,
  },
  data() {
    return {
      isOpen: false,
      checked: false,
    };
  },
  computed: {
    isFolder() {
      return this.item.children && this.item.children.length;
    },
  },
  methods: {
    toggle() {
      if (this.isFolder) {
        this.isOpen = !this.isOpen;
      }
    },
    makeFolder() {
      if (!this.isFolder) {
        this.$emit("make-folder", this.item);
        this.isOpen = true;
      }
    },
    updateEntities() {
      if(this.checked)
        store.commit('add', this.item.name);
      else
        store.commit("remove", this.item.name);
    }
  },
};
</script>

<style scoped></style>
