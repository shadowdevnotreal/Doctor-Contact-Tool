#!/usr/bin/env python3
"""
DoctorDork - Medical Professional Research Tool
Author: Slow
Version: 2.0.0
Description: Comprehensive tool for researching doctors and medical professionals
"""

import os
import sys
import json
import csv
import webbrowser
import urllib.parse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ANSI Color codes for cross-platform support
class Colors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DoctorDork:
    """Main application class for DoctorDork"""

    VERSION = "2.1.0"
    CONFIG_FILE = Path.home() / ".doctordork_config.json"
    HISTORY_FILE = Path.home() / ".doctordork_history.json"

    # Medical board URLs for all 51 US jurisdictions
    MEDICAL_BOARDS = {
        "AL": {"name": "Alabama", "url": "https://www.albme.org/Licensing/Verification.aspx"},
        "AK": {"name": "Alaska", "url": "https://www.commerce.alaska.gov/cbp/main/Search/Professional"},
        "AZ": {"name": "Arizona", "url": "https://azmd.gov/"},
        "AR": {"name": "Arkansas", "url": "https://www.armedicalboard.org/Public/verify/default.aspx"},
        "CA": {"name": "California", "url": "https://www.mbc.ca.gov/Lookup.aspx"},
        "CO": {"name": "Colorado", "url": "https://apps.colorado.gov/dora/licensing/Lookup/LicenseLookup.aspx"},
        "CT": {"name": "Connecticut", "url": "https://www.elicense.ct.gov/Lookup/LicenseLookup.aspx"},
        "DE": {"name": "Delaware", "url": "https://dpr.delaware.gov/boards/medicalpractice/"},
        "DC": {"name": "District of Columbia", "url": "https://doh.dc.gov/bomed"},
        "FL": {"name": "Florida", "url": "https://mqa-internet.doh.state.fl.us/MQASearchServices/Home"},
        "GA": {"name": "Georgia", "url": "https://gcmb.mylicense.com/verification/"},
        "HI": {"name": "Hawaii", "url": "https://mypvl.dcca.hawaii.gov/public-license-search/"},
        "ID": {"name": "Idaho", "url": "https://bom.idaho.gov/BOMPortal/"},
        "IL": {"name": "Illinois", "url": "https://www.idfpr.com/LicenseLookup/"},
        "IN": {"name": "Indiana", "url": "https://mylicense.in.gov/everification/Search.aspx"},
        "IA": {"name": "Iowa", "url": "https://eservices.iowa.gov/licensediniowa/"},
        "KS": {"name": "Kansas", "url": "https://www.ksbha.org/"},
        "KY": {"name": "Kentucky", "url": "https://web1.ky.gov/GenSearch/LicenseList.aspx?AGY=5"},
        "LA": {"name": "Louisiana", "url": "https://www.lsbme.la.gov/"},
        "ME": {"name": "Maine", "url": "https://www.maine.gov/md/"},
        "MD": {"name": "Maryland", "url": "https://www.mbp.state.md.us/bpqapp/"},
        "MA": {"name": "Massachusetts", "url": "https://www.mass.gov/orgs/board-of-registration-in-medicine"},
        "MI": {"name": "Michigan", "url": "https://www.michigan.gov/lara/bureau-list/bpl/occ/prof/medicine"},
        "MN": {"name": "Minnesota", "url": "https://mn.gov/boards/medical-practice/"},
        "MS": {"name": "Mississippi", "url": "https://www.msbml.ms.gov/"},
        "MO": {"name": "Missouri", "url": "https://pr.mo.gov/licensee-search.asp"},
        "MT": {"name": "Montana", "url": "https://boards.bsd.dli.mt.gov/med"},
        "NE": {"name": "Nebraska", "url": "https://www.nebraska.gov/LISSearch/search.cgi"},
        "NV": {"name": "Nevada", "url": "https://medboard.nv.gov/"},
        "NH": {"name": "New Hampshire", "url": "https://www.nh.gov/oplc/"},
        "NJ": {"name": "New Jersey", "url": "https://newjersey.mylicense.com/verification/"},
        "NM": {"name": "New Mexico", "url": "https://www.nmmb.state.nm.us/"},
        "NY": {"name": "New York", "url": "https://www.op.nysed.gov/verification-search"},
        "NC": {"name": "North Carolina", "url": "https://www.ncmedboard.org/"},
        "ND": {"name": "North Dakota", "url": "https://www.ndbomex.com/"},
        "OH": {"name": "Ohio", "url": "https://elicense.ohio.gov/"},
        "OK": {"name": "Oklahoma", "url": "https://www.okmedicalboard.org/"},
        "OR": {"name": "Oregon", "url": "https://omb.oregon.gov/"},
        "PA": {"name": "Pennsylvania", "url": "https://www.pals.pa.gov/#/page/search"},
        "RI": {"name": "Rhode Island", "url": "https://health.ri.gov/licenses/detail.php?id=231"},
        "SC": {"name": "South Carolina", "url": "https://verify.llronline.com/"},
        "SD": {"name": "South Dakota", "url": "https://boardsandcommissions.sd.gov/"},
        "TN": {"name": "Tennessee", "url": "https://apps.health.tn.gov/Licensure/"},
        "TX": {"name": "Texas", "url": "https://profile.tmb.state.tx.us/"},
        "UT": {"name": "Utah", "url": "https://dopl.utah.gov/"},
        "VT": {"name": "Vermont", "url": "https://sos.vermont.gov/opr/"},
        "VA": {"name": "Virginia", "url": "https://www.dhp.virginia.gov/"},
        "WA": {"name": "Washington", "url": "https://fortress.wa.gov/doh/providercredentialsearch/"},
        "WV": {"name": "West Virginia", "url": "https://wvbom.wv.gov/"},
        "WI": {"name": "Wisconsin", "url": "https://dsps.wi.gov/"},
        "WY": {"name": "Wyoming", "url": "https://wyomedboard.state.wy.us/"},
    }

    # Review platforms
    REVIEW_PLATFORMS = {
        "Google": "https://www.google.com/search?q={doctor_name}+{city}+{state}+doctor+reviews",
        "Healthgrades": "https://www.healthgrades.com/search?what={doctor_name}&where={city}%2C+{state}",
        "Vitals": "https://www.vitals.com/search?q={doctor_name}&locationsearch={city}%2C+{state}",
        "RateMDs": "https://www.ratemds.com/best-doctors/?search={doctor_name}&location={city}%2C+{state}",
        "Zocdoc": "https://www.zocdoc.com/search/?dr_specialty=&insurance_carrier=&search_query={doctor_name}&address={city}%2C+{state}",
    }

    # Social media platforms
    SOCIAL_PLATFORMS = {
        "LinkedIn": "https://www.linkedin.com/search/results/all/?keywords={doctor_name}+{specialty}",
        "Twitter": "https://twitter.com/search?q={doctor_name}+doctor",
        "Facebook": "https://www.facebook.com/search/top?q={doctor_name}+doctor",
    }

    # Medicare/Provider lookup platforms
    MEDICARE_LOOKUP = {
        "NPI Registry": "https://npiregistry.cms.hhs.gov/search?searchType=ind&lastName={last_name}&firstName={first_name}&state={state}",
        "Medicare Physician Compare": "https://www.medicare.gov/care-compare/search?type=Physician&searchType=Physician&page=1&search={doctor_name}",
    }

    # Publication search platforms
    PUBLICATION_LOOKUP = {
        "PubMed": "https://pubmed.ncbi.nlm.nih.gov/?term={doctor_name}",
        "Google Scholar": "https://scholar.google.com/scholar?q={doctor_name}",
    }

    # Specialty board certification platforms
    SPECIALTY_VERIFICATION = {
        "ABMS Certification": "https://www.certificationmatters.org/find-your-doctor.aspx",
        "AOA Board Certification": "https://www.osteopathic.org/home/",
    }

    # Education and training platforms
    EDUCATION_LOOKUP = {
        "AMA DoctorFinder": "https://www.ama-assn.org/life-career/professional-satisfaction/ama-doctorfinder",
        "Doximity": "https://www.doximity.com/search?q={doctor_name}",
    }

    # Hospital affiliation platforms
    HOSPITAL_AFFILIATIONS = {
        "Healthgrades Hospital Affiliations": "https://www.healthgrades.com/search?what={doctor_name}&where={city}%2C+{state}",
        "Vitals Hospital Info": "https://www.vitals.com/search?q={doctor_name}&locationsearch={city}%2C+{state}",
        "WebMD Provider Directory": "https://doctor.webmd.com/results?ps={doctor_name}&pt=&lid={state}",
    }

    # Insurance acceptance platforms
    INSURANCE_ACCEPTANCE = {
        "Zocdoc Insurance Search": "https://www.zocdoc.com/search/?dr_specialty=&insurance_carrier=&search_query={doctor_name}&address={city}%2C+{state}",
        "Healthgrades Insurance Info": "https://www.healthgrades.com/search?what={doctor_name}&where={city}%2C+{state}",
        "Vitals Insurance Accepted": "https://www.vitals.com/search?q={doctor_name}&locationsearch={city}%2C+{state}",
    }

    # Language support lookup platforms
    LANGUAGE_SUPPORT = {
        "Healthgrades Languages": "https://www.healthgrades.com/search?what={doctor_name}&where={city}%2C+{state}",
        "Vitals Language Info": "https://www.vitals.com/search?q={doctor_name}&locationsearch={city}%2C+{state}",
        "Zocdoc Language Filter": "https://www.zocdoc.com/search/?search_query={doctor_name}&address={city}%2C+{state}",
    }

    # Telemedicine options platforms
    TELEMEDICINE_OPTIONS = {
        "Healthgrades Virtual Care": "https://www.healthgrades.com/search?what={doctor_name}+telehealth&where={city}%2C+{state}",
        "Zocdoc Video Visits": "https://www.zocdoc.com/search/?dr_specialty=&insurance_carrier=&search_query={doctor_name}&address={city}%2C+{state}&visitType=virtual",
        "Doximity Video": "https://www.doximity.com/search?q={doctor_name}",
        "Teladoc Provider Search": "https://www.teladoc.com/",
    }

    # Appointment booking platforms
    APPOINTMENT_BOOKING = {
        "Zocdoc Booking": "https://www.zocdoc.com/search/?dr_specialty=&insurance_carrier=&search_query={doctor_name}&address={city}%2C+{state}",
        "Healthgrades Appointments": "https://www.healthgrades.com/search?what={doctor_name}&where={city}%2C+{state}",
        "Vitals Schedule": "https://www.vitals.com/search?q={doctor_name}&locationsearch={city}%2C+{state}",
        "MyChart Epic": "https://www.mychartonline.com/",
    }

    def __init__(self):
        """Initialize DoctorDork application"""
        self.config = self.load_config()
        self.history = self.load_history()
        self.search_results = {}

    def load_config(self) -> Dict:
        """Load configuration from file"""
        default_config = {
            "auto_open_browser": True,
            "export_format": "html",
            "save_history": True,
            "show_progress": True,
        }

        if self.CONFIG_FILE.exists():
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return {**default_config, **json.load(f)}
            except:
                return default_config
        return default_config

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump(self.config, f, indent=4)
            self.print_success("Configuration saved successfully!")
        except Exception as e:
            self.print_error(f"Error saving configuration: {e}")

    def load_history(self) -> List[Dict]:
        """Load search history from file"""
        if self.HISTORY_FILE.exists():
            try:
                with open(self.HISTORY_FILE, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []

    def save_history(self, search_data: Dict):
        """Save search to history"""
        if not self.config.get("save_history", True):
            return

        search_data["timestamp"] = datetime.now().isoformat()
        self.history.append(search_data)

        # Keep only last 100 searches
        self.history = self.history[-100:]

        try:
            with open(self.HISTORY_FILE, 'w') as f:
                json.dump(self.history, f, indent=4)
        except Exception as e:
            self.print_error(f"Error saving history: {e}")

    def clear_screen(self):
        """Clear terminal screen"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def print_logo(self):
        """Display application logo"""
        logo = f"""{Colors.CYAN}
╔═══════════════════════════════════════════════════════════════════════╗
║                                                                       ║
║   ____             _             ____             _                   ║
║  |  _ \\  ___   ___| |_ ___  _ __|  _ \\  ___  _ __| | __              ║
║  | | | |/ _ \\ / __| __/ _ \\| '__| | | |/ _ \\| '__| |/ /              ║
║  | |_| | (_) | (__| || (_) | |  | |_| | (_) | |  |   <               ║
║  |____/ \\___/ \\___|\\__\\___/|_|  |____/ \\___/|_|  |_|\\_\\             ║
║                                                                       ║
║              Medical Professional Research Tool v{self.VERSION}            ║
║                                                                       ║
║          Streamline your doctor research from 30+ to 2 minutes       ║
║                                                                       ║
╚═══════════════════════════════════════════════════════════════════════╝
{Colors.RESET}"""
        print(logo)

    def print_success(self, message: str):
        """Print success message"""
        print(f"{Colors.GREEN}✓ {message}{Colors.RESET}")

    def print_error(self, message: str):
        """Print error message"""
        print(f"{Colors.RED}✗ {message}{Colors.RESET}")

    def print_info(self, message: str):
        """Print info message"""
        print(f"{Colors.BLUE}ℹ {message}{Colors.RESET}")

    def print_warning(self, message: str):
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠ {message}{Colors.RESET}")

    def print_menu(self):
        """Display main menu"""
        menu = f"""
{Colors.YELLOW}╔════════════════════════════════════════════════════════════════╗
║                         MAIN MENU                              ║
╠════════════════════════════════════════════════════════════════╣
║  1. Doctor Contact Search    - Find doctors with contact forms ║
║  2. Medical Board Lookup     - Verify licenses (51 states)     ║
║  3. Review Aggregation       - Search 5 review platforms       ║
║  4. Ethics Violation Report  - File medical board complaints   ║
║  5. Social Media Search      - Find professional profiles      ║
║  6. Comprehensive Search     - All features in one operation   ║
║  7. Batch Processing         - Process multiple queries        ║
║  8. Settings                 - Configure preferences           ║
║  9. Exit                     - Close application               ║
╚════════════════════════════════════════════════════════════════╝{Colors.RESET}
"""
        print(menu)

    def get_doctor_info(self) -> Dict:
        """Get doctor information from user"""
        print(f"\n{Colors.CYAN}Enter Doctor Information:{Colors.RESET}")

        doctor_name = input(f"{Colors.WHITE}Doctor's name: {Colors.RESET}").strip()
        city = input(f"{Colors.WHITE}City: {Colors.RESET}").strip()
        state = input(f"{Colors.WHITE}State (2-letter code): {Colors.RESET}").strip().upper()
        specialty = input(f"{Colors.WHITE}Specialty (optional): {Colors.RESET}").strip()

        return {
            "doctor_name": doctor_name,
            "city": city,
            "state": state,
            "specialty": specialty
        }

    def contact_search(self, doctor_info: Optional[Dict] = None):
        """Search for doctors with contact forms"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== DOCTOR CONTACT SEARCH ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]
        specialty = doctor_info["specialty"]

        # Build Google dork query
        query_parts = [
            '(group:doctor OR group:physician)',
            '(inurl:contact OR inurl:contact-us OR inurl:"contact us")',
            f'"{doctor_name}"',
            f'"{city}"',
            f'"{state}"'
        ]

        if specialty:
            query_parts.append(f'"{specialty}"')

        query = " ".join(query_parts)
        url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"

        self.search_results["contact_search"] = url

        print(f"\n{Colors.GREEN}Generated Search Query:{Colors.RESET}")
        print(f"{Colors.WHITE}{query}{Colors.RESET}\n")

        if self.config.get("auto_open_browser", True):
            self.print_info("Opening browser...")
            try:
                webbrowser.open(url)
                self.print_success("Browser opened successfully!")
            except Exception as e:
                self.print_error(f"Could not open browser: {e}")
                print(f"\n{Colors.YELLOW}Search URL:{Colors.RESET} {url}")
        else:
            print(f"\n{Colors.YELLOW}Search URL:{Colors.RESET} {url}")

        self.save_history({"type": "contact_search", **doctor_info, "url": url})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def medical_board_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up medical board verification"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== MEDICAL BOARD LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            state = input(f"{Colors.WHITE}Enter state (2-letter code) or 'ALL' for all states: {Colors.RESET}").strip().upper()
        else:
            state = doctor_info.get("state", "").upper()

        if state == "ALL" or not state:
            print(f"\n{Colors.CYAN}Medical Board Lookup URLs for All 51 Jurisdictions:{Colors.RESET}\n")
            for code, info in sorted(self.MEDICAL_BOARDS.items()):
                print(f"{Colors.YELLOW}{code} - {info['name']:<20}{Colors.RESET} {info['url']}")

            print(f"\n{Colors.INFO}Total: 51 jurisdictions{Colors.RESET}")
        elif state in self.MEDICAL_BOARDS:
            board_info = self.MEDICAL_BOARDS[state]
            print(f"\n{Colors.GREEN}Medical Board: {board_info['name']}{Colors.RESET}")
            print(f"{Colors.WHITE}URL: {board_info['url']}{Colors.RESET}\n")

            if self.config.get("auto_open_browser", True):
                self.print_info("Opening medical board website...")
                try:
                    webbrowser.open(board_info['url'])
                    self.print_success("Browser opened successfully!")
                except Exception as e:
                    self.print_error(f"Could not open browser: {e}")

            self.save_history({"type": "medical_board_lookup", "state": state, "url": board_info['url']})
        else:
            self.print_error(f"Invalid state code: {state}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def review_aggregation(self, doctor_info: Optional[Dict] = None):
        """Search multiple review platforms"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== REVIEW AGGREGATION ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Searching 5 review platforms for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.REVIEW_PLATFORMS.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<15}{Colors.RESET} {url}")

        self.search_results["review_aggregation"] = urls

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open all review sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "review_aggregation", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def ethics_violation_report(self, doctor_info: Optional[Dict] = None):
        """File ethics violation report"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== ETHICS VIOLATION REPORTING ==={Colors.RESET}\n")

        if not doctor_info:
            state = input(f"{Colors.WHITE}Enter state (2-letter code): {Colors.RESET}").strip().upper()
        else:
            state = doctor_info.get("state", "").upper()

        if state in self.MEDICAL_BOARDS:
            board_info = self.MEDICAL_BOARDS[state]
            print(f"\n{Colors.YELLOW}File a complaint with: {board_info['name']} Medical Board{Colors.RESET}")
            print(f"{Colors.WHITE}Board URL: {board_info['url']}{Colors.RESET}\n")

            self.print_warning("IMPORTANT: This will direct you to the medical board's website.")
            self.print_warning("Look for 'File a Complaint' or 'Report Misconduct' section.")

            proceed = input(f"\n{Colors.WHITE}Open medical board website? (y/n): {Colors.RESET}").strip().lower()
            if proceed == 'y':
                try:
                    webbrowser.open(board_info['url'])
                    self.print_success("Browser opened successfully!")
                except Exception as e:
                    self.print_error(f"Could not open browser: {e}")

                self.save_history({"type": "ethics_report", "state": state, "url": board_info['url']})
        else:
            self.print_error(f"Invalid state code: {state}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def social_media_search(self, doctor_info: Optional[Dict] = None):
        """Search social media platforms"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== SOCIAL MEDIA SEARCH ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        specialty = doctor_info.get("specialty", "physician")

        print(f"\n{Colors.CYAN}Searching 3 social platforms for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.SOCIAL_PLATFORMS.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                specialty=urllib.parse.quote(specialty)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<15}{Colors.RESET} {url}")

        self.search_results["social_media"] = urls

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open all social media sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "social_media_search", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def medicare_participation_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up Medicare participation and NPI information"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== MEDICARE PARTICIPATION LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        state = doctor_info.get("state", "")

        # Parse name into first and last for NPI Registry
        name_parts = doctor_name.replace("Dr.", "").replace("Dr", "").strip().split()
        first_name = name_parts[0] if len(name_parts) > 0 else ""
        last_name = name_parts[-1] if len(name_parts) > 1 else name_parts[0] if len(name_parts) > 0 else ""

        print(f"\n{Colors.CYAN}Checking Medicare participation for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.MEDICARE_LOOKUP.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                first_name=urllib.parse.quote(first_name),
                last_name=urllib.parse.quote(last_name),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["medicare_lookup"] = urls

        print(f"\n{Colors.INFO}ℹ These databases show:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Medicare enrollment status{Colors.RESET}")
        print(f"  • {Colors.WHITE}National Provider Identifier (NPI){Colors.RESET}")
        print(f"  • {Colors.WHITE}Practice locations and credentials{Colors.RESET}")
        print(f"  • {Colors.WHITE}Medicare patient ratings{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open Medicare lookup sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "medicare_lookup", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def publication_search(self, doctor_info: Optional[Dict] = None):
        """Search for doctor's publications and research"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== PUBLICATION SEARCH ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]

        print(f"\n{Colors.CYAN}Searching publications for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.PUBLICATION_LOOKUP.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<20}{Colors.RESET} {url}")

        self.search_results["publication_search"] = urls

        print(f"\n{Colors.INFO}ℹ Publication databases show:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Research papers and studies{Colors.RESET}")
        print(f"  • {Colors.WHITE}Citations and impact metrics{Colors.RESET}")
        print(f"  • {Colors.WHITE}Areas of medical expertise{Colors.RESET}")
        print(f"  • {Colors.WHITE}Academic contributions{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open publication databases? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "publication_search", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def specialty_verification(self, doctor_info: Optional[Dict] = None):
        """Verify board certifications and specialties"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== SPECIALTY BOARD VERIFICATION ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        specialty = doctor_info.get("specialty", "")

        print(f"\n{Colors.CYAN}Verifying board certifications for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.SPECIALTY_VERIFICATION.items():
            url = url_template
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["specialty_verification"] = urls

        print(f"\n{Colors.INFO}ℹ Board certification databases show:{Colors.RESET}")
        print(f"  • {Colors.WHITE}ABMS board certifications (24+ specialties){Colors.RESET}")
        print(f"  • {Colors.WHITE}AOA osteopathic certifications{Colors.RESET}")
        print(f"  • {Colors.WHITE}Certification status and expiration{Colors.RESET}")
        print(f"  • {Colors.WHITE}Subspecialty certifications{Colors.RESET}")

        if specialty:
            print(f"\n{Colors.CYAN}Note: Searching for specialty: {specialty}{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open certification databases? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "specialty_verification", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def education_training_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up education and training background"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== EDUCATION & TRAINING LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]

        print(f"\n{Colors.CYAN}Looking up education & training for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.EDUCATION_LOOKUP.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<20}{Colors.RESET} {url}")

        self.search_results["education_lookup"] = urls

        print(f"\n{Colors.INFO}ℹ Education databases show:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Medical school attended{Colors.RESET}")
        print(f"  • {Colors.WHITE}Residency and fellowship training{Colors.RESET}")
        print(f"  • {Colors.WHITE}Year of graduation{Colors.RESET}")
        print(f"  • {Colors.WHITE}Professional credentials{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open education databases? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "education_lookup", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def hospital_affiliations_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up hospital affiliations"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== HOSPITAL AFFILIATIONS LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Looking up hospital affiliations for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.HOSPITAL_AFFILIATIONS.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<35}{Colors.RESET} {url}")

        self.search_results["hospital_affiliations"] = urls

        print(f"\n{Colors.INFO}ℹ Hospital affiliation data shows:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Primary hospital affiliations{Colors.RESET}")
        print(f"  • {Colors.WHITE}Admitting privileges{Colors.RESET}")
        print(f"  • {Colors.WHITE}Practice locations{Colors.RESET}")
        print(f"  • {Colors.WHITE}Hospital quality ratings{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open hospital affiliation sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "hospital_affiliations", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def insurance_acceptance_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up accepted insurance providers"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== INSURANCE ACCEPTANCE LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Checking insurance acceptance for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.INSURANCE_ACCEPTANCE.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["insurance_acceptance"] = urls

        print(f"\n{Colors.INFO}ℹ Insurance information shows:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Accepted insurance plans{Colors.RESET}")
        print(f"  • {Colors.WHITE}Medicare/Medicaid participation{Colors.RESET}")
        print(f"  • {Colors.WHITE}In-network vs out-of-network{Colors.RESET}")
        print(f"  • {Colors.WHITE}Payment policies{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open insurance lookup sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "insurance_acceptance", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def language_support_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up languages spoken by doctor"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== LANGUAGE SUPPORT LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Looking up languages spoken by: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.LANGUAGE_SUPPORT.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["language_support"] = urls

        print(f"\n{Colors.INFO}ℹ Language information shows:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Languages spoken by doctor{Colors.RESET}")
        print(f"  • {Colors.WHITE}Interpreter services available{Colors.RESET}")
        print(f"  • {Colors.WHITE}Multilingual office staff{Colors.RESET}")
        print(f"  • {Colors.WHITE}Translation services{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open language lookup sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "language_support", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def telemedicine_options_lookup(self, doctor_info: Optional[Dict] = None):
        """Look up telemedicine/virtual visit options"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== TELEMEDICINE OPTIONS LOOKUP ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Checking telemedicine options for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.TELEMEDICINE_OPTIONS.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["telemedicine_options"] = urls

        print(f"\n{Colors.INFO}ℹ Telemedicine platforms show:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Virtual visit availability{Colors.RESET}")
        print(f"  • {Colors.WHITE}Video consultation platforms{Colors.RESET}")
        print(f"  • {Colors.WHITE}Online prescription services{Colors.RESET}")
        print(f"  • {Colors.WHITE}Remote patient monitoring{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open telemedicine sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "telemedicine_options", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def appointment_booking_links(self, doctor_info: Optional[Dict] = None):
        """Get appointment booking links"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== APPOINTMENT BOOKING LINKS ==={Colors.RESET}\n")

        if not doctor_info:
            doctor_info = self.get_doctor_info()

        doctor_name = doctor_info["doctor_name"]
        city = doctor_info["city"]
        state = doctor_info["state"]

        print(f"\n{Colors.CYAN}Finding appointment booking options for: {doctor_name}{Colors.RESET}\n")

        urls = []
        for platform, url_template in self.APPOINTMENT_BOOKING.items():
            url = url_template.format(
                doctor_name=urllib.parse.quote(doctor_name),
                city=urllib.parse.quote(city),
                state=urllib.parse.quote(state)
            )
            urls.append((platform, url))
            print(f"{Colors.YELLOW}{platform:<30}{Colors.RESET} {url}")

        self.search_results["appointment_booking"] = urls

        print(f"\n{Colors.INFO}ℹ Booking platforms provide:{Colors.RESET}")
        print(f"  • {Colors.WHITE}Online appointment scheduling{Colors.RESET}")
        print(f"  • {Colors.WHITE}Patient portal access{Colors.RESET}")
        print(f"  • {Colors.WHITE}Same-day appointment availability{Colors.RESET}")
        print(f"  • {Colors.WHITE}Waitlist notifications{Colors.RESET}")

        print(f"\n{Colors.YELLOW}Note: Real-time availability varies by practice.{Colors.RESET}")

        if self.config.get("auto_open_browser", True):
            open_choice = input(f"\n{Colors.WHITE}Open booking sites? (y/n): {Colors.RESET}").strip().lower()
            if open_choice == 'y':
                for platform, url in urls:
                    try:
                        webbrowser.open(url)
                        self.print_success(f"Opened {platform}")
                    except Exception as e:
                        self.print_error(f"Could not open {platform}: {e}")

        self.save_history({"type": "appointment_booking", **doctor_info, "urls": dict(urls)})

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def comprehensive_search(self):
        """Run all search features at once"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== COMPREHENSIVE SEARCH ==={Colors.RESET}\n")

        doctor_info = self.get_doctor_info()

        print(f"\n{Colors.CYAN}Running all search modules...{Colors.RESET}\n")

        # Temporarily disable auto-open to prevent browser overload
        original_setting = self.config.get("auto_open_browser", True)
        self.config["auto_open_browser"] = False

        # Run all searches
        self.print_info("1/14 - Running contact search...")
        self.contact_search(doctor_info)

        self.print_info("2/14 - Looking up medical board...")
        self.medical_board_lookup(doctor_info)

        self.print_info("3/14 - Checking Medicare participation...")
        self.medicare_participation_lookup(doctor_info)

        self.print_info("4/14 - Searching publications...")
        self.publication_search(doctor_info)

        self.print_info("5/14 - Verifying specialty certifications...")
        self.specialty_verification(doctor_info)

        self.print_info("6/14 - Looking up education & training...")
        self.education_training_lookup(doctor_info)

        self.print_info("7/14 - Checking hospital affiliations...")
        self.hospital_affiliations_lookup(doctor_info)

        self.print_info("8/14 - Looking up insurance acceptance...")
        self.insurance_acceptance_lookup(doctor_info)

        self.print_info("9/14 - Checking language support...")
        self.language_support_lookup(doctor_info)

        self.print_info("10/14 - Finding telemedicine options...")
        self.telemedicine_options_lookup(doctor_info)

        self.print_info("11/14 - Getting appointment booking links...")
        self.appointment_booking_links(doctor_info)

        self.print_info("12/14 - Aggregating reviews...")
        self.review_aggregation(doctor_info)

        self.print_info("13/14 - Searching social media...")
        self.social_media_search(doctor_info)

        self.print_info("14/14 - Complete!")

        # Restore original setting
        self.config["auto_open_browser"] = original_setting

        print(f"\n{Colors.GREEN}Comprehensive search completed!{Colors.RESET}")

        # Offer to export results
        export_choice = input(f"\n{Colors.WHITE}Export results? (y/n): {Colors.RESET}").strip().lower()
        if export_choice == 'y':
            self.export_results(doctor_info)

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def batch_processing(self):
        """Process multiple doctors at once"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== BATCH PROCESSING ==={Colors.RESET}\n")

        print(f"{Colors.CYAN}Enter doctors to search (one per line, format: Name, City, State, Specialty){Colors.RESET}")
        print(f"{Colors.YELLOW}Example: John Smith, Boston, MA, Cardiology{Colors.RESET}")
        print(f"{Colors.YELLOW}Enter a blank line when done:{Colors.RESET}\n")

        doctors = []
        while True:
            line = input(f"{Colors.WHITE}Doctor #{len(doctors)+1}: {Colors.RESET}").strip()
            if not line:
                break

            parts = [p.strip() for p in line.split(',')]
            if len(parts) >= 3:
                doctor_info = {
                    "doctor_name": parts[0],
                    "city": parts[1],
                    "state": parts[2],
                    "specialty": parts[3] if len(parts) > 3 else ""
                }
                doctors.append(doctor_info)
            else:
                self.print_error("Invalid format. Use: Name, City, State, Specialty")

        if not doctors:
            self.print_warning("No doctors entered.")
            input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            return

        print(f"\n{Colors.GREEN}Processing {len(doctors)} doctor(s)...{Colors.RESET}\n")

        # Temporarily disable auto-open
        original_setting = self.config.get("auto_open_browser", True)
        self.config["auto_open_browser"] = False

        for i, doctor_info in enumerate(doctors, 1):
            print(f"{Colors.CYAN}Processing {i}/{len(doctors)}: {doctor_info['doctor_name']}{Colors.RESET}")
            self.contact_search(doctor_info)

        # Restore original setting
        self.config["auto_open_browser"] = original_setting

        print(f"\n{Colors.GREEN}Batch processing completed!{Colors.RESET}")

        # Offer to export results
        export_choice = input(f"\n{Colors.WHITE}Export results? (y/n): {Colors.RESET}").strip().lower()
        if export_choice == 'y':
            self.export_batch_results(doctors)

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def settings_menu(self):
        """Configure application settings"""
        while True:
            self.clear_screen()
            self.print_logo()
            print(f"\n{Colors.BOLD}{Colors.GREEN}=== SETTINGS ==={Colors.RESET}\n")

            print(f"{Colors.YELLOW}Current Settings:{Colors.RESET}")
            print(f"  1. Auto-open browser: {Colors.GREEN if self.config['auto_open_browser'] else Colors.RED}{self.config['auto_open_browser']}{Colors.RESET}")
            print(f"  2. Export format: {Colors.CYAN}{self.config['export_format']}{Colors.RESET}")
            print(f"  3. Save history: {Colors.GREEN if self.config['save_history'] else Colors.RED}{self.config['save_history']}{Colors.RESET}")
            print(f"  4. Show progress: {Colors.GREEN if self.config['show_progress'] else Colors.RED}{self.config['show_progress']}{Colors.RESET}")
            print(f"\n{Colors.YELLOW}Actions:{Colors.RESET}")
            print(f"  5. View search history")
            print(f"  6. Clear search history")
            print(f"  7. Reset to defaults")
            print(f"  8. Back to main menu")

            choice = input(f"\n{Colors.WHITE}Select option (1-8): {Colors.RESET}").strip()

            if choice == '1':
                self.config['auto_open_browser'] = not self.config['auto_open_browser']
                self.save_config()
            elif choice == '2':
                print(f"\n{Colors.CYAN}Export formats: csv, json, html{Colors.RESET}")
                fmt = input(f"{Colors.WHITE}Enter format: {Colors.RESET}").strip().lower()
                if fmt in ['csv', 'json', 'html']:
                    self.config['export_format'] = fmt
                    self.save_config()
                else:
                    self.print_error("Invalid format")
                    input(f"{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif choice == '3':
                self.config['save_history'] = not self.config['save_history']
                self.save_config()
            elif choice == '4':
                self.config['show_progress'] = not self.config['show_progress']
                self.save_config()
            elif choice == '5':
                self.view_history()
            elif choice == '6':
                confirm = input(f"{Colors.RED}Clear all history? (y/n): {Colors.RESET}").strip().lower()
                if confirm == 'y':
                    self.history = []
                    try:
                        self.HISTORY_FILE.unlink()
                        self.print_success("History cleared!")
                    except:
                        pass
                    input(f"{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif choice == '7':
                confirm = input(f"{Colors.RED}Reset all settings? (y/n): {Colors.RESET}").strip().lower()
                if confirm == 'y':
                    self.config = {
                        "auto_open_browser": True,
                        "export_format": "html",
                        "save_history": True,
                        "show_progress": True,
                    }
                    self.save_config()
                    self.print_success("Settings reset to defaults!")
                    input(f"{Colors.CYAN}Press Enter to continue...{Colors.RESET}")
            elif choice == '8':
                break

    def view_history(self):
        """View search history"""
        self.clear_screen()
        self.print_logo()
        print(f"\n{Colors.BOLD}{Colors.GREEN}=== SEARCH HISTORY ==={Colors.RESET}\n")

        if not self.history:
            self.print_info("No search history found.")
        else:
            print(f"{Colors.CYAN}Last {min(20, len(self.history))} searches:{Colors.RESET}\n")
            for i, entry in enumerate(reversed(self.history[-20:]), 1):
                timestamp = entry.get('timestamp', 'Unknown')
                search_type = entry.get('type', 'Unknown')
                doctor_name = entry.get('doctor_name', 'N/A')
                print(f"{Colors.YELLOW}{i}. {Colors.RESET}{timestamp} - {search_type} - {doctor_name}")

        input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

    def export_results(self, doctor_info: Dict):
        """Export search results"""
        export_format = self.config.get('export_format', 'html')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doctordork_results_{timestamp}.{export_format}"

        try:
            if export_format == 'csv':
                self.export_csv(filename, doctor_info)
            elif export_format == 'json':
                self.export_json(filename, doctor_info)
            elif export_format == 'html':
                self.export_html(filename, doctor_info)

            self.print_success(f"Results exported to: {filename}")
        except Exception as e:
            self.print_error(f"Export failed: {e}")

    def export_csv(self, filename: str, doctor_info: Dict):
        """Export results to CSV"""
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['Category', 'Platform/Board', 'URL'])

            for category, data in self.search_results.items():
                if isinstance(data, list):
                    for platform, url in data:
                        writer.writerow([category, platform, url])
                else:
                    writer.writerow([category, 'Google Search', data])

    def export_json(self, filename: str, doctor_info: Dict):
        """Export results to JSON"""
        export_data = {
            "timestamp": datetime.now().isoformat(),
            "doctor_info": doctor_info,
            "results": self.search_results
        }

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=4)

    def export_html(self, filename: str, doctor_info: Dict):
        """Export results to HTML"""
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DoctorDork Search Results</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
        }}
        .header p {{
            font-size: 1.1em;
            opacity: 0.9;
        }}
        .info-section {{
            background: #f8f9fa;
            padding: 20px 30px;
            border-bottom: 2px solid #e9ecef;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .info-item {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }}
        .info-label {{
            font-size: 0.85em;
            color: #6c757d;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 5px;
        }}
        .info-value {{
            font-size: 1.1em;
            font-weight: 600;
            color: #333;
        }}
        .results-section {{
            padding: 30px;
        }}
        .category {{
            margin-bottom: 30px;
        }}
        .category-title {{
            font-size: 1.5em;
            color: #667eea;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e9ecef;
        }}
        .link-list {{
            list-style: none;
        }}
        .link-item {{
            background: #f8f9fa;
            margin: 10px 0;
            padding: 15px;
            border-radius: 8px;
            transition: all 0.3s ease;
        }}
        .link-item:hover {{
            background: #e9ecef;
            transform: translateX(5px);
        }}
        .platform-name {{
            font-weight: 600;
            color: #495057;
            margin-bottom: 5px;
        }}
        .link-url {{
            color: #667eea;
            text-decoration: none;
            word-break: break-all;
        }}
        .link-url:hover {{
            text-decoration: underline;
        }}
        .footer {{
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            font-size: 0.9em;
        }}
        .stats {{
            display: flex;
            justify-content: space-around;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .stat-item {{
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: bold;
        }}
        .stat-label {{
            font-size: 0.9em;
            opacity: 0.9;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🩺 DoctorDork Search Results</h1>
            <p>Comprehensive Medical Professional Research Report</p>
        </div>

        <div class="info-section">
            <div class="info-grid">
                <div class="info-item">
                    <div class="info-label">Doctor Name</div>
                    <div class="info-value">{doctor_info.get('doctor_name', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">City</div>
                    <div class="info-value">{doctor_info.get('city', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">State</div>
                    <div class="info-value">{doctor_info.get('state', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Specialty</div>
                    <div class="info-value">{doctor_info.get('specialty', 'N/A')}</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Generated</div>
                    <div class="info-value">{datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
                </div>
            </div>
        </div>

        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">{len(self.search_results)}</div>
                <div class="stat-label">Search Categories</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">{sum(len(v) if isinstance(v, list) else 1 for v in self.search_results.values())}</div>
                <div class="stat-label">Total Resources</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">51</div>
                <div class="stat-label">Medical Boards</div>
            </div>
        </div>

        <div class="results-section">
"""

        for category, data in self.search_results.items():
            category_name = category.replace('_', ' ').title()
            html_content += f"""
            <div class="category">
                <h2 class="category-title">{category_name}</h2>
                <ul class="link-list">
"""

            if isinstance(data, list):
                for platform, url in data:
                    html_content += f"""
                    <li class="link-item">
                        <div class="platform-name">{platform}</div>
                        <a href="{url}" class="link-url" target="_blank">{url}</a>
                    </li>
"""
            else:
                html_content += f"""
                    <li class="link-item">
                        <div class="platform-name">Google Search</div>
                        <a href="{data}" class="link-url" target="_blank">{data}</a>
                    </li>
"""

            html_content += """
                </ul>
            </div>
"""

        html_content += f"""
        </div>

        <div class="footer">
            <p><strong>DoctorDork v{self.VERSION}</strong> - Medical Professional Research Tool</p>
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
        </div>
    </div>
</body>
</html>
"""

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)

    def export_batch_results(self, doctors: List[Dict]):
        """Export batch processing results"""
        export_format = self.config.get('export_format', 'html')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"doctordork_batch_{timestamp}.{export_format}"

        try:
            if export_format == 'csv':
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=['doctor_name', 'city', 'state', 'specialty'])
                    writer.writeheader()
                    writer.writerows(doctors)
            elif export_format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump({"timestamp": datetime.now().isoformat(), "doctors": doctors}, f, indent=4)

            self.print_success(f"Batch results exported to: {filename}")
        except Exception as e:
            self.print_error(f"Export failed: {e}")

    def run(self):
        """Main application loop"""
        while True:
            self.clear_screen()
            self.print_logo()
            self.print_menu()

            choice = input(f"\n{Colors.WHITE}Select an option (1-9): {Colors.RESET}").strip()

            if choice == '1':
                self.contact_search()
            elif choice == '2':
                self.medical_board_lookup()
            elif choice == '3':
                self.review_aggregation()
            elif choice == '4':
                self.ethics_violation_report()
            elif choice == '5':
                self.social_media_search()
            elif choice == '6':
                self.comprehensive_search()
            elif choice == '7':
                self.batch_processing()
            elif choice == '8':
                self.settings_menu()
            elif choice == '9':
                self.clear_screen()
                print(f"\n{Colors.CYAN}Thank you for using DoctorDork!{Colors.RESET}")
                print(f"{Colors.GREEN}Goodbye!{Colors.RESET}\n")
                sys.exit(0)
            else:
                self.print_error("Invalid option. Please select 1-9.")
                input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")


def main():
    """Entry point for DoctorDork application"""
    try:
        app = DoctorDork()
        app.run()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Application interrupted by user.{Colors.RESET}")
        print(f"{Colors.GREEN}Goodbye!{Colors.RESET}\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}An unexpected error occurred: {e}{Colors.RESET}")
        sys.exit(1)


if __name__ == "__main__":
    main()
