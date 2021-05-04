from typing import Union, Dict, List

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QMessageBox

from src.models.dataframe_model import DataFrameModel
from src.modules.convert_module import ConvertModule
from src.modules.export_module import ExportModule
from src.modules.import_module import ImportModule
from src.utility.extractors import mock_tact_scenario
from src.utility.utility import get_exception


class FileHandler(QObject):
    task_busy: pyqtSignal = pyqtSignal(str)
    task_failed: pyqtSignal = pyqtSignal(str)
    task_finished: pyqtSignal = pyqtSignal(object)

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.importer: Union[ImportModule, None] = None
        self.converter: Union[ConvertModule, None] = None
        self.exporter: Union[ExportModule, None] = None

    def import_and_convert(self, paths):
        self.importer = ImportModule(paths)
        self.importer.task_finished.connect(self.on_import_success)
        self.importer.task_failed.connect(self.on_task_failed)
        self.importer.task_busy.connect(self.on_task_busy)

        self.importer.start()

    def on_import_success(self, _import: Dict) -> None:
        self.parent.model.mer_data = _import['mer_data']

        _continue = self.verify_tact_scenarios(_import['unique_refs'], _import['mer_data'])

        if _continue:
            self.convert_data()
        else:
            self.task_failed.emit('Import Failed')

    def convert_data(self) -> None:
        self.converter = ConvertModule(self.parent.model.mer_data)
        self.converter.task_finished.connect(self.on_convert_success)
        self.converter.task_failed.connect(self.on_task_failed)
        self.converter.task_busy.connect(self.on_task_busy)
        self.converter.start()

    def on_convert_success(self, converted_data: Dict[str, DataFrameModel]) -> None:
        self.task_finished.emit(converted_data)

    def on_task_busy(self, txt):
        self.task_busy.emit(txt)

    def on_task_failed(self, txt):
        self.task_failed.emit(txt)

    def start_export(self, data: Dict[str, DataFrameModel], dst: str):
        print('Start export...')
        self.exporter: ExportModule = ExportModule(data, dst)
        self.exporter.task_finished.connect(self.on_export_finished)
        self.exporter.task_failed.connect(self.on_task_failed)
        self.exporter.start()

    def on_export_finished(self):
        print('Export finished')

    def verify_tact_scenarios(self, unique_refs: List[str], mer_data: Dict[str, DataFrameModel]) -> bool:
        if 'TACTICAL_SCENARIO' not in mer_data \
                or len(unique_refs) > mer_data['TACTICAL_SCENARIO'].df_unfiltered['REFERENCE'].nunique():

            confirm: QMessageBox = QMessageBox.warning(self.parent.view, 'Warning',
                                                       'No Tactical Scenario found, continue?',
                                                       QMessageBox.No | QMessageBox.Yes)
            if confirm == QMessageBox.Yes:
                try:
                    self.parent.model.mer_data = mock_tact_scenario(mer_data, unique_refs)
                except Exception as e:
                    print(get_exception(e))
                return True
            else:
                return False
        return True

