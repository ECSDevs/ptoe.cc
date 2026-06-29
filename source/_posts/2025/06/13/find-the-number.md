---
ai_analyzed: true
categories:
- 编程
- 算法
- 数据结构
date: 2025-06-13 20:13:33
mathjax: true
tags:
- 数据结构
- 排序算法
- C++
- 算法
title: '[C++] 找数'
---

有两组数字，请找出第二组数中的哪些数在第一组中出现了，并从小到大输出。

<!-- More -->

## I/O

### 输入

- 第一行两个整数 n 和 m，分别代表 2 组数的数量。
- 第二行 n 个正整数。
- 第三行 m 个正整数。

#### 样例

```
7 7
8 7 9 8 2 6 3
9 6 8 3 3 2 10
```

### 输出

按照要求输出满足条件的数，数与数之间用空格隔开。

#### 样例

```
2 3 3 6 8 9
```

### 数据范围

对于 100% 的数据 $1≤n,m≤100000$，每个数 $≤2×10^9$

## 答案

这题我们用 map 就能很简单的做出来，输入第一组数的时候在 map 中保存哪些数存在，再在输入第二组数的时候将 map 中标记为存在的数存进 vector，最后用 STL 函数 sort 排序，输出即可。

```cpp
#include <bits/stdc++.h>
using namespace std;

map<int, bool> f;
vector<int> b;
int n, m, t;

int main(){
	cin >> n >> m;
	while(n--){
		cin >> t;
		f[t] = true;
	}
	while(m--){
		cin >> t;
		if(f[t]) b.emplace_back(t);
	}
	sort(b.begin(), b.end());
	for(auto& a : b) cout << a << " ";
	return 0;
}
```
