import re

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Replace the specific settings part of renderAdminForm
old_settings = """<h3 class="font-bold text-lg text-blue-900 border-b pb-2 mb-4">1. Cấu hình mức độ cảnh báo (Random)</h3>
                <div class="flex gap-4 items-center">
                    <label class="font-semibold text-sm">Số lỗi vi phạm mỗi ngày (Random):</label>
                    <input type="number" id="cfg_minV" class="border p-1 w-20 text-center font-bold" value="">
                    <span>đến</span>
                    <input type="number" id="cfg_maxV" class="border p-1 w-20 text-center font-bold" value="">
                </div>"""

new_settings = """<h3 class="font-bold text-lg text-blue-900 border-b pb-2 mb-4">1. Cấu hình hệ thống (Cảnh báo & Số lượng)</h3>
                <div class="flex flex-col gap-3">
                    <div class="flex gap-4 items-center">
                        <label class="font-semibold text-sm w-48">Số lỗi ngẫu nhiên / ngày:</label>
                        <input type="number" id="cfg_minV" class="border p-1 w-16 text-center font-bold" value="">
                        <span>đến</span>
                        <input type="number" id="cfg_maxV" class="border p-1 w-16 text-center font-bold" value="">
                    </div>
                    <div class="flex gap-4 items-center">
                        <label class="font-semibold text-sm w-48 text-red-700">SỐ LƯỢNG HỒ SƠ CON:</label>
                        <input type="number" id="cfg_numChildren" class="border p-1 w-16 text-center font-bold text-red-700" value="" min="1" max="10">
                        <span class="text-xs italic text-gray-500">(Sau khi lưu, hệ thống sẽ tự động cập nhật số lượng khung thông tin bên dưới)</span>
                    </div>
                </div>"""

html = html.replace(old_settings, new_settings)

# Replace the Save Button logic
old_save_start = "document.getElementById('saveConfigBtn').addEventListener('click', () => {"
old_save_end = "localStorage.setItem('phoneUsageConfig', JSON.stringify(appConfig));"

save_block_start = html.find(old_save_start)
save_block_end = html.find(old_save_end) + len(old_save_end)

if save_block_start != -1:
    new_save_logic = """document.getElementById('saveConfigBtn').addEventListener('click', () => {
            // 1. Settings
            appConfig.settings.minViolationsPerDay = parseInt(document.getElementById('cfg_minV').value) || 2;
            appConfig.settings.maxViolationsPerDay = parseInt(document.getElementById('cfg_maxV').value) || 3;
            let numChildren = parseInt(document.getElementById('cfg_numChildren').value) || 2;
            appConfig.settings.numChildren = numChildren;

            // 2. Members (Dynamic based on numChildren)
            const newMembers = { 
                bo: appConfig.members.bo, 
                me: appConfig.members.me 
            };
            
            // Cập nhật thông tin bố/mẹ nếu có trên form
            if (document.getElementById(cfg_mem_bo_name)) {
                newMembers.bo.name = document.getElementById(cfg_mem_bo_name).value;
                newMembers.bo.dob = document.getElementById(cfg_mem_bo_dob).value;
                newMembers.bo.job = document.getElementById(cfg_mem_bo_work).value;
            }
            if (document.getElementById(cfg_mem_me_name)) {
                newMembers.me.name = document.getElementById(cfg_mem_me_name).value;
                newMembers.me.dob = document.getElementById(cfg_mem_me_dob).value;
                newMembers.me.job = document.getElementById(cfg_mem_me_work).value;
            }

            // Xử lý các con
            for (let i = 1; i <= numChildren; i++) {
                let cKey = 'child' + i;
                if (document.getElementById(cfg_mem__name)) {
                    // Cập nhật từ form nếu đã tồn tại
                    newMembers[cKey] = {
                        ...appConfig.members[cKey],
                        name: document.getElementById(cfg_mem__name).value,
                        dob: document.getElementById(cfg_mem__dob).value,
                        className: document.getElementById(cfg_mem__work).value
                    };
                } else {
                    // Tạo mới hoàn toàn nếu chưa tồn tại trên form (do tăng số lượng)
                    const existingChild = appConfig.members[cKey];
                    if (existingChild) {
                         newMembers[cKey] = existingChild; // Có sẵn trong config nhưng chưa render lên form do bug
                    } else {
                         // Sinh profile mới
                         const defaultColors = ['#047857', '#b91c1c', '#0369a1', '#a21caf', '#164e63'];
                         newMembers[cKey] = {
                             name: 'Con ' + i, totalTime: '15.0 giờ', favoriteDevice: 'Máy cá nhân', 
                             color: defaultColors[(i-1) % 5], type: 'child',
                             dob: '01/01/2015', age: 10, className: '5A', school: 'Tiểu học', teacher: 'Cô A',
                             weights: { youtube: 30, game: 20, tiktok: 0, duolingo: 10, facebook: 0, zalo: 0, web: 0, shopee: 0, call: 10 }
                         };
                    }
                }
            }
            appConfig.members = newMembers;

            // 3. Violations (Chỉ lưu các key có trong newMembers)
            const newViolations = { bo: [], me: [] };
            for (const id in appConfig.members) {
                const ta = document.getElementById(cfg_viol_);
                if (ta) {
                    newViolations[id] = ta.value.split('\\n').map(s => s.trim()).filter(s => s !== '');
                } else if (appConfig.violations[id]) {
                    newViolations[id] = appConfig.violations[id];
                } else {
                    // Mặc định cho con mới
                    newViolations[id] = ["Chơi game quá thời gian quy định", "Không chịu làm bài tập", "Lười đi tắm"];
                }
            }
            appConfig.violations = newViolations;

            // 4. Penalties
            const penRows = document.querySelectorAll('.penalty-row');
            appConfig.penalties = [];
            penRows.forEach(row => {
                let v = row.querySelector('.p-viol').value.trim();
                let p = row.querySelector('.p-pen').value.trim();
                if (v && p) {
                    appConfig.penalties.push({ violation: v, penalty: p });
                }
            });

            // 5. Platforms
            const platRows = document.querySelectorAll('.platform-row');
            appConfig.platforms = [];
            platRows.forEach(row => {
                let icon = row.querySelector('.p-icon').value.trim();
                let id = row.querySelector('.p-id').value.trim();
                let name = row.querySelector('.p-name').value.trim();
                if (id && name) {
                    appConfig.platforms.push({ id: id, name: name, icon: icon });
                }
            });

            localStorage.setItem('phoneUsageConfig', JSON.stringify(appConfig));"""
            
    html = html[:save_block_start] + new_save_logic + html[save_block_end:]
else:
    print("Cannot find save block.")

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "w", encoding="utf-8") as f:
    f.write(html)
