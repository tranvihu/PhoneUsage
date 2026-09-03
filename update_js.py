import re

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. We need to extract the CẤU HÌNH DỮ LIỆU ĐỘNG block and move it BEFORE the DATA SETUP CHO BIỂU ĐỒ.
# The CẤU HÌNH DỮ LIỆU ĐỘNG block starts at "// --- CẤU HÌNH DỮ LIỆU ĐỘNG" and ends before "function initializeDynamicUI"

config_start = html.find("// --- CẤU HÌNH DỮ LIỆU ĐỘNG")
config_end = html.find("// Khởi tạo giao diện")

if config_start != -1 and config_end != -1:
    config_block = html[config_start:config_end]
    
    # Remove config block from its original position
    html = html[:config_start] + html[config_end:]
    
    # Find insertion point for config (right after Map initialization finishes)
    # The map block ends around         });
    # Let's insert it right before // --- DATA SETUP CHO BIỂU ĐỒ ---
    data_setup_start = html.find("// --- DATA SETUP CHO BIỂU ĐỒ ---")
    if data_setup_start != -1:
        html = html[:data_setup_start] + config_block + "\n        " + html[data_setup_start:]
    else:
        print("Could not find DATA SETUP CHO BIỂU ĐỒ")

# 2. Now replace the chart dataset generation
chart_data_start = html.find("// Màu sắc nghiêm túc")
chart_data_end = html.find("// --- UPDATE TODAY BUTTON ---")

