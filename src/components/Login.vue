<template>
  <v-container>
    <v-alert v-if="message" type="error">{{ message }}</v-alert>
    <v-row>
      <v-col md="4" offset-md="4">
        <v-card class="login pa-8 mt-16">
          <v-form ref="loginForm">
            <v-text-field
              v-model="username"
              label="用户名"
              required
            ></v-text-field>
            <v-text-field
              v-model="password"
              label="密码"
              required
            ></v-text-field>
            <v-btn color="primary" @click="login">登录</v-btn>
          </v-form>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: "Login",

  data: () => ({
    username: "",
    password: "",
    message: "",
  }),

  methods: {
    async login() {
      if (!this.$refs.loginForm.validate()) return;

      const response = await fetch(process.env.VUE_APP_API_BASE_URL + "login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: this.username,
          password: this.password,
        }),
      });

      if (response.status <= 299) {
        this.$router.push("/");
        return;
      }

      const messageBody = JSON.parse(await response.text());
      this.message = messageBody.message[0].message;
    },
  },
};
</script>
