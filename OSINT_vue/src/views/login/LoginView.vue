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
      // 获取登录方式
      const loginType = document.querySelector('#login-type').getAttribute('value');
      console.log(loginType);
      // 获取记住我
      const rememberMe = document.querySelector('#checkbox-rememberMe').checked;
      // 获取登录信息
      let loginInfo = {};
      if (loginType === 'useEmail') {
        const emailEle = document.querySelector('#loginEmail');
        const pwdEle = document.querySelector('#loginEmail-pwd');
        // 验证是否通过表单验证
        if ( emailEle.reportValidity() && pwdEle.reportValidity()){
          loginInfo = {
            email: document.querySelector('#loginEmail').value,
            password: document.querySelector('#loginEmail-pwd').value,
            rememberMe: rememberMe
          }
        } else {
          snackbar({
            message: "请检查邮箱和密码是否正确",
          });
        }

      } else {
        const phoneEle = document.querySelector('#loginPhone');
        const pwdEle = document.querySelector('#loginPhone-pwd');
        // 验证是否通过表单验证
        if ( phoneEle.reportValidity() && pwdEle.reportValidity()){
          loginInfo = {
            phone: document.querySelector('#loginPhone').value,
            password: document.querySelector('#loginPhone-pwd').value,
            rememberMe: rememberMe
          }
        } else {
          snackbar({
            message: "请检查手机号码和密码是否正确",
          });

        }
      }
      // 发送登录请求
      if(loginInfo.password){
        // 模拟向后端异步请求

        console.log(loginInfo);
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
          <mdui-button variant="filled" @click="submitLoginRequest()">登录</mdui-button>
          <div class="action-1-1">
            <mdui-button variant="tonal" @click="routerTo('/signup')">注册</mdui-button>
            <mdui-button variant="outlined" @click="routerTo('/findpass')">忘记密码</mdui-button>
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