## Documentation for macOS_application_speedtest_for_python

### Project Description

`macOS_application_speedtest_for_python` is an application for testing internet connection speed on macOS. It allows users to quickly and easily measure download and upload speeds, as well as latency (ping).
The project also provides system information, including the computer name, network adapters, their IP addresses, and MAC addresses, displayed directly in the program window.
The project is built based on another one of my applications, which you can check out on GitHub:
[Internet Speed Test](https://github.com/AlexTkDev/different_mini-apps/tree/main/check_internrt_speed)

### Installation

#### System Requirements
- macOS (version 10.14 or later)
- Python 3.6 or higher
- Installed dependencies listed in `requirements.txt`

#### Installing Dependencies
To install the dependencies, execute the following commands:

```bash
# Clone repository
git clone https://github.com/AlexTkDev/macOS_application_speedtest_for_python.git
# Create a virtual environment (recommended)
python -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
```

### Usage
After installation, you can run the application by executing:
```bash
python main.py
```

#### Application Interface
The application features a simple and intuitive interface where you can view:
- **Download Speed**
- **Upload Speed**
- **Ping**

When the application is launched, it will automatically begin testing internet speed.

#### Building the Application
To build the application in `.app` format, run the following command:
```bash
pyinstaller main.spec
```
After building, the application will be located in the `dist` directory, and you can launch it by double-clicking the icon.

### Configuration
The project include a `alexs_speedtest.py` file, where you can find settings such as 
parameters for speed testing. Feel free to modify these parameters according to your needs.

### License
This project is licensed under the MIT License. Please refer to the `LICENSE` file for more detailed information.

### Code Analysis with Pylint
This project uses **Pylint** for static code analysis to ensure that code adheres to Python's 
best practices and follows PEP 8 style guidelines. Pylint checks for errors, potential issues,
and enforces consistent coding style, making it a valuable tool for maintaining code quality.

### How to Install Pylint
To install Pylint, use the following command in your terminal:
```bash
pip install pylint
```
### Running Pylint
Once installed, you can run Pylint on a specific Python file with:
```bash
pylint your_file.py
```
Or, to analyze all Python files in the project, run:
```bash
 pylint *.py
```
This setup is also configured to run automatically within GitHub Actions on every code push, 
checking the code with multiple Python versions for compatibility.

### Contribution
If you would like to contribute to the project, please create a fork of the repository and submit a Pull Request with your changes.

### Contact
For questions or suggestions, you can reach out to me via [GitHub](https://github.com/AlexTkDev).

***

## Документация к проекту macOS_application_speedtest_for_python

### Описание проекта
`macOS_application_speedtest_for_python` — это приложение для проверки скорости интернет-соединения на macOS. Оно позволяет пользователям быстро и удобно измерять скорость загрузки и выгрузки, а также задержку (ping).
В проекте также представлена информация о системе, включая название компьютера, сетевые адаптеры, их IP-адреса и MAC-адреса, отображаемая прямо в окне программы.
Проект разработан на основе другого моего приложения, которое вы можете посмотреть по ссылке на GitHub:
[Internet Speed Test](https://github.com/AlexTkDev/different_mini-apps/tree/main/check_internrt_speed)

### Установка

#### Системные требования
- macOS (версия 10.14 и выше)
- Python 3.6 или выше
- Установленные зависимости, перечисленные в `requirements.txt`

#### Установка зависимостей
Для установки зависимостей выполните следующие команды:

```bash
# Клонируйте репозиторий
git clone https://github.com/AlexTkDev/macOS_application_speedtest_for_python.git
# Создание виртуального окружения (рекомендуется)
python -m venv .venv
source .venv/bin/activate
# Установка зависимостей
pip install -r requirements.txt
```

### Использование
После установки вы можете запустить приложение, выполнив команду:
```bash
python main.py
```

#### Интерфейс приложения
Приложение имеет простой и интуитивно понятный интерфейс, где вы можете увидеть:
- **Скорость загрузки** (Download Speed)
- **Скорость выгрузки** (Upload Speed)
- **Задержка** (Ping)

При запуске приложения оно автоматически начнет тестирование скорости интернета.
#### Сборка приложения
Для сборки приложения в формате `.app`, выполните следующую команду:
```bash
pyinstaller main.spec
```
После сборки приложение будет находиться в директории `dist`, и его можно будет запустить двойным щелчком мыши.

### Конфигурация
В проекте файл `alexs_speedtest.py`, в котором находятся настройки, такие как параметры для 
тестирования скорости. Вы можете изменять эти параметры в соответствии с вашими потребностями.
### Лицензия
Этот проект лицензирован под MIT License. Пожалуйста, ознакомьтесь с файлом `LICENSE` для получения более подробной информации.

### Анализ кода с помощью Pylint
В данном проекте используется **Pylint** для статического анализа кода, чтобы обеспечить 
соблюдение лучших практик Python и следование рекомендациям PEP 8. Pylint проверяет наличие 
ошибок, потенциальные проблемы и обеспечивает единообразный стиль кода, что делает его ценным 
инструментом для поддержания качества кода.

### Как установить Pylint
Для установки Pylint используйте следующую команду в терминале:
```bash
pip install pylint
```
### Запуск Pylint
После установки вы можете запустить Pylint для конкретного Python файла с помощью:
```bash
pylint ваш_файл.py
```
Или, чтобы проанализировать все Python файлы в проекте, выполните:
```bash
pylint *.py
```
Эта настройка также сконфигурирована для автоматического запуска в GitHub Actions при каждом 
пуше кода, проверяя код на совместимость с несколькими версиями Python.

### Контрибуция
Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте Pull Request с вашими изменениями.

### Связь
Для вопросов или предложений вы можете связаться со мной через [GitHub](https://github.com/AlexTkDev).
