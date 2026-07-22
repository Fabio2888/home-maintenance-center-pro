\# Changelog



\## v2.2.0



\- New: native "Aggiungi manutenzione" form (text/select/number/button

  entities, no input_helper or script required) to create new items

  straight from any dashboard.

\- New: best-effort automatic creation of a `local_calendar` entry

  ("Manutenzioni Casa") on first setup, if none is configured yet.

  Runs in the background and never blocks setup if it fails; you

  can always pick a calendar manually from the integration Options.

\- New: up to 3 independently configurable `notify.*` push targets

  (options \> "Push notification device 1/2/3"), replacing the

  single-device option from v2.1.0.



\## v2.1.0



\- Fix: calendar events had zero duration (start == end), hiding

  items sharing a due date from agenda/list calendar views.

\- Fix: services.py was never registered in \_\_init\_\_.py, so no

  home\_maintenance.\* service actually existed.

\- Fix: coordinator.get\_item() was called by services.py but never

  defined, which would have crashed every item-targeted service.

\- Fix: add\_item service called coordinator.async\_add\_item() with

  the wrong signature and never generated an item\_id.

\- Fix: NotificationManager existed but was never instantiated or

  scheduled, so no notification was ever sent.

\- New: optional sync of due items to an external local calendar

  entity (options \> "Local calendar to sync").

\- New: optional push notifications to a chosen notify.\* device,

  alongside the existing persistent notification (options \>

  "Push notification device").



\## v0.1.0



\- Initial project structure

\- Config Flow

\- Options Flow

\- Coordinator

\- Sensors

\- Calendar

\- Buttons

\- History

\- Statistics

\- Maintenance Manager

