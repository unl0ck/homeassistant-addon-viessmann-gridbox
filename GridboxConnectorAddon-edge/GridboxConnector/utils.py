import json
import logging

class SensitiveDataFilter(logging.Filter):
    def filter(self, record):
        message = record.getMessage()
        try:
            # Versuchen, die Nachricht als JSON zu parsen
            data = json.loads(message)
            # Sensible Daten filtern, falls vorhanden
            if 'username' in data:
                data['username'] = '***'
            if 'password' in data:
                data['password'] = '***'
            if 'id_token' in data:
                data['id_token'] = '***'
            if 'access_token' in data:
                data['access_token'] = '***'
            # Das modifizierte Dictionary zurück in einen String konvertieren
            record.msg = json.dumps(data)
        except json.JSONDecodeError:
            # Wenn die Nachricht kein JSON ist, nichts tun
            pass
        return True