# 使用随机丢弃将交叉后不符合规定的染色体修正
# 判断连续十代适应度标准差是否小于某值作为终止条件判定标准

# 导入库
import random
import numpy as np


class GA:
    def __init__(self, fitness_func, qualified_func, n, population_size, fitness_d):
        # 外部传参
        self.fitness_func = fitness_func  # 适应度评估函数
        self.qualified_func = qualified_func  # 基因合格化函数
        self.n = n  # 编码长度
        self.population_size = population_size  # 群体中个体数量
        self.fitness_d = fitness_d  # 判断终止条件，连续几代适应度差值的绝对值小它则终止。d意为difference差值.
        # 内部传参
        self.population = np.zeros((self.population_size, self.n))  # 存储当前种群的每个个体基因
        self.y_population = np.zeros(self.population_size)  # 存储当前种群每个个体适应度
        self.initialize_population()  # 初始化种群函数
        self.data_code = np.array([])  # 数据集，已测试编码的记录，存储种群中每个个体基因
        self.data_y = np.array([])  # 数据集，已测试编码结果的记录，存储适应度
        self.data_y_max = np.array([])    # 数据集，已测试编码结果的记录，存储每代适应度最大值

    # 初始化种群
    def initialize_population(self):
        for size in range(self.population_size):  # 循环初始化每个个体基因
            self.population[size] = [random.randint(0, 1) for _ in range(self.n)]  # 循环初始化个体每个基因，随机设置为0或1

    # 计算适应度并保存
    def cal_fitness(self):
        for size in range(self.population_size):  # 循环种群每个个体
            self.population[size] = self.qualified_func(self.population[size])  # 将各个个体基因合格化
            self.y_population[size] = self.fitness_func(self.population[size])  # 计算每个个体适应度
            if np.ndim(self.data_code) == 1:  # 若data_code为一维数组，即初始
                self.data_code = np.array([self.population[size]])  # 将当前基因序列作为数组存入population中
            else:
                self.data_code = np.vstack((self.data_code, self.population[size]))  # 将当前基因序列作为数组存入population中
            self.data_y = np.append(self.data_y, self.y_population[size])  # 将适应度数组y_population存入data_y中
        self.data_y_max = np.append(self.data_y_max, max(self.y_population))  # 将当代适应度最大值存入data_y_max中

    # 选择操作，这里使用锦标赛选择
    def selection(self):
        # 初始化一个空列表selected_population，用于存储经过选择过程后保留下来的优秀个体
        selected_population = []
        # 使用for循环进行population_size次迭代，即对种群中的每个位置都进行一次选择操作
        for _ in range(self.population_size):
            competitors = random.sample(range(self.population_size), 3)  # 随机选取3个个体作为竞争者
            # 比较三个竞争者适应度并选取出适应度最高的个体
            winner = self.population[competitors[np.argmax(self.y_population[competitors])]]
            # 将适应度最高的个体添加到selected_population列表中
            selected_population.append(winner)
        self.population = np.array(selected_population)  # 将原种群替换为新选出的优秀个体组成的种群

    # 交叉操作，这里使用单点交叉
    def crossover(self):
        for i in range(0, self.population_size, 2):  # 循环选取两个个体作为父代配对
            parent1 = self.population[i]  # 选取第i个个体作为父代之一
            parent2 = self.population[i + 1]  # 选取第i+1个个体作为父代之二
            crossover_point = random.randint(1, self.n - 1)  # 随机选择第1位到第n-1位作为交叉点
            # child1由parent1前半部分基因（从0到crossover_point-1的位置）与parent2后半部分基因（从crossover_point到n-1的位置）拼接而成
            child1 = np.append(parent1[:crossover_point], parent2[crossover_point:])
            # child2则相反，由parent2前半部分基因与parent1后半部分基因拼接而成
            child2 = np.append(parent2[:crossover_point], parent1[crossover_point:])

            self.population[i] = child1  # 子代一替换父代一
            self.population[i + 1] = child2  # 子代二替代父代二

    # 变异操作，这里使用位翻转变异
    def mutation(self):
        mutation_rate = 0.01  # 设置变异率
        for i in range(self.population_size):  # 循环种群每个个体
            for j in range(self.n):  # 循环每个个体基因
                if random.random() < mutation_rate:  # 若随机数小于变异率则变异
                    self.population[i][j] = 1 - self.population[i][j]  # 原基因取反

    def end_judge(self):  # 迭代终止判断
        data_y_end_judge = self.data_y_max[-6:]  # 获取倒数六代适应度最大值
        data_y_end_judge = np.array(data_y_end_judge)
        if self.fitness_d >= data_y_end_judge.std():
            # 当最近十次迭代适应度最大值标准差小于终止条件规定值则将判断end置为1
            end = 1
        else:
            # 否则为0
            end = 0
        return end  # 返回判断end值(0/1)

    # 运行
    def run(self):
        generation = 0  # 初始化迭次数
        end = 0  # 初始化终止判断
        while 1:  # while循环迭代
            self.cal_fitness()  # 评估适应度
            if generation >= 6:  # 判断迭代次数，大于6开始终止判断
                end = self.end_judge()  # 判断是否满足终止条件，满足则返回1
            generation = generation + 1  # 迭代次数加一
            if end:  # 如果end为1（真），则满足终止条件，跳出循环
                break  # 跳出循环
            self.selection()  # 选择个体
            self.crossover()  # 交叉
            self.mutation()  # 变异
        best_code = self.data_code[np.argmax(self.data_y)]  # 输出适应度最大对应的最优编码
        best_solution = max(self.data_y)  # 输出最优适应度结果
        return best_code, best_solution, generation  # 返回最优编码，最优适应度，迭代次数
