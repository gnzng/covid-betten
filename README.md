[![Build Status](https://travis-ci.org/gnzng/covid-beds.svg?branch=main)](https://travis-ci.org/gnzng/covid-beds)

\_project offline

Die Aktuallisierung der Website wurde eingestellt. Ich hatte die Übersicht erstsellt, als es noch keine Auftragung der zugänglichen Daten gab. Mittlerweile können [hier](https://www.intensivregister.de/#/aktuelle-lage/zeitreihen) ähnliche Daten und deren Auftragung direkt von der DIVI bezogen und gefunden werden.

# COVID Bettenbelegung in Deutschland

Daten waren von https://www.divi.de/divi-intensivregister-tagesreport-archiv-csv?layout=table

Gemeindeschlüssel können [hier](https://www.riserid.eu/data/user_upload/downloads/info-pdf.s/Diverses/Liste-Amtlicher-Gemeindeschluessel-AGS-2015.pdf) von RISER ID gefunden werden. Man beachte dass hier Gemeinden so zusammengefasst werden, dass die letzten 3 Ziffern weggelassen werden.

<img width="1437" alt="Screenshot 2021-06-06 at 20 06 03" src="https://user-images.githubusercontent.com/65827185/120935520-811e2d80-c703-11eb-98c8-6489cbbcf664.png">

_alle Angaben sind ohne Gewähr_

# what I've learned here:

- [x] setup workflow with continues integration Travis CI
- [x] get data automatic from API and process it
- [x] reading and process data from pdf
- [x] visualization and interaction using plotly
- [x] use dash for visualization
