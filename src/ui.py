from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QListWidget, QListWidgetItem, 
                             QLabel, QTextEdit, QSplitter, QMessageBox, QInputDialog, QApplication, QComboBox)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt, QSize

from backend import FlatpakBackend

class FlatpakManager(QWidget):
    def __init__(self):
        super().__init__()
        self.backend = FlatpakBackend()
        
        self.translations = {
            "ru": {
                "title": "Easy Flatpak Manager",
                "btn_refresh": "Обновить список",
                "btn_install": "Установить из Flathub",
                "choose_app": "Выберите приложение",
                "btn_kill": "Закрыть приложение",
                "btn_run": "Запустить",
                "btn_update": "Обновить",
                "btn_uninstall": "Удалить",
                "desc": "Описание:",
                "version": "Версия:",
                "loading": "Загрузка описания...",
                "msg_success": "Успех",
                "msg_error": "Ошибка",
                "msg_installed": "успешно установлено!",
                "msg_updated": "обновлен!",
                "msg_deleted": "удален.",
                "btn_yes": "Да",
                "btn_no": "Нет",
                "window_update": "Обнавление",
                "window_delete": "Удаление",
                "window_install": "Установка",
                "window_install_example": "Введите ID приложения из Flathub\n(например: org.kde.krita):"
            },
            "en": {
                "title": "Easy Flatpak Manager",
                "btn_refresh": "Refresh list",
                "btn_install": "Install from Flathub",
                "choose_app": "Choose application",
                "btn_kill": "Close app",
                "btn_run": "Run",
                "btn_update": "Update",
                "btn_uninstall": "Uninstall",
                "desc": "Description:",
                "version": "Version:",
                "loading": "Loading description...",
                "msg_success": "Success",
                "msg_error": "Error",
                "msg_installed": "successfully installed!",
                "msg_updated": "updated!",
                "msg_deleted": "uninstalled.",
                "btn_yes": "Yes",
                "btn_no": "No",
                "window_update": "Update app",
                "window_delete": "Delete app",
                "window_install": "Install app",
                "window_install_example": "Enter App ID from Flathub\n(e.g.: org.kde.krita):"
            }
        }
        self.current_lang = "ru" 
        
        self.initUI()
        self.load_apps_to_list()

    def tr(self, key):
        return self.translations[self.current_lang].get(key, key)

    def initUI(self):
        self.setWindowTitle(self.tr("title"))
        self.resize(900, 600)

        main_layout = QHBoxLayout()
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Русский", "English"])
        self.lang_combo.currentIndexChanged.connect(self.change_language)
        left_layout.addWidget(self.lang_combo)

        self.btn_refresh = QPushButton(self.tr("btn_refresh"))
        self.btn_refresh.clicked.connect(self.load_apps_to_list)
        
        self.btn_install = QPushButton(self.tr("btn_install"))
        self.btn_install.clicked.connect(self.action_install)
        
        self.list_widget = QListWidget()
        self.list_widget.setIconSize(QSize(32, 32))
        self.list_widget.currentItemChanged.connect(self.on_app_selected)
        
        left_layout.addWidget(self.btn_refresh)
        left_layout.addWidget(self.btn_install)
        left_layout.addWidget(self.list_widget)

        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        header_layout = QHBoxLayout()
        
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(64, 64)
        
        title_layout = QVBoxLayout()
        self.name_label = QLabel(self.tr("choose_app"))
        self.name_label.setFont(QFont("Arial", 16, QFont.Bold))
        self.id_label = QLabel("")
        self.id_label.setStyleSheet("color: gray;")
        title_layout.addWidget(self.name_label)
        title_layout.addWidget(self.id_label)
        
        header_layout.addWidget(self.icon_label)
        header_layout.addLayout(title_layout)
        header_layout.addStretch()

        self.desc_label = QTextEdit()
        self.desc_label.setReadOnly(True)
        
        self.desc_title = QLabel(self.tr("desc"))
        
        action_layout = QHBoxLayout()
        self.btn_kill = QPushButton(self.tr("btn_kill"))
        self.btn_run = QPushButton(self.tr("btn_run"))
        self.btn_update = QPushButton(self.tr("btn_update"))
        self.btn_uninstall = QPushButton(self.tr("btn_uninstall"))
        
        self.btn_kill.clicked.connect(self.action_kill)
        self.btn_run.clicked.connect(self.action_run)
        self.btn_update.clicked.connect(self.action_update)
        self.btn_uninstall.clicked.connect(self.action_uninstall)
        
        action_layout.addWidget(self.btn_kill)
        action_layout.addWidget(self.btn_run)
        action_layout.addWidget(self.btn_update)
        action_layout.addWidget(self.btn_uninstall)

        right_layout.addLayout(header_layout)
        right_layout.addWidget(self.desc_title)
        right_layout.addWidget(self.desc_label)
        right_layout.addLayout(action_layout)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([300, 600])

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)
        self.set_buttons_enabled(False)

    def change_language(self, index):
        self.current_lang = "ru" if index == 0 else "en"
        self.setWindowTitle(self.tr("title"))
        self.btn_refresh.setText(self.tr("btn_refresh"))
        self.btn_install.setText(self.tr("btn_install"))
        self.btn_kill.setText(self.tr("btn_kill"))
        self.btn_run.setText(self.tr("btn_run"))
        self.btn_update.setText(self.tr("btn_update"))
        self.btn_uninstall.setText(self.tr("btn_uninstall"))
        self.desc_title.setText(self.tr("desc"))
        
        if not self.list_widget.currentItem():
            self.name_label.setText(self.tr("choose_app"))
        else:
            self.on_app_selected(self.list_widget.currentItem(), None)

    def set_buttons_enabled(self, enabled):
        self.btn_kill.setEnabled(enabled)
        self.btn_run.setEnabled(enabled)
        self.btn_update.setEnabled(enabled)
        self.btn_uninstall.setEnabled(enabled)

    def load_apps_to_list(self):
        self.list_widget.clear()
        self.name_label.setText(self.tr("choose_app"))
        self.id_label.setText("")
        self.desc_label.clear()
        self.icon_label.clear()
        self.set_buttons_enabled(False)

        apps = self.backend.get_installed_apps()
        for app_name, app_id, app_version in apps:
            item = QListWidgetItem(app_name)
            item.setData(Qt.UserRole, app_id)
            item.setData(Qt.UserRole + 1, app_version)
            
            icon = QIcon.fromTheme(app_id)
            if not icon.isNull():
                item.setIcon(icon)
            self.list_widget.addItem(item)

    def on_app_selected(self, current, previous):
        if not current: return
        app_id = current.data(Qt.UserRole)
        app_version = current.data(Qt.UserRole + 1)
        
        self.name_label.setText(current.text())
        self.id_label.setText(app_id)
        self.set_buttons_enabled(True)
        
        icon = QIcon.fromTheme(app_id)
        if not icon.isNull():
            self.icon_label.setPixmap(icon.pixmap(64, 64))
        else:
            self.icon_label.clear()

        self.desc_label.setText(f"{self.tr('version')} {app_version}\n\n{self.tr('loading')}")
        QApplication.processEvents()
        
        description = self.backend.get_app_description(app_id)
        self.desc_label.setText(f"{self.tr('version')} {app_version}\n\n{description}")

    def get_current_app_id(self):
        item = self.list_widget.currentItem()
        return item.data(Qt.UserRole) if item else None

    def action_run(self):
        app_id = self.get_current_app_id()
        if app_id: self.backend.run_app(app_id)

    def action_kill(self):
        app_id = self.get_current_app_id()
        if app_id: self.backend.kill_app(app_id)

    def action_update(self):
        app_id = self.get_current_app_id()
        if app_id:
            QMessageBox.information(self, self.tr("window_update"), f"{app_id} {self.tr('msg_updated')}")
            success, error = self.backend.update_app(app_id)
            if not success:
                QMessageBox.warning(self, self.tr("msg_error"), error)
            self.load_apps_to_list()

    def action_uninstall(self):
        app_id = self.get_current_app_id()
        if not app_id: return
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(self.tr("window_delete"))
        msg_box.setText(f"{self.tr('btn_uninstall')} {app_id}?")
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.button(QMessageBox.Yes).setText(self.tr("btn_yes"))
        msg_box.button(QMessageBox.No).setText(self.tr("btn_no"))
        
        reply = msg_box.exec_()
        
        if reply == QMessageBox.Yes:
            success, error = self.backend.uninstall_app(app_id)
            if success:
                QMessageBox.information(self, self.tr("msg_success"), f"{app_id} {self.tr('msg_deleted')}")
                self.load_apps_to_list()
            else:
                QMessageBox.warning(self, self.tr("msg_error"), error)

    def action_install(self):
        app_id, ok = QInputDialog.getText(self, self.tr("window_install"), 
                                          self.tr("window_install_example"))
        if ok and app_id.strip():
            app_id = app_id.strip()
            self.setWindowTitle(f"Installing {app_id}...")
            QApplication.processEvents()
            
            success, error = self.backend.install_app(app_id)
            
            self.setWindowTitle(self.tr("title"))
            if success:
                QMessageBox.information(self, self.tr("msg_success"), f"{app_id} {self.tr('msg_installed')}")
                self.load_apps_to_list()
            else:
                QMessageBox.warning(self, self.tr("msg_error"), f"{error}")