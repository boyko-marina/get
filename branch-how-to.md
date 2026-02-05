### 1. Создание ветки
# Создать ветку с именем "new-feature"
git branch new-feature

### 2. Создание и переключение
# Создать и сразу переключиться
git checkout -b new-feature
# Или в новых версиях Git:
git switch -c new-feature

## Как переключиться в ветку
# Переключиться на существующую ветку
git checkout имя_ветки
# Или:
git switch имя_ветки

# Посмотреть все ветки
git branch

# Посмотреть все ветки (включая удаленные)
git branch -a
