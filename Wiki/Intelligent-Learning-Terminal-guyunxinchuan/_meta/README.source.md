# 古韵薪传（GuyunXinchuan）

本仓库为「古韵薪传」多端工程：**Android 原生应用**、**Web 演示站（Vite + React）** 与 **微信小程序（原生 + TypeScript）**，统一国风视觉与 mock 数据语义；各端独立构建，互不依赖。

## 目录结构（相对仓库根）

| 路径 | 说明 |
|------|------|
| `app/` | **Android Gradle 工程根**：`settings.gradle.kts`、`gradlew*`、`gradle/` 等 |
| `app/app/` | **Application 模块**：`src/`、`AndroidManifest.xml`、`build.gradle.kts` |
| `web/` | **Web 版**：Vite + React，详见 `web/README.md`（若存在）或 `web/start.py` 内注释 |
| `miniprogram/` | **微信小程序版**：原生小程序 + TS，详见 **`miniprogram/README.md`** |

Android 工程名：`GuyunXinchuan`（见 `app/settings.gradle.kts`）。

---

## Android 应用

包名 `com.guyunxinchuan.heritage.music`，主题为传统国风与现代 UI 结合（音乐/非遗相关能力等）。

### 环境要求

- **JDK**：11（与 `app/app/build.gradle.kts` 中 `JavaVersion.VERSION_11` 一致）
- **Android Studio**：建议支持 **AGP 9.1.1**、`compileSdk 36` 的版本
- **Android SDK**：API 36（`platforms;android-36`），最低 **minSdk 21**

### 构建与运行（Windows / PowerShell）

在 **`app/`（Gradle 根目录）** 下执行：

```powershell
Set-Location -LiteralPath '<本仓库根目录>\app'
.\gradlew.bat assembleDebug
```

调试安装：

```powershell
.\gradlew.bat installDebug
```

**Android Studio**：**File → Open**，选择仓库内的 **`app`** 文件夹（内含 `settings.gradle.kts` 的那一层），同步完成后运行。

### 维护说明

- 忽略规则见 **`app/.gitignore`**
- 业务与界面代码在 **`app/app/`** 模块下

---

## Web 版

在仓库根目录：

```powershell
Set-Location -LiteralPath '<本仓库根目录>'
python .\web\start.py
```

将检查 Node/npm、按需安装依赖并启动 Vite；具体参数见 `web/start.py`。

---

## 微信小程序版

在仓库根目录：

```powershell
Set-Location -LiteralPath '<本仓库根目录>'
python .\miniprogram\start.py
```

将尝试通过「微信开发者工具」CLI 打开 `miniprogram/` 目录。**AppID、CLI 与安全端口** 等说明见 **`miniprogram/README.md`**。

---

## 许可证

若需对外分发，请在仓库中补充 `LICENSE` 并在此 README 中更新说明。
