
import sys
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QStatusBar, QFileDialog, QVBoxLayout, QWidget, QColorDialog, QInputDialog #********** 
)
from PyQt6.QtCore import Qt

from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkRenderingCore import vtkRenderer, vtkActor #**********
import mbsModel


#--*--*--*--*--*--*  Translation, Rotation, Skalierung *--*--*--*--*--*--*--*--*--*
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
#--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
# isinstance 
        # Fenster-Einstellungen
        self.setWindowTitle("pyFreeDyn - Qt Anwendung")
        self.setGeometry(100, 100, 1024, 768)

        # Menüleiste erstellen
        self.create_menu()

        # Transformationsobjekt erstellen
        self.transform = vtkTransform()  
        self.transform_filter = vtkTransformPolyDataFilter()  

        # Statusleiste erstellen
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit")

        # Zentrales Widget (VTK Render Window)
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout für zentrales Widget
        layout = QVBoxLayout(self.central_widget)

        # VTK Render Window hinzufügen
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        layout.addWidget(self.vtk_widget)

        # Renderer einrichten
        self.renderer = vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.vtk_widget.Initialize()

        # Platzhalter für das geladene Modell
        self.model = None

    def create_menu(self):
        """Erstellt die Menüleiste mit den geforderten Einträgen."""
        menu_bar = QMenuBar(self)
        self.setMenuBar(menu_bar)

        # File-Menü erstellen
        file_menu = menu_bar.addMenu("File")

        # Menü-Einträge hinzufügen
        file_menu.addAction("Load", self.load_model)
        file_menu.addAction("Save", self.save_model)
        file_menu.addAction("ImportFdd", self.import_fdd)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

#*********************************************************************************************************
        # Farbänderungs-Menü
        file_menu.addAction("Change Color", self.change_model_color)
        file_menu.addAction("Change Material", self.change_model_material)

#--*--*--*--*--*--*  Translation, Rotation, Skalierung *--*--*--*--*--*--*--*--*--*

        # Transformation-Menü (verschieben, drehen, skalieren)
        file_menu.addAction("Translate", self.translate_model)
        file_menu.addAction("Rotate", self.rotate_model)
        file_menu.addAction("Scale", self.scale_model)

#--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*

    def load_model(self):
        """Lädt ein Modell aus einer JSON-Datei."""
        filepath, _ = QFileDialog.getOpenFileName(self, "Modell laden", "", "JSON-Dateien (*.json)")
        if filepath:
            self.model = mbsModel.mbsModel()
            self.model.loadDatabase(filepath)
            self.statusBar.showMessage(f"Modell geladen: {filepath}")
            self.show_model()

    def save_model(self):
        """Speichert das aktuelle Modell in eine JSON-Datei."""
        if self.model:
            filepath, _ = QFileDialog.getSaveFileName(self, "Modell speichern", "", "JSON-Dateien (*.json)")
            if filepath:
                self.model.saveDatabase(filepath)
                self.statusBar.showMessage(f"Modell gespeichert: {filepath}")
        else:
            self.statusBar.showMessage("Kein Modell vorhanden, um es zu speichern.")

    def import_fdd(self):
        """Importiert ein Modell aus einer FDD-Datei."""
        filepath, _ = QFileDialog.getOpenFileName(self, "FDD-Datei importieren", "", "FDD-Dateien (*.fdd)")
        if filepath:
            self.model = mbsModel.mbsModel()
            self.model.importFddFile(filepath)
            self.statusBar.showMessage(f"FDD-Modell importiert: {filepath}")
            self.show_model()

    def show_model(self):
        """Zeigt das aktuelle Modell im VTK-Renderer an."""
        if self.model:
            self.renderer.RemoveAllViewProps()  # Entfernt bestehende Darstellungen
            self.model.showModel(self.renderer)
            self.vtk_widget.GetRenderWindow().Render()
            self.statusBar.showMessage("Modell wird angezeigt.")

