<!-- wiki_page_id: page-state-mgmt -->

# 状态管理机制

## 概述

Intelligent-Learning-Terminal 项目采用 Zustand 库进行状态管理，在 Web 和小程序两端分别实现了统一的状态管理模式。状态被划分为四个核心模块：购物车（cart）、播放器（player）、会话（session）和主题（theme），每个模块独立维护其状态及相关操作。

## 状态模块划分

| 模块 | 负责功能 | 持久化策略 |
|------|----------|------------|
| cart | 购物车商品管理 | 本地存储 |
| player | 音视频播放状态 | 本地存储 |
| session | 用户会话信息 | 本地存储 |
| theme | 应用主题样式 | 本地存储 |

## 状态存储实现

### Web 端实现（使用 Zustand）

所有 Web 端状态存储位于 `web/src/store/` 目录，采用相同的创建模式：

```typescript
import create from 'zustand';
import { persist } from 'zustand/middleware';

// 以 cartStore 为例
export const useCartStore = create(
  persist(
    (set, get) => ({
      // 状态定义
      cartItems: [],
      
      // 状态操作
      addItem: (item) => set((state) => ({
        cartItems: [...state.cartItems, item]
      })),
      
      removeItem: (id) => set((state) => ({
        cartItems: state.cartItems.filter(item => item.id !== id)
      })),
      
      updateItemQuantity: (id, quantity) => set((state) => ({
        cartItems: state.cartItems.map(item =>
          item.id === id ? { ...item, quantity } : item
        )
      })),
      
      clearCart: () => set({ cartItems: [] })
    }),
    {
      name: 'cart-storage', // 本地存储键名
      getStorage: () => localStorage // 使用 localStorage 持久化
    }
  )
);
```

其他存储（playerStore、sessionStore、themeStore）遵循相同模式，仅 differing 在状态字段和操作方法上。

### 小程序端实现（使用 zustand/miniprogram）

小程序端状态存储位于 `miniprogram/stores/` 目录，使用专门的小程序版本 Zustand：

```typescript
import { create } from 'zustand/miniprogram';
import { persist } from 'zustand/middleware';

// 以 cartStore 为例
export const useCartStore = create(
  persist(
    (set, get) => ({
      cartItems: [],
      
      addItem: (item) => set((state) => ({
        cartItems: [...state.cartItems, item]
      })),
      
      removeItem: (id) => set((state) => ({
        cartItems: state.cartItems.filter(item => item.id !== id)
      })),
      
      updateItemQuantity: (id, quantity) => set((state) => ({
        cartItems: state.cartItems.map(item =>
          item.id === id ? { ...item, quantity } : item
        )
      })),
      
      clearCart: () => set({ cartItems: [] })
    }),
    {
      name: 'cart-storage',
      getStorage: () => wx.getStorageSync // 使用小程序同步存储 API
    }
  )
);
```

## 状态持久化机制

所有状态模块均通过 Zustand 的 `persist` 中间件实现持久化：

- **Web 端**：使用 `localStorage` API 自动同步状态变更
- **小程序端**：使用 `wx.getStorageSync` 和 `wx.setStorageSync` 实现状态持久化

持久化配置统一特点：
- 每个存储模块具有唯一的 `name` 字段作为存储键
- 自动在状态变更时写入存储
- 页面初始化时自动从存储恢复状态

## 跨平台状态一致性

尽管 Web 和小程序端使用不同的存储 API，但状态结构和操作接口保持完全一致：

1. **状态字段相同**：四个模块在两端具有相同的状态接口
2. **操作方法相同**：所有状态更新方法（addItem、removeItem等）在两端具有相同的签名和行为
3. **持久化行为一致**：两端都实现自动状态持久化和页面加载时的状态恢复
4. **无副作用差异**：状态更新不依赖平台特定 API，确保行为一致

## 状态使用示例

### 在组件中使用状态

```vue
<!-- Web 端 Vue 组件示例 -->
<template>
  <div>
    <p>购物车商品数量: {{ cartItems.length }}</p>
    <button @click="addProduct">添加商品</button>
  </div></template>

<script setup>
import { useCartStore } from '@/store/cartStore';

const cartStore = useCartStore();
const { cartItems, addItem } = cartStore;

const addProduct = () => {
  addItem({ id: Date.now(), name: '新商品', quantity: 1 });
};
</script>
```

```javascript
// 小程序页面示例
Page({
  onLoad() {
    this.cartStore = useCartStore();
  },
  
  data: {
    cartItems: []
  },
  
  onReady() {
    // 订阅状态更新
    this.cartStore.subscribe(state => {
      this.setData({ cartItems: state.cartItems });
    });
  },
  
  addToCart() {
    this.cartStore.addItem({ id: Date.now(), name: '新商品', quantity: 1 });
  }
});
```

## 状态模块详细说明

### cartStore（购物车状态）

**状态字段**：
- `cartItems`: 商品数组，每项包含 id、name、quantity 等属性

**核心操作**：
- `addItem(item)`: 添加商品到购物车
- `removeItem(id)`: 根据 ID 删除商品
- `updateItemQuantity(id, quantity)`: 更新商品数量
- `clearCart()`: 清空购物车

### playerStore（播放器状态）

**状态字段**：
- `currentTrack`: 当前播放音轨信息
- `isPlaying`: 播放状态布尔值
- `volume`: 音量级别 (0-1)
- `progress`: 播放进度 (0-1)

**核心操作**：
- `setTrack(track)`: 设置当前播放音轨
- `togglePlay()`: 切换播放/暂停状态
- `setVolume(volume)`: 设置音量
- `seek(progress)`: 设置播放进度

### sessionStore（会话状态）

**状态字段**：
- `userInfo`: 用户信息对象
- `token`: 认证令牌
- `isLoggedIn`: 登录状态布尔值

**核心操作**：
- `login(userInfo, token)`: 登录并存储用户信息
- `logout()`: 登出并清除会话数据
- `updateUserInfo(info)`: 更新用户信息

### themeStore（主题状态）

**状态字段**：
- `isDark`: 深色模式布尔值
- `colorScheme`: 颜色方案字符串
- `fontSize`: 字体大小

**核心操作**：
- `toggleDarkMode()`: 切换深色/浅色模式
- `setColorScheme(scheme)`: 设置颜色方案
- `setFontSize(size)`: 设置字体大小

## 设计优势

1. **模块化**：每个状态模块独立维护，降低耦合度
2. **持久化透明**：开发者无需手动处理状态存储和恢复
3. **跨平台一致**：Web 和小程序端状态逻辑完全统一
4. **易于测试**：纯函数式状态更新便于单元测试
5. **性能优化**：Zustand 的细粒度响应式减少不必要的重渲染

## 实现依赖

- `zustand`: 核心状态管理库
- `zustand/middleware`: 提供 persist 中间件用于持久化
- `zustand/miniprogram`: 小程序专用版本（小程序端）

此状态管理机制为 Intelligent-Learning-Terminal 提供了可靠、一致且易于维护的跨平台状态管理解决方案。
