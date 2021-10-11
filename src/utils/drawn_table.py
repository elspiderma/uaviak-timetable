from dataclasses import dataclass
from io import BytesIO

from PIL import ImageFont, Image, ImageDraw


def get_bytes_image(img: Image) -> bytes:
    io = BytesIO()
    img.save(io, format="jpeg")
    return io.getvalue()


@dataclass
class Cell:
    """Ячейка таблицы.
    """
    text: str
    color: tuple[int, int, int] = (0, 0, 0)
    background_color: tuple[int, int, int] = (255, 255, 255)


class TableDrawError(Exception):
    """Ошибка рисования таблицы.
    """
    pass


class DrawnTable:
    """Класс, представляющий нарисованную таблицу.
    """
    def __init__(self, font: str, size_font: int, padding_horizontal: int = 10, padding_vertical: int = 2,
                 line_thickness: int = 3):
        self._cells: list[list[Cell]] = [[]]

        self._font = ImageFont.truetype(font, size_font)

        self.padding_horizontal = padding_horizontal
        self.padding_vertical = padding_vertical
        self.line_thickness = line_thickness

    def append(self, cell: Cell, row: int = None) -> None:
        """Добавляет новую ячейку в ряд.

        Args:
            cell: Ячейка.
            row: Номер ряда, если None, то используется самый последний.
        """
        if row is None:
            row = -1
        elif row < 0 or row >= len(self._cells):
            raise RuntimeError(f'Not found row #{row}')

        self._cells[row].append(cell)

    def row(self) -> None:
        """Добавляет новый пустой ряд.
        """
        self._cells.append(list())

    def is_correct_table(self) -> bool:
        """Проверяет, является ли таблица корректной.

        Returns:
            True -- если таблица корректна, иначе False.
        """
        # Считаем количество ячеек в каждом ряде.
        count_cells_in_row = [len(i) for i in self._cells]

        conditions = (
            len(set(count_cells_in_row)) == 1,  # Все строки должны содержать одинаковое кол-во ящеек.
            0 not in count_cells_in_row  # Ряд в таблице должен содержать хотя бы одну ячейку.
        )

        return all(conditions)

    def _get_size_columns_and_row(self) -> tuple[list[int], list[int]]:
        """Возвращает длины столбцов и высоты строк.

        Returns:
            Кортеж, в котором нулевой элемент -- длины столбцов, а первый элемент -- высоты строк.
        """
        columns = list(zip(*self._cells))

        wight_text_columns = [0 for i in range(len(columns))]
        height_text_rows = [0 for i in range(len(self._cells))]

        for n_column, column in enumerate(columns):
            for n_row, cell in enumerate(column):
                width_text_cell, height_text_cell = self._font.getsize(cell.text)

                # Длиной стобца/высотой строки является длина/высота самой длинной/высокой ячейки в столбце/строке.
                wight_text_columns[n_column] = max(width_text_cell, wight_text_columns[n_column])
                height_text_rows[n_row] = max(height_text_cell, height_text_rows[n_row])

        # Добавляем отступы и получаем длины и высоты строк и столбцов
        wight_columns = [i + self.padding_horizontal * 2 for i in wight_text_columns]
        height_rows = [i + self.padding_vertical * 2 for i in height_text_rows]

        return wight_columns, height_rows

    def _get_size_table(self) -> tuple[list[int], list[int], int, int]:
        """Возвращает длины столбцов, высоты строк и общие размеры таблицы.

        Returns:
            Кортеж, в котором
                нулевой элемент -- длины столбцов,
                первый элемент -- высоты строк,
                второй элемент -- ширина таблицы,
                третий элемент -- высота таблицы
        """
        def calculate_total_size(sizes: list[int]) -> int:
            return sum(sizes) + (len(sizes) - 1) * self.line_thickness

        wight_columns, height_rows = self._get_size_columns_and_row()

        table_width = calculate_total_size(wight_columns)
        table_height = calculate_total_size(height_rows)

        return wight_columns, height_rows, table_width, table_height

    def draw(self) -> Image:
        """Рисует таблицу.

        Returns:
            Изображение с таблицой.
        """
        if not self.is_correct_table():
            raise TableDrawError('This table is invalid')

        wight_columns, height_rows, table_width, table_height = self._get_size_table()

        img = Image.new('RGB', (table_width, table_height), (255, 255, 255))
        img_draw = ImageDraw.Draw(img)

        x, y = 0, 0
        for n_row, (height_row, row) in enumerate(zip(height_rows, self._cells)):
            for n_column, (wight_column, cell) in enumerate(zip(wight_columns, row)):
                # Линии отделяющие колонки рисуем только один раз, при прорисовке первого ряда (n_row == 0),
                # а так же не рисуем их для 1 колонки.
                if n_column != 0 and n_row == 0:
                    img_draw.line(
                        xy=((x - self.line_thickness / 2, 0), (x - self.line_thickness / 2, table_height)),
                        fill=(0, 0, 0),
                        width=self.line_thickness
                    )

                # Задний фон ячейки.
                img_draw.rectangle(
                    xy=((x, y), (x + wight_column, y + height_row)),
                    fill=cell.background_color
                )

                # Рисуем текст по середине ячейки.
                text_x = x + wight_column / 2 - self._font.getsize(cell.text)[0] / 2
                text_y = y + self.padding_vertical

                img_draw.text(
                    xy=(text_x, text_y),
                    text=cell.text,
                    font=self._font,
                    fill=cell.color
                )

                x += wight_column + self.line_thickness

            # Рисуем разделитель строк начиная со 2 строки.
            if n_row != 0:
                img_draw.line(
                    xy=((0, y - self.line_thickness / 2), (table_width, y - self.line_thickness / 2)),
                    fill=(0, 0, 0),
                    width=self.line_thickness
                )

            x = 0
            y += height_row + self.line_thickness

        return img
