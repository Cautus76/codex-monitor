# Codex Monitor pro Wingpanel

[English](README.md) · **Čeština**

Neoficiální ukazatel **aktuálních limitů Codexu** pro **elementary OS / Pantheon Wingpanel 8**. V horní liště zobrazuje zbývající pětihodinový a týdenní limit. Obsahuje i terminálový příkaz `codex-limits`. Obnovuje údaje každých 60 sekund a používá stávající přihlášení do Codex CLI.

**Stav: testovací verze; načítání pluginu je potřeba ověřit přímo v Pantheonu.** Projekt není oficiálně spojen s OpenAI ani elementary.

## Požadavky

- Pantheon / Wingpanel 8 (cílově 8.0.4)
- Codex CLI s `codex app-server` a přihlášením do ChatGPT (živý dotaz ověřen s Codex CLI 0.162.1)
- Python 3, Vala, GTK 3 a vývojové knihovny Wingpanelu
- Přístup k internetu

Není potřeba API klíč, `pipx` ani placené API.

## Instalace

```bash
bash install.sh
```

Instalátor ověří Codex a Wingpanel, nabídne chybějící závislosti přes `apt`, případně spustí oficiální přihlášení do Codexu. Modul přeloží a pouze při instalaci do systémové složky požádá o `sudo`. Nakonec se odhlas a znovu přihlas.

Podporujeme zatím distribuce postavené na Debianu/Ubuntu a prostředí Pantheon. Jiné grafické lišty (KDE, GNOME, XFCE) nejsou podporované.

## Ověření

```bash
codex login status
codex-limits
codex-limits --json
file build/libcodex-monitor.so
nm -D build/libcodex-monitor.so | grep get_indicator
```

Ukázkový výstup:

```text
Pětihodinový limit: 0% zbývá
  Obnovení: 15.10.2026 21:40
Týdenní limit: 68% zbývá
  Obnovení: 22.10.2026 11:09
```

Cílovou složku pluginů vypíše:

```bash
pkg-config --variable=indicatorsdir wingpanel
```

Samotný úspěšný překlad nezaručuje načtení do lišty. Při potížích zkontroluj protokoly `journalctl --user` a spuštění Wingpanelu.

## Odinstalace

```bash
bash uninstall.sh
```

Potom se odhlas a znovu přihlas. Skript neodstraňuje Codex CLI, jeho přihlášení ani systémové knihovny.

## Jazyk

- Angličtina je výchozí.
- Čeština se zapne automaticky při `LANG` nebo `LC_ALL` začínajícím na `cs`.

V terminálu lze jazyk zvolit ručně: `codex-limits --lang en` nebo `codex-limits --lang cs`.

## Technické poznámky

- Čte aktuální limity dotazem `account/rateLimits/read` přes `codex app-server --stdio`.
- Nečte ani nezveřejňuje obsah `~/.codex/auth.json`.
- Když není síť nebo přihlášení, hlásí nedostupnost místo zobrazování zastaralých procent.
- Rozhraní App Serveru je experimentální a může se změnit.
