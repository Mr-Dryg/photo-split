import os
import shutil

angles = [0, 20, 45]
light_conditions = ["Natural-daylight", "Office-LED", "Warm-indoor", "Dim-light"]
backgrounds = ["Neutral wall", "Textured desk", "Outdoor pavement", "Docs-on-docs"]

print("╔══════════════════════════════════════════════════════════════╗")
print("║              Photo Split — раскладка фото                  ║")
print("╚══════════════════════════════════════════════════════════════╝")
print()
print("Программа ожидает такую структуру папок:")
print()
print("📁 Ваша_папка (путь, который вы введёте)")
print(" ├── 📁 Россия")
print(" │    ├── 📁 1234567890  (Passport ID)")
print(" │    │    ├── photo1.jpg")
print(" │    │    ├── photo2.jpg")
print(" │    │    └── ...")
print(" │    └── 📁 9876543210")
print(" │         └── ...")
print(" └── 📁 США")
print("      └── ...")
print()
print("ℹ️  Вложенные папки (страны → Passport ID) будут обработаны автоматически.")
print("   Папки и файлы на верхнем уровне будут проигнорированы.")
print()
print("📦 На каждый Passport ID будет создано 48 комбинаций (угол×освещение×фон).")
print("   Файлы распределяются циклически и переименовываются в формат:")
print("   {PassportID}_L(1-4)_B(1-4)_A(1-3)_D(1-2).{ext}")
print()
directory = input("📂 Введите путь до нужной папки: ").strip()
res_dir = os.path.join(directory + "_res")
os.makedirs(res_dir, exist_ok=True)

countries = [entry.name for entry in os.scandir(directory) if entry.is_dir() and not entry.name.startswith('.')]
total_countries = len(countries)
print(f"\nНайдено стран: {total_countries}")
print()

if len(countries) == 0:
    print("═" * 56)
    print("⚠️  ОШИБКА!!!")
    print(f"   Не найдено ни одной страны. Проверьте структуру папок")
    print("═" * 56)
    exit()

for ci, country in enumerate(countries, 1):
    print(f"[{ci}/{total_countries}] Обработка страны: {country}")
    country_path = os.path.join(directory, country)
    passport_ids = [entry.name for entry in os.scandir(country_path) if entry.is_dir() and not entry.name.startswith('.')]

    if len(passport_ids) == 0:
        print(f"  ⚠️  Страна «{country}» — не найдено ни одного Passport Id")
        print()
        continue

    for pass_id in passport_ids:
        pass_id_path = os.path.join(country_path, pass_id)
        files = [f for f in os.listdir(pass_id_path) if os.path.isfile(os.path.join(pass_id_path, f))]
        files.sort()
        total_files = len(files)
        print(f"  → {pass_id}: {total_files} файлов")

        for i, filename in enumerate(files):
            i_angle = (i // 2) % len(angles)
            i_light_condition = (i // 6) % len(light_conditions)
            i_background = (i // 24) % len(backgrounds)

            src_path = os.path.join(pass_id_path, filename)
            dst_path = os.path.join(
                res_dir,
                country,
                pass_id,
                str(angles[i_angle]), 
                light_conditions[i_light_condition], 
                backgrounds[i_background], 
                filename
            )
            os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            shutil.copy2(src_path, dst_path)
            _, ext = os.path.splitext(filename)
            os.rename(dst_path, os.path.join(
                os.path.dirname(dst_path),
                f"{pass_id}_L{i_light_condition+1}_B{i_background+1}_A{i_angle+1}_D{i%2 + 1}{ext}"
            ))

        print(f"    {'✅' if total_files else '⚠️ '} {total_files} файлов обработано")
    print(f"  ✅ Страна «{country}» — готово")
    print()

print("═" * 56)
print("✅  ВСЁ ГОТОВО!")
print(f"   Результат сохранён в папке:")
print(f"   📁 {res_dir}")
print("═" * 56)
input()
