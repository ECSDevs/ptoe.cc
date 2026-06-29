---
ai_analyzed: true
categories:
- 编程
- 算法
- 数据结构
date: 2025-06-13 20:35:16
tags:
- C++
- 编程
- 递归
- 算法
- 深度优先搜索
- 数据结构
title: '[C++] 全排列'
---

有 1∼n 这 n（n<10）个数，现将这 n 个数组成一个 n 位的数，每个数只能用一次，例如 n=2，则 12，21 等都是符合条件的数，但 11 和 22 不行。

问，输入 n 后，将符合条件的所有的 n 位数输出，且按照从小到大顺序输出。

<!-- More -->

## I/O

### 输入

一个正整数 n。

```in 样例
2
```

### 输出

按从小到大输出所有的全排列数，每行一个数（中间用空格隔开）。

```out 样例
1 2
2 1
```

## 答案

```cpp
#include <bits/stdc++.h>
using namespace std;

int n;
map<int, bool> used;

void printSort(int deep){
	if(deep>=n){
		cout << endl;
		return;
	}
	for(int i=1;i<=n;i++)
		if(!used[i]){
			cout << i << " ";
			used[i] = true;
			printSort(deep+1);
			used[i] = false;
		}
}

int main(){
	cin >> n;
	printSort(0);
	return 0;
}
```

简单递归。