#*********************************************************************************************************
    def change_model_color(self):
        """Ändert die Farbe des geladenen Modells."""
        if not self.model:
            self.statusBar.showMessage("Kein Modell geladen. Farbe kann nicht geändert werden.")
            return
        
        # Farbwahl-Dialog öffnen
        color = QColorDialog.getColor()

        # Überprüfen, ob der Benutzer eine Farbe ausgewählt hat
        if color.isValid():
            rgb = [color.red() / 255.0, color.green() / 255.0, color.blue() / 255.0]

            # Alle Actors im Renderer finden und deren Farbe ändern
            self.change_color_of_actors(rgb)

            # Neu rendern
            self.vtk_widget.GetRenderWindow().Render()
            self.statusBar.showMessage("Farbe des Modells geändert.")

    def change_color_of_actors(self, rgb):
        """Ändert die Farbe aller Actors im Renderer."""
        # Durch alle ViewProps im Renderer iterieren
        for i in range(self.renderer.GetViewProps().GetNumberOfItems()):
            actor = self.renderer.GetViewProps().GetItemAsObject(i)
            if isinstance(actor, vtkActor):  # Hier wird jetzt vtkActor direkt verwendet
                actor.GetProperty().SetColor(rgb)

    def change_model_material(self):
        """Ändert das Material des geladenen Modells."""
        if not self.model:
            self.statusBar.showMessage("Kein Modell geladen. Material kann nicht geändert werden.")
            return

        # Material-Auswahl-Dialog öffnen
        materials = ["Stahl", "Alu", "Holz"]
        material, ok = QInputDialog.getItem(self, "Material auswählen", "Material:", materials, 0, False)

        if ok and material:
            if material == "Stahl":
                rgb = [0.3, 0.3, 0.3]  # Dunkelgrau
            elif material == "Alu":
                rgb = [0.75, 0.75, 0.75]  # Hellgrau
            elif material == "Holz":
                rgb = [0.6, 0.4, 0.2]  # Braun

            # Alle Actors im Renderer finden und deren Farbe ändern
            self.change_color_of_actors(rgb)

            # Neu rendern
            self.vtk_widget.GetRenderWindow().Render()
            self.statusBar.showMessage(f"Material des Modells geändert zu {material}.")

    def change_color_of_actors(self, rgb):
        """Ändert die Farbe aller Actors im Renderer."""
        # Durch alle ViewProps im Renderer iterieren
        for i in range(self.renderer.GetViewProps().GetNumberOfItems()):
            actor = self.renderer.GetViewProps().GetItemAsObject(i)
            if isinstance(actor, vtkActor):  # Hier wird jetzt vtkActor direkt verwendet
                actor.GetProperty().SetColor(rgb)



#--*--*--*--*--*--*  Translation, Rotation, Skalierung *--*--*--*--*--*--*--*--*--* 
# Modelltransformationen
    def translate_model(self):
        """Verschiebe das Modell entlang der Achsen."""
        self.transform.Identity()  # Reset der Transformation
        self.transform.Translate(300.0, 0.0, 0.0)  # Verschiebe entlang der X-Achse um 10 Einheiten
        self.apply_transform()

    def rotate_model(self):
        """Drehe das Modell um 45 Grad um die Y-Achse."""
        self.transform.Identity()  # Reset der Transformation
        self.transform.RotateY(45)  # Drehung um die Y-Achse
        self.apply_transform()

    def scale_model(self):
        """Skaliere das Modell um den Faktor 5."""
        self.transform.Identity()  # Reset der Transformation
        self.transform.Scale(5, 5, 5)  # Skalierung um den Faktor 5
        self.apply_transform()

    def apply_transform(self):
        """Wendet die Transformation auf das Modell an."""
        for i in range(self.renderer.GetViewProps().GetNumberOfItems()):
            actor = self.renderer.GetViewProps().GetItemAsObject(i)
            if isinstance(actor, vtkActor):
                # Transformation direkt auf den Actor anwenden
                actor.SetUserTransform(self.transform)

        # Rendering nach der Transformation
        self.vtk_widget.GetRenderWindow().Render()
        self.statusBar.showMessage("Modell transformiert.")

        # Reset der Kameraansicht
        self.renderer.ResetCamera()
        self.vtk_widget.GetRenderWindow().Render()

#--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*--*




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
