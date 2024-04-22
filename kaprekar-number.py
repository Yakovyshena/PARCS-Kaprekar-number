from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers
        print("Inited")

    def solve(self):
        print("Job Started")
        print("Workers %d" % len(self.workers))
        (a, b) = self.read_input()
        step_n = (b - a) / len(self.workers)
        step_left = (b - a) % len(self.workers)
        mapped = []
        for i in range(0, len(self.workers)):
            print("map %d" % i)
            if i == len(self.workers) - 1:
                mapped.append(self.workers[i].mymap(str(a + i * step_n), str(a + step_left + (i + 1) * step_n)))
            else:
                mapped.append(self.workers[i].mymap(str(a + i * step_n), str(a + (i + 1) * step_n)))
        kaprekar_numbers = self.myreduce(mapped)
        self.write_output(kaprekar_numbers)
        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b):
        a = int(a)
        b = int(b)
        kaprekar_numbers = []
        for num in range(a, b + 1):
            if Solver.is_kaprekar(num):
                kaprekar_numbers.append(str(num))
        return kaprekar_numbers

    @staticmethod
    @expose
    def myreduce(mapped):
        print("reduce")
        output = []
        for kaprekar_numbers in mapped:
            print("reduce loop")
            output = output + kaprekar_numbers.value
        print("reduce done")
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        n = int(f.readline())
        k = int(f.readline())
        f.close()
        return n, k

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(', '.join(output))
        f.write('\n')
        f.close()
        print("output done")

    @staticmethod
    def is_kaprekar(n):
        square = str(n * n)
        for i in range(1, len(square)):
            part1 = int(square[:i])
            part2 = int(square[i:])
            if part1 + part2 == n and part1 != 0 and part2 != 0:
                return True
        return False
