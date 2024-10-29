## Documentation for check_internrt_speed_application_MacOS

### Project Description

`check_internrt_speed_application_MacOS` is an application designed to check internet 
speed on macOS. It allows users to quickly and conveniently measure download and upload 
speeds, as well as latency (ping).

### Installation

#### System Requirements
- macOS (version 10.14 or later)
- Python 3.6 or higher
- Installed dependencies listed in `requirements.txt`

#### Installing Dependencies
To install the dependencies, execute the following commands:

```bash
# Clone repository
# Change directory to the project
cd check_internrt_speed_application_MacOS

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
The project include a `Alexs_SpeedTest.py` file, where you can find settings such as 
parameters for speed testing. Feel free to modify these parameters according to your needs.

### License
This project is licensed under the MIT License. Please refer to the `LICENSE` file for more detailed information.

### Contribution
If you would like to contribute to the project, please create a fork of the repository and submit a Pull Request with your changes.

### Contact
For questions or suggestions, you can reach out to me via [GitHub](https://github.com/AlexTkDev).

***

## Документация к проекту check_internrt_speed_application_MacOS

### Описание проекта
`check_internrt_speed_application_MacOS` — это приложение для проверки скорости 
интернет-соединения на macOS. Оно позволяет пользователям быстро и удобно измерять 
скорость загрузки и выгрузки, а также задержку (ping).

### Установка

#### Системные требования
- macOS (версия 10.14 и выше)
- Python 3.6 или выше
- Установленные зависимости, перечисленные в `requirements.txt`

#### Установка зависимостей
Для установки зависимостей выполните следующие команды:

```bash
# Переход в каталог проекта
cd check_internrt_speed_application_MacOS

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
В проекте файл `Alexs_SpeedTest.py`, в котором находятся настройки, такие как параметры для 
тестирования скорости. Вы можете изменять эти параметры в соответствии с вашими потребностями.
### Лицензия
Этот проект лицензирован под MIT License. Пожалуйста, ознакомьтесь с файлом `LICENSE` для получения более подробной информации.

### Контрибьюция
Если вы хотите внести свой вклад в проект, пожалуйста, создайте форк репозитория и отправьте Pull Request с вашими изменениями.

### Связь
Для вопросов или предложений вы можете связаться со мной через [GitHub](https://github.com/AlexTkDev).
