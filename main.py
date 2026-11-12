"""Ciccio IVIM - avvia il programma in locale (127.0.0.1) e lo apre nel browser.
Nessun dato lascia il computer: la pagina e' autonoma e non fa richieste di rete."""
import sys, os, threading, webbrowser, http.server
import tkinter as tk

def res(name):
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, name)

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.split("?")[0] not in ("/", "/index.html"):
            self.send_error(404)
            return
        with open(res("ciccio_ivim.html"), "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def log_message(self, *a):
        pass

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
url = f"http://127.0.0.1:{srv.server_address[1]}/"
threading.Thread(target=srv.serve_forever, daemon=True).start()
webbrowser.open(url)

root = tk.Tk()
root.title("Ciccio IVIM")
root.geometry("340x140")
root.resizable(False, False)
tk.Label(root, text="Ciccio IVIM è in esecuzione.\nChiudi questa finestra per uscire.\nSolo ricerca, non per uso clinico.",
         pady=12).pack()
tk.Button(root, text="Riapri nel browser", command=lambda: webbrowser.open(url)).pack(pady=4)
tk.Button(root, text="Esci", command=root.destroy).pack()
root.mainloop()
srv.shutdown()
