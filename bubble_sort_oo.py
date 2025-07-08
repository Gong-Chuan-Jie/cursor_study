import time
import random
from typing import List, Callable, Optional
from enum import Enum
from dataclasses import dataclass


class SortStrategy(Enum):
    """排序策略枚举"""
    STANDARD = "standard"
    OPTIMIZED = "optimized"
    BIDIRECTIONAL = "bidirectional"


@dataclass
class SortResult:
    """排序结果数据类"""
    sorted_array: List
    execution_time: float
    comparisons: int
    swaps: int
    strategy: SortStrategy


class BubbleSorter:
    """
    面向对象的冒泡排序器
    支持多种排序策略和性能监控
    """
    
    def __init__(self, strategy: SortStrategy = SortStrategy.STANDARD):
        """
        初始化排序器
        
        Args:
            strategy: 排序策略
        """
        self.strategy = strategy
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0.0
        
    def reset_metrics(self):
        """重置性能指标"""
        self.comparisons = 0
        self.swaps = 0
        self.execution_time = 0.0
    
    def _compare(self, a, b) -> bool:
        """比较两个元素并记录比较次数"""
        self.comparisons += 1
        return a > b
    
    def _swap(self, arr: List, i: int, j: int):
        """交换数组中的两个元素并记录交换次数"""
        arr[i], arr[j] = arr[j], arr[i]
        self.swaps += 1
    
    def sort_standard(self, arr: List) -> List:
        """
        标准冒泡排序
        
        Args:
            arr: 待排序数组
            
        Returns:
            排序后的数组
        """
        n = len(arr)
        arr_copy = arr.copy()
        
        for i in range(n):
            swapped = False
            
            for j in range(0, n - i - 1):
                if self._compare(arr_copy[j], arr_copy[j + 1]):
                    self._swap(arr_copy, j, j + 1)
                    swapped = True
            
            if not swapped:
                break
        
        return arr_copy
    
    def sort_optimized(self, arr: List) -> List:
        """
        优化版冒泡排序
        记录最后一次交换的位置
        
        Args:
            arr: 待排序数组
            
        Returns:
            排序后的数组
        """
        n = len(arr)
        arr_copy = arr.copy()
        last_swap = n - 1
        
        while last_swap > 0:
            current_swap = 0
            
            for j in range(last_swap):
                if self._compare(arr_copy[j], arr_copy[j + 1]):
                    self._swap(arr_copy, j, j + 1)
                    current_swap = j
            
            last_swap = current_swap
        
        return arr_copy
    
    def sort_bidirectional(self, arr: List) -> List:
        """
        双向冒泡排序（鸡尾酒排序）
        
        Args:
            arr: 待排序数组
            
        Returns:
            排序后的数组
        """
        arr_copy = arr.copy()
        n = len(arr_copy)
        left = 0
        right = n - 1
        
        while left < right:
            # 从左到右冒泡
            for i in range(left, right):
                if self._compare(arr_copy[i], arr_copy[i + 1]):
                    self._swap(arr_copy, i, i + 1)
            right -= 1
            
            # 从右到左冒泡
            for i in range(right, left, -1):
                if self._compare(arr_copy[i - 1], arr_copy[i]):
                    self._swap(arr_copy, i - 1, i)
            left += 1
        
        return arr_copy
    
    def sort(self, arr: List) -> SortResult:
        """
        执行排序并返回结果
        
        Args:
            arr: 待排序数组
            
        Returns:
            排序结果对象
        """
        self.reset_metrics()
        start_time = time.time()
        
        if self.strategy == SortStrategy.STANDARD:
            sorted_arr = self.sort_standard(arr)
        elif self.strategy == SortStrategy.OPTIMIZED:
            sorted_arr = self.sort_optimized(arr)
        elif self.strategy == SortStrategy.BIDIRECTIONAL:
            sorted_arr = self.sort_bidirectional(arr)
        else:
            raise ValueError(f"不支持的排序策略: {self.strategy}")
        
        self.execution_time = time.time() - start_time
        
        return SortResult(
            sorted_array=sorted_arr,
            execution_time=self.execution_time,
            comparisons=self.comparisons,
            swaps=self.swaps,
            strategy=self.strategy
        )
    
    def benchmark(self, arr: List) -> dict:
        """
        对同一数组使用不同策略进行性能对比
        
        Args:
            arr: 待排序数组
            
        Returns:
            性能对比结果
        """
        results = {}
        
        for strategy in SortStrategy:
            self.strategy = strategy
            result = self.sort(arr)
            results[strategy.value] = {
                'execution_time': result.execution_time,
                'comparisons': result.comparisons,
                'swaps': result.swaps
            }
        
        return results


class ArrayGenerator:
    """数组生成器类"""
    
    @staticmethod
    def random_array(size: int, min_val: int = 1, max_val: int = 1000) -> List[int]:
        """生成随机数组"""
        return [random.randint(min_val, max_val) for _ in range(size)]
    
    @staticmethod
    def sorted_array(size: int) -> List[int]:
        """生成已排序数组"""
        return list(range(1, size + 1))
    
    @staticmethod
    def reverse_sorted_array(size: int) -> List[int]:
        """生成逆序数组"""
        return list(range(size, 0, -1))
    
    @staticmethod
    def nearly_sorted_array(size: int, swap_count: int = 10) -> List[int]:
        """生成接近排序的数组"""
        arr = list(range(1, size + 1))
        for _ in range(swap_count):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr


def print_array(arr: List, message: str = ""):
    """打印数组的辅助函数"""
    if message:
        print(f"{message}: ", end="")
    print(arr)


def print_benchmark_results(results: dict):
    """打印性能对比结果"""
    print("\n=== 性能对比结果 ===")
    print(f"{'策略':<15} {'执行时间(秒)':<15} {'比较次数':<12} {'交换次数':<12}")
    print("-" * 60)
    
    for strategy, metrics in results.items():
        print(f"{strategy:<15} {metrics['execution_time']:<15.6f} "
              f"{metrics['comparisons']:<12} {metrics['swaps']:<12}")


if __name__ == "__main__":
    # 测试用例
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],
        [],
        [3, 3, 3, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1]
    ]
    
    print("=== 面向对象冒泡排序演示 ===\n")
    
    # 测试不同策略
    for i, arr in enumerate(test_arrays, 1):
        print(f"测试用例 {i}:")
        print_array(arr, "原始数组")
        
        for strategy in SortStrategy:
            sorter = BubbleSorter(strategy)
            result = sorter.sort(arr)
            print_array(result.sorted_array, f"{strategy.value}排序后")
            print(f"  执行时间: {result.execution_time:.6f}秒, "
                  f"比较次数: {result.comparisons}, 交换次数: {result.swaps}")
        
        print("-" * 50)
    
    # 性能对比
    print("\n=== 大规模数据性能对比 ===")
    
    # 生成测试数据
    generator = ArrayGenerator()
    test_sizes = [100, 500, 1000]
    
    for size in test_sizes:
        print(f"\n数组大小: {size}")
        
        # 随机数组
        random_arr = generator.random_array(size)
        sorter = BubbleSorter()
        results = sorter.benchmark(random_arr)
        print_benchmark_results(results)
        
        # 逆序数组
        reverse_arr = generator.reverse_sorted_array(size)
        results = sorter.benchmark(reverse_arr)
        print("\n逆序数组:")
        print_benchmark_results(results)
        
        # 接近排序数组
        nearly_arr = generator.nearly_sorted_array(size)
        results = sorter.benchmark(nearly_arr)
        print("\n接近排序数组:")
        print_benchmark_results(results) 