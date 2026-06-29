---
ai_analyzed: true
categories:
- 学科
- 数学
date: 2026-05-21 21:56:48
mathjax: true
tags:
- 立体几何
- 几何
- 三角函数
- 数学
title: 球面余弦定理
---

![示意图](/images/2026/05/21/ball_cosine/image.png)

如图，球 $O$ 是以点 $O$ 为球心的单位球，圆 $O$ 是球 $O$ 的大圆（球心截面）。

过点 $O'$ 作平行于圆 $O$ 的球截面圆 $O'$。

在圆 $O$ 上任取两点 $A, B$，分别在圆 $O'$ 上做其正投影。

作射线 $O'A', O'B'$，分别过 $A, B$ 的正投影点并交圆 $O'$ 于 $A', B'$。

连接 $OA, OB, OA', OB'$。

现探究 $\angle A'OB'$ 与 $\angle AOB$、$\angle A'OA$ 的关系。

<!-- more -->

## 探究过程

不妨建立空间直角坐标系。令 $OB$ 为 $x$ 轴正方向，$OO'$ 为 $z$ 轴正方向，点 $O$ 为原点，建立空间直角坐标系如图所示。

易知圆 $O$ 位于平面 $xy$ 上且为单位圆。

设圆 $O'$ 位于平面 $z = h$ 上（$-1 < h < 1$），$\angle AOB = \alpha$，$\angle A'OB' = \beta$，$\angle A'OA = \gamma$。

则易知：
$$
O(0, 0, 0), \quad O'(0, 0, h), \quad A(\cos\alpha, \sin\alpha, 0), \quad B(1, 0, 0)
$$

由于圆 $O'$ 在球面 $x^2 + y^2 + z^2 = 1$ 且平面 $z = h$ 上，则它的半径为：
$$
r = \sqrt{1 - h^2}
$$

向量 $\overrightarrow{OA}$ 和 $\overrightarrow{OB}$ 投影到圆 $O'$ 所在平面后，对应点 $A'$ 和 $B'$ 的经度角保持不变，即：
$$
A'(r\cos\alpha, r\sin\alpha, h), \quad B'(r, 0, h)
$$

由于 $A'$ 和 $B'$ 都在球面上，所以 $|\overrightarrow{OA'}| = |\overrightarrow{OB'}| = 1$。

接着利用向量点积可以得到：
$$
\cos\beta = \overrightarrow{OA'} \cdot \overrightarrow{OB'} = r^2 \cos\alpha + h^2
$$
$$
\cos\gamma = \overrightarrow{OA'} \cdot \overrightarrow{OA} = r
$$

则：
$$
\sin^2\gamma = 1 - \cos^2\gamma = 1 - r^2 = 1 - (1 - h^2) = h^2
$$

代入，最终得：
$$
\cos\beta = \cos\alpha \cos^2\gamma + \sin^2\gamma
$$

## 结论

**球面余弦定理**：
$$
\cos\angle A'OB' = \cos\angle AOB \cdot \cos^2\angle A'OA + \sin^2\angle A'OA
$$
