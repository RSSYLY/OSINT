<script>
import {useMainStore} from "@/store/store.js";
import { snackbar } from "mdui/functions/snackbar.js";

export default {
  setup() {
    // 更改导航栏标题
    const store = useMainStore();
    store.pageInfo.title = "注册";
  },
  methods: {
    // 提交注册请求
    submitSignupRequest() {
      // 获取注册信息
      const emailEle = document.querySelector('#signup-email');
      const pwdEle = document.querySelector('#signup-pwd');
      const pwdReEle = document.querySelector('#signup-pwd-re');
      const phoneEle = document.querySelector('#signup-phone');
      const agreeUserLicenseEle = document.querySelector('#checkbox-agree-user-license');
      // 验证是否通过表单验证
      if ( emailEle.reportValidity() && pwdEle.reportValidity() && pwdReEle.reportValidity() && agreeUserLicenseEle.checked){
        const signupInfo = {
          email: emailEle.value,
          password: pwdEle.value,
          passwordRe: pwdReEle.value,
          phone: phoneEle.value
        }
        // 发送注册请求
        if(signupInfo.password === signupInfo.passwordRe){
          // 模拟向后端异步请求
          console.log(signupInfo);
        } else {
          snackbar({
            message: "两次密码输入不一致",
          });
        }
      } else {
        snackbar({
          message: "请检查注册信息是否正确",
        });
      }
    },
    routerTo(path) {
      this.$router.push(path);
    }
  }
}

</script>

<template>
  <div class="container">
    <div class="container-left">
      <div class="left-title">OSINT</div>
      <div class="left-subtitle">开源情报收集与分析系统</div>
    </div>
    <div class="container-right">
      <mdui-card class="card">
        <div class="card-header">
          <mdui-avatar class="card-header-avatar">
            <mdui-icon name="people_alt"></mdui-icon>
          </mdui-avatar>
          <div class="card-header-title">注册</div>
        </div>
        <div class="signup-form">
          <mdui-text-field icon="email" label="邮箱" type="email" id="signup-email" required></mdui-text-field>
          <mdui-text-field icon="key" label="密码" type="password" id="signup-pwd" required></mdui-text-field>
          <mdui-text-field icon="key" label="重复密码" type="password" id="signup-pwd-re" required></mdui-text-field>
          <mdui-text-field icon="phone" label="手机号码（选填）" type="number" id="signup-phone"></mdui-text-field>
          <mdui-checkbox id="checkbox-agree-user-license">同意用户协议</mdui-checkbox>
        </div>
        <div class="card-others">
          <div class="action-1">
            <mdui-button variant="filled" @click="submitSignupRequest()">注册</mdui-button>
            <div class="action-1-1">
              <mdui-button variant="tonal" @click="routerTo('/login')">登录</mdui-button>
            </div>
          </div>
        </div>
      </mdui-card>
    </div>
  </div>

</template>

<style scoped>
@media screen and (min-width: 1200px) {
  .container{
    padding: 0 80px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 64px);
  }
  .container-left{
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: flex-start;
    width: 60%;
  }
  .container-right{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 40%;
  }

}
@media screen and (min-width: 768px) and (max-width: 1200px) {
  .container{
    padding: 0 40px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 64px);
  }
  .container-left{
    display: none;
  }
  .container-right{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 60%;
  }
}
@media screen and (max-width: 768px){
  .container{
    padding: 0 20px;
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
    height: calc(100vh - 64px);
  }
  .container-left{
    display: none;
  }
  .container-right{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 80%;
  }
}
.container{
  /* 背景图片居中 */
  background: url('@/assets/img/background/towels-2822910_1920.jpg') no-repeat center;
  background-size: cover;
}
.left-title{
  font-size:var(--mdui-typescale-headline-large-size);
  font-weight: var(--mdui-typescale-headline-large-weight);
  color:rgba(var(--mdui-color-on-surface-dark));
}
.left-subtitle{
  font-size:var(--mdui-typescale-headline-small-size);
  font-weight: var(--mdui-typescale-headline-small-weight);
  color:rgba(var(--mdui-color-on-surface-dark));
}
.card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap:20px;
  width: 100%;
}
.card-header{
  padding: 40px 20px 10px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: rgb(var(--mdui-color-surface));
}

.signup-form{
  padding:10px 20px 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.card-others{
  padding: 0 20px 20px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.action-1{
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
}
.action-1-1{
  display: flex;
  align-items: center;
  gap: 10px;
}
</style>