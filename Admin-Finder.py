import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import collections
import os 


class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    ENDC = '\033[0m' 


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def extract_all_links(url):
    try:
        response = requests.get(url, timeout=10, allow_redirects=True)
        response.raise_for_status() 
        soup = BeautifulSoup(response.text, 'html.parser')
        
        all_links = set() 

        # Find all <a> tags
        for link_tag in soup.find_all('a', href=True):
            href = link_tag['href']
            full_url = urljoin(url, href)
            if full_url.startswith('http'): 
                all_links.add(full_url)
        

        for img_tag in soup.find_all('img', src=True):
            src = img_tag['src']
            full_url = urljoin(url, src)
            if full_url.startswith('http'):
                all_links.add(full_url)


        for link_tag in soup.find_all('link', href=True):
            href = link_tag['href']
            full_url = urljoin(url, href)
            if full_url.startswith('http'):
                all_links.add(full_url)

        
        for script_tag in soup.find_all('script', src=True):
            src = script_tag['src']
            full_url = urljoin(url, src)
            if full_url.startswith('http'):
                all_links.add(full_url)
        
        
        
        return sorted(list(all_links)) # Return as sorted list
    except requests.exceptions.RequestException as e:
        print(f"{Colors.RED}Error fetching {url}: {e}{Colors.ENDC}")
        return []


