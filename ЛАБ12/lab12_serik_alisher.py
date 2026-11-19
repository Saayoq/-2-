import asyncio
import time
from typing import Any

SENTINEL = object()

records: list[dict[str, Any]] = [
    {"student": "Алия", "grade": 85},
    {"student": "Дамир", "grade": 54},
    {"student": "Руслан", "grade": 78},
    {"student": "", "grade": 91},          # ошибка: пустое имя
    {"student": "Мадина", "grade": 105},    # ошибка: оценка вне диапазона
    {"student": "Аружан", "grade": 92},
    {"student": "Ерлан", "grade": 0},
]


def validate(record: dict[str, Any]) -> None:
    """Проверяет имя студента и диапазон оценки."""
    student = str(record.get("student", "")).strip()
    grade = record.get("grade")

    if not student:
        raise ValueError("Не указано имя студента")
    if isinstance(grade, bool) or not isinstance(grade, (int, float)):
        raise ValueError("Оценка должна быть числом")
    if not 0 <= grade <= 100:
        raise ValueError("Оценка должна быть от 0 до 100")


async def producer(queue: asyncio.Queue, data: list[dict[str, Any]]) -> None:
    """Получает записи и помещает их в ограниченную очередь."""
    for record in data:
        await asyncio.sleep(0.05)
        await queue.put(record)
        print(f"Производитель: добавлена запись {record}")

    # По одному сигналу завершения для каждого потребителя.
    for _ in range(2):
        await queue.put(SENTINEL)


async def process(record: dict[str, Any]) -> dict[str, Any]:
    """Имитирует асинхронную обработку и проверяет запись."""
    await asyncio.sleep(0.10)
    validate(record)
    grade = record["grade"]
    return {
        **record,
        "status": "зачет" if grade >= 60 else "незачет",
    }


async def consumer(
    name: str,
    queue: asyncio.Queue,
    results: list[dict[str, Any]],
    errors: list[str],
) -> None:
    """Извлекает и обрабатывает записи до получения SENTINEL."""
    while True:
        item = await queue.get()
        try:
            if item is SENTINEL:
                print(f"{name}: завершение работы")
                return

            try:
                result = await asyncio.wait_for(process(item), timeout=1.0)
                results.append(result)
                print(f"{name}: обработано {result}")
            except asyncio.TimeoutError:
                errors.append(f"{item}: превышено время обработки")
            except ValueError as error:
                errors.append(f"{item}: {error}")
        finally:
            # Вызывается для каждого извлеченного элемента, включая SENTINEL.
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue = asyncio.Queue(maxsize=3)
    results: list[dict[str, Any]] = []
    errors: list[str] = []
    started = time.perf_counter()

    workers = [
        asyncio.create_task(
            consumer(f"Потребитель-{i}", queue, results, errors)
        )
        for i in range(1, 3)
    ]

    await producer(queue, records)
    await queue.join()
    await asyncio.gather(*workers)

    average = (
        sum(item["grade"] for item in results) / len(results)
        if results else 0.0
    )
    elapsed = time.perf_counter() - started

    print("\\n--- Итоговая статистика ---")
    print(f"Успешно обработано записей: {len(results)}")
    print(f"Количество ошибок: {len(errors)}")
    print(f"Средний балл: {average:.2f}")
    print(f"Время выполнения: {elapsed:.2f} с")

    print("\\n--- Результаты ---")
    for item in results:
        print(
            f"{item['student']}: {item['grade']} баллов — {item['status']}"
        )

    print("\\n--- Ошибки ---")
    for error in errors:
        print(error)


if __name__ == "__main__":
    asyncio.run(main())
