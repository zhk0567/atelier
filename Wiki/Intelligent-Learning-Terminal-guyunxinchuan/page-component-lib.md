<!-- wiki_page_id: page-component-lib -->

<details>
<summary>Relevant source files</summary>

The following files were used as context for generating this wiki page:

- [miniprogram\components\cover\index.json](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\cover\index.json)
- [miniprogram\components\cover\index.ts](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\cover\index.ts)
- [miniprogram\components\icon\index.json](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\icon\index.json)
- [miniprogram\components\icon\index.ts](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\icon\index.ts)
- [miniprogram\components\section\index.json](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\section\index.json)
- [miniprogram\components\section\index.ts](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/miniprogram\components\section\index.ts)
- [web\src\components\Cover.tsx](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/web\src\components\Cover.tsx)
- [web\src\components\Icon.tsx](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/web\src\components\Icon.tsx)
- [web\src\components\Section.tsx](https://github.com/zhk0567/Intelligent-Learning-Terminal/blob/guyunxinchuan/web\src\components\Section.tsx)
</details>

# 可复用组件库

## 概述

Intelligent-Learning-Terminal 项目提供了一套可复用的组件库，用于在微信小程序和 Web 应用中构建统一的用户界面。该组件库包括 Cover、Icon 和 Section 三个核心组件，分别实现了小程序和 Web 端的版本，以确保跨平台的一致性。

## 组件列表

| 组件名称 | 小程序实现 | Web 实现 | 说明 |
|----------|------------|----------|------|
| Cover    | miniprogram/components/cover | web/src/components/Cover.tsx | 封面组件，用于展示标题和背景 |
| Icon     | miniprogram/components/icon  | web/src/components/Icon.tsx  | 图标组件，支持自定义名称和样式 |
| Section  | miniprogram/components/section | web/src/components/Section.tsx | 区块组件，用于页面内容分段 |

## 组件详情

### Cover 组件

#### 小程序实现（miniprogram/components/cover）

- **index.json**：定义组件使用 `component: true` 启用组件功能
- **index.ts**：
  - 使用 Behavior 定义组件行为
  - 包含属性定义（properties）：
    - `title`: 标题文本，类型为 String
    - `imageUrl`: 背景图片URL，类型为 String
  - 包含数据定义（data）：用于内部状态管理
  - 包含方法（methods）：目前为空对象，预留扩展接口

#### Web 实现（web/src/components/Cover.tsx）

- 使用 React 函数式组件
- 接收属性：
  - `title`: 标题文本（string）
  - `imageUrl`: 背景图片URL（string）
- 返回 JSX 结构：
  - 外层 div 使用类名 `cover` 进行样式控制
  - 包含 img 元素展示背景图片（当 imageUrl 存在时）
  - 包含 h1 元素展示标题文本

### Icon 组件

#### 小程序实现（miniprogram/components/icon）

- **index.json**：定义组件使用 `component: true`
- **index.ts**：
  - 使用 Behavior 定义组件行为
  - 包含属性定义（properties）：
    - `name`: 图标名称，类型为 String
    - `size`: 图标尺寸，类型为 String，默认值为 '24px'
    - `color`: 图标颜色，类型为 String，默认值为 '#333'
  - 包含数据定义（data）：用于内部状态管理
  - 包含方法（methods）：目前为空对象

#### Web 实现（web/src/components/Icon.tsx）

- 使用 React 函数式组件
- 接收属性：
  - `name`: 图标名称（string）
  - `size`: 图标尺寸（string，默认 '24px'）
  - `color`: 图标颜色（string，默认 '#333'）
- 返回 JSX 结构：
  - 使用 i 元素并设置类名为 `icon` 以及动态类名（基于 name）
  - 通过 style 属性动态设置字体大小和颜色

### Section 组件

#### 小程序实现（miniprogram/components/section）

- **index.json**：定义组件使用 `component: true`
- **index.ts**：
  - 使用 Behavior 定义组件行为
  - 包含属性定义（properties）：
    - `title`: 区块标题，类型为 String
    - `padding`: 内边距，类型为 String，默认值为 '16px'
  - 包含数据定义（data）：用于内部状态管理
  - 包含方法（methods）：目前为空对象

#### Web 实现（web/src/components/Section.tsx）

- 使用 React 函数式组件
- 接收属性：
  - `title`: 区块标题（string）
  - `padding`: 内边距（string，默认 '16px'）
- 返回 JSX 结构：
  - 外层 div 使用类名 `section` 并通过 style 属性设置内边距
  - 包含 h2 元素展示区块标题（当 title 存在时）
  - 包含 props.children 用于渲染子元素

## 设计特点

1. **跨平台一致性**：小程序和 Web 端组件保持相同的属性接口和行为表现
2. **可配置性**：所有组件通过属性（props）进行配置，支持灵活定制
3. **扩展性**：组件实现预留了方法空间，便于后续添加业务逻辑
4. **样式分离**：通过类名和内联样式相结合的方式，实现样式的灵活控制
5. **轻量级**：组件实现简洁，未引入复杂依赖，易于维护和迁移

## 使用指南

### 在小程序中使用

1. 确保在对应页面的 json 配置文件中声明使用的自定义组件：
   ```json
   {
     "usingComponents": {
       "cover": "/components/cover/index",
       "icon": "/components/icon/index",
       "section": "/components/section/index"
     }
   }
   ```

2. 在 WXML 中直接使用组件：
   ```xml
   <cover title="欢迎使用" imageUrl="/assets/bg.jpg" /><icon name="search" size="32px" color="#007aff" /><section title="功能介绍" padding="20px">
     <view>具体内容...</view></section>
   ```

### 在 Web 应用中使用

1. 在需要使用的地方导入组件：
   ```tsx
   import Cover from '@/components/Cover';
   import Icon from '@/components/Icon';
   import Section from '@/components/Section';
   ```

2. 在 JSX 中使用组件：
   ```tsx
   <Cover title="欢迎使用" imageUrl="/assets/bg.jpg" />
   <Icon name="search" size="32px" color="#007aff" />
   <Section title="功能介绍" padding="20px">
     <div>具体内容...</div>
   </Section>
   ```

## 实现对比

| 方面 | 小程序实现 | Web 实现 |
|------|------------|----------|
| 框架 | 原生小程序组件 | React 函数式组件 |
| 属性定义 | Behavior.properties | 函数参数 |
| 状态管理 | this.data | Hooks（当前未使用）或内部状态 |
| 事件处理 | 方法定义在 methods 中 | 事件处理函数 |
| 渲染层 | WXML 模板 | JSX |
| 样式引用 | 外部或内联 WXSS | CSS 模块或内联样式 |

## 维护建议

1. 保持小程序和 Web 端组件的 API 一致性
2. 当添加新属性时，同时更新两端实现
3. 考虑将样式抽离到统一的样式文件中以避免重复
4. 为复杂组件添加 PropTypes 或 TypeScript 类型检查
5. 编写单元测试以确保组件行为符合预期

## 相关文件结构

```text
miniprogram/
└── components/
    ├── cover/
    │   ├── index.json
    │   └── index.ts
    ├── icon/
    │   ├── index.json
    │   └── index.ts
    └── section/
        ├── index.json
        └── index.ts

web/
└── src/
    └── components/
        ├── Cover.tsx
        ├── Icon.tsx
        └── Section.tsx
```</details>