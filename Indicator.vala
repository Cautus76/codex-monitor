public class CodexMonitor.Indicator : Wingpanel.Indicator {
    private Gtk.Label? label;
    private Gtk.Box? popup;
    private Gtk.Label? details;
    private bool busy = false;
    private string current = "Codex …";
    private string status = "";

    public Indicator () {
        Object (code_name: "codex-monitor");
    }

    construct {
        visible = true;
        GLib.Timeout.add_seconds (60, () => {
            refresh ();
            return GLib.Source.CONTINUE;
        });
    }

    private bool is_czech () {
        string? lang = GLib.Environment.get_variable ("LC_ALL");
        if (lang == null || lang == "") lang = GLib.Environment.get_variable ("LANG");
        return lang != null && lang.down ().has_prefix ("cs");
    }

    private void refresh () {
        if (busy) return;
        busy = true;
        new GLib.Thread<void*> ("codex-monitor-refresh", () => {
            string output = "";
            string err = "";
            int exit_status = 0;
            bool ok = false;
            try {
                string path = GLib.Environment.get_home_dir () + "/.local/share/codex-monitor/codex-limits.py";
                string[] args = { "/usr/bin/python3", path, "--short" };
                GLib.Process.spawn_sync (null, args, null, GLib.SpawnFlags.SEARCH_PATH,
                                         null, out output, out err, out exit_status);
                ok = exit_status == 0 && output.strip () != "";
            } catch (GLib.SpawnError e) {
                err = e.message;
            }
            string result = ok ? output.strip () : (is_czech () ? "Codex: nedostupný" : "Codex: unavailable");
            string detail = ok ? (is_czech () ? "Aktualizováno ze serveru Codex. Obnova každých 60 s.\nPro podrobnosti: codex-limits" : "Live Codex server data. Refresh every 60s.\nFor details: codex-limits")
                               : (is_czech () ? "Nepodařilo se načíst limity.\n" : "Unable to retrieve limits.\n") + err.strip ();
            GLib.Idle.add (() => {
                current = result;
                status = detail;
                if (label != null) label.label = current;
                if (details != null) details.label = current + "\n" + status;
                busy = false;
                return GLib.Source.REMOVE;
            });
            return null;
        });
    }

    public override void opened () { refresh (); }
    public override void closed () { }

    public override Gtk.Widget get_display_widget () {
        if (label == null) {
            label = new Gtk.Label (current);
            label.margin_start = 8;
            label.margin_end = 8;
            label.show ();
            refresh ();
        }
        return label;
    }

    public override Gtk.Widget? get_widget () {
        if (popup == null) {
            popup = new Gtk.Box (Gtk.Orientation.VERTICAL, 8);
            popup.margin = 12;
            details = new Gtk.Label (current + "\n" + status);
            popup.pack_start (details, false, false, 0);
            popup.show_all ();
        }
        return popup;
    }
}

public Wingpanel.Indicator? get_indicator (GLib.Module module, Wingpanel.IndicatorManager.ServerType server_type) {
    if (server_type != Wingpanel.IndicatorManager.ServerType.SESSION) return null;
    return new CodexMonitor.Indicator ();
}
