<script>
import {useMainStore} from "@/store/store.js";
import { snackbar } from "mdui/functions/snackbar.js";

export default {
  setup() {
    // 更改导航栏标题
    const store = useMainStore();
    store.pageInfo.title = "找回密码";
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
              active:false
            },
            {
              title:'找回密码',
              link:'/findpass',
              active:true
            }
          ]
        }
      ]
    }
  },
  methods: {
    sendCode(){
      // 先判断是那种类型
      if(this.findPwdType === 'useEmail'){
        // 邮箱找回密码
        this.sendEmailCode();
      } else if(this.findPwdType === 'usePhone'){
        // 手机找回密码
        this.sendPhoneCode();
      }
    },
    sendEmailCode(){
      // 获取邮箱
      const emailEle = document.querySelector('#findpass-email');
      // 验证邮箱是否通过表单验证
      if ( emailEle.reportValidity() ){
        // 获取要发送的数据为json
        const submitInfo={
          type : 'email',
          target: emailEle.value
        }
        console.debug("发送验证码到邮箱",submitInfo)
        // 按钮加载状态
        this.isSubmitting = true;
        // 异步请求
        this.$axios.post('/authenticate/forgot-password/send-code/',submitInfo)
          .then(response=>{
            console.debug("发送验证码返回：",response.data)
            // 按钮加载状态
            this.isSubmitting = false;
            if(response.data.error === 0){
              // 请求成功
              // 下一步
              this.findingPwdStep = 1;
              snackbar({
                message: "验证码已发送",
              });
            } else {
              // 请求失败
              snackbar({
                message: response.data.message,
              });
            }
          })
          .catch(error=>{
            console.debug("后端请求失败",error)
            // 按钮加载状态
            this.isSubmitting = false;
            // 请求失败
            snackbar({
              message: "内部错误",
            });
          })
      } else {
        snackbar({
          message: "请填写表单",
        });
      }
    },
    sendPhoneCode(){
      // 获取手机
      const phoneEle = document.querySelector('#findpass-phone');
      // 验证手机是否通过表单验证
      if ( phoneEle.reportValidity() ){
        // 获取要发送的数据为json
        const submitInfo={
          type : 'phone',
          target: phoneEle.value
        }
        console.debug("发送验证码到手机",submitInfo)
        // 按钮加载状态
        this.isSubmitting = true;
        // 异步请求
        this.$axios.post('/authenticate/forgot-password/send-code/',submitInfo)
          .then(response=>{
            console.debug("发送验证码返回：",response.data)
            // 按钮加载状态
            this.isSubmitting = false;
            if(response.data.error === 0){
              // 请求成功
              // 下一步
              this.findingPwdStep = 1;
              snackbar({
                message: "验证码已发送",
              });
            } else {
              // 请求失败
              snackbar({
                message: response.data.message,
              });
            }
          })
          .catch(error=>{
            console.debug("后端请求失败",error)
            // 按钮加载状态
            this.isSubmitting = false;
            // 请求失败
            snackbar({
              message: "内部错误",
            });
          })
      } else {
        snackbar({
          message: "请填写表单",
        });
      }
    },
   submitPass(){
      // 获取登录类型
      const loginType = () => {
        if(this.findPwdType === 'useEmail'){
          return 'email';
        } else if(this.findPwdType === 'usePhone'){
          return 'phone';
        }
     }
      // 获取验证码
      const recCodeEle = document.querySelector('#findpass-rec-code');
      // 获取密码
      const newPwdEle = document.querySelector('#set-new-pwd');
      // 获取重复密码
      const newPwdReEle = document.querySelector('#set-new-pwd-re');
      // 验证表单是否通过验证
      if ( recCodeEle.reportValidity() && newPwdEle.reportValidity() && newPwdReEle.reportValidity() ){
        // 同时确保两边密码一致
        if(newPwdEle.value !== newPwdReEle.value){
          snackbar({
            message: "两次密码不一致",
          });
          return;
        }
        // 获取要发送的数据为json
        const submitInfo={
          type:loginType(),
          target: loginType() === 'email' ? document.querySelector('#findpass-email').value : document.querySelector('#findpass-phone').value,
          verificationCode : recCodeEle.value,
          password: newPwdEle.value
        }
        console.debug("提交新密码",submitInfo)
        // 按钮加载状态
        this.isSubmitting = true;
        // 异步请求
        this.$axios.post('/authenticate/forgot-password/',submitInfo)
          .then(response=>{
            console.debug("提交新密码返回：",response.data)
            // 按钮加载状态
            this.isSubmitting = false;
            if(response.data.error === 0){
              // 请求成功
              // 带回登录页
              this.$router.push('/login');
              snackbar({
                message: "密码修改成功",
              });
            } else {
              // 请求失败
              snackbar({
                message: response.data.message,
              });
            }
          })
          .catch(error=>{
            console.debug("后端请求失败",error)
            // 按钮加载状态
            this.isSubmitting = false;
            // 请求失败
            snackbar({
              message: "内部错误",
            });
          })
      } else {
        snackbar({
          message: "请填写表单",
        });
      }
   },
    routerTo(path) {
      this.$router.push(path);
    }
  },
  data() {
    return {
      findPwdType: 'useEmail',
      findingPwdStep: 0
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
          <div class="card-header-title">找回密码</div>
        </div>
        <mdui-tabs v-if="findingPwdStep===0" value="useEmail" id="find-pwd-type">
          <mdui-tab value="useEmail" icon="email" inline @click="findPwdType = 'useEmail'">邮箱</mdui-tab>
          <mdui-tab value="usePhone" icon="phone" inline @click="findPwdType = 'usePhone'">手机</mdui-tab>
        </mdui-tabs>
        <div class="signup-form">
<!--          <mdui-linear-progress :value="(findingPwdStep+1)/2"></mdui-linear-progress>-->
          <mdui-text-field v-if="findPwdType === 'useEmail'" :disabled="this.findingPwdStep!==0" icon="email" label="邮箱" type="email" id="findpass-email" required></mdui-text-field>
          <mdui-text-field v-if="findPwdType === 'usePhone'" :disabled="this.findingPwdStep!==0" icon="phone" label="手机" type="number" id="findpass-phone" required></mdui-text-field>
          <mdui-text-field v-if="findingPwdStep === 1" icon="key" label="验证码" type="number" id="findpass-rec-code" required></mdui-text-field>
          <mdui-text-field v-if="findingPwdStep === 1" icon="key" label="密码" type="password" id="set-new-pwd" required></mdui-text-field>
          <mdui-text-field v-if="findingPwdStep === 1" icon="key" label="重复密码" type="password" id="set-new-pwd-re" required></mdui-text-field>
        </div>
        <div class="card-others">
          <div class="action-1">
            <mdui-button v-if="findingPwdStep===0" variant="tonal" @click="routerTo('/login')">返回登录</mdui-button>
            <mdui-button v-if="findingPwdStep===1" variant="tonal" @click="findingPwdStep = 0">上一步</mdui-button>
            <mdui-button v-if="findingPwdStep === 0" variant="filled" @click="sendCode">下一步</mdui-button>
            <mdui-button v-if="findingPwdStep === 1" variant="filled" @click="submitPass">提交</mdui-button>
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
  width: 100%;
}
.card-header{
  padding: 40px 20px 20px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: rgb(var(--mdui-color-surface));
}
.card mdui-tab{
  padding: 10px;
}

.signup-form{
  padding:20px 20px 10px 20px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}
.card-others{
  padding: 20px 20px 20px 20px;
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
.shade{
  z-index: 0;
  position: absolute;
  width: 100%;
  height: calc(100vh - 64px);
  background: rgba(var(--mdui-color-surface-dim),.8);
}
</style>