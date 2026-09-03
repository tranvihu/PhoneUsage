import re

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Modify defaultConfig
new_config = """        const defaultConfig = {
            members: {
                bo: { 
                    name: 'Bố', totalTime: '20.5 giờ', favoriteDevice: 'Máy cá nhân', color: '#1e40af',
                    dob: '07/08/1989', age: 37, job: 'Công nhân viên chức', type: 'adult',
                    weights: { youtube: 15, facebook: 30, zalo: 20, web: 40, tiktok: 10, shopee: 0, call: 5, game: 0, duolingo: 0 }
                },
                me: { 
                    name: 'Mẹ', totalTime: '28.0 giờ', favoriteDevice: 'Máy cá nhân', color: '#7e22ce',
                    dob: '27/11/1989', age: 37, job: 'Công nhân viên chức', type: 'adult',
                    weights: { youtube: 15, facebook: 30, zalo: 20, web: 20, tiktok: 25, shopee: 35, call: 5, game: 0, duolingo: 0 }
                },
                child1: { 
                    name: 'Nhật Khánh', totalTime: '18.7 giờ', favoriteDevice: 'Máy cá nhân', color: '#047857',
                    dob: '17/04/2029', age: 6, className: '1C', school: 'Tiểu học Bình Hàn', teacher: 'Cô Luyên', type: 'child',
                    weights: { youtube: 40, game: 30, tiktok: 0, duolingo: 10, facebook: 0, zalo: 0, web: 0, shopee: 0, call: 10 }
                },
                child2: { 
                    name: 'Nhật Linh', totalTime: '20.8 giờ', favoriteDevice: 'Máy cá nhân', color: '#b91c1c',
                    dob: '08/10/2017', age: 9, className: '4C', school: 'Tiểu học Bình Hàn', teacher: 'Cô Yến', type: 'child',
                    weights: { youtube: 30, game: 10, tiktok: 0, duolingo: 10, facebook: 15, zalo: 15, web: 0, shopee: 0, call: 10 }
                }
            },
            platforms: [
                { id: 'youtube', name: 'YouTube', icon: '▶️' },
                { id: 'facebook', name: 'Facebook', icon: '📘' },
                { id: 'zalo', name: 'Zalo', icon: '💬' },
                { id: 'tiktok', name: 'TikTok', icon: '🎵' },
                { id: 'game', name: 'Trò chơi điện tử', icon: '🎮' },
                { id: 'duolingo', name: 'Duolingo', icon: '🦉' },
                { id: 'web', name: 'Trình duyệt Web', icon: '🌐' },
                { id: 'shopee', name: 'Shopee', icon: '🛍️' },
                { id: 'call', name: 'Cuộc gọi/Tin nhắn', icon: '📞' }
            ],
            violations: {
                bo: [ "Thức khuya đọc báo qua 23h đêm", "Sử dụng điện thoại trong bữa ăn", "Lướt TikTok âm lượng lớn", "Mua sắm online vượt chỉ tiêu", "Vừa sạc vừa dùng điện thoại" ],
                me: [ "Thức khuya đọc báo qua 23h đêm", "Sử dụng điện thoại trong bữa ăn", "Lướt TikTok âm lượng lớn", "Mua sắm online vượt chỉ tiêu", "Vừa sạc vừa dùng điện thoại" ],
                child2: [ "Gọi điện thoại buôn chuyện quá lâu", "Tranh giành đồ chơi với em trai", "Lén dùng TikTok của mẹ", "Vừa làm bài tập vừa nhắn tin", "Không chịu nhường em chơi cùng", "Để âm lượng quá lớn khi xem video", "Không chịu gội đầu" ],
                child1: [ "Xem YouTube lúc nghỉ trưa", "Đến giờ không chịu đi tắm", "Chơi game quá nhiều không nghỉ mắt", "Giành điện thoại của chị gái", "Nằm xem điện thoại sát mắt", "Vừa ăn cơm vừa đòi xem điện thoại", "Đánh chị gái" ]
            },
            penalties: [
                { violation: "Xem điện thoại > 3 giờ/ngày", penalty: "Úp mặt góc tường 30 phút. Thu máy 1 tuần." },
                { violation: "Lén lút dùng trong giờ nghỉ trưa", penalty: "Chịu 3 roi vào mông. Viết bản kiểm điểm 2 trang." },
                { violation: "Lười biếng, đến giờ không chịu đi tắm", penalty: "Cắt toàn bộ giờ giải trí. Quét nhà 3 ngày." },
                { violation: "Vượt ngưỡng 90% (Cảnh báo Đỏ)", penalty: "Chuyển hồ sơ sang Đồn CA. Gửi công văn hạ thi đua." }
            ],
            settings: {
                minViolationsPerDay: 2,
                maxViolationsPerDay: 3,
                numChildren: 2
            }
        };

        // Lấy cấu hình từ LocalStorage hoặc dùng mặc định
        let appConfig;
        try {
            appConfig = JSON.parse(localStorage.getItem('phoneUsageConfig')) || defaultConfig;
            
            // Xử lý migrate dữ liệu cũ nếu người dùng đã lưu khanh/linh trong localStorage
            if(appConfig.members.khanh) {
                appConfig.members.child1 = appConfig.members.khanh;
                delete appConfig.members.khanh;
            }
            if(appConfig.members.linh) {
                appConfig.members.child2 = appConfig.members.linh;
                delete appConfig.members.linh;
            }
            if(appConfig.violations.khanh) {
                appConfig.violations.child1 = appConfig.violations.khanh;
                delete appConfig.violations.khanh;
            }
            if(appConfig.violations.linh) {
                appConfig.violations.child2 = appConfig.violations.linh;
                delete appConfig.violations.linh;
            }
            if(appConfig.settings.numChildren === undefined) {
                appConfig.settings.numChildren = 2;
            }
        } catch (e) {
            appConfig = defaultConfig;
        }"""

html = re.sub(r'const defaultConfig = \{.*?} catch \(e\) \{\s*appConfig = defaultConfig;\s*\}', new_config, html, flags=re.DOTALL)

with open("D:\\CODE\\VS\\PhoneUsage\\index.html", "w", encoding="utf-8") as f:
    f.write(html)
