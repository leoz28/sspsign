# ✈️ sspsign – 多机场签到自动化脚本

支持 **多账号、多机场批量签到**，兼容常见机场面板，支持 **青龙面板** 和 **GitHub Actions**，内置 **失败重试机制**，并支持 **多平台推送（含 Bark 图标）**。

---

## 🌟 一键使用（青龙订阅）

```bash
ql repo https://ghproxy.com/https://github.com/leoz28/sspsign/raw/main/ssp.py
```

📌 如果你想 **本地直接运行** 或 **不使用环境变量**，请修改脚本开头的：
```python
cs = 2
```

---

## 📅 青龙订阅配置

| 参数 | 内容 |
|------|------|
| 名称 | 多机场签到 |
| 链接 | `https://kkgithub.com/wdvipa/sspsign.git` |
| 定时类型 | crontab |
| 定时规则 | `2 2 28 * *`（每月 28 日凌晨 2:02） |
| 白名单 | `ssp.py` |

---

## ⚙️ 环境变量说明

### ✉️ 主要参数（必填）

| 参数 | 说明 | 格式 |
|------|------|------|
| `ssp` | 多机场签到数据 | 每行一个机场，格式：`机场名称\|网址\|账号1,密码1;账号2,密码2` |

**示例：**
```
机场A|https://xxx.com|user1@qq.com,password1;user2@qq.com,password2
机场B|https://yyy.com|user3@qq.com,password3
```

---

### 📢 推送配置（选填）

| 参数名 | 说明 | 示例 / 格式 |
|--------|------|-------------|
| `ssp_fs` | 启用的推送方式（多个用 & 分隔） | `push&kt&stb&tel&bark` |
| `ssp_push` | PushPlus 的 token | `PUSHPLUS_TOKEN` |
| `ssp_ktkey` | 酷推 key | `KT_KEY` |
| `ssp_skey` | Server 酱 key | `SCKEY` |
| `ssp_qkey` | Qmsg 私聊 key | `QMSG_KEY` |
| `ssp_telkey` | Telegram 推送配置 | 第一行为 Bot Token，第二行为用户 ID（用换行分隔） |
| `ssp_barkkey` | Bark 推送 key | `BARK_KEY` |
| `ssp_barkicon` | Bark 图标地址（可选） | `https://i.loli.net/2021/09/02/MZpeJ6bEDwNBqgr.png` |

---

## 🧩 支持的面板主题

- ✅ editXY 面板
- ✅ Metron 面板
- ⚠️ 若详情解析失败，可尝试更改面板字段首字母大小写

---

## 🔁 更新日志

- **新增**：失败重试机制，最多尝试 5 次
- **修复**：editXY 和 Metron 签到详情解析
- **支持**：多机场、多账号签到
- **支持**：PushPlus / Telegram / 酷推 / Qmsg / Server酱 / Bark（含图标）
- **新增**：可切换变量运行或直接填写数据运行

---

## ❤️ 支持作者

如果这个项目对你有帮助，请随手点个 ⭐ Star！

---

如需更多定制功能（如 Bark 推送声音 / 分组 / 跳转链接），欢迎提 Issue 或 PR。
