import pytest
import undetected_chromedriver as uc
import time

def test_ozon_seo_data():
    # Настройки маскировки
    options = uc.ChromeOptions()
    options.add_argument("--disable-blink-features=AutomationControlled")
    
    # ВАЖНО: Указываем твою 145-ю версию, чтобы не было ошибки "SessionNotCreated"
    try:
        driver = uc.Chrome(options=options, version_main=145)
    except Exception:
        # Если 145 не сработает, пробуем авто-определение
        driver = uc.Chrome(options=options)

    try:
        # 1. Заходим на Озон (пробуем сразу категорию, там часто слабее защита)
        driver.get("https://www.ozon.ru")
        
        print("\n[WAIT] Ждем загрузку страницы (10 секунд)...")
        time.sleep(10) 

        # 2. Делаем скриншот для истории успеха
        driver.save_screenshot("debug_final.png")

        # 3. Улучшенный JS: ищем данные или хотя бы заголовок страницы
        script = """
        const n = window.__NUXT__;
        if (n) {
            return "NUXT: " + (n.data?.seo?.title || n.state?.seo?.title || "Титл не найден в объекте");
        }
        return "NUXT не найден. Title страницы: " + document.title;
        """
        
        result = driver.execute_script(script)
        print(f"[RESULT] Что нашел скрипт: {result}")

        # 4. Проверка
        assert "OZON" in result.upper() or "ОЗОН" in result.upper(), f"Блокировка! Результат: {result}"
        print("[SUCCESS] Озон повержен! Тест пройден.")

    except Exception as e:
        print(f"[ERROR] Тест упал: {e}")
        raise e
        
    finally:
        driver.quit()