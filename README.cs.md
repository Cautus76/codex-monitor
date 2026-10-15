# Codex Monitor pro Wingpanel

[English](README.md) · **Čeština**

Neoficiální indikátor limitů Codexu pro elementary OS / Pantheon Wingpanel 8.
Zobrazuje zbývající pětihodinový a týdenní limit a čas do obnovení pětihodinového limitu:

```text
Codex 5h 63% (reset 3h 31m) | 7d 62%
```

Čísla jsou pouze ukázka. Procenta znamenají **zbývající**, nikoli spotřebovanou kapacitu. Obnova probíhá při spuštění, otevření nabídky a každých 60 sekund. Dotazy běží v pracovním vlákně a nepřekrývají se. Nejsou potřeba žádné balíčky pro pip.

Verze **1.0.0-rc.1** je veřejné předběžné vydání. Uživatel potvrdil funkčnost původní instalace na elementary OS 8.1. Překlad, živé dotazy a izolovaná instalace i odinstalace byly ověřeny s Wingpanelem 8.0.4 a Codex CLI 0.162.1. Načtení nové instalace v běžícím panelu a čistá instalace na jiném počítači zatím ověřeny nejsou. Projekt není oficiálně spojen s OpenAI ani elementary.

## Požadavky

- Linux s Pantheonem a Wingpanelem 8; nejde o aplikaci pro macOS, GNOME, KDE ani XFCE.
- Pro dodaný instalátor distribuce založená na Debianu/Ubuntu, `apt-get` a `sudo`.
- [Oficiální Codex CLI](https://developers.openai.com/codex/cli/) dostupný v terminálu přes `PATH`, přihlášený účtem ChatGPT s limity Codexu. Účet používající jen API klíč nemusí tyto limity poskytovat.
- Python 3.8+, Bash, překladač C, Vala, pkg-config a vývojové soubory GTK 3, GLib a Wingpanelu.
- Připojení k internetu pro aktuální limity.

Instalátor nabídne doplnění chybějících sestavovacích balíčků:

```bash
sudo apt-get install build-essential valac pkg-config libwingpanel-dev libgtk-3-dev libglib2.0-dev python3
```

Vývojové balíčky Wingpanelu musí být dostupné v repozitářích distribuce. Není potřeba API klíč ani další placený API přístup.

## Stažení a instalace

Stáhni a rozbal zdrojový archiv ze stránky [Releases](https://github.com/Cautus76/codex-monitor/releases), otevři terminál v rozbalené složce a spusť:

```bash
bash install.sh
```

Případně s nainstalovaným Gitem:

```bash
git clone https://github.com/Cautus76/codex-monitor.git
cd codex-monitor
bash install.sh
```

Spouštěj jako běžný uživatel pracovní plochy, **bez `sudo`**. Instalátor případně nabídne oficiální `codex login`, přeloží modul a před přepsáním nainstalovaných souborů ověří živé limity. O oprávnění správce požádá pro balíčky a systémový modul Wingpanelu. Potom se odhlas a znovu přihlas. Aktualizace probíhá stejným postupem.

Nainstalované soubory:

- `~/.local/share/codex-monitor/codex-limits.py`: skript skutečně používaný panelem.
- `~/.local/share/codex-monitor/codex-path`: místní cesta ke Codex CLI kvůli rozdílům mezi prostředím terminálu a panelu.
- `~/.local/share/codex-monitor/indicators-dir`: cesta k modulu pro odinstalaci.
- `~/.local/bin/codex-limits`: odkaz na terminálový příkaz.
- `$(pkg-config --variable=indicatorsdir wingpanel)/libcodex-monitor.so`: systémový modul.

Úprava stažených zdrojů sama neaktualizuje instalaci. Po aktualizaci nebo přesunutí Codex CLI znovu spusť instalátor.

## Použití v terminálu

```bash
~/.local/bin/codex-limits
~/.local/bin/codex-limits --short
~/.local/bin/codex-limits --json
~/.local/bin/codex-limits --lang en
~/.local/bin/codex-limits --version
```

Pokud máš `~/.local/bin` v PATH, stačí `codex-limits`. Skript podporuje češtinu a angličtinu; jazyk vybírá podle `LC_ALL`, `LC_MESSAGES`, potom `LANG`. JSON obsahuje zbývající procenta, unixové časy resetu a délku okna v minutách, pokud ji server poskytne. Podrobný text ukazuje reset v místním časovém pásmu. Odpočet v panelu zaokrouhluje nahoru na minuty a mění se při obnově dat, nikoli každou sekundu. Po uplynutí resetu ukazuje nulu, dokud server nevrátí nové údaje.

## Odinstalace

V rozbalené nebo naklonované složce projektu jako běžný uživatel:

```bash
bash uninstall.sh
```

Odhlas se a znovu přihlas. Odstraní se modul a pomocné soubory; Codex CLI, přihlášení a systémové sestavovací balíčky zůstanou zachovány. Systémový modul sdílí uživatelé počítače, jeho odebrání se proto týká všech jeho uživatelů.

## Řešení problémů

- **Nedostupný:** spusť `codex login status`, případně `codex login`. Ověř internet a `python3 codex-limits.py --short`. Chyba serveru, přihlášení, prázdné limity nebo vypršení 20sekundového limitu dotazu vyvolají stav nedostupnosti místo starých procent. Další pokus proběhne při obnově za 60 sekund nebo otevření nabídky.
- **Terminál funguje, panel ne:** vyzkoušej `python3 ~/.local/share/codex-monitor/codex-limits.py --short`. Spusť instalátor z terminálu, kde funguje `codex`, aby se obnovila uložená cesta. Také běhové prostředí CLI (například Node.js) musí fungovat v prostředí panelu.
- **Příkaz nenalezen:** použij `~/.local/bin/codex-limits` nebo přidej `~/.local/bin` do PATH svého shellu.
- **Indikátor se nezobrazil:** odhlas se a přihlas, zkontroluj `pkg-config --variable=indicatorsdir wingpanel` a chyby Wingpanelu v `journalctl --user -b`. Úspěšný překlad sám nepotvrzuje načtení v panelu.
- **Chybí hlavičky Wingpanelu:** doinstaluj `libwingpanel-dev` z repozitářů distribuce. Jiný panel tento modul nenačte.
- **Dva indikátory:** může být přítomen starý prototyp `libcodex-limits.so`. Instalátor upozorní, ale neodstraňuje ho. Odeber jej až po ověření, že jde skutečně o starý prototyp.
- **Změna rozhraní CLI:** aktualizuj Codex i projekt. Rozhraní app-server je experimentální. Při hlášení chyby uveď verzi OS, Wingpanelu a CLI; před přiložením logů odstraň soukromé údaje.

## Soukromí a fungování

Skript používá oficiální [protokol Codex app-server](https://developers.openai.com/codex/app-server): initialize, initialized a `account/rateLimits/read` přes místní stdio. Nespouští generování odpovědí a nečte přihlašovací soubory. Přihlášení i komunikaci s OpenAI obstarává Codex CLI. Monitor neukládá historii limitů ani přihlašovací údaje, nepřidává telemetrii a neotevírá síťový server. Nevypisuje obsah chybových odpovědí serveru. Codex může ukládat vlastní logy podle svého nastavení.

Do repozitáře nepatří přihlašovací soubory, místní cesty CLI ani skutečné výstupy účtu. Licence: [MIT](LICENSE). Změny: [CHANGELOG.md](CHANGELOG.md).

## Vývojové kontroly

```bash
python3 -m unittest discover -s tests -v
python3 -m py_compile codex-limits.py
bash -n install.sh uninstall.sh
python3 tests/install-smoke.py
python3 codex-limits.py --short
```

Izolovaný test vyžaduje sestavovací závislosti. Používá skutečný překlad Vala, dočasné složky HOME a pluginů, simulovaný Codex server a náhradu sudo. Nemění běžnou instalaci. Poslední příkaz je samostatná kontrola skutečného účtu a připojení; jeho výstup nezveřejňuj. Podrobnosti ověření a zbývající kontroly jsou v [VALIDATION.md](VALIDATION.md).