def find_admin_panel(url):
    admin_paths = [
    "/admin", "/login", "/wp-admin", "/administrator", "/dashboard",
    "/panel", "/cpanel", "/webadmin", "/adminpanel", "/controlpanel",
    "/user/login", "/wp-login.php", "/admin.php", "/backend", "/login.php",
    "/manage", "/secure", "/siteadmin", "/webmaster", "/cp", "/control",
    "/site/login", "/access", "/web/admin", "/admin/login", "/cp-login",
    "/admin-login", "/adminarea", "/webmaster/login", "/member/login",
    "/portal", "/staff", "/superadmin",
    
    # ------------------------------- وردپرس
    "/wp-admin", "/wp-login.php", "/wp-login", "/wp-admin.php",
    "/wp-admin/setup-config.php", "/wp-content/plugins", "/wp-includes",
    
    # ------------------------------- جوملا
    "/administrator/index.php", "/joomla/administrator", "/joomla/login",
    
    # ------------------------------- دروپال
    "/user/login", "/admin/config", "/drupal/login", "/drupal/admin",
    
    # ------------------------------- مجنتو
    "/adminhtml", "/admin123", "/magento/admin", "/magento/index.php/admin",
    
    # ------------------------------- اپن‌کارت / پرستاشاپ
    "/admin/", "/admin123/", "/admin1/", "/admin2/", "/adm/", "/shop/admin",
    "/prestashop/admin", "/prestashop/login", "/store/admin",
    
    # ------------------------------- لاراول / PHP / Node
    "/admin/login", "/admin/dashboard", "/admin-panel", "/panel",
    "/login.php", "/useradmin", "/dashboard/login", "/backend/login",
    "/auth/login", "/account/login", "/system-admin",
    
    # ------------------------------- phpMyAdmin و مشابه DB panels
    "/phpmyadmin", "/pma", "/sqladmin", "/mysql", "/dbadmin", "/database",
    
    # ------------------------------- هاستینگ‌ها و کنترل‌پنل‌ها
    "/cpanel", "/webmail", "/plesk", "/ispconfig", "/vesta", "/directadmin",
    "/serveradmin", "/whm", "/admincp/", "/sitecontrol",
    
    # ------------------------------- فریم‌ورک‌ها و CMSهای متفاوت
    "/typo3", "/typo3/index.php", "/silverstripe/admin", "/umbraco",
    "/craftcms/admin", "/october/backend", "/strapi/admin",
    
    # ------------------------------- اختصاصی / متداول در پروژه‌های سفارشی
    "/admin_area", "/admin_console", "/admin_interface", "/control",
    "/manage", "/panel_admin", "/config_admin", "/moderation",
    "/staff/login", "/login_admin", "/root", "/superuser/login",
    
    # ------------------------------- مسیرهای پشتی / تستی
    "/hidden_admin", "/secret", "/private", "/testadmin", "/beta/admin",
    "/oldadmin", "/backup/admin", "/userpanel", "/clientarea",
    
    # ------------------------------- مسیرهای خاص API یا SPA
    "/api/admin", "/api/dashboard", "/graphql", "/admin/api",
    "/backend/api/login", "/admin/auth", "/jwt/login",
    "admin1.php", "Login.htm", "administrators", "admin1.html",
    "admin2.php", "admin2.html", "yonetim.php", "yonetim.html",
    "yonetici.php", "yonetici.html", "ccms/", "ccms/login.php",
    "ccms/index.php", "maintenance/", "webmaster/", "adm/", 
    "configuration/", "configure/", "websvn/", "admin/", 
    "admin/account.php", "admin/account.html", "admin/index.php", 
    "admin/index.html", "admin/login.php", "admin/login.html", 
    "admin/home.php", "admin/controlpanel.html", "admin/controlpanel.php", 
    "admin.php", "admin.html", "admin/cp.php", "admin/cp.html", 
    "cp.php", "cp.html", "/wp-admin", "administrator/", 
    "administrator/index.html", "administrator/index.php", 
    "administrator/login.html", "administrator/login.php", 
    "administrator/account.html", "administrator/account.php", 
    "administrator.php", "administrator.html", "login.php", 
    "login.html", "modelsearch/login.php", "moderator.php", 
    "moderator.html", "moderator/login.php", "moderator/login.html", 
    "moderator/admin.php", "moderator/admin.html", "moderator/", 
    "account.php", "account.html", "controlpanel/", 
    "controlpanel.php", "controlpanel.html", "admincontrol.php", 
    "admincontrol.html", "adminpanel.php", "adminpanel.html", 
    "admin1.asp", "admin2.asp", "yonetim.asp", "yonetici.asp", 
    "admin/account.asp", "admin/index.asp", "admin/login.asp", 
    "admin/home.asp", "admin/controlpanel.asp", "admin.asp", 
    "admin/cp.asp", "cp.asp", "administrator/index.asp", 
    "administrator/login.asp", "administrator/account.asp", 
    "administrator.asp", "login.asp", "modelsearch/login.asp", 
    "moderator.asp", "moderator/login.asp", "moderator/admin.asp", 
    "account.asp", "controlpanel.asp", "admincontrol.asp", 
    "adminpanel.asp", "fileadmin/", "fileadmin.php", "fileadmin.asp", 
    "fileadmin.html", "administration/", "administration.php", 
    "administration.html", "sysadmin.php", "sysadmin.html", 
    "phpmyadmin/", "myadmin/", "sysadmin.asp", "sysadmin/", 
    "ur-admin.asp", "ur-admin.php", "ur-admin.html", "ur-admin/", 
    "Server.php", "Server.html", "Server.asp", "Server/", 
    "wp-admin/", "administr8.php", "administr8.html", 
    "administr8/", "administr8.asp", "webadmin/", "webadmin.php", 
    "webadmin.asp", "webadmin.html", "administratie/", "admins/", 
    "admins.php", "admins.asp", "admins.html", "administrivia/", 
    "Database_Administration/", "WebAdmin/", "useradmin/", 
    "sysadmins/", "admin1/", "system-administration/", 
    "administrators/", "pgadmin/", "directadmin/", "staradmin/", 
    "ServerAdministrator/", "SysAdmin/", "administer/", 
    "LiveUser_Admin/", "sys-admin/", "typo3/", "panel/", 
    "cpanel/", "cPanel/", "cpanel_file/", "platz_login/", 
    "rcLogin/", "blogindex/", "formslogin/", "autologin/", 
    "support_login/", "meta_login/", "manuallogin/", 
    "simpleLogin/", "loginflat/", "utility_login/", 
    "showlogin/", "memlogin/", "members/", "login-redirect/", 
    "sub-login/", "wp-login/", "login1/", "dir-login/", 
    "login_db/", "xlogin/", "smblogin/", "customer_login/", 
    "UserLogin/", "login-us/", "acct_login/", "admin_area/", 
    "bigadmin/", "project-admins/", "phppgadmin/", "pureadmin/", 
    "sql-admin/", "radmind/", "openvpnadmin/", "wizmysqladmin/", 
    "vadmind/", "ezsqliteadmin/", "hpwebjetadmin/", "newsadmin/", 
    "adminpro/", "Lotus_Domino_Admin/", "bbadmin/", 
    "vmailadmin/", "Indy_admin/", "ccp14admin/", "irc-macadmin/", 
    "banneradmin/", "sshadmin/", "phpldapadmin/", "macadmin/", 
    "administratoraccounts/", "admin4_account/", "admin4_colon/", 
    "radmind-1/", "Super-Admin/", "AdminTools/", "cmsadmin/", 
    "SysAdmin2/", "globes_admin/", "cadmins/", "phpSQLiteAdmin/", 
    "navSiteAdmin/", "server_admin_small/", "logo_sysadmin/", 
    "server/", "database_administration/", "power_user/", 
    "system_administration/", "ss_vms_admin_sm/", "admins", 
    "mail", "adm", "party", "admin", "administration", 
    "administrator", "administrators", "database", "admin.php", 
    "admin.asp", "administrator.php", "administrator.asp", 
    "administrators.asp", "login.php", "login.asp", 
    "logon.asp", "logon.php", "quanly.asp", "quanly.php", 
    "quantri.php", "quantri.asp", "quantriweb.asp", 
    "admin_index.asp", "admin_index.php", "password.asp", 
    "password.php", "dangnhap.asp", "dangnhap.php", "user.php", 
    "user.asp", "phpinfo.", "logs.", "log.", "adminwww", 
    "db.", "Readme.", "urllist.", "admin_file", "admin_files", 
    "admin_login", "cpg", "inc_lib", "inc_conf", "inc_config", 
    "lib_config", "login", "logon", "forum", "forums", 
    "diendan", "restricted", "forum1", "forum2", "user.asp", 
    "phpinfo.", "logs.", "log.", "adminwww", "db.", 
    "Readme.", "urllist.", "admin_file", "admin_files", 
    "admin_login", "cpg", "inc_lib", "inc_conf", "inc_config", 
    "lib_config", "login", "logon", "forum", "forums", 
    "diendan", "restricted", "forum1", "forum2", "forum3", 
    "diendan1", "diendan2", "foto", "diendan3", "php", 
    "phpbb", "awstats", "test", "img-sys", "cgi-sys", 
    "java-sys", "php-sys", "adserver", "login-sys", 
    "admin-sys", "community", "cgi-sys/mchat.", "demo", 
    "download", "temp", "tmp", "ibf", "ipb", "vbb", 
    "vbb1", "vbb2", "adminp", "vbb3", "README", "INSTALL", 
    "install", "docs", "document", "documents", "DOC", 
    "CHANGELOG", "guest", "phpMyAdmin", "phpbb1", "phpbb2", 
    "phpBB", "phpBB2", "PHPBB", "hackconkec", "12931293", 
    "secret", "root", "cgi-bin", "files", "scripts", 
    "nobody", "home", "manager", "manage", "live", 
    "exec", "livehelp", "livechat", "chat", "phplive", 
    "php.", "ko", "khong", "khongdungnua", "kodungnua", 
    "vut", "cuc", "cut", "db", "data", "site", 
    "cgi", "taolao", "class", "online", "common", 
    "shop", "shopadmin", "thesun", "news", "store", 
    "text", "source", "sources", "control", "controls", 
    "console", "cp", "admincp", "web", "modules", 
    "_admin", "_admin_file", "admin_site", "_login", 
    "pages", "access", "password", "pwd", "pass", 
    "user", "users", "_users", "admin_user", "admin_users", 
    "content", "cart", "carts", "cc", "paypal", 
    "cvv", "cvv2", "main1", "main", "webalizer", 
    "widgets", "acc", "accounts", "achive", "nhanvien", 
    "domain", "gallerry", "mysql", "order", "orders", 
    "4rum", "photo", "phpmyadmin", "share", "save", 
    "help", "admin_", "login_", "webmaster", "webmanager", 
    "quanly", "portal", "pub", "server", "seucre", 
    "security", "securelogin", "admin_security", "adm_sec", 
    "admin_sec", "setting", "support", "sysuser", "mgr", 
    "upload", "webcart", "webmail", "tools", "zorum", 
    "phorum", "log", "adminlogs", "adminlog", "logs", 
    "asp", "jsp", "js", "java", "javascript", 
    "javascripts", "auth", "bank", "buy", "cash", 
    "client", "code", "connect", "dbase", "dir", 
    "directory", "down", "up", "downloads", "fileadmin", 
    "hidden", "hompage", "htdocs", "www", "html", 
    "html1", "html2", "html3", "includes", "config", 
    "configuration", "info", "installation", "installinstall", 
    "bbs", "install1", "install2", "install3", "_install", 
    "install12", "install123", "lib", "library", 
    "logging", "members", "old", "pics", "public", 
    "purchase", "sale", "sales", "secured", "sell", 
    "services", "src", "staff", "super_admin", "sys", 
    "system", "testing", "tests", "upgrade", "update", 
    "webdata", "weblog", "weblogs", "webdb", "wwwboard", 
    "wwwforum", "wwwadmin", "wwwsite", "xxx", "xxx2", 
    "vn", "english", "en", "dos", "ddos", 
    "guestbook", "images", "image", "icon", "phanmem", 
    "cpanel", "customers", "modcp", "music", "global", 
    "join", "kernel", "readme", "software", "soft", 
    "hack", "hacke", "hackdicon", "hackweb", "Data", 
    "hacker", "hacking", "textfiles", "private", "tut", 
    "nhac", "nghenhac", "amnhac", "thethao", "cache", 
    "language", "learning", "learn", "elearning", "vi", 
    "rum", "tool", "win", "windows", "nix", 
    "slax", "su", "sub", "nano", "linux", 
    "myadmin", "siteadmin", "phpadmin", "phplogin", 
    "list", "lists", "money", "sex", "hentai", 
    "movie", "video", "error", "errorlog", "error_log", 
    "cfg", "blog", "classes", "counter", "extra", 
    "links", "pear", "tester", "women", "apche", 
    "iis", "generic", "netapp", "netscape", "base", 
    "basic", "advanced", "general", "bugs", "cfdocs", 
    "cgi-local", "custdata", "cutenews", "databases", 
    "datas", "dbs", "dc", "adc", "debug", 
    "dev", "developer", "development", "edit", "eventum", 
    "etc", "firewall", "quantri", "gb", "hostadmin", 
    "inc", "mailman", "mambo", "giaitri", "master", 
    "shell", "file", "msadm", "mp3", "avi", 
    "wmv", "wma", "myphpnuke", "phpnuke", "nuke", 
    "cool", "good", "bad", "phpwebsite", "pls", 
    "helpdesk", "postnuke", "power", "samples", "servlet", 
    "session", "shoutbox", "datadump", "dump", "dbdump", 
    "ssl", "supporter", "syshelp", "us", "vbulletin", 
    "viewimg", "webcalendar", "webtools", "xsql", 
    "accounting", "advwebadmin", "agent", "applicattion", 
    "applicattions", "backup", "beta", "ccbill", 
    "cert", "certificate", "doc-html", "dat", "exe", 
    "txt", "pdf", "books", "ebooks", "book", 
    "ftp", "homepage", "incoming", "information", 
    "phpmyreport", "report", "vitual", "vitualpath", 
    "internal", "intranet", "lan", "wan", "boxes", 
    "scr", "temporal", "template", "stat", "webstat", 
    "webadmin", "web_admin", "webmaster_logs", "filemgmt", 
    "admmgmt", "adm_mgmt", "dream", "diary", "essay", 
    "exp", "expl", "exploit", "exploits", "greeting", 
    "link", "sendmail", "start", "trash", "acp", 
    "block", "checkout", "css", "deny", "public_html", 
    "codes", "album", "phim", "love", "thugian", 
    "truyen", "funny", "fun", "fuck", "fuckyou", 
    "game", "games", "forums1", "forums2", "forums3", 
    "discuss", "discussion", "component", "baomat", 
    "2000", "2001", "2002", "2003", "2004", 
    "2005", "2006", "2007", "2008", "123456", 
    "revision", "papers", "cntt", "include", "123", 
    "12", "1234", "privates", "sock", "socks", 
    "host", "hosts", "domains", "back", "cnn", 
    "bd", "net", "inet", "internet", "check", 
    "checker", "tinh", "tinhyeu", "luubut", 
    "nhatki", "nhatky", "uocnguyen", "anh", "thuvien", 
    "cauhinh", "wish", "superadmin", "product", 
    "products", "hosting", "statics", "plugins", 
    "polls", "helps", "doc", "manual", "faqman", 
    "man", "manpage", "manpages", "faq", "affiliate", 
    "uploadfile", "uploadfiles", "trochoi", "funs", 
    "group", "admingroup", "listing", "misc", 
    "signup", "sql", "favorites", "friends", 
    "controlpanel", "membership", "tinnhan", "tintuc", 
    "thaoluan", "freeware", "adware", "bantin", 
    "squad", "email", "intro", "kho", "khonhac", 
    "nhakho", "releases", "banluan", "history", 
    "commercial", "repair", "card", "cards"
]   
   
    base_url = url.rstrip('/')

    found_panels = []
    print(f"\n{Colors.YELLOW}--- Initiating Admin Panel Scan for {base_url} ---{Colors.ENDC}")
    for path in admin_paths:
        full_url = f"{base_url}{path}"
        try:
            print(f"Testing: {full_url} ... ", end='')
            response = requests.head(full_url, allow_redirects=True, timeout=5) 
            
            if response.status_code == 200:
                print(f"{Colors.GREEN}TRUE (200 OK){Colors.ENDC}")
                found_panels.append(full_url)
            elif 300 <= response.status_code < 400: 
                print(f"{Colors.YELLOW}TRUE (Redirect {response.status_code}){Colors.ENDC}")
                found_panels.append(full_url)
            else:
                print(f"{Colors.RED}FALSE ({response.status_code}){Colors.ENDC}")
        except requests.exceptions.RequestException:
            print(f"{Colors.RED}FALSE (Connection Error){Colors.ENDC}")
            pass 
    
    if not found_panels:
        print(f"\n{Colors.BLUE}No common admin panels found for {base_url}.{Colors.ENDC}")
    return found_panels

