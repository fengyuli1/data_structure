class Fib:
    def f(self, n):
        if n < 1:
            return 0
        memo = [0]
        memo.extend([0] * n)
        return self.helper(memo, n)

    def helper(self, memo, n):
        print(memo, n)
        if n == 1 or n == 2:
            return 1
        if memo[n] != 0:
            return memo[n]
        memo[n] = self.helper(memo, n - 1) + self.helper(memo, n - 2)
        return memo[n]

    def f2(self, n):
        print(n)
        if n == 1 or n == 2:
            return 1
        return self.f3(n - 1) + self.f4(n - 2)

    def f3(self, n):
        print("左边第{}次".format(n))
        if n == 1 or n == 2:
            return 1
        return self.f3(n - 1) + self.f3(n - 2)

    def f4(self, n):
        print("右边第{}次".format(n))
        if n == 1 or n == 2:
            return 1
        return self.f4(n - 1) + self.f4(n - 2)


fib = Fib()
print(fib.f(5))
