<template>
  <v-container>
    <v-row>
      <v-col
        md="4"
        offset-md="4"
      >
        <v-card class="login pa-8 mt-16">
          <v-form
            ref="loginForm"
            @submit.prevent="login"
          >
            <v-text-field
              v-model="username"
              label="用户名"
              required
            />
            <v-text-field
              v-model="password"
              type="password"
              label="密码"
              required
            />
            <v-btn
              type="submit"
              color="primary"
            >
              登录
            </v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "Login",

  data: () => ({
    username: "",
    password: "",
    message: ""
  }),

  methods: {
    async login() {
      if (!this.$refs.loginForm.validate()) return;

      try {
        await axios.post(process.env.VUE_APP_API_BASE_URL + "login", {
          username: this.username,
          password: this.password
        });

        this.$emit("login");
        this.$router.push("/");
        return;
      } catch (e) {
        this.$dialog.notify.error(e.message, {
          position: "top-right",
          timeout: 5000
        });
      }
    }
  }
};
</script>
