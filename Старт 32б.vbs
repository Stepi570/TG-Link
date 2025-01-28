' Создаем объект WScript.Shell и FileSystemObject
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

' Получаем текущую папку, в которой находится скрипт
currentFolder = fso.GetParentFolderName(WScript.ScriptFullName)

' Путь к файлу python64.exe
exePath = currentFolder & "\python32.exe"

' Проверяем, существует ли python64.exe, и запускаем его, если он доступен
If fso.FileExists(exePath) Then
    ' Запускаем установку и ждем ее завершения
    shell.Run """" & exePath & """", 1, True
    MsgBox "Установка python64.exe завершена."
Else
    MsgBox "Файл python32.exe не найден по пути: " & exePath & ". Убедитесь, что он находится в той же папке, что и скрипт.", 16, "Ошибка"
    WScript.Quit
End If

' Путь к файлу Tg Link.lnk
filePath = currentFolder & "\Tg Link.lnk"

' Путь в реестре для автозапуска
registryPath = "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run\MyVBSScript"

' Проверяем, существует ли Tg Link.lnk, и добавляем его в автозапуск, если он доступен
If fso.FileExists(filePath) Then
    shell.RegWrite registryPath, """" & filePath & """", "REG_SZ"
    MsgBox "Tg Link.lnk добавлен в автозапуск."
Else
    MsgBox "Файл Tg Link.lnk не найден по пути: " & filePath & ". Убедитесь, что он находится в той же папке, что и скрипт.", 16, "Ошибка"
End If

' Освобождаем объекты
Set shell = Nothing
Set fso = Nothing
