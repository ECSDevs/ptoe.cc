---
ai_analyzed: true
categories:
- 编程
- 算法
date: 2025-07-25 14:18:59
tags:
- 编程
- 数学
- C++
- 算法
title: '[C++] 多线程计算π'
---

让 AI 写了个多线程计算 π 的程序，非常适合跑分（（（

<!-- More -->

```cpp
#define _USE_MATH_DEFINES
#include <iostream>
#include <random>
#include <thread>
#include <vector>
#include <chrono>
#include <atomic>
#include <mutex>
#include <cmath>

// 全局变量
std::atomic<unsigned long long> total_in_circle(0);
unsigned long long total_points = 0;
std::mutex cout_mutex;

// 每个线程的工作函数
void monte_carlo_pi(unsigned long long points_per_thread, int thread_id) {
	std::random_device rd;
	std::mt19937 gen(rd());
	std::uniform_real_distribution<> dis(-1.0, 1.0);

	unsigned long long in_circle = 0;

	auto start = std::chrono::high_resolution_clock::now();

	for (unsigned long long i = 0; i < points_per_thread; ++i) {
		double x = dis(gen);
		double y = dis(gen);
		if (x * x + y * y <= 1.0) {
			++in_circle;
		}
	}

	auto end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> elapsed = end - start;

	// 累加到全局计数器
	total_in_circle += in_circle;

	// 输出线程信息
	std::lock_guard<std::mutex> lock(cout_mutex);
	std::cout << "Thread " << thread_id << " completed in " << elapsed.count()
	<< " seconds (" << points_per_thread << " points)" << std::endl;
}

int main(int argc, char* argv[]) {
	if (argc != 3) {
		std::cerr << "Usage: " << argv[0] << " <total_points> <num_threads>" << std::endl;
		return 1;
	}

	total_points = std::stoull(argv[1]);
	unsigned int num_threads = std::stoi(argv[2]);

	if (num_threads == 0) {
		num_threads = std::thread::hardware_concurrency();
		std::cout << "Using " << num_threads << " threads (auto-detected)" << std::endl;
	}

	unsigned long long points_per_thread = total_points / num_threads;
	unsigned long long remainder = total_points % num_threads;

	std::vector<std::thread> threads;
	threads.reserve(num_threads);

	auto program_start = std::chrono::high_resolution_clock::now();

	// 创建线程
	for (unsigned int i = 0; i < num_threads; ++i) {
		unsigned long long points = points_per_thread;
		if (i < remainder) {
			points += 1;
		}
		threads.emplace_back(monte_carlo_pi, points, i);
	}

	// 等待所有线程完成
	for (auto& thread : threads) {
		thread.join();
	}

	auto program_end = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> program_elapsed = program_end - program_start;

	// 计算π值
	double pi_estimate = 4.0 * total_in_circle.load() / total_points;
	double error = std::abs(pi_estimate - M_PI);

	// 输出结果
	std::cout << "\nResults:" << std::endl;
	std::cout << "Total points: " << total_points << std::endl;
	std::cout << "Points in circle: " << total_in_circle << std::endl;
	std::cout << "Estimated π: " << pi_estimate << std::endl;
	std::cout << "Actual π: " << M_PI << std::endl;
	std::cout << "Error: " << error << std::endl;
	std::cout << "Total time: " << program_elapsed.count() << " seconds" << std::endl;
	std::cout << "Points per second: "
	<< total_points / program_elapsed.count() << std::endl;

	return 0;
}
```
