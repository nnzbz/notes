# 我对skywalking-rocketbot-ui的改动

1. `vue.config.js`
   在 `module.exports = {` 下面添加

   ```json
   ....

   publicPath: process.env.NODE_ENV === 'production'
   ? '/skywalking/'
   : '/',

   ....

   devServer: {
     proxy: {
       '/skywalking/graphql': {
         // target: `${process.env.SW_PROXY_TARGET || 'http://127.0.0.1:12800'}`,
         target: `${process.env.SW_PROXY_TARGET || 'http://up:8090/skywalking/graphql'}`,
         // changeOrigin: true,
         pathRewrite: { '^/skywalking/graphql': '' },
       },
     },
   },

   ....
   ```

2. 全文搜索 `/graphql` 改为 `/skywalking/graphql`