# Web Crawler function
def web_crawler(start_url, max_depth=2):
    """
    Crawls a website to extract all internal links up to a specified depth.
    """
    queue = collections.deque([(start_url, 0)]) 
    visited_urls = set()
    internal_links_found = set()

    print(f"\n{Colors.YELLOW}--- Starting Web Crawl for {start_url} ---{Colors.ENDC}")
    print(f"Maximum Depth: {max_depth}")

    while queue:
        current_url, depth = queue.popleft()

        if current_url in visited_urls:
            continue
        if depth > max_depth:
            continue
        
        
        if urlparse(current_url).netloc != urlparse(start_url).netloc:
            continue

        visited_urls.add(current_url)
        internal_links_found.add(current_url)
        print(f"{Colors.CYAN}Crawling: {current_url} (Depth: {depth}){Colors.ENDC}")

        
        links_on_page = extract_all_links(current_url)
        for link in links_on_page:
            if link not in visited_urls:
                
                if urlparse(link).netloc == urlparse(start_url).netloc:
                    queue.append((link, depth + 1))
                else:
                    
                    internal_links_found.add(link) 

    print(f"\n{Colors.YELLOW}--- Web Crawl Finished ---{Colors.ENDC}")
    print(f"{Colors.BLUE}Total internal and external links found during crawl: {len(internal_links_found)}{Colors.ENDC}")
    
    print("\n")
    for link in sorted(list(internal_links_found)):
        print(f"{Colors.WHITE}- {link}{Colors.ENDC}")
    
    return sorted(list(internal_links_found)) 


