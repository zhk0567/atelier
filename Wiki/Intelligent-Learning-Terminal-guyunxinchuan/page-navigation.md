<!-- wiki_page_id: page-navigation -->

# 导航与路由系统

## 概述

Intelligent Learning Terminal 采用双端架构（Web + 小程序），导航与路由系统分别在 Web 端和小程序端实现。Web 端使用 React Router 进行页面路由，小程序端通过 tabBar 配置实现底部导航栏切换。

## Web 端路由系统

### 路由结构

Web 应用采用 React Router v6 进行路由管理，主要路由定义在 `App.tsx` 中（虽然未直接提供，但可从页面组件推断）。

### 页面组件

- **Home.tsx**：主页组件，对应路径 `/`
- **About.tsx**：关于页面组件，对应路径 `/about`

### 导航组件

`BottomNav.tsx` 实现了底部导航栏，提供 Home 和 About 页面之间的切换。

```tsx
// web/src/layout/BottomNav.tsx
import { Link } from 'react-router-dom';

const BottomNav = () => {
  return (
    <nav className="bottom-nav"><Link to="/" className="nav-item">
        首页
      </Link>
      <Link to="/about" className="nav-item">
        关于
      </Link>
    </nav>
  );
};

export default BottomNav;
```

### 路由特点

- 使用 `react-router-dom` 的 `Link` 组件进行客户端导航
- 底部导航栏固定在视图底部，提供主要页面切换
- 路由路径采用简洁的层级结构

## 小程序端导航系统

### 底部导航栏（tabBar）

小程序端通过 `app.json` 配置全局 tabBar，并在 `pages/tabBar` 目录下实现具体页面。

```json
// miniprogram/app.json
{
  "tabBar": {
    "color": "#999",
    "selectedColor": "#1aad19",
    "borderStyle": "white",
    "backgroundColor": "#ffffff",
    "list": [
      {
        "pagePath": "pages/tabBar/index",
        "text": "首页",
        "iconPath": "assets/icon_home.png",
        "selectedIconPath": "assets/icon_home_hl.png"
      },
      {
        "pagePath": "pages/about/index",
        "text": "关于",
        "iconPath": "assets/icon_about.png",
        "selectedIconPath": "assets/icon_about_hl.png"
      }
    ]
  }
}
```

### 页面结构

- **tabBar/index**：主页，对应 tabBar 的第一个项
- **about/index**：关于页面，对应 tabBar 的第二个项

### 启动页（splash）

小程序包含启动页，用于在主内容加载前展示品牌或加载状态。

```json
// miniprogram/pages/splash/index.json
{
  "usingComponents": {}
}
```

```ts
// miniprogram/pages/splash/index.ts
Page({
  onLoad() {
    setTimeout(() => {
      wx.switchTab({
        url: '/pages/tabBar/index'
      });
    }, 1500);
  }
});
```

### 导航特点

- 使用 `wx.switchTab` 在 tabBar 页面之间切换
- 启动页延迟 1.5 秒后自动跳转到主页
- tabBar 配置支持自定义图标和颜色主题
- 所有 tabBar 页面必须在 `app.json` 的 `list` 中声明

## 跨平台一致性

尽管 Web 端和小程序端在实现技术栈上有所不同（React vs 原生小程序），但两端在导航结构上保持一致：

1. 都提供首页和关于两个主要页面
2. 都使用底部导航栏作为主要导航方式
3. 导航项顺序保持一致：首页 → 关于
4. 视觉风格通过配置保持协调（颜色、图标等）

## 性能与优化

### Web 端

- 使用客户端路由避免页面刷新
- 链接预加载可通过 React Router 的链接预fetch特性实现（需额外配置）

### 小程序端

- tabBar 切换原生性能良好
- 启动页使用定时跳转避免白屏
- 所有 tabBar 页面预编译，切换迅速

## 扩展性

### 添加新页面

**Web 端**：
1. 创建新的页面组件
2. 在路由配置中添加新路径
3. 在 `BottomNav.tsx` 中添加新导航项

**小程序端**：
1. 创建新的页面目录和文件
2. 在 `app.json` 的 `tabBar.list` 中添加新项
3. 确保页面路径与配置一致

### 主题定制

两端均支持通过配置文件修改导航栏颜色、图标等样式：
- Web 端：通过修改 CSS 样式
- 小程序端：通过修改 `app.json` 中的 tabBar 配置

## 依赖关系

### Web 端依赖
- react-router-dom：用于客户端路由管理

### 小程序端依赖
- 微信小程序原生组件：无需额外依赖，使用内置 tabBar 组件

## 结论

Intelligent Learning Terminal 的导航与路由系统为用户提供了在 Web 和小程序端一致的导航体验。Web 端利用 React Router 实现灵活的客户端路由，而小程序端则利用原生 tabBar 组件实现高性能的底部导航。两端的设计都遵循简洁直观的原则，确保用户可以轻松在首页和关于页面之间切换。系统具有良好的扩展性，便于未来添加新功能和页面。
