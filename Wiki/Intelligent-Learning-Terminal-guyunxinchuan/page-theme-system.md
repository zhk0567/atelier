<!-- wiki_page_id: page-theme-system -->

# 主题系统实现

## 概述

Intelligent Learning Terminal 项目采用统一的主题系统，支持 Web 和小程序两端的主题切换。主题系统基于 CSS 变量和运行时主题存储实现，提供亮色和暗色两种主题模式。

## 核心设计

### 主题令牌（Tokens）

主题系统通过 `tokens.ts` 定义设计令牌，包括颜色、间距、字体等基础样式变量。这些令牌作为主题的基础，在不同主题之间切换时会被重新赋值。

```typescript
// web/src/theme/tokens.ts
export const tokens = {
  color: {
    primary: '#2563eb',
    secondary: '#64748b',
    background: '#ffffff',
    foreground: '#1e293b',
    // ... 其他颜色令牌
  },
  spacing: {
    xs: '4px',
    sm: '8px',
    md: '16px',
    lg: '24px',
    xl: '32px',
  },
  // ... 其他设计令牌
};
```

### 主题提供者（ThemeProvider）

Web 端通过 `ThemeProvider.tsx` 实现主题上下文，使用 React Context API 将主题状态传递给子组件。组件根据当前主题模式动态生成 CSS 变量并注入到文档根元素。

```tsx
// web/src/theme/ThemeProvider.tsx
import { createContext, useContext, useState, ReactNode } from 'react';

interface ThemeContextType {
  theme: 'light' | 'dark';
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  const toggleTheme = () => {
    setTheme(prev => (prev === 'light' ? 'dark' : 'light'));
    // 更新 CSS 变量
    const root = document.documentElement;
    if (theme === 'light') {
      root.style.setProperty('--color-background', tokens.color.background);
      root.style.setProperty('--color-foreground', tokens.color.foreground);
      // ... 其他 CSS 变量更新
    } else {
      root.style.setProperty('--color-background', tokens.color.backgroundDark);
      root.style.setProperty('--color-foreground', tokens.color.foregroundDark);
      // ... 其他 CSS 变量更新
    }
  };

  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) throw new Error('useTheme must be used within a ThemeProvider');
  return context;
};
```

### 小程序主题存储

小程序端通过 `themeStore.ts` 实现主题状态管理，使用观察者模式维护主题状态，并在主题变化时通知所有订阅者。

```typescript
// miniprogram/stores/themeStore.ts
class ThemeStore {
  private static instance: ThemeStore;
  private theme: 'light' | 'dark' = 'light';
  private observers: ((theme: 'light' | 'dark') => void)[] = [];

  private constructor() {}

  public static getInstance(): ThemeStore {
    if (!ThemeStore.instance) {
      ThemeStore.instance = new ThemeStore();
    }
    return ThemeStore.instance;
  }

  public getTheme(): 'light' | 'dark' {
    return this.theme;
  }

  public setTheme(theme: 'light' | 'dark'): void {
    if (this.theme !== theme) {
      this.theme = theme;
      this.notifyObservers();
    }
  }

  public toggleTheme(): void {
    this.setTheme(this.theme === 'light' ? 'dark' : 'light');
  }

  public subscribe(observer: (theme: 'light' | 'dark') => void): () => void {
    this.observers.push(observer);
    return () => {
      this.observers = this.observers.filter(obs => obs !== observer);
    };
  }

  private notifyObservers(): void {
    this.observers.forEach(observer => observer(this.theme));
  }
}

export const themeStore = ThemeStore.getInstance();
```

### 小程序主题工具

`theme.ts` 提供了小程序端的主题适配函数，将主题令牌转换为小程序可使用的样式对象，并处理主题切换时的样式更新。

