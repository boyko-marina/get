# Инструкция по Git

## Создание SSH-ключа

### 1. Генерация ключа
ssh-keygen -t ed25519 -C "ваш_email@example.com"
Ответьте на вопросы:
- Нажмите Enter для пути по умолчанию
- Введите пароль (рекомендуется)
- Повторите пароль

### 2. Проверка ключей
ls -la ~/.ssh/
# Должны быть:
# id_ed25519      - приватный ключ
# id_ed25519.pub  - публичный ключ

## Добавление ключа в аккаунт GitHub

### 1. Копирование публичного ключа
# Для копирования в буфер обмена:
cat ~/.ssh/id_ed25519.pub | pbcopy  # macOS
cat ~/.ssh/id_ed25519.pub | clip    # Windows
# Или просто скопируйте вывод команды:
cat ~/.ssh/id_ed25519.pub

### 2. Добавление на GitHub
1. Откройте GitHub → Settings → SSH and GPG keys
2. Нажмите "New SSH key"
3. Вставьте ключ в поле "Key"
4. Нажмите "Add SSH key"

### 3. Проверка
ssh -T git@github.com
# Должно быть: "Hi username! You've successfully authenticated..."

## Клонирование репозитория

### 1. Получение SSH-ссылки
1. На странице репозитория нажмите Code
2. Выберите SSH
3. Скопируйте ссылку вида:
   git@github.com:username/repository.git

### 2. Клонирование
git clone git@github.com:username/repository.git

### 3. Переход в папку проекта
cd название_репозитория
