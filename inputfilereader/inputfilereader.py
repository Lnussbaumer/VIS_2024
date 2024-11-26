
import mbsObject # Importiere das Modul, das die Definitionen der mbsObject-Klasse enthält.
import json  # JSON-Bibliothek für das Speichern und Laden von Objekten im JSON-Format.



# Öffnet die Datei "test.fdd" im Lesemodus und liest ihren Inhalt.
f = open("inputfilereader/test.fdd", "r")
fileContent = f.read().splitlines()  # Liest die Datei Zeile für Zeile in eine Liste von Strings ein.
f.close()  # Schließt die Datei, da sie nicht mehr benötigt wird.

# Initialisiere Variablen für die Verarbeitung der Datei.
currentBlockType = ""  # Speichert den Typ des aktuell gefundenen Blocks (z. B. "RIGID_BODY").
currentTextBlock = []  # Temporäre Liste, um die Zeilen eines Blocks zu speichern.
listOfMbsObjects = []  # Liste, um alle erkannten mbsObjects zu speichern.

# Definiert die zu suchenden Objekttypen in der Datei.
search4Objects = ["RIGID_BODY", "CONSTRAINT"]

# Durchläuft jede Zeile im Inhalt der Datei.
for line in fileContent:
    # Überprüft, ob die Zeile ein neues Blockzeichen enthält (hier: `$`).
    if line.find("$") >= 0:  # `find("$")` gibt die Position von `$` zurück, oder -1, wenn es nicht gefunden wurde.
        if currentBlockType != "":  # Wenn gerade ein Block gesammelt wird:
            if currentBlockType == "RIGID_BODY":  # Überprüft, ob der aktuelle Block ein "RIGID_BODY" ist.
                # Erstelle ein neues rigidBody-Objekt aus den gesammelten Zeilen und füge es der Liste hinzu.
                listOfMbsObjects.append(mbsObject.rigidBody(currentTextBlock))
            currentBlockType = ""  # Setze den aktuellen Blocktyp zurück, da der Block abgeschlossen ist.

    # Überprüft, ob die aktuelle Zeile den Beginn eines neuen Objekts (z. B. "RIGID_BODY") enthält.
    for type_i in search4Objects:
        # Sucht nach einem Objekttyp (z. B. "RIGID_BODY") innerhalb eines definierten Bereichs der Zeile.
        if line.find(type_i, 1, len(type_i) + 1) >= 0:
            currentBlockType = type_i  # Speichert den Typ des gefundenen Blocks.
            currentTextBlock.clear()  # Löscht die aktuelle Textblockliste, da ein neuer Block beginnt.
            break  # Stoppt die Schleife, wenn ein Blocktyp gefunden wurde.

    # Füge die aktuelle Zeile (unabhängig vom Inhalt) zur Blocktextliste hinzu.
    currentTextBlock.append(line)

# Gibt die Anzahl der erstellten Objekte aus.
print(len(listOfMbsObjects))  # Anzahl der erkannten mbsObjects.

# --------------------------------------
# JSON-Export der Objektdaten:
# --------------------------------------

# Liste zur Speicherung der Modellobjektdaten für den JSON-Export.
modelObjects = []

# Konvertiere jedes mbsObject in ein Dictionary seiner Parameter.
for object in listOfMbsObjects:
    modelObjects.append(object.parameter)  # Speichert die Parameter des Objekts.

# Konvertiere die Liste der Modellobjekte in das JSON-Format.
jDataBase = json.dumps({"modelObjects": modelObjects})

# Schreibe die JSON-Daten in eine Datei namens "test.json".
with open("inputfilereader/test.json", "w") as outfile:
    outfile.write(jDataBase)  # Speichert die JSON-Daten in der Datei.

# --------------------------------------
# JSON-Import (Laden der Daten aus der JSON-Datei):
# --------------------------------------

# Öffne die JSON-Datei zum Lesen.
f = open("inputfilereader/test.json", "r")
data = json.load(f)  # Lade die JSON-Daten als Python-Dictionary.
f.close()  # Schließe die JSON-Datei.

# --------------------------------------
# Erstellung einer .fds-Datei:
# --------------------------------------

# Öffne eine neue Datei im Schreibmodus, um die Objektdaten zu schreiben.
fds = open("inputfilereader/test.fds", "w")

# Schreibe die Daten jedes mbsObjects im spezifischen Eingabedateiformat.
for mbsObject_i in listOfMbsObjects:
    mbsObject_i.writeInputfile(fds)  # Ruft die Methode `writeInputfile` auf, um die Daten zu formatieren.

# Schließt die .fds-Datei nach dem Schreiben.
fds.close()

#-------------------------------------------------------


