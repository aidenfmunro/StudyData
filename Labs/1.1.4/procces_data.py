import matplotlib.pyplot as plot
from math import factorial as fact
from math import exp

# TODO scipy.optimize.curve_fit

class Data_Tau:
    _counter = 0
    def __init__(self, data: list, tau: int):
        self.id = type(self)._counter
        type(self)._counter += 1

        self.data = data
        self.tau = tau
        self.data_tau = self.calculate_data_tau()

        self.average = self.calculate_average()
        self.dispersion = self.calculate_dispersion()
        self.error_rate = self.calculate_error_rate()

        self.counts_table = self.calculate_counts()
        self.frequencies_table = self.calculate_frequencies()

        print(self.data_tau)


    def calculate_data_tau(self) -> list:
        prefs = [0] * (len(self.data) + 1)
        prefs[1] = self.data[0]

        for i in range(2, len(prefs)):
            prefs[i] = prefs[i - 1] + self.data[i - 1]

        data_tau = [0] * (len(self.data) // self.tau)

        for i in range(len(data_tau)):
            data_tau[i] = prefs[(i + 1) * self.tau] - prefs[i * self.tau] 


        return data_tau


    def calculate_counts(self) -> dict:
        counts_table = {}
        for el in self.data_tau:
            if el in counts_table:
                counts_table[el] += 1
            else:
                counts_table[el] = 1
        return counts_table


    def calculate_frequencies(self) -> dict:
        frequencies_table = {}

        for el in self.counts_table:
            frequencies_table[el] = self.counts_table[el] / len(self.data_tau)
        
        return frequencies_table


    def calculate_sigma_inclusion(self, sigmas) -> float:
        k = 0
        for el in self.data_tau:
            if abs(el - self.average) < self.dispersion * sigmas:
                k += 1
        return k / len(self.data_tau)
    

    def calculate_average(self) -> float:
        return sum(self.data_tau) / len(self.data_tau)


    def calculate_dispersion(self) -> float:
        dispersion_sq = 0
        for el in self.data_tau:
            dispersion_sq += (el - self.average) ** 2

        return (dispersion_sq / len(self.data_tau)) ** 0.5


    def calculate_error_rate(self) -> float:
        return self.dispersion / (len(self.data) ** 0.5)


    def plot_frequencies_table(self, x_lim, colors):
        points = sorted(self.frequencies_table.items())

        ANNOTATION_HEIGHT = 0.01

        x = []
        y = []
        for el in points:
            if el[0] <= x_lim:
                x.append(el[0])
                y.append(el[1]) 

        plot.bar(x, y, width=1, color=colors[self.id % len(colors)])
        plot.annotate(f'tau = {self.tau * 10}s', xy=(0, 0.08 - ANNOTATION_HEIGHT * self.id), color=colors[self.id % len(colors)])

        # plot.savefig(f'Figure {self.tau}.png', dpi=300)
        # plot.close()


def main():
    path = 'data.txt'
    data = read_file(path)

    taus = [1, 2, 3]  # [tau] = 10s
    colors = 'bgrcykw'
    x_lim = 100

    plot.xlabel('Число импульсов')
    plot.ylabel('Доля случаев')

    for tau in taus:
        print(f'tau = {tau}')
        data_tau = Data_Tau(data, tau)

        with open(f'Data tau = {tau}', 'w') as f:
            print(f'Average particles = {data_tau.average}',
                  f'Dispersion = {data_tau.dispersion}',
                  f'Error rate = {data_tau.error_rate}',
                  f'Average intensity = {data_tau.average / data_tau.tau}',
                  f'Average intensity error = {data_tau.error_rate / data_tau.tau}',
                  f'1 sigma inclusion = {data_tau.calculate_sigma_inclusion(1)}',
                  f'2 sigma inclusion = {data_tau.calculate_sigma_inclusion(2)}',
                  f'3 sigma inclusion = {data_tau.calculate_sigma_inclusion(3)}',
                  file=f, sep='\n')
            
        data_tau.plot_frequencies_table(x_lim, colors)

    data_tau = Data_Tau(data, 2)
    X_OFFSET = 0
    xs = [i for i in range(X_OFFSET, x_lim + 1)]
    ys = [0] * len(xs)

    for i, x in enumerate(xs):
        ys[i] = data_tau.average ** x * exp(-data_tau.average) / fact(x)

    plot.plot([x - X_OFFSET for x in xs], ys, color=colors[(data_tau.id + 1) % len(colors)])

    plot.savefig('Figure.png', dpi=300)
    


def read_file(path) -> list:
    with open(path) as f:
        data = [int(x.rstrip('\n').rstrip('')) for x in f.readlines() if x[0] != '#']
    return data


if __name__ == '__main__':
    main()