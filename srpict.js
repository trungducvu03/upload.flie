// News Data
        const newsData = [
            {
                category: 'bongda',
                categoryName: 'BÓNG ĐÁ',
                title: 'Ronaldo ghi hat-trick trong trận đấu lịch sử',
                excerpt: 'Cristiano Ronaldo đã có màn trình diễn xuất sắc với 3 bàn thắng giúp đội nhà giành chiến thắng 4-1.',
                date: '02/02/2026',
                icon: '⚽'
            },
            {
                category: 'bongda',
                categoryName: 'BÓNG ĐÁ',
                title: 'Man City vô địch Premier League lần thứ 7',
                excerpt: 'Manchester City đã chính thức bảo vệ thành công ngôi vương Premier League sau chiến thắng 3-0.',
                date: '01/02/2026',
                icon: '⚽'
            },
            {
                category: 'tennis',
                categoryName: 'TENNIS',
                title: 'Nadal thắng trận mở màn Australian Open',
                excerpt: 'Rafael Nadal đã có chiến thắng thuyết phục 3-0 trong trận đấu đầu tiên tại Australian Open 2026.',
                date: '02/02/2026',
                icon: '🎾'
            },
            {
                category: 'basketball',
                categoryName: 'BÓNG RỔ',
                title: 'Lakers giành chiến thắng nghẹt thở trước Warriors',
                excerpt: 'LA Lakers đã có trận thắng kịch tính với tỷ số 118-116 trước Golden State Warriors.',
                date: '01/02/2026',
                icon: '🏀'
            },
            {
                category: 'motorsport',
                categoryName: 'ĐUA XE',
                title: 'Hamilton ký hợp đồng kỷ lục với Ferrari',
                excerpt: 'Lewis Hamilton chính thức gia nhập đội đua Ferrari với mức lương kỷ lục trong lịch sử F1.',
                date: '31/01/2026',
                icon: '🏎️'
            },
            {
                category: 'other',
                categoryName: 'THỂ THAO KHÁC',
                title: 'VĐV Việt Nam giành HCV Olympic',
                excerpt: 'Đoàn thể thao Việt Nam đã có thêm một huy chương vàng tại Olympic mùa đông 2026.',
                date: '02/02/2026',
                icon: '🏆'
            }
        ];

        // Advertisement Timer
        let adCounter = 5;
        const adOverlay = document.getElementById('adOverlay');
        const adTimer = document.getElementById('adTimer');
        const countdown = document.getElementById('countdown');

        const adInterval = setInterval(() => {
            adCounter--;
            adTimer.textContent = adCounter;
            countdown.textContent = adCounter;
            
            if (adCounter <= 0) {
                clearInterval(adInterval);
                adOverlay.classList.add('hidden');
            }
        }, 1000);

        // Display News
        function displayNews(category = 'all') {
            const newsGrid = document.getElementById('newsGrid');
            newsGrid.innerHTML = '';

            const filteredNews = category === 'all' 
                ? newsData 
                : newsData.filter(news => news.category === category);

            filteredNews.forEach(news => {
                const newsCard = `
                    <div class="news-card">
                        <div class="news-image">${news.icon}</div>
                        <div class="news-content">
                            <span class="news-category">${news.categoryName}</span>
                            <h3 class="news-title">${news.title}</h3>
                            <p class="news-excerpt">${news.excerpt}</p>
                            <p class="news-date">📅 ${news.date}</p>
                        </div>
                    </div>
                `;
                newsGrid.innerHTML += newsCard;
            });
        }

        // Initialize
        displayNews();

        // Navigation Functions
        function showHome() {
            displayNews('all');
        }

        function showCategory(category) {
            displayNews(category);
        }

        // Modal Functions
        function openLoginModal() {
            document.getElementById('loginModal').classList.add('active');
        }

        function closeLoginModal() {
            document.getElementById('loginModal').classList.remove('active');
        }

        function openRegisterModal() {
            document.getElementById('registerModal').classList.add('active');
        }

        function closeRegisterModal() {
            document.getElementById('registerModal').classList.remove('active');
        }

        function switchToRegister() {
            closeLoginModal();
            openRegisterModal();
        }

        function switchToLogin() {
            closeRegisterModal();
            openLoginModal();
        }

        // Close modal when clicking outside
        window.onclick = function(event) {
            const loginModal = document.getElementById('loginModal');
            const registerModal = document.getElementById('registerModal');
            
            if (event.target === loginModal) {
                closeLoginModal();
            }
            if (event.target === registerModal) {
                closeRegisterModal();
            }
        }

        // Form Handling
        function handleLogin(event) {
            event.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;

            // Simulate login
            console.log('Đăng nhập:', { email, password });
            
            alert('✅ Đăng nhập thành công!\nChào mừng bạn đến với Thể Thao 24/7');
            closeLoginModal();
            
            // Reset form
            event.target.reset();
        }

        function handleRegister(event) {
            event.preventDefault();
            
            const name = document.getElementById('registerName').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            const confirmPassword = document.getElementById('registerConfirmPassword').value;

            // Validate passwords match
            if (password !== confirmPassword) {
                alert('❌ Mật khẩu xác nhận không khớp!');
                return;
            }

            // Simulate registration
            console.log('Đăng ký:', { name, email, password });
            
            alert('✅ Đăng ký thành công!\nVui lòng đăng nhập để tiếp tục.');
            closeRegisterModal();
            openLoginModal();
            
            // Reset form
            event.target.reset();
        }

        // Add smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
            });
        });
