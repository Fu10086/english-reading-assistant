# GitHub 推送指南

## 第一步：在 GitHub 创建仓库

1. 访问：https://github.com/new
2. 仓库名称：`english-reading-assistant`
3. 描述：`AI-powered English reading assistant based on Claude`
4. 选择：Public（公开）
5. **不要**勾选 "Add a README file"（我们已经有了）
6. **不要**勾选 "Add .gitignore"（我们已经有了）
7. 点击 "Create repository"

## 第二步：推送代码

创建仓库后，GitHub 会显示推送命令。在服务器执行：

```bash
cd /home/ubuntu/english-reading-assistant

# 添加远程仓库（替换成你的用户名）
git remote add origin https://github.com/你的用户名/english-reading-assistant.git

# 推送代码
git push -u origin master
```

如果需要输入用户名和密码：
- 用户名：你的 GitHub 用户名
- 密码：使用 Personal Access Token（不是 GitHub 密码）

### 如何获取 Personal Access Token：

1. 访问：https://github.com/settings/tokens
2. 点击 "Generate new token" → "Generate new token (classic)"
3. 勾选 `repo` 权限
4. 点击 "Generate token"
5. 复制 token（只显示一次）
6. 在推送时用 token 作为密码

## 第三步：验证

推送成功后，访问：
```
https://github.com/你的用户名/english-reading-assistant
```

应该能看到所有文件和 README。

---

## 推送后的仓库链接

在申请材料中填写：
```
https://github.com/你的用户名/english-reading-assistant
```
