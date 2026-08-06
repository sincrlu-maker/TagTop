# 细分 — 标签配对 Demo

这是一个前端 POC，模拟“视频自动打标签 → 用户确认 → 基于标签配对”流程。所有逻辑在浏览器中运行（mock），便于在 GitHub Pages 上一键部署演示。

本仓库需要创建一个名为 starter/tag-social 的分支并包含本提交的文件；工作流会在推送到该分支时自动构建并把站点部署到 gh-pages。

本地运行：
1. npm install
2. npm run dev
3. 打开 http://localhost:5173

部署：
- 将变更 push 到 starter/tag-social 分支（或者在 GitHub 网页端新建分支并逐文件添加）
- GitHub Actions workflow 会在 push 到 starter/tag-social 时触发并把 dist 发布到 gh-pages

说明：
- 当前的标签生成为本地 mock（根据文件名模拟）。要替换为真实模型/后端，请把 Upload 组件里的 mock 模块替换为调用后端推理的 API，并在前端调用保存 API。
