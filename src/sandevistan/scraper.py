"""
Apple Security Updates Scraper.

Extracts security updates and vulnerability details from Apple's support website.
Supports JSON, CSV, and SQLite output formats.
"""

import json
import csv
import sqlite3
from datetime import datetime
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup


def _fetch_updates_list(url):
    """
    Fetches the main Apple security updates page and extracts basic update information.

    Args:
        url: Apple security updates page URL

    Returns:
        List of dictionaries with keys: name, link, available_for, release_date
    """
    print(f"Fetching data from {url}...")

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')
    updates = []

    for table in soup.find_all('table'):
        for row in table.find_all('tr'):
            cols = row.find_all('td')

            if len(cols) < 3:
                continue

            # Extract name and link from first column
            name_col = cols[0]
            link_tag = name_col.find('a')

            if link_tag:
                name = link_tag.get_text(strip=True)
                link = link_tag.get('href', '')

                if link and not link.startswith('http'):
                    link = 'https://support.apple.com' + link
            else:
                name = name_col.get_text(strip=True)
                link = ''

            if 'This update has no published CVE entries.' in name:
                name = name.replace('This update has no published CVE entries.', '').strip()
                link = ''

            available_for = cols[1].get_text(strip=True)
            release_date = cols[2].get_text(strip=True)

            if name and available_for and release_date:
                updates.append({
                    'name': name,
                    'link': link,
                    'available_for': available_for,
                    'release_date': release_date
                })

    print(f"Found {len(updates)} security updates")
    return updates


def _fetch_advisory_details(advisory_url):
    """
    Fetches an individual advisory page and extracts vulnerability details.

    Each vulnerability is structured as an <h3> component heading followed by
    <p> blocks containing: Available for, Impact, Description, CVE IDs, and Credits.

    Args:
        advisory_url: URL of the advisory page

    Returns:
        List of dictionaries with vulnerability details
    """
    if not advisory_url:
        return []

    print(f"  Fetching advisory: {advisory_url}")

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(advisory_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        vulnerabilities = []

        for h3 in soup.find_all('h3'):
            component_name = h3.get_text(strip=True)

            if not component_name or len(component_name) > 200:
                continue

            # Collect paragraph blocks following this component heading
            current = h3.find_next_sibling()
            p_blocks = []

            while current and len(p_blocks) < 10:
                if current.name in ['h1', 'h2', 'h3']:
                    break
                if current.name == 'p':
                    text = current.get_text(strip=True)
                    if text:
                        p_blocks.append(text)
                current = current.find_next_sibling()

            # Parse structured data from paragraph blocks
            available_for = ''
            impact = ''
            description = ''
            cves_list = []
            credits = ''
            webkit_bugzilla_id = ''

            for p_block in p_blocks:
                if p_block.startswith('Available for'):
                    available_for = p_block
                elif p_block.startswith('Impact'):
                    impact = p_block
                elif p_block.startswith('Description'):
                    description = p_block
                elif p_block.startswith('CVE-'):
                    if ':' in p_block:
                        cve, credit = p_block.split(":", 1)
                        cves_list.append(cve)
                        credits += credit.strip() + '\n'
                    else:
                        cves_list.append(p_block)
                elif p_block.startswith('WebKit Bugzilla'):
                    webkit_bugzilla_id = p_block.split(':', 1)[1].strip()
                elif p_block.startswith("We would like to acknowledge"):
                    credits = p_block

            cve_ids = ', '.join(cves_list)

            # Detect if vulnerability was actively exploited
            combined_text = ' '.join(p_blocks).lower()
            exploited = 'exploited' in combined_text or 'actively exploited' in combined_text

            vulnerabilities.append({
                'component': component_name,
                'available_for': available_for,
                'impact': impact,
                'description': description,
                'cve_id': cve_ids,
                'credit': credits,
                'webkit_bugzilla_id': webkit_bugzilla_id,
                'exploited': exploited,
                'advisory_url': advisory_url
            })

        print(f"    Found {len(vulnerabilities)} vulnerability entries")
        return vulnerabilities

    except requests.RequestException as e:
        print(f"    Error fetching advisory: {e}")
        return []
    except Exception as e:
        print(f"    Error parsing advisory: {e}")
        return []


def scrape_security_updates(url, delay, include_details):
    """
    Scrapes Apple security updates, optionally fetching detailed vulnerability information.

    Args:
        url: Apple security updates page URL
        delay: Delay in seconds between advisory requests (rate limiting)
        include_details: If True, fetch vulnerability details from each advisory page

    Returns:
        Tuple of (updates, vulnerabilities) where each is a list of dictionaries.
        If include_details is False, vulnerabilities will be an empty list.
    """
    updates = _fetch_updates_list(url)

    if not include_details:
        return updates, []

    vulnerabilities = []

    print(f"\nFetching details from {len(updates)} advisories...")
    for i, update in enumerate(updates, 1):
        print(f"\n[{i}/{len(updates)}] {update['name']}")

        if update['link']:
            advisory_vulns = _fetch_advisory_details(update['link'])
            vulnerabilities.extend(advisory_vulns)

            if i < len(updates):
                time.sleep(delay)
        else:
            print(f"  Skipping (no link available)")

    print(f"\nTotal vulnerabilities found: {len(vulnerabilities)}")
    return updates, vulnerabilities


def save_to_json(updates, vulnerabilities, filepath):
    """
    Saves updates and vulnerabilities to a JSON file.

    Args:
        updates: List of security update dictionaries
        vulnerabilities: List of vulnerability dictionaries
        filepath: Output file path
    """
    data = {
        'security_updates': updates,
        'vulnerabilities': vulnerabilities,
        'scraped_at': datetime.now().isoformat()
    }

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(updates)} updates and {len(vulnerabilities)} vulnerabilities to {filepath}")