def main():
    clear_screen()
    print(f"{Colors.CYAN}======================================={Colors.ENDC}")
    print(f"{Colors.CYAN}          {Colors.YELLOW}Web Reconnaissance Tool{Colors.ENDC}{Colors.CYAN}    {Colors.ENDC}")
    print(f"{Colors.CYAN}======================================={Colors.ENDC}")
    print(f"{Colors.BLUE}Telegram: @silent_mimi{Colors.ENDC}\n")

    target_url = input(f"{Colors.YELLOW}Enter the target URL (e.g., https://example.com): {Colors.ENDC}").strip()

    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        print(f"{Colors.RED}Invalid URL. Please include 'http://' or 'https://'. Exiting.{Colors.ENDC}")
        sys.exit(1)

    while True:
        print(f"\n{Colors.CYAN}--- Choose an Option ---{Colors.ENDC}")
        print(f"{Colors.GREEN}1. Extract all links (including images, CSS, JS, etc.) and crawl website{Colors.ENDC}")
        print(f"{Colors.GREEN}2. Find Admin Panel{Colors.ENDC}")
        print(f"{Colors.RED}3. Exit{Colors.ENDC}")

        choice = input(f"{Colors.YELLOW}Enter your choice (1, 2, or 3): {Colors.ENDC}").strip()

        if choice == '1':
            try:
                max_depth_input = int(input(f"{Colors.YELLOW}Enter maximum crawl depth (e.g., 2 for shallow, 5 for deeper): {Colors.ENDC}").strip())
                if max_depth_input < 0:
                    print(f"{Colors.RED}Depth cannot be negative. Setting to default (2).{Colors.ENDC}")
                    max_depth_input = 2
            except ValueError:
                print(f"{Colors.RED}Invalid depth. Setting to default (2).{Colors.ENDC}")
                max_depth_input = 2
            
            clear_screen()
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.CYAN}          {Colors.YELLOW}Web Reconnaissance Tool{Colors.ENDC}{Colors.CYAN}    {Colors.ENDC}")
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.BLUE}Telegram: @silent_mimi{Colors.ENDC}\n")
            print(f"{Colors.WHITE}Target URL: {target_url}{Colors.ENDC}")
            print(f"{Colors.WHITE}Max Depth: {max_depth_input}{Colors.ENDC}")
            
            web_crawler(target_url, max_depth=max_depth_input)
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}") 
            clear_screen()
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.CYAN}          {Colors.YELLOW}Web Reconnaissance Tool{Colors.ENDC}{Colors.CYAN}    {Colors.ENDC}")
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.BLUE}Telegram: @silent_mimi{Colors.ENDC}\n")


        elif choice == '2':
            clear_screen()
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.CYAN}          {Colors.YELLOW}Web Reconnaissance Tool{Colors.ENDC}{Colors.CYAN}    {Colors.ENDC}")
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.BLUE}Telegram: @silent_mimi{Colors.ENDC}\n")
            print(f"{Colors.WHITE}Target URL: {target_url}{Colors.ENDC}")
            
            found_panels = find_admin_panel(target_url)
            if found_panels:
                print(f"\n{Colors.GREEN}--- Found Admin Panel Links ---{Colors.ENDC}")
                for panel_url in found_panels:
                    print(f"{Colors.GREEN}+ {panel_url}{Colors.ENDC}")
            input(f"\n{Colors.YELLOW}Press Enter to continue...{Colors.ENDC}") 
            clear_screen()
            print(f"{Colors.CYAN}======================================={Colors.ENDC}")
            print(f"{Colors.CYAN}          {Colors.YELLOW}Web Reconnaissance Tool{Colors.ENDC}{Colors.CYAN}    {Colors.ENDC}")
            print(f"{Colors.BLUE}Telegram: @silent_mimi{Colors.ENDC}\n")

        elif choice == '3':
            print(f"{Colors.BLUE}Exiting the tool. Goodbye!{Colors.ENDC}")
            sys.exit(0)
        else:
            print(f"{Colors.RED}Invalid choice. Please enter 1, 2, or 3.{Colors.ENDC}")

if __name__ == "__main__":
    main()