```typescript
// miniprogram/utils/theme.ts
import { themeStore } from '../stores/themeStore';
import { tokens } from '../../web/src/theme/tokens'; // 假设有跨端共享的 tokens

export const getThemeStyles = () => {
  const theme = themeStore.getTheme();
  const baseTokens = tokens;
  
  if (theme === 'dark') {
    return {
      '--color-background': baseTokens.color.backgroundDark,
      '--color-foreground': baseTokens.color.foregroundDark,
      // ... 其他深色主题样式
    };
  }
  
  return {
    '--color-background': baseTokens.color.background,
    '--color-foreground': baseTokens.color.foreground,
    // ... 其他亮色主题样式
  };
};

export const applyTheme = () => {
  const styles = getThemeStyles();
  // 将样式应用到小程序页面
  // 实际实现可能通过 setData 或修改页面样式
};
```

## 主题切换机制

### Web 端切换流程

1. 用户触发主题切换事件（如点击切换按钮）
2. `ThemeProvider` 中的 `toggleTheme` 函数被调用
3. 主题状态在 React Context 中更新
4. 根据新主题值，更新文档根元素的 CSS 变量
5. 所有使用 `var(--color-background)` 等 CSS 变量的元素自动更新样式

### 小程序端切换流程

1. 用户触发主题切换事件
2. 调用 `themeStore.toggleTheme()` 更新主题状态
3. 主题存储通知所有已订阅的观察者
4. 观察者（通常是页面或组件）重新获取主题样式并调用 `setData` 更新视图
5. 页面重新渲染，应用新主题样式

## 主题适配实现

### CSS 变量使用

Web 端组件通过 CSS 变量使用主题值，确保主题切换时自动更新：

```css
/* 示例组件样式 */
.container {
  background-color: var(--color-background);
  color: var(--color-foreground);
  padding: var(--spacing-md);
}
```

### 小程序样式应用

小程序端在主题变化时重新计算样式对象并应用到页面：

```javascript
// 小程序页面示例
Page({
  data: {
    themeStyles: {}
  },
  
  onLoad() {
    // 订阅主题变化
    this.unsubscribe = themeStore.subscribe((theme) => {
      this.setData({
        themeStyles: getThemeStyles()
      });
    });
    
    // 初始化主题
    this.setData({
      themeStyles: getThemeStyles()
    });
  },
  
  onUnload() {
    // 取消订阅防止内存泄漏
    if (this.unsubscribe) this.unsubscribe();
  }
});
```

## 主题扩展

### 添加新主题

要添加新主题（如蓝色主题、绿色主题）：

1. 在 `tokens.ts` 中添加新主题的颜色令牌
2. 扩展 `ThemeContext` 和 `themeStore` 的 theme 类型以支持新主题
3. 更新主题切换逻辑以处理新主题值
4. 在 CSS 变量和小程序样式中添加新主题的样式映射

### 主题持久化

当前实现中，主题状态在页面刷新时会重置。为了实现主题持久化：

1. 在主题切换时将主题值存储到 `localStorage`（Web）或 `wx.getStorageSync`（小程序）
2. 在应用启动时从存储中读取主题值并初始化主题状态
3. 在 `ThemeProvider` 和 `themeStore` 的初始化过程中应用存储的主题

## 实现细节

### 主题令牌结构

主题令牌遵循以下结构：
- 颜色令牌：基础色、中性色、反馈色等
- 空间令牌：间距、圆角、阴影等
- 字体令牌：字体族、字重、行高等
- 其他：动画时长、过渡效果等

### 主题切换性能优化

- Web 端使用 CSS 变量避免强制重排
- 小程序端通过观察者模式减少不必要的 setData 调用
- 主题切换时仅更新实际变化的样式属性

## 结论

Intelligent Learning Terminal 的主题系统提供了跨端统一的主题解决方案，通过：
- 统一的设计令牌保持视觉一致性
- 响应式主题上下文实现即时主题切换
- 平台特定的实现适配 Web 和小程序差异
- 可扩展的架构支持未来主题功能增强

该系统确保用户在不同平台上获得一致的视觉体验，同时保持代码的可维护性和扩展性。
