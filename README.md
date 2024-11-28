# PCL2-homepage-collection
托管 PCL2 自定义主页文件

**此托管与 PCL2 官方无关，此处收录与 PCL2 收录无关**

为了降低自定义主页的成本和维护门槛（但并非质量门槛，本 collection 有权拒绝低质主页），本 collection 将维护一个统一的 CDN 供主页作者使用，无需为维护和潜在的攻击风险担心。

主页作者可以提供一个可以被 GitHub Action 访问的 url（例如 GitHub 文件、最新 Release 直链），并在 issue 申请收录（参考 [#2528](https://github.com/Hex-Dragon/PCL2/discussions/2528) 提供信息）。

此处将维护一个主页列表，并定时收集主页文件，部署到 GitHub pages，然后由 CDN 提供主页文件外链。

更新延迟由 GitHub action 间隔（每 5 分钟一次）决定。

鸣谢：CDN 由 @pysio2007 提供~
