<template>
  <!-- eslint-disable vue/no-v-html -->
  <div class="profile">
    <v-list class="py-4">
      <v-list-item>
        <v-list-item-avatar
          size="72"
          color="grey lighten-2"
        >
          <img
            v-if="avatar"
            src="avatar"
          >
          <v-icon v-else>
            mdi-account
          </v-icon>
        </v-list-item-avatar>
        <span
          v-if="user.username"
          class="pa-4"
          v-text="user.username"
        />
        <span
          v-else
          class="pa-4"
          @click="login"
        >登录</span>
      </v-list-item>
    </v-list>
    <v-list>
      <v-list-item
        v-if="user.is_superuser"
        @click="() => $refs.archive.click()"
      >
        <v-list-item-icon>
          <v-icon>mdi-upload</v-icon>
        </v-list-item-icon>
        <v-list-item-title>上传题目包</v-list-item-title>
        <input
          ref="archive"
          type="file"
          hidden
          @input="uploadArchive"
        >
      </v-list-item>
      <v-list-item
        v-if="user.is_superuser"
        to="/problems/create"
      >
        <v-list-item-icon>
          <v-icon>mdi-file-plus</v-icon>
        </v-list-item-icon>
        <v-list-item-title>创建题目</v-list-item-title>
      </v-list-item>
      <v-list-item @click="logout">
        <v-list-item-icon>
          <v-icon>mdi-logout</v-icon>
        </v-list-item-icon>
        <v-list-item-title>注销</v-list-item-title>
      </v-list-item>
    </v-list>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: "Profile",

  props: { user: { type: Object, default: () => {} } },

  data: () => ({
    avatar: "",
  }),

  methods: {
    async login() {
      axios
        .options("/msal/login")
        .then(() => {
          window.location = "/msal/login";
        })
        .catch(() => {});
    },

    async logout() {
      await axios.post(`${process.env.VUE_APP_API_BASE_URL}logout`);
      this.user = {};
    },

    uploadArchive() {
      const archiveFormData = new FormData();
      archiveFormData.append("file", this.$refs.archive.files[0]);
      axios.put(
        `${process.env.VUE_APP_API_BASE_URL}problems/import_markdown`,
        archiveFormData,
        { headers: { "Content-Type": "multipart/form-data" } }
      );
    },
  },
};
</script>
