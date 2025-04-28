// 主要功能的JavaScript文件
$(document).ready(function() {
    // 设置默认偏好
    setupDefaultPreferences();
    
    // 检查登录状态
    if (checkLoginStatus()) {
        // 已登录，加载内容
        loadContent();
    } else {
        // 未登录，也加载最新播客
        loadLatestPodcasts();
        // 加载分类
        loadCategories();
    }
    
    // 初始化轮播图
    initSlider();
    
    // 创建偏好设置弹窗
    createPreferenceModal();
    
    // 绑定事件
    bindEvents();
});

// 设置默认偏好
function setupDefaultPreferences() {
    window.defaultPreferences = ['Technology', 'Music'];
}

// 加载内容
function loadContent() {
    // 获取当前用户
    const currentUser = JSON.parse(localStorage.getItem('currentUser'));
    
    // 加载最新播客
    loadLatestPodcasts();
    
    // 加载分类
    loadCategories();
}

// 获取当前偏好设置
function getCurrentPreferences() {
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        return user.preferences || window.defaultPreferences;
    }
    return window.defaultPreferences;
}

// 加载最新播客
function loadLatestPodcasts(selectedCategory = null) {
    // 从模拟数据中获取播客
    let podcasts = [...mockData.podcasts];
    
    // 获取用户偏好
    const preferences = getCurrentPreferences();
    
    // 如果选择了特定分类，按分类筛选
    if (selectedCategory) {
        podcasts = podcasts.filter(podcast => podcast.category === selectedCategory);
    } 
    // 否则根据偏好筛选
    else if (preferences && preferences.length > 0) {
        podcasts = podcasts.filter(podcast => preferences.includes(podcast.category));
    }
    
    // 如果筛选后没有任何播客，则显示所有播客
    if (podcasts.length === 0) {
        podcasts = [...mockData.podcasts];
    }
    
    // 按日期排序
    podcasts.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // 只取前6个，但至少显示1个
    const latestPodcasts = podcasts.slice(0, Math.min(6, podcasts.length));
    
    // 清空容器
    $('#latest-podcasts').empty();
    
    // 根据播客数量添加不同的类名
    $('#latest-podcasts').removeClass('single-podcast two-podcasts');
    if (latestPodcasts.length === 1) {
        $('#latest-podcasts').addClass('single-podcast');
    } else if (latestPodcasts.length === 2) {
        $('#latest-podcasts').addClass('two-podcasts');
    }
    
    if (latestPodcasts.length === 0) {
        // 如果没有博客，显示提示信息
        $('#latest-podcasts').html('<div class="no-podcasts">No podcasts found</div>');
        return;
    }
    
    // 添加播客到容器
    latestPodcasts.forEach(podcast => {
        const podcastHtml = `
            <div class="podcast-item" data-id="${podcast.id}">
                <div class="podcast-cover">
                    <img src="${podcast.cover}" alt="${podcast.title}">
                </div>
                <div class="podcast-info">
                    <h3>${podcast.title}</h3>
                    <p>${podcast.author}</p>
                    <div class="podcast-meta">
                        <span class="podcast-category">${podcast.category}</span>
                        <span class="podcast-duration">${podcast.duration}</span>
                        <span class="podcast-views">${podcast.views} Times</span>
                    </div>
                </div>
            </div>
        `;
        
        $('#latest-podcasts').append(podcastHtml);
    });
    
    // 添加点击事件
    $('.podcast-item').click(function() {
        const podcastId = $(this).data('id');
        window.location.href = `podcast.html?id=${podcastId}`;
    });
}

// 加载分类
function loadCategories() {
    // 获取所有分类
    const categories = [...new Set(mockData.podcasts.map(podcast => podcast.category))];
    
    // 清空容器
    $('#category-list').empty();
    
    // 添加"全部"分类
    $('#category-list').append(`<li><a href="#" class="active" data-category="all">All</a></li>`);
    
    // 添加分类到容器
    categories.forEach(category => {
        $('#category-list').append(`<li><a href="#" data-category="${category}">${category}</a></li>`);
    });
    
    // 添加点击事件
    $('.category-list li a').click(function(e) {
        e.preventDefault();
        
        // 移除所有活动状态
        $('.category-list li a').removeClass('active');
        
        // 添加当前项的活动状态
        $(this).addClass('active');
        
        // 获取分类
        const category = $(this).data('category');
        
        // 根据分类加载播客
        if (category === 'all') {
            loadLatestPodcasts();
        } else {
            loadLatestPodcasts(category);
        }
    });
}

