# 🏠 Home Maintenance Center Pro

Integrazione custom per **Home Assistant** che tiene traccia delle
manutenzioni periodiche di casa (filtri, climatizzatori, bombole,
scadenze idrauliche, ecc.), con notifiche automatiche, sincronizzazione
su calendario e un piccolo "form" nativo per aggiungere nuove voci
direttamente da dashboard — nessuna configurazione YAML richiesta per
l'uso quotidiano.

![version](https://img.shields.io/badge/version-2.2.0-blue)
![HA](https://img.shields.io/badge/Home%20Assistant-2024.6%2B-41BDF5)
![license](https://img.shields.io/badge/license-MIT-green)

---

## ✨ Funzionalità

- **Un device per manutenzione**: ogni voce (es. "Filtri Depuratore",
  "Bombola CO₂") diventa un device HA a sé stante, con le proprie
  entità (`sensor`, `binary_sensor`, `date`, `number`, `switch`,
  `button`, `calendar`).
- **Calcolo automatico delle scadenze**: giorni rimanenti, stato
  "in scadenza"/"scaduta", basato su data ultima manutenzione +
  intervallo in giorni.
- **Pulsante "Segna come fatta"** su ogni device: aggiorna da solo
  data e prossima scadenza.
- **Form nativo per aggiungere nuove manutenzioni** dalla dashboard
  (entità `text` + `select` + `number` + `button`), senza bisogno di
  `input_text`/`input_select`/script esterni.
- **Notifiche** (persistenti in HA + push) fino a **3 dispositivi**
  configurabili dalle Opzioni, con giorni di preavviso personalizzabili.
- **Sincronizzazione opzionale** delle scadenze su un calendario
  locale a scelta (es. `calendar.manutenzioni_casa`), con tentativo
  automatico di creazione al primo avvio.
- **Diagnostica e controlli di integrità** (Impostazioni → Sistema →
  Repairs) per intervalli non validi, ID duplicati o date mancanti.
- **Sensori di riepilogo**: totale manutenzioni, regolari, in
  scadenza, scadute, "casa in ordine" / "richiede attenzione".
- Multilingua: italiano e inglese.

---

## 📦 Installazione

### Tramite HACS (consigliato)

1. HACS → Integrazioni → menu (⋮) in alto a destra → **Repository
   personalizzati**
2. Aggiungi l'URL di questo repository, categoria **Integration**
3. Cerca "Home Maintenance Center Pro" → **Installa**
4. Riavvia Home Assistant

### Manuale

1. Copia la cartella `custom_components/home_maintenance_center`
   nella cartella `custom_components` della tua installazione HA
2. Riavvia Home Assistant

### Configurazione

Impostazioni → Dispositivi e servizi → **+ Aggiungi integrazione** →
cerca "Home Maintenance Center Pro".

Dopo l'installazione, apri **Configura** sull'integrazione per
impostare:

| Opzione | Descrizione |
|---|---|
| Giorni di preavviso | es. `30,15,7,3,1` |
| Ora delle notifiche | ora del giorno (0–23) in cui vengono controllate le scadenze |
| Ripeti notifiche scadute | se notificare ogni giorno le manutenzioni già scadute |
| Dispositivo notifiche push 1/2/3 | fino a 3 servizi `notify.*` (es. `mobile_app_iphone_fabio`) |
| Calendario locale da sincronizzare | un'entità `calendar.*` su cui specchiare le scadenze |

---

## 🖥️ Dashboard di esempio

Nella cartella [`dashboard/`](./dashboard) trovi un esempio di
dashboard Lovelace pronta da incollare, con:

- Badge sempre visibili (scadute, in scadenza, attenzione)
- Riepilogo automatico (scadute / in scadenza / regolari) generato
  via template Jinja — si aggiorna da solo con le nuove manutenzioni
- Form "Aggiungi nuova manutenzione"
- Griglia "Segna manutenzioni effettuate" (richiede la card
  [auto-entities](https://github.com/thomasloven/lovelace-auto-entities)
  via HACS → Frontend, per restare automatica anche lei)
- Vista Calendario

---

## 🔧 Servizi disponibili

| Servizio | Descrizione |
|---|---|
| `home_maintenance.add_item` | Crea una nuova manutenzione (`name`, `category`, `interval_days`) |
| `home_maintenance.remove_item` | Elimina una manutenzione (`item_id`) |
| `home_maintenance.mark_completed` | Segna una manutenzione come effettuata oggi (`item_id`) |
| `home_maintenance.postpone_item` | Posticipa la prossima scadenza di N giorni (`item_id`, `days`) |
| `home_maintenance.reset_item` | Ricalcola la scadenza dall'intervallo originale (`item_id`) |
| `home_maintenance.reload` | Ricarica tutte le manutenzioni da storage |

Tutti i servizi sono chiamabili anche da automazioni, script o
Strumenti per sviluppatori → Azioni.

---

## 🗺️ Struttura del progetto

```
custom_components/home_maintenance_center/
├── __init__.py           # setup, servizi, notifiche, sync calendario
├── coordinator.py        # DataUpdateCoordinator + logica CRUD condivisa
├── config_flow.py        # flusso di configurazione iniziale
├── options_flow.py       # opzioni (notifiche, calendario)
├── calendar_sync.py      # sync scadenze su calendario locale esterno
├── notify.py             # motore di notifica (persistenti + push)
├── repairs.py            # controlli di integrità (Settings > Repairs)
├── services.py           # servizi home_maintenance.*
├── entity.py             # classi base condivise (device_info, ecc.)
├── sensor.py / binary_sensor.py / date.py / number.py
│   / select.py / text.py / switch.py / button.py / calendar.py
├── managers/
│   └── storage_manager.py   # persistenza su storage HA
├── models/
│   └── maintenance_item.py  # modello dati di una manutenzione
├── translations/         # it.json, en.json
└── manifest.json
```

---

## 🧪 Note tecniche / limiti noti

- La creazione automatica del calendario locale al primo avvio è
  **best-effort**: se fallisce (versione HA diversa, integrazione
  `local_calendar` non disponibile, ecc.) non blocca l'avvio
  dell'integrazione — puoi sempre selezionare un calendario a mano
  dalle Opzioni.
- Le entità del form "Aggiungi manutenzione" (`text`, `select`,
  `number`) mantengono il valore digitato solo in memoria: si
  azzerano ad ogni riavvio di Home Assistant.
- L'eliminazione di una manutenzione (`remove_item`) è definitiva e
  non richiede conferma via servizio: se la richiami da una
  dashboard, valuta di aggiungere una conferma lato UI.

---

## 📝 Changelog

Vedi [CHANGELOG.md](./CHANGELOG.md) per la cronologia completa delle
versioni.

---

## 🤝 Contribuire

Pull request e segnalazioni di bug sono benvenute tramite le Issue
di GitHub.

## 📄 Licenza

MIT — vedi [LICENSE](./LICENSE).
