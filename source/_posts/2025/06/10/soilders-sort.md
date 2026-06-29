---
ai_analyzed: true
categories:
- 编程
- 算法
- 数据结构
date: 2025-06-10 21:09:49
mathjax: true
tags:
- C++
- 编程
- 算法
- 排序算法
- 数据结构
title: '[C++] 士兵排列'
---

## 题面

假如你是长官，现在有一些新兵入伍。但是他们不是同时到达军营集合。对于某一个士兵 $i$（编号从 $1$ 到 $n$）, 如果 $s[i]=1$，那么他从队尾入队，如果 $s[i]=0$，那么他从队头入队。当所有士兵入队后，这个时候士兵就有一个排列。然后，从队头到队尾，每个士兵会说出他的能力值 $a[i]$，你需要按照能力值从高到低输出对应的一个排列。

<!-- More -->

## I/O

### 输入

对于每组测试样例，

第一行输入一个正整数 $ n (1 \le n \le 10^5) $，表示士兵的个数。

第二行输入一个字符串 $ s (1 \le |s| \le 10^5) $，表示士兵入队的方式。

第三行输入 $n$ 个正整数 $a_i (1 \le a_i \le 10^9)$，表示入完队后每个士兵从头到尾说出他自己的能力值。
保证每个能力值不同，即 $a_i \ne a_j (i \ne j, 1 \le i,j \le n)$。

#### 样例

```
6
011010
6 1 2 4 5 3
```

### 输出

对于每组测试样例，输出一行排列，表示按上述要求排好序后的一个排列。

#### 样例

```
6 3 2 5 1 4
```

## 题解

由题意，使用STL Deque双向队列模拟，即可

_注：Wayback Machine的代码似乎有问题，我重写了，和之前的思路不一样;)，但是理论上没问题。另外，我找不到那题的OJ了_

```cpp
#include <bits/stdc++.h>
using namespace std;

int main(){
	deque< pair<int, int> > soilders;
	int n;
	cin >> n;
//	cout << "We got n = " << n << endl;
	for(int i=0;i<n;i++){
		char type;
		cin >> type;
//		cout << "We got soilder " << i+1 << " is " << (type=='1'?"Back":"Front") << " inserted." << endl;
		switch (type) {
		case '1':
			soilders.emplace_back(i+1, 0);
			break;
		case '0':
			soilders.emplace_front(i+1, 0);
			break;
		default:
			break;
		}
	}
	vector< pair<int, int> > soilders_listed;
	soilders_listed.reserve(n);
	while(!soilders.empty()){
		int identity = soilders.front().first,
			ability;
		cin >> ability;
		soilders_listed.emplace_back(
			identity,
			ability
		);
//		cout << "We got soilder " << identity << "'s ability is " << ability << endl;
		soilders.pop_front();
	}
	sort(soilders_listed.begin(), soilders_listed.end(),
		[](const pair<int, int>& a, const pair<int, int>& b){
			return a.second > b.second;
		}
	);
	for(auto soilder : soilders_listed){
		cout << soilder.first << " ";
	}
	return 0;
}
```
