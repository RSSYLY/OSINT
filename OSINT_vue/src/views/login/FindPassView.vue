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
          <mdui-linear-progress :value="(findingPwdStep+1)/4"></mdui-linear-progress>
          <mdui-text-field v-if="findPwdType === 'useEmail' && !findingPwdStep" icon="email" label="邮箱" type="email" id="findpass-email" required></mdui-text-field>
          <mdui-text-field v-if="findPwdType === 'usePhone' && !findingPwdStep" icon="phone" label="手机" type="number" id="findpass-phone" required></mdui-text-field>
          <p v-if="findingPwdStep===1"><mdui-icon name='done_all'></mdui-icon>已发送验证码，请您查看</p>
          <mdui-text-field v-if="findingPwdStep === 1" icon="key" label="验证码" type="number" id="findpass-rec-code" required></mdui-text-field>
          <mdui-text-field v-if="findingPwdStep === 2" icon="key" label="密码" type="password" id="set-new-pwd" required></mdui-text-field>
          <mdui-text-field v-if="findingPwdStep === 2" icon="key" label="重复密码" type="password" id="set-new-pwd-re" required></mdui-text-field>
        </div>
        <div class="card-others">
          <div class="action-1">
            <mdui-button variant="tonal" @click="routerTo('/login')">返回登录</mdui-button>
            <mdui-button v-if="findingPwdStep === 0" variant="filled" @click="submitFirstRequest()">下一步</mdui-button>
            <mdui-button v-if="findingPwdStep === 1" variant="filled" @click="submitSecondRequest()">下一步</mdui-button>
            <mdui-button v-if="findingPwdStep === 2" variant="filled" @click="submitThirdRequest()">下一步</mdui-button>
            <mdui-button v-if="findingPwdStep === 3" variant="filled" @click="routerTo('/login')">完成</mdui-button>
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
  padding:10px 20px 0 20px;
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