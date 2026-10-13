Experimenteller Community-Testbuild von Kaspa NG mit Rusty Kaspa **2.1.0**.
Kein offizielles Aspectron-Release. Die NG-Anwendungsnummer bleibt 2.0.1.

## Downloads

- **windows-x64.zip**: Windows 64-Bit, portable EXE ohne Konsolenfenster.
- **linux-x64.tar.gz**: Linux 64-Bit, gebaut auf Ubuntu 22.04 (glibc 2.35 oder neuer). Desktop-Laufzeitbibliotheken erforderlich; unter Ubuntu: `sudo apt install libgtk-3-0 libxkbcommon0 libegl1 libgl1 libxcb-shape0 libxcb-xfixes0`.
- **macos-arm64.tar.gz**: Apple Silicon (M1 und neuer), macOS 15 oder neuer, App-Bundle.
- **macos-x64.tar.gz**: Intel-Mac, macOS 15 oder neuer, App-Bundle.
- **SHA256SUMS.txt**: Pruefsummen der vier Archive.

Archive vollstaendig entpacken. Windows: `kaspa-ng.exe`; Linux: `./kaspa-ng`; macOS: `Kaspa NG Test.app`.
Optimierte Builds (`cargo build --locked --release --bin kaspa-ng`, Rust 1.95.0).
Keine Windows-Herausgebersignatur, keine Apple-Developer-Signatur/Notarisierung. macOS kann das Oeffnen blockieren; keine systemweiten Sicherheitsfunktionen abschalten.

## Getrennte Testdaten

Ein anderer Downloadordner trennt keine Wallets oder Einstellungen. `--appdir` allein betrifft nur den Node.
Ein **neues lokales Betriebssystem-Benutzerkonto** anlegen, dort anmelden und das Archiv dort entpacken.
Unter Windows kann das Konto **KaspaTest** heissen. Keine Seeds, Wallets, Einstellungen oder Node-Daten aus dem Hauptkonto uebernehmen.
Bereits laufende NG-/kaspad-Instanzen vorher beenden, um Portkonflikte zu vermeiden.

Zuerst ohne Node-Verbindung starten:

- Windows, PowerShell im entpackten Ordner: `.\kaspa-ng.exe --disable`
- Linux, Terminal im entpackten Ordner: `./kaspa-ng --disable`
- macOS, Terminal im entpackten Ordner: `open "Kaspa NG Test.app" --args --disable`

`--disable` unterbindet Node-Dienste beim Start; andere Internetabfragen sind weiterhin moeglich.
Fuer Sync-/Wallet-Tests **Testnet 10** auswaehlen, eine **neue Testwallet** anlegen und dann **Integrated Daemon** aktivieren.
Keine echten KAS verwenden. Die Trennung der Dateien entsteht durch das neue Benutzerkonto, nicht durch `--disable`.

## Pruefung und Herkunft

Jedes Paket enthaelt `BUILD-INFO.txt` mit Quellcommit, Rust-Version und Plattform sowie die Lizenzen.
Die Abhaengigkeiten sind in Cargo.lock fixiert; RK basiert auf v2.1.0 mit bestehenden Aspectron-SDK-Anpassungen.
Jeder Plattform-Build muss erfolgreich sein und bei `--help` RK 2.1.0 melden, bevor dieses Release veroeffentlicht wird.
Vorhandene NG-Unit-Tests wurden zuvor unter Windows ausgefuehrt. GUI-Bedienung, vollstaendige Synchronisation und Wallet-Transaktionen sind noch nicht plattformuebergreifend validiert.
