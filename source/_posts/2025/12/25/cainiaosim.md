---
ai_analyzed: true
categories:
- 编程
- 算法
- 数据结构
date: 2025-12-25 11:19:17
tags:
- C++
- 编程
- 算法
- 数据结构
- 模拟
title: '[C++] 菜鸟驿站模拟'
---

闲着没事写的

<!-- More -->

```cpp
#include <bits/stdc++.h>
using namespace std;
using namespace chrono;

// 随机数
random_device rd;
mt19937 gen(rd());
uniform_int_distribution dist(0, 999999);
bitset<1000000> conflict;

// 驿站模拟
array<array<vector<int>, 10>, 10> post;

int getItem(){
    int x;
    do{
        x = dist(gen);
    }while(conflict[x]);
    return x;
}

void putItem(int item){
    int col = item / 100000, // 货架号
        row = item / 010000 % 10; // 层数

    auto& r = post[col][row];
    r.insert(lower_bound(r.begin(), r.end(), item), item);
}

int findItem(int item){
    int col = item / 100000, // 货架号
        row = item / 010000 % 10; // 层

    auto& r = post[col][row];
    return distance(r.begin(), lower_bound(r.begin(), r.end(), item));
}


int main(){
    int n;
    cout << "How much item you want to insert? ";
    cin >> n;

    auto b = high_resolution_clock::now();
    while(n--){
        int item = getItem();
        cout << item << " ";
        putItem(item);
    }
    auto e = high_resolution_clock::now();
    auto d = duration_cast<milliseconds>(e-b);
    cout << endl << "Cost " << d.count() << "ms" << endl;

    while(true){
        int i;
        cout << "What item you want to find? ";
        cin >> i;

        b = high_resolution_clock::now();
        cout << i/100000 << "-" << i/10000%10 << "-" << findItem(i) << endl;
        e = high_resolution_clock::now();
        d = duration_cast<milliseconds>(e-b);
        cout << "Cost " << d.count() << "ms" << endl;
    }

    return 0;
}
```
