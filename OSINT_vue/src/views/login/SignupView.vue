<script>
import {useMainStore} from "@/store/store.js";
import { snackbar } from "mdui/functions/snackbar.js";

export default {
  setup() {
    // 更改导航栏标题
    const store = useMainStore();
    store.pageInfo.title = "注册";
    // 更改抽屉
    store.pageInfo.drawer={
      items:[
        {
          title:'认证',
          items:[
            {
              title:'登录',
              link:'/login',
              active:false
            },
            {
              title:'注册',
              link:'/signup',
              active:true
            },
            {
              title:'找回密码',
              link:'/findpass',
              active:false
            }
          ]
        }
      ]
    }
  },
  methods: {
    // 发送验证码
    submitVerificationCode(){
      // 获取邮箱
      const emailEle = document.querySelector('#signup-email');
      // 验证邮箱是否通过表单验证
      if ( emailEle.reportValidity() ){
        // 获取要发送的数据为json
        const submitInfo={
          email: emailEle.value
        }
        console.debug("发送验证码",submitInfo)
        // 按钮加载状态
        this.isSubmitting = true;
        // 异步请求
        this.$axios.post('/authenticate/register/send-code/',submitInfo)
          .then(response=>{
            console.debug("发送验证码",response)
            // 按钮加载状态
            this.isSubmitting = false;
            if(response.data.error === 0){
              // 请求成功
              // 下一步
              this.signupStep = 1;
              snackbar({
                message: response.data.message
              });
            } else {
              snackbar({
                message: response.data.message,
              });
            }
          })
          .catch(error=>{
            console.error("发送验证码失败，后端返回数据异常或无响应",error)
            // 按钮加载状态
            this.isSubmitting = false;
            snackbar({
              message: "内部错误",
            });
          })
      } else {
        snackbar({
          message: "请检查邮箱是否正确",
        });
      }
    },
    // 提交注册请求
    submitSignupRequest() {
      // 获取注册信息
      const emailEle = document.querySelector('#signup-email');
      const verificationCodeEle = document.querySelector('#verification-code');
      const pwdEle = document.querySelector('#signup-pwd');
      const pwdReEle = document.querySelector('#signup-pwd-re');
      const phoneEle = document.querySelector('#signup-phone');
      const agreeUserLicenseEle = document.querySelector('#checkbox-agree-user-license');
      // 验证是否通过表单验证
      if ( emailEle.reportValidity() && verificationCodeEle.reportValidity() && pwdEle.reportValidity() && pwdReEle.reportValidity() && agreeUserLicenseEle.checked){
        const signupInfo = {
          email: emailEle.value,
          verificationCode: verificationCodeEle.value,
          password: pwdEle.value,
          phone: phoneEle.value
        }
        // 发送注册请求
        if(pwdEle.value === pwdReEle.value){
          // 按钮加载状态
          this.isSubmitting = true;
          // 向后端异步请求
          this.$axios.post('/authenticate/register/',signupInfo)
            .then(response=>{
              console.debug("发送注册请求",response)
              // 按钮加载状态
              this.isSubmitting = false;
              if(response.data.error === 0){
                snackbar({
                  message: response.data.message,
                });
                this.signupStep = 2;
                // 跳转到登录页
                this.$router.push('/login');
              } else {
                snackbar({
                  message: response.data.message,
                });
              }
            })
            .catch(error=>{
              console.error("注册失败，后端返回数据异常或无响应",error)
              // 按钮加载状态
              this.isSubmitting = false;
              snackbar({
                message: "内部错误",
              });
            })
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
  },
  data(){
    return{
      signupStep: 0,
      isSubmitting: false
    }
  }
}

</script>

<template>
  <div class="container">
    <div class="shade"></div>
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
        <mdui-linear-progress :value="(signupStep+1)/3"></mdui-linear-progress>
        <div class="signup-form">
          <mdui-text-field icon="email" label="邮箱" type="email" id="signup-email" required :disabled="this.signupStep!==0"></mdui-text-field>
          <mdui-text-field v-if="this.signupStep===1" icon="key" label="验证码" type="number" id="verification-code" required></mdui-text-field>
          <mdui-text-field v-if="this.signupStep===1" icon="key" label="密码" type="password" id="signup-pwd" required></mdui-text-field>
          <mdui-text-field v-if="this.signupStep===1" icon="key" label="重复密码" type="password" id="signup-pwd-re" required></mdui-text-field>
          <mdui-text-field v-if="this.signupStep===1" icon="phone" label="手机号码（选填）" type="number" id="signup-phone"></mdui-text-field>
          <mdui-checkbox id="checkbox-agree-user-license">同意用户协议</mdui-checkbox>
        </div>
        <div class="card-others">
          <div class="action-1">
            <div class="action-1-1">
              <mdui-button v-if="this.signupStep===1" variant="tonal" @click="this.signupStep=0" :disabled="isSubmitting">返回上一步</mdui-button>
              <mdui-button variant="outlined" @click="routerTo('/login')">返回登录</mdui-button>
            </div>
            <mdui-button v-if="this.signupStep===0" variant="filled" @click="submitVerificationCode()" :disabled="isSubmitting" :loading="isSubmitting">下一步</mdui-button>
            <mdui-button v-if="this.signupStep===1" variant="filled" @click="submitSignupRequest()" :disabled="isSubmitting" :loading="isSubmitting">注册</mdui-button>
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
    width: 70%;
  }
  .container-right{
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 30%;
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
  z-index: 1;
  font-size:var(--mdui-typescale-display-medium-size);
  font-weight: var(--mdui-typescale-display-medium-weight);
}
.left-subtitle{
  z-index: 1;
  font-size:var(--mdui-typescale-headline-small-size);
  font-weight: var(--mdui-typescale-headline-small-weight);
}
.card{
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap:0px;
  width: 100%;
}
.card-header{
  padding: 40px 20px 30px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: rgb(var(--mdui-color-surface));
}

.signup-form{
  padding:20px 20px 0 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.card-others{
  padding:10px 20px 20px 20px;
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
.shade{
  z-index: 0;
  position: absolute;
  width: 100%;
  height: calc(100vh - 64px);
  background: rgba(var(--mdui-color-surface-dim),.8);
}
</style>