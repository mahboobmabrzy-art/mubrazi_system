from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="المبرزي للبصريات والسمعيات", docs_url=None, redoc_url=None)

APPS_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbyoFAzEGabJye2fNjKN7rvU_tIO-Q7jmIIN9Gh3_mTti6IY1banuYuPqaT-ShLaOQAa7A/exec"

def init_db():
    conn = sqlite3.connect("mubrazi.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS invoices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            clientName TEXT,
            phone TEXT,
            totalAmount REAL,
            paidAmount REAL,
            remainingAmount REAL
        )
    """)
    conn.commit()
    conn.close()

init_db()

class FullInvoice(BaseModel):
    clientName: str = ""
    invoiceNo: str = ""
    phone: str = ""
    date: str = ""
    branch: str = "الفرع الرئيسي"
    totalAmount: float = 0.0
    paidAmount: float = 0.0
    category: str = ""
    type: str = ""
    color: str = ""
    r_sph: str = ""
    r_cyl: str = ""
    r_axis: str = ""
    r_add: str = ""
    l_sph: str = ""
    l_cyl: str = ""
    l_axis: str = ""
    l_add: str = ""
    ipd: str = ""

@app.post("/api/save_local")
async def save_local(payload: FullInvoice):
    data_dict = payload.dict()
    try:
        conn = sqlite3.connect("mubrazi.db")
        cursor = conn.cursor()
        rem = data_dict["totalAmount"] - data_dict["paidAmount"]
        cursor.execute("INSERT INTO invoices (clientName, phone, totalAmount, paidAmount, remainingAmount) VALUES (?, ?, ?, ?, ?)",
                       (data_dict["clientName"], data_dict["phone"], data_dict["totalAmount"], data_dict["paidAmount"], rem))
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/", response_class=HTMLResponse)
async def read_root():
    headers = {
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
        "Expires": "0"
    }
    content = f"""
    <!DOCTYPE html>
    <html lang="ar" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>المبرزي للبصريات والسمعيات</title>
        <style>
            body {{ font-family: system-ui, sans-serif; padding: 10px; background: #f4f6f9; direction: rtl; }}
            .card {{ background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); margin-bottom: 15px; }}
            h2 {{ color: #1e3a8a; text-align: center; margin-top: 5px; }}
            .grid-2 {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
            .grid-3 {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 8px; }}
            .form-group {{ margin-bottom: 8px; }}
            label {{ display: block; font-size: 0.85rem; font-weight: bold; margin-bottom: 2px; }}
            input {{ width: 100%; padding: 8px; border: 1px solid #ccc; border-radius: 4px; box-sizing: border-box; text-align: center; font-size: 0.95rem; }}
            table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
            th, td {{ border: 1px solid #000; padding: 6px; text-align: center; font-size: 0.9rem; }}
            th {{ background: #e2e8f0; }}
            .optics-input {{ width: 100%; min-width: 65px; padding: 10px 4px; font-size: 1.1rem; font-weight: bold; text-align: center; color: #1e3a8a; }}
            button {{ width: 100%; padding: 14px; background: #16a34a; color: white; border: none; border-radius: 5px; font-weight: bold; font-size: 1.1rem; cursor: pointer; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>المبرزي للبصريات والسمعيات</h2>
            <form id="opticsForm">
                <div class="form-group">
                    <label>الاسم:</label>
                    <input type="text" id="clientName" required placeholder="اسم العميل">
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label>رقم الفاتورة:</label>
                        <input type="text" id="invoiceNo" placeholder="تلقائي">
                    </div>
                    <div class="form-group">
                        <label>الجوال:</label>
                        <input type="tel" id="phone" placeholder="رقم الهاتف">
                    </div>
                </div>
                <div class="form-group">
                    <label>التاريخ:</label>
                    <input type="date" id="date">
                </div>
                <div class="grid-3">
                    <div class="form-group">
                        <label>المبلغ الكلي:</label>
                        <input type="number" step="0.01" id="totalAmount" oninput="calcRemaining()" placeholder="0.00">
                    </div>
                    <div class="form-group">
                        <label>الواصل:</label>
                        <input type="number" step="0.01" id="paidAmount" oninput="calcRemaining()" placeholder="0.00">
                    </div>
                    <div class="form-group">
                        <label>الباقي:</label>
                        <input type="number" step="0.01" id="remainingAmount" readonly style="background:#e9ecef;">
                    </div>
                </div>

                <table>
                    <thead>
                        <tr>
                            <th></th>
                            <th>SPH</th>
                            <th>CYL</th>
                            <th>AXIS</th>
                            <th>ADD</th>
                            <th>IPD</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <th>R</th>
                            <td><input type="text" id="r_sph" class="optics-input" placeholder="-1.00"></td>
                            <td><input type="text" id="r_cyl" class="optics-input" placeholder="-0.50"></td>
                            <td><input type="text" id="r_axis" class="optics-input" placeholder="180"></td>
                            <td><input type="text" id="r_add" class="optics-input" placeholder="+1.50"></td>
                            <td rowspan="2" style="vertical-align: middle;"><input type="text" id="ipd" class="optics-input" placeholder="64"></td>
                        </tr>
                        <tr>
                            <th>L</th>
                            <td><input type="text" id="l_sph" class="optics-input" placeholder="-1.00"></td>
                            <td><input type="text" id="l_cyl" class="optics-input" placeholder="-0.50"></td>
                            <td><input type="text" id="l_axis" class="optics-input" placeholder="175"></td>
                            <td><input type="text" id="l_add" class="optics-input" placeholder="+1.50"></td>
                        </tr>
                    </tbody>
                </table>

                <div class="grid-2">
                    <div class="form-group">
                        <label>الصنف:</label>
                        <input type="text" id="category" placeholder="اسم الصنف">
                    </div>
                    <div class="form-group">
                        <label>النوع:</label>
                        <input type="text" id="type" placeholder="النوع">
                    </div>
                </div>
                <div class="form-group">
                    <label>اللون:</label>
                    <input type="text" id="color" placeholder="اللون">
                </div>

                <button type="submit">حفظ وإرسال إلى Google Sheets</button>
            </form>
        </div>

        <script>
            function calcRemaining() {{
                const tot = parseFloat(document.getElementById('totalAmount').value) || 0;
                const paid = parseFloat(document.getElementById('paidAmount').value) || 0;
                document.getElementById('remainingAmount').value = (tot - paid).toFixed(2);
            }}

            document.getElementById('opticsForm').addEventListener('submit', async (e) => {{
                e.preventDefault();
                const payload = {{
                    clientName: document.getElementById('clientName').value,
                    invoiceNo: document.getElementById('invoiceNo').value,
                    phone: document.getElementById('phone').value,
                    date: document.getElementById('date').value,
                    totalAmount: parseFloat(document.getElementById('totalAmount').value) || 0,
                    paidAmount: parseFloat(document.getElementById('paidAmount').value) || 0,
                    category: document.getElementById('category').value,
                    type: document.getElementById('type').value,
                    color: document.getElementById('color').value,
                    r_sph: document.getElementById('r_sph').value,
                    r_cyl: document.getElementById('r_cyl').value,
                    r_axis: document.getElementById('r_axis').value,
                    r_add: document.getElementById('r_add').value,
                    l_sph: document.getElementById('l_sph').value,
                    l_cyl: document.getElementById('l_cyl').value,
                    l_axis: document.getElementById('l_axis').value,
                    l_add: document.getElementById('l_add').value,
                    ipd: document.getElementById('ipd').value
                }};

                fetch('/api/save_local', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(payload)
                }});

                try {{
                    await fetch('{APPS_SCRIPT_URL}', {{
                        method: 'POST',
                        mode: 'no-cors',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload)
                    }});
                    alert('تم الحفظ والمزامنة المباشرة بنجاح مع جدول Google Sheets!');
                    document.getElementById('opticsForm').reset();
                }} catch(err) {{
                    alert('حدث خطأ أثناء المزامنة: ' + err);
                }}
            }});
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=content, headers=headers)
