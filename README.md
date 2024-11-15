## Documentation for macOS_application_speedtest_for_python

### Project Description

`macOS_application_speedtest_for_python` is a macOS application designed to test your internet connection 
speed using Python. The program provides a convenient interface for measuring download, upload, and ping speeds, 
and also supports retesting and viewing test history.
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
python alexs_speedtest.py
```

#### Features
- **Internet Speed Measurement**: The app allows you to test download and upload speeds, as well as ping (latency) of your internet connection.
- **Graphical Display**: After completing a test, users can view the test results and optionally plot the test history.
- **Repeat Test**: After a test is completed, users can repeat the test without needing to restart the application.
- **Test History**: The app saves the results of previous tests, allowing users to view the test history and visualize changes in speed.

#### Key Components
- **Tkinter**: Used for creating the graphical user interface (GUI), which includes buttons for starting tests, viewing results, and plotting graphs.
- **Speedtest-cli**: A library for performing internet speed tests, which powers the app's functionality.
- **Matplotlib**: A library for visualizing the test history by plotting graphs.
- **JSON**: A library for reading and writing test results stored in JSON format.

#### How It Works
1. When the app is launched, users can click the **"Start Speed Test"** button to initiate the test.
2. The app runs a speed test using the **speedtest-cli** library, measuring download speed, upload speed, and ping.
3. Once the test is completed, the results are displayed in the app's interface.
4. Users can save the test results to the **history.json** file and visualize the data using **matplotlib**.
5. For a repeat test, users can simply click the **"Repeat Speed Test"** button, which hides the history buttons until the new test is finished.


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
`macOS_application_speedtest_for_python` — это приложение для macOS, предназначенное для проверки 
скорости интернет-соединения с использованием Python. Программа предоставляет удобный интерфейс для измерения 
скорости загрузки, выгрузки и пинга, а также поддерживает повторные тесты и просмотр истории тестов.
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
python alexs_speedtest.py
```

#### Возможности
- **Измерение скорости интернета**: Приложение позволяет проверить скорость загрузки и выгрузки данных, а также пинг вашего интернет-соединения.
- **Графическое отображение**: После завершения теста пользователи могут увидеть результаты теста в наглядной форме, а также построить график истории тестов.
- **Повторный тест**: После завершения теста пользователи могут повторно запустить тест без необходимости перезапуска приложения.
- **История тестов**: Приложение сохраняет результаты предыдущих тестов, предоставляя возможность просматривать историю тестов и визуализировать изменения скорости интернета.

#### Основные компоненты
- **Tkinter**: Используется для создания графического интерфейса пользователя (GUI), где отображаются кнопки для запуска теста, результатов и графиков.
- **Speedtest-cli**: Библиотека для проведения тестов скорости интернет-соединения, на основе которой работает приложение.
- **Matplotlib**: Используется для построения графиков истории тестов.

#### Используемые библиотеки
- **Tkinter**: Стандартная библиотека Python для создания графических интерфейсов.
- **speedtest-cli**: Библиотека для проведения тестов скорости интернета.
- **matplotlib**: Библиотека для визуализации данных, используется для построения графиков.
- **json**: Библиотека для работы с форматами данных JSON, используется для сохранения и загрузки истории тестов.

#### Как это работает
1. При запуске приложения пользователь может нажать кнопку **"Start Speed Test"**, чтобы начать тестирование скорости интернет-соединения.
2. Приложение запускает тест с использованием библиотеки **speedtest-cli**, который измеряет скорость загрузки, выгрузки и пинг.
3. После завершения теста результаты отображаются в окне приложения.
4. Пользователь может сохранить результаты тестов в файл **history.json**, а также построить график с помощью библиотеки **matplotlib**.
5. Для повторного теста достаточно нажать на кнопку **"Repeat Speed Test"**, и тест будет выполнен снова, скрыв кнопки истории до окончания нового теста.


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
