pyinstaller main.py --exclude-module=pygame --exclude-module=PyQt5 --exclude-module=PySide6 --exclude-module=cipher --onefile --icon="./icon.ico" --name="cipher"