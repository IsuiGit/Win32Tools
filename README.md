# topCollegeDLLTesting

## Как с этим работать?

### Для работы с программой тестирования topCollegeDLLTesting необходимо:

1. Скачать файлы из репозитория
2. Запустить файл `main.py`
3. В открывшемся окне выбрать вкладку `DLL -> Import .dll`
4. Далее `DLL -> Import test case`
5. После сообщений об успешной загрузке файлов, запустите проверку `DLL -> Run tests`
6. Ответы о тестировании вашей библиотеки можно увидеть в окне приложения

### Тест-кейсы и подключение .dll библиотеки

Для успешного выполнения проверки вашей dll библиотеки, необходимо соблюсти два условия:

1. Подключить скомпилированную dll библиотеку
2. Написать тест-кейсы для тестирования в формате .json, и подключить их в проект

#### Структура .json файла для тест-кейсов

Структура файла с тест-кейсами выглядит как:

```
{
	"function_name": {
		"args": null (or [] if args exists),
		"iters": <int>
	},
	...
}
```
где `function_name` - имя функции из библиотеки, `args` - набор аргументов функции, `iters` - количество итераций выполнения функции

Пример файла с тестами (данная структура подойдет для тестирования .dll библиотеки с занятия):

```
{
	"fibonacci_init": {
		"args": [1, 1],
		"iters": 1
	},
	"fibonacci_next": {
		"args": null,
		"iters": 5
	},
	"fibonacci_current": {
		"args": null,
		"iters": 1
	},
	"fibonacci_index": {
		"args": null,
		"iters": 1
	}
}
```

### Updates

#### Minor 0.3 update 19.02.25:
1. Функции тестого модуля c_tools теперь запускаются через потоковую обертку модуля t_tools[threading]
2. t_tools.py - новый модуль с модифицированным классом Thread, для запуска и получения ответа потока выполнения

#### Major 1.0 update 19.02.25:
1. Новый модуль `shedule.py`: запуск и исполнение модуля `c_tools.py` через класс `Popen` библиотеки `subprocess`.
	```
	...
	p = subprocess.Popen(["python", "c_tools.py", path, case], stdout=subprocess.PIPE)
	...
	```
2. Обновленные зависимости: вызов теста `.dll` библиотек по схеме `gui -> t_tools.runThread(shedule.runProcess, args=*args)`
	```
	from t_tools import runThread
	from shedule import runProcess
	...
	dllFuncTestResponse = runThread(runProcess, args=[self.dll_path, self.case_path])
	...
	```
3. Isolated Mode: все тесты запускаются в изолированном потоке, а результаты записываются в `sys.stdout`.

#### Minor 1.1.2(2225) update 20.02.2025:
1. Исправлен баг: `c_tool.py not found` - установлены относительные пути поиска исполняемых скриптов.
2. Добавлен `External win32 Services` для тестирования сторонних служб (`in progress`)
3. Функция `ServiceFuncTest` вызывает срабатывание несистемных сервисов с набором параметров `flags` из файла `json` для тестирования
