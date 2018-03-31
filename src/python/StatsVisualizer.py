import matplotlib.pyplot as plt
import pandas as pd

PROJECT_VERSION = '0.1.0'


class StatsVisualizer:

    df_columns = ['x', 'y', 'z', 'v_x', 'v_y', 'v_z', 'particle_number', 'iter_number']
    
    def __init__(self, file_path="out_stats.csv"):
        self.fig, self.ax = plt.subplots()
        self._file_path = file_path
        self.df = pd.read_csv(file_path)

    def _get_column(self, col_name, particle_no):
        """
        Gets Series column for one particle
        @param particle_no: Number of particle
        @param col_name: Name of column
        @return: Pandas Series object with column
        """
        return self.df[col_name][self.df.particle_number == particle_no]

    def create_plot(self, x_var, y_var, particle_number,  _label="Figure 1"):
        """
        Creates plot: y_var = f(x_var). Doesn't draw it
        @param x_var: Variable of X axis
        @param y_var: Variable of Y axis
        @param particle_number: Number of particle to track
        @param _label: Label to graph
        @return: None
        """
        if x_var not in self.df_columns:
            raise ValueError("x_var is not in csv-file")
        if y_var not in self.df_columns:
            raise ValueError("y_var is not in csv-file")
        x = self._get_column(x_var, particle_number)
        y = self._get_column(y_var, particle_number)
        self.ax.plot(x, y)
        # Prettify plot
        self.ax.set_xlabel(x_var)
        self.ax.set_ylabel(y_var)
        self.ax.grid(True)
        self.ax.set_title(_label)

    def show_plot(self):
        self.fig.show()

    def save_plot(self, out_file="figure.pdf"):
        self.fig.savefig(out_file)


#TODO: Перепиши меня с использованием ООП и регистрацией команд!!!!
class GUI:

    def __init__(self):
        self.visualizer = None

    @staticmethod
    def _print_delimiter():
        print('--------------------------------')

    @staticmethod
    def _print_usage():
        GUI._print_delimiter()
        print("Интерактивная визуализация природных моделей v.{}. Выберете опцию:".format(PROJECT_VERSION))
        print("1. Считать файл со статистикой")
        print("2. Создать график двух величин")
        print("3. Отобразить график")
        print("4. Сохранить график в файл")
        print("q. Выйти")
        print("?. Вывести это меню еще раз")
        available_options = ['1', '2', '3', '4', 'q', '?']
        GUI._print_delimiter()
        return available_options


    @staticmethod
    def _print_go_to_menu(msg):
        print("{}. Возврат в главное меню...".format(msg))
        GUI._print_delimiter()

    @staticmethod
    def _read_file():
        while True:
            print("Введите путь до файла со статистикой...")
            path = input()
            try:
                vis = StatsVisualizer(path)
            except:
                print("Не удалось считать файл. Повторить? (y/n)")
                ans = input()
                if ans.lower() == 'y':
                    continue
                else:
                    return None
            return vis

    @staticmethod
    def _read_vars():
        while True:
            print("Введите через пробел три величины: "
                  "1) Ту, что откладывать по оси Ox"
                  "2) Ту, что откладывать по оси Oy"
                  "3) Номер частицы")
            print("Допустимые величины: ", end='')
            print()
            for i in StatsVisualizer.df_columns:
                print(i, end=' ')
            opts = input()
            try:
                opts = opts.split()
                x_var, y_var, particle_number = opts[0], opts[1], opts[2]
                particle_number = int(particle_number)
                if x_var not in StatsVisualizer.df_columns or y_var not in StatsVisualizer.df_columns:
                    print("Неправильный ввод. Повторить? (y/n)")
                    ans = input()
                    if ans.lower() == 'y':
                        continue
                    else:
                        return None, None
            except:
                print("Неправильный ввод. Повторить? (y/n)")
                ans = input()
                if ans.lower() == 'y':
                    continue
                else:
                    return None, None
            return x_var, y_var, particle_number

    def _main_loop(self):
        while True:
            available_options = GUI._print_usage()
            opt = input()
            if opt not in available_options:
                GUI._print_go_to_menu("Некорректный выбор опции")
            if opt == '1':
                self.visualizer = GUI._read_file()
                if self.visualizer is not None:
                    GUI._print_go_to_menu("Файл считан")
                else:
                    GUI._print_go_to_menu("Файл НЕ считан")
            elif opt == '2':
                x_var, y_var, particle_number = GUI._read_vars()
                if x_var is None:
                    GUI._print_go_to_menu("Нет значений")
                else:
                    print("Значения установлены")
                    print("Создаем график...")
                    if self.visualizer is None:
                        GUI._print_go_to_menu("Сначала нужно считать файл со статистикой")
                        continue
                    self.visualizer.create_plot(x_var, y_var, particle_number)
                    GUI._print_go_to_menu("График готов")
            elif opt == '3':
                print("Рисуем график...")
                if self.visualizer is None:
                    GUI._print_go_to_menu("Сначала нужно считать файл со статистикой")
                    continue
                self.visualizer.show_plot()
                GUI._print_go_to_menu("График был показан")
            elif opt == '4':
                print("Введите путь для выходного файла ...")
                out_path = input()
                self.visualizer.save_plot(out_path)
                self._print_go_to_menu("График был сохранен")
            elif opt == 'q':
                print("Благодарим за использование наших услуг! Приятного дня")
                return
            elif opt == '?':
                continue

    def start(self):
        self._main_loop()


if __name__ == "__main__":
    gui = GUI()
    gui.start()