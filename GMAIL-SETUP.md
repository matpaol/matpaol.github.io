# Attivazione report Gmail

Email a paolini134@gmail.com verso le 20:17 italiane, con i dati di ieri.
GitHub può ritardare i cron e sospenderli dopo 60 giorni di inattività nei repo pubblici.

Secrets richiesti: CF_API_TOKEN, CF_ACCOUNT_ID, GMAIL_APP_PASSWORD.
CF_ACCOUNT_ID è supportato anche come Repository variable. Le password solo nei Secrets.
La password per l'app deve appartenere a paolini134@gmail.com; gli spazi vengono rimossi.
Resend e REPORT_FROM non servono più: questo documento sostituisce EMAIL-SETUP.md.

Carica sul branch predefinito questi percorsi esatti:
- .github/workflows/daily-report.yml
- scripts/daily_report.py

Su Mac Cmd+Shift+. mostra la cartella nascosta .github nel Finder.
In alternativa su GitHub Add file → Create new file: usa il percorso completo
come nome e incolla il contenuto del file corrispondente.

Poi Actions → Daily portfolio report → Run workflow. Controlla job e posta/Spam.
Se ieri non c'era lo snippet, zero visite è normale. Esecuzioni manuali ripetute
inviano email ripetute. La consegna va verificata nella casella.

Test locale senza rete: python scripts/daily_report.py --preview
Query live e invio non ancora verificati: richiedono i Secrets del tuo account.
Gli errori API interrompono il job senza inviare falsi report con zero visite.