// 初始化轮播图
function initSlider() {
    let currentSlide = 0;
    const slides = $('.slide');
    const dots = $('.dot');
    const totalSlides = slides.length;
    let slideInterval;
    
    // 显示指定幻灯片
    function showSlide(index) {
        slides.removeClass('active');
        $(slides[index]).addClass('active');
        
        dots.removeClass('active');
        $(dots[index]).addClass('active');
        
        currentSlide = index;
    }
    
    // 下一张幻灯片
    function nextSlide() {
        let nextIndex = currentSlide + 1;
        if (nextIndex >= totalSlides) {
            nextIndex = 0;
        }
        showSlide(nextIndex);
    }
    
    // 上一张幻灯片
    function prevSlide() {
        let prevIndex = currentSlide - 1;
        if (prevIndex < 0) {
            prevIndex = totalSlides - 1;
        }
        showSlide(prevIndex);
    }
    
    // 点击下一个按钮
    $('.next-btn').click(function() {
        clearInterval(slideInterval);
        nextSlide();
        startSlideInterval();
    });
    
    // 点击上一个按钮
    $('.prev-btn').click(function() {
        clearInterval(slideInterval);
        prevSlide();
        startSlideInterval();
    });
    
    // 点击指示点
    $('.dot').click(function() {
        clearInterval(slideInterval);
        const index = $(this).data('index');
        showSlide(index);
        startSlideInterval();
    });
    
    // 开始自动轮播
    function startSlideInterval() {
        slideInterval = setInterval(nextSlide, 5000);
    }
    
    // 鼠标悬停时暂停轮播
    $('.slider').hover(
        function() { clearInterval(slideInterval); },
        function() { startSlideInterval(); }
    );
    
    // 初始启动轮播
    startSlideInterval();
}

// 绑定事件
function bindEvents() {
    // 搜索框事件
    $('.search-box input').keypress(function(e) {
        if (e.which === 13) {
            const searchTerm = $(this).val().trim();
            if (searchTerm) {
                // 进行搜索
                alert(`Search is currently unavailable：${searchTerm}`);
            }
        }
    });
    
    $('.search-box button').click(function() {
        const searchTerm = $('.search-box input').val().trim();
        if (searchTerm) {
            // 进行搜索
            alert(`Search is currently unavailable：${searchTerm}`);
        }
    });
    
    // 登录/注册按钮点击事件
    $('#login-register-btn').click(function(e) {
        e.preventDefault();
        showLoginModal();
    });
    
    // 偏好设置按钮点击事件（导航栏中的按钮和下拉菜单中的按钮）
    $('#open-preference-btn, #preference-btn').click(function(e) {
        e.preventDefault();
        
        // 检查用户是否已登录
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
            showLoginModal();
            return;
        }
        
        // 显示偏好设置弹窗
        $('#preference-modal').addClass('show');
    });
}

// 创建偏好设置弹窗
function createPreferenceModal() {
    // 创建偏好设置弹窗HTML
    const modalHTML = `
        <div class="modal" id="preference-modal">
            <div class="modal-content preference-modal-content">
                <span class="close-btn preference-close-btn">&times;</span>
                <h2>Preferences</h2>
                <p>Please select the categories you are interested in, and we will recommend related content for you</p>
                
                <div class="preference-options">
                    <div class="preference-option">
                        <input type="checkbox" id="pref-tech" value="Technology">
                        <label for="pref-tech">Technology</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-music" value="Music">
                        <label for="pref-music">Music</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-history" value="History">
                        <label for="pref-history">History</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-health" value="Health">
                        <label for="pref-health">Health</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-workplace" value="Career">
                        <label for="pref-workplace">Career</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-culture" value="Culture">
                        <label for="pref-culture">Culture</label>
                    </div>
                </div>
                
                <button class="btn" id="save-preferences">Save Preferences</button>
            </div>
        </div>
    `;
    
    // 添加到页面
    $('body').append(modalHTML);
    
    // 如果用户已登录，加载已有偏好
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        const preferences = user.preferences || [];
        
        // 选中已有偏好
        preferences.forEach(pref => {
            $(`input[value="${pref}"]`).prop('checked', true);
        });
    } else {
        // 未登录用户，选中默认偏好
        const defaultPrefs = window.defaultPreferences;
        defaultPrefs.forEach(pref => {
            $(`input[value="${pref}"]`).prop('checked', true);
        });
    }
    
    // 绑定弹窗事件（在创建弹窗后绑定）
    bindPreferenceModalEvents();
}

// 绑定偏好设置弹窗事件
function bindPreferenceModalEvents() {
    // 关闭偏好设置弹窗
    $('.preference-close-btn').click(function() {
        $('#preference-modal').removeClass('show');
    });
    
    // 点击弹窗外部区域关闭
    $('#preference-modal').click(function(e) {
        if (e.target === this) {
            $(this).removeClass('show');
        }
    });
    
    // 保存偏好设置
    $('#save-preferences').click(function() {
        const selectedPreferences = [];
        
        // 获取选中的偏好
        $('.preference-option input:checked').each(function() {
            selectedPreferences.push($(this).val());
        });
        
        // 保存到用户数据
        const currentUser = localStorage.getItem('currentUser');
        if (currentUser) {
            const user = JSON.parse(currentUser);
            user.preferences = selectedPreferences;
            localStorage.setItem('currentUser', JSON.stringify(user));
        } else {
            // 未登录用户，保存到全局变量
            window.defaultPreferences = selectedPreferences;
        }
        
        // 更新UI
        alert('Preferences saved!');
        $('#preference-modal').removeClass('show');
        
        // 重新加载内容
        loadLatestPodcasts();
        
        // 重新加载分类（激活第一个分类）
        loadCategories();
    });
}

// 工具函数：随机打乱数组
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
} 