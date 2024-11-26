# mbsObkject:
# Diese Klasse dient als Basisklasse für verschiedene Objekte in einem Mehrkörpersystem. 
# Sie liest Parameter aus Textdaten ein und schreibt die Daten später in eine Datei.

# rigid Body:
# Diese Klasse repräsentiert einen starren Körper und erbt die Grundfunktionen von mbsObject.
# Ein starrer Körper hat spezifische Parameter wie Masse (mass) und den Schwerpunkt (COG, center of gravity), die als Vektoren behandelt werden.



# Basisklasse für Mehrkörpersystem-Objekte:

class mbsObject:
    def __init__(self, obj_type, subtype, text, parameter):
        """
        Konstruktor der Basisklasse mbsObject.
        
        :param obj_type: Der Typ des Objekts (z. B. "Body").
        :param subtype: Der Subtyp des Objekts (z. B. "Rigid_EulerParameter_PAI").
        :param text: Liste von Strings, die die Parameterbeschreibungen enthalten (z. B. "mass: 5.0").
        :param parameter: Ein Dictionary, das die möglichen Parameter des Objekts definiert, mit ihrem Typ und Standardwert.
        """
        self.__type = obj_type  # Speichert den Typ des Objekts.
        self.__subtype = subtype  # Speichert den Subtyp des Objekts.
        self.parameter = parameter  # Speichert die Parameter und ihre Werte als Dictionary.

        # Verarbeitet die Eingabetexte und aktualisiert die Parameterwerte.
        for line in text:
            # Zerlegt jede Zeile in Schlüssel (Parametername) und Wert.
            splitted = line.split(":")  # Beispiel: "mass: 5.0" → ["mass", "5.0"]

            # Gehe durch alle Schlüssel (z. B. "mass", "COG") im Parameter-Dictionary.
            for key in parameter.keys():
                # Überprüfe, ob der Schlüssel im Text gefunden wurde (z. B. "mass").
                if splitted[0].strip() == key:  # Entferne dabei Leerzeichen um den Schlüssel.
                    # Wenn der Parameter ein Float ist, konvertiere den Wert entsprechend.
                    if parameter[key]["type"] == "float":
                        parameter[key]["value"] = self.str2float(splitted[1])
                    # Wenn der Parameter ein Vektor ist, konvertiere den Wert entsprechend.
                    elif parameter[key]["type"] == "vector":
                        parameter[key]["value"] = self.str2vector(splitted[1])

    def writeInputfile(self, file):
        """
        Schreibt die Parameter des Objekts in ein Eingabedateiformat.
        
        :param file: Eine Datei (im Schreibmodus geöffnet), in die die Ausgabe geschrieben wird.
        """
        text = []  # Liste, die die Zeilen des Textes enthält.

        # Schreibe den Header (z. B. "Body Rigid_EulerParameter_PAI").
        text.append(self.__type + " " + self.__subtype + "\n")

        # Iteriere über die Parameter und füge sie der Textliste hinzu.
        for key in self.parameter.keys():
            # Überprüfe den Typ des Parameters (Float oder Vektor) und formatiere ihn.
            if self.parameter[key]["type"] == "float":
                text.append("\t" + key + " = " + self.float2str(self.parameter[key]["value"]) + "\n")
            elif self.parameter[key]["type"] == "vector":
                text.append("\t" + key + " = " + self.vector2str(self.parameter[key]["value"]) + "\n")

        # Schreibe das Ende des Objekts (z. B. "EndBody").
        text.append("End" + self.__type + "\n%\n")

        # Schreibe die Textliste in die Datei.
        file.writelines(text)

    def str2float(self, inString):
        """
        Konvertiert einen String (z. B. "5.0") in einen Float (z. B. 5.0).
        
        :param inString: Der Eingabestring.
        :return: Der konvertierte Float-Wert.
        """
        return float(inString)

    def float2str(self, inFloat):
        """
        Konvertiert einen Float (z. B. 5.0) in einen String (z. B. "5.0").
        
        :param inFloat: Der Eingabe-Float.
        :return: Der konvertierte String.
        """
        return str(inFloat)

    def str2vector(self, inString):
        """
        Konvertiert einen String (z. B. "1.0,2.0,3.0") in eine Liste von Floats ([1.0, 2.0, 3.0]).
        
        :param inString: Der Eingabestring.
        :return: Eine Liste von Floats.
        """
        # Zerlege den String an den Kommata und konvertiere jedes Element in einen Float.
        return [float(coord) for coord in inString.split(",")]

    def vector2str(self, inVector):
        """
        Konvertiert eine Liste von Floats ([1.0, 2.0, 3.0]) in einen String ("1.0,2.0,3.0").
        
        :param inVector: Die Eingabeliste.
        :return: Der formatierte String.
        """
        # Verbinde die Elemente der Liste mit Kommas zu einem String.
        return ",".join(str(coord) for coord in inVector)


# Abgeleitete Klasse für starre Körper (rigid body)
class rigidBody(mbsObject):
    def __init__(self, text):
        """
        Konstruktor für einen starren Körper (rigidBody).
        
        :param text: Liste von Strings, die die Parameterbeschreibungen enthalten (z. B. "mass: 5.0").
        """
        # Definition der spezifischen Parameter für einen starren Körper.
        parameter = {
            "mass": {"type": "float", "value": 1.0},  # Standardwert für die Masse: 1.0.
            "COG": {"type": "vector", "value": [0.0, 0.0, 0.0]}  # Standardwert für den Schwerpunkt: [0, 0, 0].
        }

        # Initialisiere die Basisklasse (mbsObject) mit dem Typ und den Parametern.
        super().__init__("Body", "Rigid_EulerParameter_PAI", text, parameter)

