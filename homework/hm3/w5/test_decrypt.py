import unittest
from decrypt import decrypt  # предполагаем, что функция decrypt находится в модуле decrypt.py

class TestDecrypt(unittest.TestCase):
    """Тесты для функции decrypt."""

    def test_single_dot_removal(self):
        """Тесты с одной точкой (удаляется точка, символ остаётся)."""
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),
            ("1..2.3", "23"),                # содержит и две, и одну точку
            ("абр......a.", "a"),
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_double_dot_backspace(self):
        """Тесты с двумя точками (удаление предыдущего символа)."""
        test_cases = [
            ("абраа..-кадабра", "абра-кадабра"),
            ("абраа..-.кадабра", "абра-кадабра"),
            ("абра--..кадабра", "абра-кадабра"),
            ("абрау...-кадабра", "абра-кадабра"),   # ... -> сначала две точки (удаляют 'у'), затем одна точка (удаляется)
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_empty_result(self):
        """Тесты, приводящие к пустой строке."""
        test_cases = [
            ("абра........", ""),
            (".", ""),
            ("1.......................", ""),
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

    def test_mixed(self):
        """Смешанные тесты, включающие все правила."""
        test_cases = [
            ("абра-кадабра.", "абра-кадабра"),       # одна точка в конце
            ("абраа..-кадабра", "абра-кадабра"),     # две точки после 'а'
            ("абраа..-.кадабра", "абра-кадабра"),    # сочетание
            ("абра--..кадабра", "абра-кадабра"),     # две точки после '-'
            ("абрау...-кадабра", "абра-кадабра"),    # три точки
            ("абр......a.", "a"),                    # много точек
            ("1..2.3", "23"),                        # цифры
        ]
        for encrypted, expected in test_cases:
            with self.subTest(encrypted=encrypted):
                self.assertEqual(decrypt(encrypted), expected)

if __name__ == "__main__":
    unittest.main()