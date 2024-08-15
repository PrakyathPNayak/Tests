import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
import webbrowser

class IPMapApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('IP to Map')

        layout = QVBoxLayout()

        self.ip_label = QLabel('Enter IP address:', self)
        layout.addWidget(self.ip_label)

        self.ip_input = QLineEdit(self)
        layout.addWidget(self.ip_input)

        self.generate_button = QPushButton('Generate HTML', self)
        self.generate_button.clicked.connect(self.generate_html)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def generate_html(self):
        ip = self.ip_input.text()
        if not ip:
            QMessageBox.warning(self, 'Error', 'IP address cannot be empty')
            return

        location = self.get_ip_location(ip)
        if location:
            self.create_html_file(location)
            QMessageBox.information(self, 'Success', 'HTML file generated successfully')
        else:
            QMessageBox.warning(self, 'Error', 'Could not retrieve location for the given IP address')

    def get_ip_location(self, ip):
        try:
            response = requests.get(f'http://ipinfo.io/{ip}/json')
            if response.status_code == 200:
                data = response.json()
                return data.get('loc')
            else:
                return None
        except Exception as e:
            print(f'Error retrieving IP location: {e}')
            return None

    def create_html_file(self, location):
        lat, lon = location.split(',')
        html_content = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>IP Location</title>
            <meta charset="utf-8">
            <meta name="viewport" content="initial-scale=1.0">
            <meta name="description" content="Map showing the location of the given IP address">
            <style>
                #map {{
                    height: 100%;
                    width: 100%;
                }}
                html, body {{
                    height: 100%;
                    margin: 0;
                    padding: 0;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <script>
                function initMap() {{
                    var location = {{ lat: {lat}, lng: {lon} }};
                    var map = new google.maps.Map(document.getElementById('map'), {{
                        zoom: 8,
                        center: location
                    }});
                    var marker = new google.maps.Marker({{
                        position: location,
                        map: map
                    }});
                }}
            </script>
            <script async defer src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap"></script>
        </body>
        </html>
        '''

        with open('ip_location_map.html', 'w') as file:
            file.write(html_content)

        webbrowser.open('ip_location_map.html')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = IPMapApp()
    ex.show()
    sys.exit(app.exec_())