if chart_data_start != -1 and chart_data_end != -1:
    new_chart_code = """// Dữ liệu biểu đồ động dựa trên appConfig
        const baseUserLabels = Object.values(appConfig.members).map(u => u.name);
        const hourlyLabels = ['8h-10h', '10h-12h', '12h-14h', '14h-16h', '16h-18h', '18h-20h', '20h-22h'];

        const originalDailyDatasets = Object.keys(appConfig.members).map(key => {
            const user = appConfig.members[key];
            const data = Array.from({length: 7}, () => parseFloat((Math.random() * 4 + 1).toFixed(1)));
            return {
                id: key, label: user.name, data: data, 
                borderColor: user.color || '#1e40af', backgroundColor: user.color || '#1e40af', 
                tension: 0.1, borderWidth: 2, pointRadius: 3
            };
        });

        const originalCrossDatasets = Object.keys(appConfig.members).map(key => {
            const user = appConfig.members[key];
            const data = Object.keys(appConfig.members).map(k => key === k ? 0 : parseFloat((Math.random() * 5).toFixed(1)));
            data.push(parseFloat((Math.random() * 5).toFixed(1))); // Cho "Ông/Bà"
            return {
                label: 'TB của ' + user.name,
                data: data,
                backgroundColor: user.color || '#1e40af'
            };
        });
        
        // Thêm Ông/Bà vào baseUserLabels cho Cross Chart
        const crossLabels = [...baseUserLabels, 'Ông/Bà'];

        const originalHourlyDatasets = Object.keys(appConfig.members).map(key => {
            const user = appConfig.members[key];
            const data = Array.from({length: 7}, () => parseFloat((Math.random() * 1.5).toFixed(1)));
            return {
                id: key, label: user.name, data: data, 
                borderColor: user.color || '#1e40af', backgroundColor: (user.color || '#1e40af') + '33', 
                fill: true, tension: 0.1, borderWidth: 1, pointRadius: 2
            };
        });

        // --- KHỞI TẠO BIỂU ĐỒ ---
        const commonOptions = {
            responsive: true, maintainAspectRatio: false,
            scales: {
                x: { grid: { color: '#e5e7eb' } },
                y: { grid: { color: '#e5e7eb' }, beginAtZero: true }
            }
        };

        const dailyChart = new Chart(document.getElementById('dailyUsageChart'), {
            type: 'line', data: { labels: daysLabels, datasets: JSON.parse(JSON.stringify(originalDailyDatasets)) },
            options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, max: 10 } } }
        });

        const crossChart = new Chart(document.getElementById('crossUsageChart'), {
            type: 'bar', data: { labels: crossLabels, datasets: JSON.parse(JSON.stringify(originalCrossDatasets)) },
            options: { ...commonOptions, scales: { x: { stacked: true }, y: { stacked: true } } }
        });

        const hourlyChart = new Chart(document.getElementById('hourlyUsageChart'), {
            type: 'line', data: { labels: hourlyLabels, datasets: JSON.parse(JSON.stringify(originalHourlyDatasets)) },
            options: { ...commonOptions, scales: { ...commonOptions.scales, y: { ...commonOptions.scales.y, max: 2.2 } } }
        });

        document.getElementById('userSelect').addEventListener('change', function(e) {
            const val = e.target.value;
            const display = document.getElementById('userInfoDisplay');
            const warningBox = document.getElementById('policeWarningBox');
            const reportContainer = document.getElementById('reportAndPenaltyContainer');
            const violationList = document.getElementById('violationList');
            
            if (val === 'all' || !val) {
                display.classList.add('hidden');
                warningBox.className = 'hidden';
                reportContainer.classList.add('hidden');
                
                dailyChart.data.datasets = JSON.parse(JSON.stringify(originalDailyDatasets));
                crossChart.data.labels = crossLabels;
                crossChart.data.datasets = JSON.parse(JSON.stringify(originalCrossDatasets));
                hourlyChart.data.datasets = JSON.parse(JSON.stringify(originalHourlyDatasets));
            } else {
                const user = appConfig.members[val];
                
                // Hiển thị báo cáo vi phạm random
                const randomViolations = getRandomViolations(val);
                reportContainer.classList.remove('hidden');
                violationList.innerHTML = randomViolations.map(v => <li>⚠️ </li>).join('');
                
                // Random app data
                const randomApps = getRandomApps(val);
                let appsHtml = '';
                randomApps.forEach(app => {
                    let textClass = app.percent === 0 ? "text-gray-400 line-through" : "text-gray-700";
                    let pctClass = app.percent === 0 ? "text-gray-400" : "text-blue-900";
                    appsHtml += <tr>
                                    <td class="border p-2 font-semibold  flex items-center gap-2">
                                        <span class="text-xl "></span> 
                                    </td>
                                    <td class="border p-2 font-bold text-center w-24 ">%</td>
                                 </tr>;
                });

                let extraInfoHtml = '';
                if (user.type === 'child') {
                    extraInfoHtml = 
                        <tr><th class="border p-2 bg-gray-100 text-left">Ngày tháng năm sinh:</th><td class="border p-2 font-semibold"></td></tr>
                        <tr><th class="border p-2 bg-gray-100 text-left">Đơn vị học tập:</th><td class="border p-2 font-bold text-gray-800">Lớp  - </td></tr>
                        <tr><th class="border p-2 bg-gray-100 text-left">Giáo viên chủ nhiệm:</th><td class="border p-2 font-bold text-blue-900"></td></tr>
                    ;
                } else {
                    extraInfoHtml = 
                        <tr><th class="border p-2 bg-gray-100 text-left">Năm sinh:</th><td class="border p-2 font-semibold"></td></tr>
                        <tr><th class="border p-2 bg-gray-100 text-left">Nghề nghiệp:</th><td class="border p-2 font-bold text-gray-800"></td></tr>
                    ;
                }

                display.innerHTML = 
                    <div class="bg-gray-200 p-2 font-bold text-gray-800 uppercase text-center border-b border-gray-400">
                        Hồ sơ viễn thông cá nhân
                    </div>
                    <div class="p-4 flex flex-col xl:flex-row gap-6">
                        <div class="w-full xl:w-1/2">
                            <table class="w-full text-sm border-collapse">
                                <tbody>
                                    <tr><th class="border p-2 bg-gray-100 text-left w-1/3">Định danh:</th><td class="border p-2 font-black  uppercase text-lg"></td></tr>
                                    
                                    <tr><th class="border p-2 bg-gray-100 text-left">Tổng thời lượng (7 ngày):</th><td class="border p-2 font-black text-red-600 text-lg"></td></tr>
                                    <tr><th class="border p-2 bg-gray-100 text-left">Thiết bị truy cập chính:</th><td class="border p-2 font-bold"></td></tr>
                                </tbody>
                            </table>
                        </div>
                        <div class="w-full xl:w-1/2">
                            <table class="w-full text-sm border-collapse">
                                <thead>
                                    <tr><th colspan="2" class="border p-2 bg-gray-100 text-center">Tỷ lệ truy cập các nền tảng kỹ thuật số</th></tr>
                                </thead>
                                <tbody>
                                    
                                </tbody>
                            </table>
                        </div>
                    </div>
                ;

                // Cảnh báo fake
                let progress = Math.floor(Math.random() * 15) + (user.type === 'child' ? 85 : 40);
                if (progress > 100) progress = 100;
                
                warningBox.classList.remove('hidden');
                if (progress >= 90) {
                    warningBox.className = "mt-4 bg-red-50 border-2 border-red-700 p-4 shadow-md relative animate-pulse";
                    warningBox.innerHTML = 
                        <div class="absolute top-0 right-0 bg-red-600 text-white font-bold text-xs px-2 py-1 uppercase">Cấp độ Đỏ</div>
                        <h3 class="text-red-800 font-black uppercase border-b-2 border-red-300 pb-2 mb-3 flex items-center text-lg">
                            <span class="mr-2 text-2xl">🚨</span> CẢNH BÁO GIÁM SÁT ĐẶC BIỆT
                        </h3>
                        <div class="flex flex-col gap-2">
                            <div class="flex justify-between font-bold text-red-900">
                                <span>Mức độ rủi ro:</span>
                                <span class="text-xl">%</span>
                            </div>
                            <div class="w-full bg-gray-300 h-6 border border-red-800 relative overflow-hidden">
                                <div class="bg-red-600 h-full flex items-center justify-end pr-2 transition-all duration-1000" style="width: %">
                                    <span class="text-white text-xs">⚠️</span>
                                </div>
                            </div>
                            <p class="text-sm font-bold text-red-700 mt-2 uppercase">YÊU CẦU CÁ NHÂN NGỪNG SỬ DỤNG THIẾT BỊ NGAY LẬP TỨC. XE ĐẶC CHỦNG ĐANG TRÊN ĐƯỜNG DI CHUYỂN!</p>
                        </div>
                    ;
                } else {
                    warningBox.className = "mt-4 bg-yellow-50 border-2 border-yellow-600 p-4 shadow-md relative";
                    warningBox.innerHTML = 
                        <h3 class="text-yellow-700 font-black uppercase border-b-2 border-yellow-200 pb-2 mb-3 flex items-center text-lg">
                            <span class="mr-2 text-2xl">⚠️</span> CẢNH BÁO GIÁM SÁT
                        </h3>
                        <div class="flex flex-col gap-2">
                            <div class="flex justify-between font-bold text-yellow-900">
                                <span>Mức độ rủi ro:</span>
                                <span class="text-xl">%</span>
                            </div>
                            <div class="w-full bg-gray-300 h-6 border border-yellow-800 relative overflow-hidden">
                                <div class="bg-yellow-500 h-full transition-all duration-1000" style="width: %"></div>
                            </div>
                            <p class="text-sm font-bold text-yellow-800 mt-2 uppercase">Chỉ số nằm trong ngưỡng an toàn. Tiếp tục duy trì.</p>
                        </div>
                    ;
                }

                // --- ĐỒNG BỘ 3 BIỂU ĐỒ ---
                dailyChart.data.datasets = JSON.parse(JSON.stringify(originalDailyDatasets)).filter(ds => ds.id === val);
                
                crossChart.data.labels = [user.name];
                let index = Object.keys(appConfig.members).indexOf(val);
                crossChart.data.datasets = JSON.parse(JSON.stringify(originalCrossDatasets)).map(ds => ({ ...ds, data: [ds.data[index]] }));

                hourlyChart.data.datasets = JSON.parse(JSON.stringify(originalHourlyDatasets)).filter(ds => ds.id === val);
            }
            
            dailyChart.update();
            crossChart.update();
            hourlyChart.update();
        });

        // """

    html = html[:chart_data_start] + new_chart_code + html[chart_data_end:]
    print("Replaced chart logic.")
else:
    print("Could not find chart logic block.")

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "w", encoding="utf-8") as f:
    f.write(html)
print("Done writing.")
