# canteen
An unsafe chat room implemented by FastAPI and Vue3.

## Todo
1. [x] 访客直接发言
2. [x] 聊天框固定大小
3. [x] 仿微信气泡
4. [x] 个人发言在右，其他发言在左
5. [x] 前端迁移至vue
6. [ ] 自由随机昵称
7. [ ] 头像
8. [ ] 缓冲区50条消息
9. [ ] 处理滚动条
10. [ ] 跨域的问题
11. [ ] 后台管理

## Reference
+ [FastAPI WebSocket](https://fastapi.tiangolo.com/zh/advanced/websockets/)
+ [Vue](https://vuejs.org/)
+ [Boomerang UI Kit](https://www.bootmb.com/themes/boomerang/)
+ [CSS3 巧妙实现聊天气泡](https://segmentfault.com/a/1190000007159738)

## Notice
Vercel 部署时需要将 Nodejs 版本由 `20.*` 改为 `18.*`，否则会报 Python 版本不支持啥的。
