import pytest

# ==========================================
# FIX: этот файл был создан заново (старый test_string_lenth.py удалён).
#
# Проблемы старой версии:
# 1. Опечатка в имени файла: "lenth" вместо "length"
# 2. Использовал input() — блокирует выполнение и делает тест
#    невозможным для CI/CD и автоматических запусков
# 3. Один тест без parametrize — не покрывал boundary cases
#
# Теперь: правильное имя, parametrize с 6 кейсами, никакого input().
# Тест НЕ связан с API — это чисто Python-упражнение на валидацию строк.
# ==========================================


@pytest.mark.parametrize("phrase, expected_pass", [
    ("hello", True),                         # короткая строка — ок
    ("a" * 15, True),                        # ровно 15 символов — boundary pass
    ("a" * 16, False),                       # 16 символов — boundary fail
    ("", True),                              # пустая строка — ок
    ("normal string", True),                 # средняя строка — ок
    ("this string is definitely way too long for the limit", False),  # длинная — fail
], ids=["short", "boundary_pass", "boundary_fail", "empty", "medium", "too_long"])
def test_string_length_within_limit(phrase, expected_pass):
    if expected_pass:
        assert len(phrase) <= 15, f"String '{phrase}' ({len(phrase)} chars) exceeds 15 char limit"
    else:
        assert len(phrase) > 15, f"String '{phrase}' should have exceeded limit"
