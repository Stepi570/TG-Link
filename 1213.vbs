' Созд' Создаем объект WScript.Shell и FileSystemObject
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Получаем текущую папку, в которой находится скрипт
currentFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Пауза в 2 минуты
WScript.Sleep 120000

' Путь к виртуальному окружению
venvPath = currentFolder & "\.venv\Scripts\Activate.bat"

' Проверяем, существует ли виртуальное окружение, и активируем его, если доступно
If fso.FileExists(venvPath) Then
    shell.Run "cmd.exe /c " & Chr(34) & venvPath & Chr(34), 0, True
Else
    MsgBox "Не найдено виртуальное окружение по пути: " & venvPath, 16, "Ошибка"
    WScript.Quit
End If

' Установка необходимых пакетов
shell.Run "cmd.exe /c pip install aiogram", 0, True
shell.Run "cmd.exe /c pip install psutil", 0, True
shell.Run "cmd.exe /c pip install opencv-python", 0, True
shell.Run "cmd.exe /c pip install pyautogui", 0, True
shell.Run "cmd.exe /c pip install Pillow", 0, True
shell.Run "cmd.exe /c pip install pygetwindow", 0, True

' Путь к основному скрипту main.py
mainScriptPath = currentFolder & "\main.py"

' Проверяем, существует ли основной скрипт, и запускаем его, если доступен
If fso.FileExists(mainScriptPath) Then
    shell.Run "cmd.exe /c python " & Chr(34) & mainScriptPath & Chr(34), 0, True
Else
    MsgBox "Файл main.py не найден по пути: " & mainScriptPath, 16, "Ошибка"
    WScript.Quit
End If

' Освобождаем объекты
Set shell = Nothing
Set fso = Nothing
