---
ai_analyzed: true
categories:
- 编程
- 算法
date: 2025-07-24 22:34:44
mathjax: true
tags:
- 数学
- 位运算
- C++
- 编程
- 算法
title: '[C++] 二进制减法'
---

闲着没事研究了下二进制减法。

<!--More-->

二进制加法都知道吧，就是异或+进位。

$$
\text{binaryAdd}(a, b) =
\begin{cases}
a & \text{if } b = 0, \\
\text{binaryAdd}(a \oplus b,\ (a \land b) \ll 1) & \text{otherwise.}
\end{cases}
$$

那么同理可得

$$
\text{binarySub}(a, b) =
\begin{cases}
a & \text{if } b = 0, \\
\text{binarySub}(a \oplus b,\ (\neg a \land b) \ll 1) & \text{otherwise.}
\end{cases}
$$

大夫真是妙手回春啊！

虽然真正计算机中是用补码+加法器直接实现的（）

注：

- $ \oplus $ 代表 `^`，按位异或
- $ \land $ 代表 `&`，按位与
- $ \neg $ 代表 `~`，按位非
- $ \ll $ 代表 `<<`，左移

## C++ 实现

```cpp
#include <iostream>
#include <string>
#include <cmath>


void showBinary(const std::string& _, int x, const size_t& digits){
	std::string b;
	while(x){
		b += '0'+(x&1);
		x >>= 1;
	}
	while(b.length()<digits) b += '0';
	for(size_t i=0; i<(b.length() / 2);i++){
		std::swap(b[i], b[b.length()-i-1]);
	}
	std::cout << _ << " = " << b << std::endl;
}

int main(){
	std::ios::sync_with_stdio(false);
	std::cin.tie(0);
	std::cout.tie(0);

	// Binary Minus
	int a, b, c;
	std::cin >> a >> b;

	size_t s = std::max((int)log2(a)+1, (int)log2(b)+1);
	std::cout << "s = " << s << std::endl;

	showBinary("a", a, s);
	showBinary("b", b, s);

	while(b){
		c = a^b;
		showBinary("a", c, s);
		b = ((~a)&b) << 1;
		showBinary("b", b, s);
		a = c;
	}

	std::cout << a;
	return 0;
}
```
