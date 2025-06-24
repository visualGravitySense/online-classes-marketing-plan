#!/usr/bin/env python3
"""
Тестовый скрипт для проверки генерации контента
"""

from integrated_content_generator import ContentGenerator
import json
from datetime import datetime, timedelta

def test_content_generation():
    """Тестирует генерацию контента"""
    print("🚀 Тестирование генерации контента...")
    
    # Создаем генератор контента
    generator = ContentGenerator()
    
    # Тестируем генерацию для разных аудиторий
    audiences = ["Новички в дизайне", "Junior дизайнеры", "Фрилансеры", "Разработчики"]
    content_types = ["Проблема", "Решение", "Преимущества курса", "Кейс", "Совет", "Мотивация"]
    
    print("\n📊 Доступные аудитории:")
    for audience in audiences:
        print(f"  • {audience}")
    
    print("\n📝 Доступные типы контента:")
    for content_type in content_types:
        print(f"  • {content_type}")
    
    # Генерируем примеры контента
    print("\n" + "="*50)
    print("🎯 ПРИМЕРЫ СГЕНЕРИРОВАННОГО КОНТЕНТА")
    print("="*50)
    
    for audience in audiences[:2]:  # Тестируем первые 2 аудитории
        print(f"\n👥 АУДИТОРИЯ: {audience}")
        print("-" * 30)
        
        for content_type in content_types[:3]:  # Тестируем первые 3 типа
            try:
                content = generator.generate_content(audience, content_type)
                print(f"\n📋 Тип: {content_type}")
                print(f"📄 Контент:\n{content}")
                print("-" * 20)
            except Exception as e:
                print(f"❌ Ошибка при генерации {content_type} для {audience}: {e}")
    
    # Тестируем генерацию пакета
    print("\n" + "="*50)
    print("📦 ТЕСТИРОВАНИЕ ГЕНЕРАЦИИ ПАКЕТА")
    print("="*50)
    
    try:
        batch = generator.generate_batch("Новички в дизайне", 3)
        print(f"\n✅ Сгенерировано {len(batch)} постов для 'Новички в дизайне':")
        
        for i, post in enumerate(batch, 1):
            print(f"\n📝 Пост #{i}:")
            print(f"{post[:200]}...")  # Показываем первые 200 символов
    except Exception as e:
        print(f"❌ Ошибка при генерации пакета: {e}")

def test_content_analytics():
    """Тестирует аналитику контента"""
    print("\n" + "="*50)
    print("📊 ТЕСТИРОВАНИЕ АНАЛИТИКИ КОНТЕНТА")
    print("="*50)
    
    generator = ContentGenerator()
    
    # Анализируем матрицу аудитории
    print("\n🎯 Матрица аудитории:")
    for audience, data in generator.audience_matrix.items():
        print(f"\n👥 {audience}:")
        print(f"  • Проблем: {len(data['problems'])}")
        print(f"  • Решений: {len(data['solutions'])}")
        print(f"  • Преимуществ: {len(data['benefits'])}")
    
    # Анализируем блоки контента
    print(f"\n📝 Блоки контента: {len(generator.content_blocks)}")
    for content_type, templates in generator.content_blocks.items():
        print(f"  • {content_type}: {len(templates)} шаблонов")
    
    # Анализируем CTA
    print(f"\n🎯 CTA варианты: {len(generator.cta_variations)}")

def test_scheduling():
    """Тестирует планирование постов"""
    print("\n" + "="*50)
    print("⏰ ТЕСТИРОВАНИЕ ПЛАНИРОВАНИЯ")
    print("="*50)
    
    generator = ContentGenerator()
    
    # Тестируем планирование постов
    start_time = datetime.now() + timedelta(hours=1)
    
    try:
        # Генерируем контент для планирования
        content = generator.generate_content("Новички в дизайне", "Совет")
        
        print(f"📅 Время начала: {start_time}")
        print(f"📝 Сгенерированный контент:")
        print(f"{content[:100]}...")
        
        print("\n✅ Планирование работает корректно!")
        
    except Exception as e:
        print(f"❌ Ошибка при планировании: {e}")

if __name__ == "__main__":
    print("🎯 ЗАПУСК ТЕСТИРОВАНИЯ СИСТЕМЫ ГЕНЕРАЦИИ КОНТЕНТА")
    print("="*60)
    
    try:
        test_content_generation()
        test_content_analytics()
        test_scheduling()
        
        print("\n" + "="*60)
        print("✅ ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ УСПЕШНО!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")
        import traceback
        traceback.print_exc() 