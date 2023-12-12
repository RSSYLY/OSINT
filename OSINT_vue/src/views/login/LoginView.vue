<script>
import {useMainStore} from "@/store/store.js";
import { snackbar } from "mdui/functions/snackbar.js";

export default {
  setup() {
    // 更改导航栏标题
    const store = useMainStore();
    store.pageInfo.title = "登录";
    // 更改抽屉
    store.pageInfo.drawer={
      items:[
        {
          title:'认证',
          items:[
            {
              title:'登录',
              link:'/login',
              active:true
            },
            {
              title:'注册',
              link:'/signup',
              active:false
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
    // 提交登录请求
    submitLoginRequest() {
      // 按钮样式
      this.isSubmitting = true;
      console.debug(this.isSubmitting)
      // 获取登录方式
      const loginType = document.querySelector('#login-type').getAttribute('value');
      console.log(loginType);
      // 获取记住我
      const rememberMe = document.querySelector('#checkbox-rememberMe').checked;
      // 获取登录信息
      let loginInfo = {};
      if (loginType === 'useEmail') {
        // 使用邮箱的情况
        const emailEle = document.querySelector('#loginEmail');
        const pwdEle = document.querySelector('#loginEmail-pwd');
        // 验证是否通过表单验证
        if ( emailEle.reportValidity() && pwdEle.reportValidity()){
          loginInfo = {
            loginType: 'email',
            email: document.querySelector('#loginEmail').value,
            password: document.querySelector('#loginEmail-pwd').value,
            rememberMe: rememberMe
          }
        } else {
          snackbar({
            message: "请检查表单",
          });
          // 按钮样式
          this.isSubmitting=false
        }

      } else {
        // 使用手机号码的情况
        const phoneEle = document.querySelector('#loginPhone');
        const pwdEle = document.querySelector('#loginPhone-pwd');
        // 验证是否通过表单验证
        if ( phoneEle.reportValidity() && pwdEle.reportValidity()){
          loginInfo = {
            loginType: 'phone',
            phone: document.querySelector('#loginPhone').value,
            password: document.querySelector('#loginPhone-pwd').value,
            rememberMe: rememberMe
          }
        } else {
          snackbar({
            message: "请检查手机号码和密码是否正确",
          });
          // 按钮样式
          this.isSubmitting=false

        }
      }
      // 发送登录请求
      if(loginInfo.password){
        // 向后端异步请求
        // 发送POST请求
        // 后端地址写在入口文件了（main.js）
        console.debug('Login info:', loginInfo);
        this.$axios.post('/authenticate/login/', loginInfo)
            .then(response => {
              console.debug('Response:', response.data)
              if (response.data.error === 0) {
                // 处理登录成功的情况
                console.log('Login successful:', response.data);
                snackbar({
                  message: response.data.message,
                });
                // 将用户信息存入store
                // 若未勾选记住我，则仅将数据（包括token）记录在store中
                // 若勾选记住我，则将token记录在store和localStorage中，下次打开页面时首先检测是否有有效token(在路由中实现)
                if (loginInfo.rememberMe) {
                  // 将token存入localStorage
                  localStorage.setItem("token", response.data.data.token);
                }
                // 将用户信息存入store
                const store = useMainStore();
                store.userInfo = response.data.data;
                store.userStatus.isLogin = true;
                // 跳转到控制台
                this.$router.push('/dashboard');


              } else {
                // 处理登录失败（账号密码错误，或账号不存在等情况）的情况
                console.log('Login failed:', response.data.message);
                snackbar({
                  message: response.data.message,
                });
                // 在这里可以根据错误信息提示用户登录失败等
                // 按钮样式
                this.isSubmitting=false
              }
            })
            .catch(error => {
              // 处理请求失败的情况
              console.error('Request failed:', error);
              snackbar({
                message: "内部错误"+error,
              });
              // 按钮样式
              this.isSubmitting=false
            });


      }

  },
    routerTo(path) {
      this.$router.push(path);
    }
},
  data(){
    return {
      isSubmitting:false
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
        <div class="card-header-title">登录</div>
      </div>
      <mdui-tabs value="useEmail" id="login-type">
        <mdui-tab value="useEmail" icon="email" inline>邮箱登录</mdui-tab>
        <mdui-tab value="usePhone" icon="phone" inline>手机登录</mdui-tab>
        <mdui-tab-panel slot="panel" value="useEmail">
          <div class="tab-panel-div">
            <mdui-text-field icon="email" label="邮箱" type="email" id="loginEmail" required></mdui-text-field>
            <mdui-text-field icon="key" label="密码" type="password" toggle-password id="loginEmail-pwd" required></mdui-text-field>
          </div>

        </mdui-tab-panel>
        <mdui-tab-panel slot="panel" value="usePhone">
          <div class="tab-panel-div">
            <mdui-text-field icon="phone" label="手机号码" type="number" id="loginPhone" required></mdui-text-field>
            <mdui-text-field icon="key" label="密码" type="password" toggle-password id="loginPhone-pwd" required></mdui-text-field>
          </div>
        </mdui-tab-panel>
      </mdui-tabs>
      <div class="card-others">
        <mdui-checkbox id="checkbox-rememberMe">记住我</mdui-checkbox>
        <div class="action-1">
          <div class="action-1-1">
            <mdui-button variant="outlined" @click="routerTo('/findpass')">忘记密码</mdui-button>
            <mdui-button variant="tonal" @click="routerTo('/signup')">注册</mdui-button>
          </div>
          <mdui-button variant="filled" @click="submitLoginRequest()" :disabled="isSubmitting" :loading="isSubmitting">登录</mdui-button>
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
  .card{
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
  }

  .card mdui-tab{
    padding: 10px;
  }
  .card mdui-tab-panel{
    padding: 20px;
  }
  .card .tab-panel-div{
    display: flex;
    flex-direction: column;
    gap:10px;
  }
  .card-others{
    padding: 0 20px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
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
  .card{
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
  }

  .card mdui-tab{
    padding: 10px;
  }
  .card mdui-tab-panel{
    padding: 20px;
  }
  .card .tab-panel-div{
    display: flex;
    flex-direction: column;
    gap:10px;
  }
  .card-others{
    padding: 0 20px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
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
  .card{
    display: flex;
    flex-direction: column;
    justify-content: center;
    width: 100%;
  }

  .card mdui-tab{
    padding: 10px;
  }
  .card mdui-tab-panel{
    padding: 20px;
  }
  .card .tab-panel-div{
    display: flex;
    flex-direction: column;
    gap:10px;
  }
  .card-others{
    padding: 0 20px 20px 20px;
    display: flex;
    flex-direction: column;
    gap: 10px;
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
.card-header{
  padding: 40px 20px 10px 20px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 10px;
  background-color: rgb(var(--mdui-color-surface));
}
.shade{
  z-index: 0;
  position: absolute;
  width: 100%;
  height: calc(100vh - 64px);
  background: rgba(var(--mdui-color-surface-dim),.8);
}
</style>