// 主要功能的JavaScript文件
$(document).ready(function() {
    // 设置默认偏好
    setupDefaultPreferences();
    
    // 加载内容
    loadLatestPodcasts();
    
    // 加载分类
    loadCategories();
    
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

// 获取当前偏好设置
function getCurrentPreferences() {
    // 从本地存储获取偏好设置
    const storedPreferences = localStorage.getItem('preferences');
    if (storedPreferences) {
        return JSON.parse(storedPreferences);
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
                    <img src="${STATIC_URL}${podcast.cover}" alt="${podcast.title}">
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
        window.location.href = `/podcast/?id=${podcastId}`;
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
    const totalSlides = slides.length;
    let slideInterval;
    
    // 显示指定幻灯片
    function showSlide(index) {
        slides.removeClass('active');
        $(slides[index]).addClass('active');
        
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
    
    // 开始自动轮播
    function startSlideInterval() {
        if (slideInterval) {
            clearInterval(slideInterval);
        }
        
        slideInterval = setInterval(function() {
            nextSlide();
        }, 5000);
    }
    
    // 绑定按钮事件
    $('.next-btn').click(function() {
        nextSlide();
        startSlideInterval();
    });
    
    $('.prev-btn').click(function() {
        prevSlide();
        startSlideInterval();
    });
    
    // 开始自动轮播
    startSlideInterval();
}

// 绑定事件
function bindEvents() {
    // 搜索框回车事件
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
    
    // 偏好设置按钮点击事件（导航栏中的按钮）
    $('#open-preference-btn').click(function(e) {
        e.preventDefault();
        
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
                        <input type="checkbox" id="pref-Career" value="Career">
                        <label for="pref-Career">Career</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-culture" value="Culture">
                        <label for="pref-culture">Culture</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Education" value="Education">
                        <label for="pref-Education">Education</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Business" value="Business">
                        <label for="pref-Business">Business</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Entertainment" value="Entertainment">
                        <label for="pref-Entertainment">Entertainment</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Society" value="Society">
                        <label for="pref-Society">Society</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Games" value="Games">
                        <label for="pref-Games">Games</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Anime" value="Anime">
                        <label for="pref-Anime">Anime</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Politics" value="Politics">
                        <label for="pref-Politics">Politics</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Lifestyle" value="Lifestyle">
                        <label for="pref-Lifestyle">Lifestyle</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Language" value="Language">
                        <label for="pref-Language">Language</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Humanities" value="Humanities">
                        <label for="pref-Humanities">Humanities</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Gender" value="Gender">
                        <label for="pref-Gender">Gender</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Mystery" value="Mystery">
                        <label for="pref-Mystery">Mystery</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Sustainability" value="Sustainability">
                        <label for="pref-Sustainability">Sustainability</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Environment" value="Environment">
                        <label for="pref-Environment">Environment</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Pets" value="Pets">
                        <label for="pref-Pets">Pets</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Futurism" value="Futurism">
                        <label for="pref-Futurism">Futurism</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Speculative" value="Speculative">
                        <label for="pref-Speculative">Speculative</label>
                    </div>
                    <div class="preference-option">
                        <input type="checkbox" id="pref-Food" value="Food">
                        <label for="pref-Food">Food</label>
                    </div>
                </div>
                
                <button class="btn" id="save-preferences">Save Preferences</button>
            </div>
        </div>
    `;
    
    // 添加到页面
    $('body').append(modalHTML);
    
    // 加载已有偏好
    const preferences = getCurrentPreferences();
    
    // 选中已有偏好
    preferences.forEach(pref => {
        $(`input[value="${pref}"]`).prop('checked', true);
    });
    
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
        
        // 获取CSRF令牌
        const csrftoken = $('input[name="csrfmiddlewaretoken"]').val() || document.querySelector('[name=csrfmiddlewaretoken]').value;
        
        // 发送到后端API
        $.ajax({
            url: '/api/save_preferences/',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ preferences: selectedPreferences }),
            headers: {
                'X-CSRFToken': csrftoken
            },
            success: function(response) {
                // 保存到本地存储
                localStorage.setItem('preferences', JSON.stringify(selectedPreferences));
                
                // 更新UI
                alert('Preferences saved!');
                $('#preference-modal').removeClass('show');
                
                // 重新加载内容
                loadLatestPodcasts();
                
                // 重新加载分类（激活第一个分类）
                $('.category-list li a[data-category="all"]').addClass('active');
                $('.category-list li a').not('[data-category="all"]').removeClass('active');
            },
            error: function(xhr, status, error) {
                console.error('Error saving preferences:', error);
                alert('Failed to save preferences. Please try again.');
            }
        });
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