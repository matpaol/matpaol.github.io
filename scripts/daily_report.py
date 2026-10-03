"""Daily Cloudflare Web Analytics digest. Credentials come only from GitHub Secrets."""
import argparse
import json
import os
import sys
import smtplib
import ssl
from email.message import EmailMessage
from datetime import datetime, timedelta, timezone
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from zoneinfo import ZoneInfo

HOST = 'matpaol.github.io'
RECIPIENT = 'paolini134@gmail.com'

def post(url, token, payload, extra=None):
    request = Request(url, data=json.dumps(payload).encode(), headers={
        'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
        **(extra or {}),
    })
    try:
        with urlopen(request, timeout=45) as response:
            return json.load(response)
    except HTTPError as error:
        raise RuntimeError(f'API request failed: HTTP {error.code}') from None

def period(now):
    today = now.astimezone(ZoneInfo('Europe/Rome')).date()
    monday = today - timedelta(days=today.weekday())
    end = datetime.combine(
        monday, datetime.min.time(), ZoneInfo('Europe/Rome')
    )
    start = end - timedelta(days=7)
    iso = lambda value: value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')
    label = f"{start.date()} — {(end - timedelta(days=1)).date()}"
    return label, iso(start), iso(end)

def query(account, start, end):
    # JSON string escaping also safely quotes GraphQL string literals.
    filt = '{datetime_geq: %s, datetime_lt: %s, requestHost: %s, bot: 0}' % (
        json.dumps(start), json.dumps(end), json.dumps(HOST))
    return '''{viewer {accounts(filter: {accountTag: %s}) {
      total: rumPageloadEventsAdaptiveGroups(filter: %s, limit: 1) {count sum {visits}}
      countries: rumPageloadEventsAdaptiveGroups(filter: %s, limit: 10, orderBy: [count_DESC]) {count dimensions {countryName}}
      pages: rumPageloadEventsAdaptiveGroups(filter: %s, limit: 10, orderBy: [count_DESC]) {count dimensions {requestPath}}
    }}}''' % (json.dumps(account), filt, filt, filt)

def render(day, data):
    totals = data.get('total', [])
    if len(totals) > 1:
        raise RuntimeError('Unexpected totals response')
    total = totals[0] if totals else {'count': 0, 'sum': {'visits': 0}}
    lines = [f'Portfolio — {day}', '', f"Visite: {total['sum']['visits']}",
             f"Pagine viste: {total['count']}", '', 'Paesi — pagine viste:']
    for row in data.get('countries', []):
        lines.append(f"- {row['dimensions'].get('countryName') or 'Non disponibile'}: {row['count']}")
    lines += ['', 'Pagine più viste:']
    for row in data.get('pages', []):
        lines.append(f"- {row['dimensions'].get('requestPath') or '/'}: {row['count']}")
    lines += ['', 'Periodo: settimana precedente, lunedì–domenica, fuso Europe/Rome.',,
              'Visite = sessioni, non persone identificate. Dati RUM: possono essere campionati',
              'e non includere visite bloccate dagli ad blocker.', 'https://' + HOST]
    return '\n'.join(lines)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--preview', action='store_true', help='Local example; no API requests')
    args = parser.parse_args()
    now = datetime.now(timezone.utc)
    if os.getenv('GITHUB_EVENT_NAME') == 'schedule' and now.astimezone(ZoneInfo('Europe/Rome')).hour != 20:
        print('Skipping alternate daylight-saving schedule')
        return
    day, start, end = period(now)
    if args.preview:
        print(render(day, {'total': [{'count': 42, 'sum': {'visits': 18}}],
                          'countries': [{'count': 30, 'dimensions': {'countryName': 'IT'}}],
                          'pages': [{'count': 12, 'dimensions': {'requestPath': '/projects/tentacle/'}}]}))
        return
    required = ['CF_ACCOUNT_ID', 'CF_API_TOKEN', 'GMAIL_APP_PASSWORD']
    if any(not os.getenv(key) for key in required):
        raise RuntimeError('Missing GitHub Secrets: ' + ', '.join(key for key in required if not os.getenv(key)))
    response = post('https://api.cloudflare.com/client/v4/graphql', os.environ['CF_API_TOKEN'],
                    {'query': query(os.environ['CF_ACCOUNT_ID'], start, end)})
    if response.get('errors'):
        raise RuntimeError('Cloudflare rejected the analytics query; check token permissions and schema in the dashboard')
    accounts = response['data']['viewer']['accounts']
    if len(accounts) != 1:
        raise RuntimeError('Cloudflare account not accessible; no report sent')
    message = EmailMessage()
    message['From'] = f'Portfolio report <{RECIPIENT}>'
    message['To'] = RECIPIENT
    message['Subject'] = f'Portfolio — riepilogo {day}'
    message.set_content(render(day, accounts[0]))
    password = ''.join(os.environ['GMAIL_APP_PASSWORD'].split())
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=ssl.create_default_context(), timeout=45) as smtp:
            smtp.login(RECIPIENT, password)
            if smtp.send_message(message):
                raise RuntimeError('Gmail refused the recipient')
    except smtplib.SMTPAuthenticationError:
        raise RuntimeError('Gmail login refused: check GMAIL_APP_PASSWORD and its account') from None
    except smtplib.SMTPException:
        raise RuntimeError('Gmail could not send the report') from None
    print('Report accepted by email provider')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, KeyError, TypeError, ValueError, OSError) as error:
        print(str(error), file=sys.stderr)
        sys.exit(1)