def save_to_csv(updates, vulnerabilities, base_path):
    """
    Saves updates and vulnerabilities to separate CSV files.

    Args:
        updates: List of security update dictionaries
        vulnerabilities: List of vulnerability dictionaries
        base_path: Base output file path (without extension)
    """
    base_path = Path(base_path)

    updates_filepath = base_path.with_suffix('.csv')
    if updates:
        with open(updates_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['name', 'link', 'available_for', 'release_date'])
            writer.writeheader()
            writer.writerows(updates)
        print(f"Saved {len(updates)} updates to {updates_filepath}")
    else:
        print("No updates to save")

    vulnerabilities_filepath = base_path.parent / f"{base_path.stem}_vulnerabilities.csv"
    if vulnerabilities:
        with open(vulnerabilities_filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'component', 'available_for', 'impact', 'description',
                'cve_id', 'credit', 'webkit_bugzilla_id', 'exploited', 'advisory_url'
            ])
            writer.writeheader()
            writer.writerows(vulnerabilities)
        print(f"Saved {len(vulnerabilities)} vulnerabilities to {vulnerabilities_filepath}")
    else:
        print("No vulnerabilities to save")


def save_to_sqlite(updates, vulnerabilities, filepath):
    """
    Saves updates and vulnerabilities to a SQLite database.

    Creates two tables: security_updates and vulnerabilities, linked by URL.
    Clears existing data before inserting new records.

    Args:
        updates: List of security update dictionaries
        vulnerabilities: List of vulnerability dictionaries
        filepath: Output database file path
    """
    if not updates and not vulnerabilities:
        print("No data to save")
        return

    conn = sqlite3.connect(filepath)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS security_updates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            link TEXT,
            available_for TEXT,
            release_date DATETIME,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS vulnerabilities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            component TEXT NOT NULL,
            available_for TEXT,
            impact TEXT,
            description TEXT,
            cve_id TEXT,
            credit TEXT,
            webkit_bugzilla_id TEXT,
            exploited BOOLEAN,
            advisory_url TEXT,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    cursor.execute('DELETE FROM security_updates')
    cursor.execute('DELETE FROM vulnerabilities')

    for update in updates:
        release_date_str = update['release_date']

        try:
            release_date_dt = datetime.strptime(release_date_str, '%d %b %Y')
            release_date_value = release_date_dt.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError:
            print(f"Warning: Could not parse date '{release_date_str}', storing as NULL")
            release_date_value = None

        cursor.execute('''
            INSERT INTO security_updates (name, link, available_for, release_date)
            VALUES (?, ?, ?, ?)
        ''', (update['name'], update['link'], update['available_for'], release_date_value))

    for vuln in vulnerabilities:
        cursor.execute('''
            INSERT INTO vulnerabilities (
                component, available_for, impact, description, cve_id, credit,
                webkit_bugzilla_id, exploited, advisory_url
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            vuln['component'],
            vuln['available_for'],
            vuln['impact'],
            vuln['description'],
            vuln['cve_id'],
            vuln['credit'],
            vuln.get('webkit_bugzilla_id', ''),
            vuln['exploited'],
            vuln['advisory_url']
        ))

    conn.commit()

    cursor.execute('SELECT COUNT(*) FROM security_updates')
    updates_count = cursor.fetchone()[0]
    cursor.execute('SELECT COUNT(*) FROM vulnerabilities')
    vuln_count = cursor.fetchone()[0]

    print(f"Saved {updates_count} updates and {vuln_count} vulnerabilities to {filepath}")
    print(f"Correlation: Join on security_updates.link = vulnerabilities.advisory_url")

    conn.close()
