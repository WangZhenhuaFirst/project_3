<template>
  <div>
    <h1>PDF关键词自动高亮</h1>
    <form id="import">
      <a-row>
        <a-col :span="8">
          <label class="custom-file-upload">
            <input type="file" @change="getFile($event)" style="display:none" />
            <a-icon type="upload" />点我上传PDF
          </label>
          <span>{{ filename }}</span>
        </a-col>
        <a-col :span="8">
          <li v-for="(subject_word, index) in subject_words" :key="index">
            <input v-model="subject_word.content" placeholder="请输入主题词" style="margin:5px;" />
            <a-icon type="plus-circle" @click="add" />
            <a-icon type="minus-circle" @click="del(index)" />
          </li>
        </a-col>
        <a-col :span="8">
          <button @click="submitForm($event)">提交</button>
        </a-col>
      </a-row>
    </form>

    <div id="result" v-if="seen">
      <a-row>
        <a-col :span="6">
          <a-button type="primary" icon="download" v-bind:href="download_url">点我下载高亮PDF</a-button>
        </a-col>
        <a-col :span="8">
          <li v-for="(keyword, index) in keywords" :key="index">{{ keyword }}</li>
        </a-col>
      </a-row>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      seen: false,
      subject_words: [{ content: "" }],
      file: "",
      filename: "",
      download_url: "",
      keywords: ""
    };
  },
  methods: {
    add() {
      this.subject_words.push({ content: "" });
    },
    del(index) {
      this.subject_words.splice(index, 1);
    },
    getFile(event) {
      this.file = event.target.files[0];
      this.filename = this.file.name;
      console.log(this.file);
    },
    submitForm(event) {
      event.preventDefault();

      if (this.file == "") {
        this.$message.error("请上传PDF文件");
      } else {
        let formData = new FormData();

        let sws = [];
        sws = this.subject_words.map(current => current["content"]);
        // console.log(sws);
        formData.append("subject_words", sws);
        formData.append("file", this.file);

        let config = {
          headers: {
            "Content-Type": "multipart/form-data"
          }
        };

        axios.post("http://127.0.0.1:5000", formData, config).then(res => {
          // console.log(res);
          this.download_url = res.data.download_url;
          this.keywords = res.data.keywords;
          this.seen = true;
        });
      }
    }
  }
};
</script>	

<style scoped>
#import {
  background-color: aqua;
  padding-top: 50px;
  padding-bottom: 80px;
}

#result {
  background-color: aquamarine;
  padding: 80px;
}

.custom-file-upload {
  border: 1px solid #ccc;
  display: inline-block;
  padding: 6px 12px;
  cursor: pointer;
}
</style>