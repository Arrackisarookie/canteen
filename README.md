# canteen
An unsafe chat room implemented by FastAPI and bootstrap.

## Todo
1. [x] 访客直接发言
2. [x] 昵称随机生成
3. [x] 转向Jinja2
4. [x] 聊天框固定大小
5. [x] 头像
6. [x] 仿微信气泡
7. [x] 自由随机昵称
8. [ ] 个人发言在右，其他发言在左
9. [ ] 缓冲区50条消息
10. [ ] 处理滚动条
11. [ ] 前端迁移至vue
12. [ ] 跨域的问题

## Reference
+ [FastAPI WebSocket](https://fastapi.tiangolo.com/zh/advanced/websockets/)
+ [Boomerang UI Kit](https://www.bootmb.com/themes/boomerang/)
+ [CSS3 巧妙实现聊天气泡](https://segmentfault.com/a/1190000007159738)

## Notice
Vercel 部署时需要将 Nodejs 版本由 `20.*` 改为 `18.*`，否则会报 Python 版本不支持啥的。
