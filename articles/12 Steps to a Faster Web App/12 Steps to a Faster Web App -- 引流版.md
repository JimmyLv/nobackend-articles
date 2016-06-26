欢迎关注[知乎专栏 —— 前端的逆袭](https://zhuanlan.zhihu.com/no-backend)
欢迎关注我的[博客](http://blog.jimmylv.info/)，[知乎](https://www.zhihu.com/people/JimmyLv)，[GitHub](https://github.com/JimmyLv)。

------

原文地址: [12 Steps to a Faster Web App -- Auth0](https://auth0.com/blog/2016/02/22/12-steps-to-a-faster-web-app/)

时过境迁，Web 应用比以往任何时候都更具交互性。搞定性能可以帮助你极大地改善终端用户的体验。阅读以下的技巧并学以致用，看看哪些可以用来改善延迟，渲染时间以及整体性能吧！

## 更快的 Web 应用

优化 Web 应用是一项费劲的工作。Web 应用不仅处于客户端和服务器端的两部分组件当中，通常来说也是由多种多样的技术栈构建而成：数据库，后端组件（一般也是搭建在不同技术架构之上的），以及前端（HTML + JavaScript + CSS + 转化器）。运行时也是变化多端的：iOS，Android，Chrome，Firefox，Edge。如果你曾经工作在一个不同的单一庞大的平台之上，通常情况下性能优化只针对于单一目标（甚至只是目标的单一版本而已），但是现在的话你就可能会意识到任务复杂度要远超于此。这就对了。但这儿也有一些通用的优化指南可以大大优化一个应用。我们将会在接下来的章节中探讨这些指南的内容。

> 一份 Bing 的研究表明，页面加载时间每增加 10ms，网站的年收入就会减少 25 万美元。 —— **Rob Trace 和 David Walp，微软高级程序经理**

### 过早优化？

优化最难的地方就是如何在开发生命周期中最适当的时候去做优化。Donald Knuth 有一句名言：_「过早优化乃万恶之源」_。这句话背后的原因非常简单：因为一不小心就会浪费时间去优化某个 1% 的地方，但是结果却并不会对性能造成什么重大影响。与此同时，一些优化还妨碍了可读性或者是可维护性，甚至还会引入新的 Bug。换句话说，优化不应当被认为是「意味着得到应用程序的最佳性能」，而是「探索优化应用的_正确的方式_，并得到_最大的效益_」。再换句话说，盲目的优化可能会导致效率的丢失，而收益却很小。在你应用以下技巧的时候请将此铭记在心。你最好的朋友就是分析工具：找到你可以进行通过优化获得最大程度改善的性能点，而不用损害应用开发的进程或者可维护性。

> 程序员们浪费了大量时间来思考，或者说是担忧，他们的程序中非关键部分的运行速度。并且他们对于性能的这些尝试，实际上却对代码的调试和维护有着非常消极的影响。我们应当忘记那些不重要的性能影响，在 97% 的时间里都可以这么说：过早优化乃万恶之源。当然我们也不应当在那关键的 3% 上放弃我们的机会。—— Donald Knuth

## 1. JavaScript 压缩和模块打包

JavaScript 应用是以源码形式进行分发的，而源码解析的效率是要比字节码低的。对于一小段脚本来说，区别可以忽略不计。但是对于更大型的应用，脚本的大小会对应用启动时间有着负面的影响。事实上，寄期望于使用 [WebAssembly](https://auth0.com/blog/2015/10/14/7-things-you-should-know-about-web-assembly/) 而获得最大程度的改善，其中之一就是可以得到更快的启动时间。

另一方面，模块打包则用于将不同脚本打包在一起并放进同一文件。更少的 HTTP 请求和单个文件解析都可以减少加载时间。通常情况下，单独一种工具就可以处理打包和压缩。[Webpack](https://webpack.github.io/) 就是其中之一。

示例代码：

```js
function insert(i) {
    document.write("Sample " + i);
}

for(var i = 0; i < 30; ++i) {
    insert(i);
}
```

结果如下：

```js
!function(r){function t(o){if(e[o])return e[o].exports;var n=e[o]={exports:{},id:o,loaded:!1};return r[o].call(n.exports,n,n.exports,t),n.loaded=!0,n.exports}var e={};return t.m=r,t.c=e,t.p="",t(0)}([function(r,t){function e(r){document.write("Sample "+r)}for(var o=0;30>o;++o)e(o)}]);
//# sourceMappingURL=bundle.min.js.map
```

### 进一步打包

你也可以使用 Webpack 打包 CSS 文件以及合并图片。这些特性都可以有助于改善启动时间。研究一下 [Webpack 文档](http://webpack.github.io/docs/)来做些测试吧！

## 2. 按需加载资源

资源（特别是图片）的按需加载或者说_惰性加载_，可以有助于你的 Web 应用在整体上获得更好的性能。对于使用大量图片的页面来说惰性加载有着显著的三个好处：

* 减少向服务器发出的并发请求数量（这就使得页面的其他部分获得更快的加载时间）
* 减少浏览器的内存使用率（更少的图片，更少的内存）
* 减少服务器端的负载

大体上的理念就是只在必要的时候才去加载图片或资源（如视频），比如在第一次被显示的时候，或者是在将要显示的时候对其进行加载。由于这种方式跟你建站的方式密切相关，惰性加载的解决方案通常需要借助其他库的插件或者扩展来实现。举个例子，[react-lazy-load](https://github.com/loktar00/react-lazy-load) 就是一个用于处理 React 惰性加载图片的插件：

```js
const MyComponent = () => (
  <div>
    Scroll to load images.
    <div className="filler" />
    <LazyLoad height={762} offsetVertical={300}>
      <img src='http://apod.nasa.gov/apod/image/1502/HDR_MVMQ20Feb2015ouellet1024.jpg' />
    </LazyLoad>
    (...)
```

一个非常好的实践范例就像 Goggle Images 的[搜索工具](https://www.google.com/search?site=&tbm=isch&source=hp&biw=1366&bih=707&q=parrots&oq=parrots&gs_l=img.12...0.0.0.4086.0.0.0.0.0.0.0.0..0.0....0...1ac..64.img..0.0.0.UJrFBFKkWMA)一样。点击前面的链接并且滑动页面滚动条就可以看到效果了。

## 3. 在使用 DOM 操作库时用上 array-ids

如果你正在使用 [React](https://facebook.github.io/react/)，[Ember](http://emberjs.com/)，[Angular](https://angularjs.org/) 或者其他 DOM 操作库，使用 array-ids（或者 Angular 1.x 中的 track-by 特性）非常有助于实现高性能，对于动态网页尤其如此。我们已经在上一篇程序衡量标准的文章中看到这个特性的效果了： [More Benchmarks: Virtual DOM vs Angular 1 & 2 vs Mithril.js vs cito.js vs The Rest (Updated and Improved!)](https://auth0.com/blog/2016/01/11/updated-and-improved-more-benchmarks-virtual-dom-vs-angular-12-vs-mithril-js-vs-the-rest/)。![](https://pic4.zhimg.com/09b1f892fb1bc817a03bfeec6afb2583_b.png)

此特性背后的主要概念就是尽可能多地重用已有的节点。**Array ids** 使得 DOM 操作引擎可以「知道」在什么时候某个节点可以被映射到数组当中的某个元素。没有 **array-ids** 或者 **track-by** 的话，大部分库都会进行重新排序而摧毁已有的节点并重新创建新的。这就非常损耗性能了。

## 4. 缓存
## 5. 启用 HTTP/2
## 6. 应用性能分析
## 7. 使用负载均衡方案
## 8. 为了更快的启动时间考虑一下同构
## 9. 使用索引加速数据库查询
## 10. 使用更快的转译方案
## 11. 避免或最小化 JavaScript 和 CSS 的使用而阻塞渲染
## 12. 用于未来的一个建议：使用 service workers + 流
## 13. 图片编码优化

更多内容请看[【译】唯快不破：Web 应用的 13 个优化步骤 - 前端的逆袭 - 知乎专栏](https://zhuanlan.zhihu.com/p/21417465?refer=no-backend)

------

欢迎关注[知乎专栏 —— 前端的逆袭](https://zhuanlan.zhihu.com/no-backend)
欢迎关注我的[博客](http://blog.jimmylv.info/)，[知乎](https://www.zhihu.com/people/JimmyLv)，[GitHub](https://github.com/JimmyLv)。