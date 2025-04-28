// 登录认证系统
$(document).ready(function() {
    // 检查用户是否已登录
    checkLoginStatus();
    
    // 绑定登录/注册按钮点击事件
    $('#login-register-btn').click(function() {
        showLoginModal();
    });
    
    // 绑定关闭按钮点击事件
    $('.close-btn').click(function() {
        hideLoginModal();
    });
    
    // 点击模态窗口外部区域关闭
    $('#login-modal').click(function(e) {
        if (e.target === this) {
            hideLoginModal();
        }
    });
    
    // 切换登录/注册标签
    $('.tab').click(function() {
        $('.tab').removeClass('active');
        $(this).addClass('active');
        
        const tabId = $(this).data('tab');
        $('.tab-pane').removeClass('active');
        if (tabId === 'login') {
            $('#login-form').addClass('active');
        } else {
            $('#register-form').addClass('active');
        }
    });
    
    // 提交登录表单
    $('#login-form-element').submit(function(e) {
        e.preventDefault();
        
        const username = $('#login-username').val();
        const password = $('#login-password').val();
        const rememberMe = $('#remember-me').is(':checked');
        
        login(username, password, rememberMe);
    });
    
    // 提交注册表单
    $('#register-form-element').submit(function(e) {
        e.preventDefault();
        
        const username = $('#register-username').val();
        const password = $('#register-password').val();
        const confirmPassword = $('#register-confirm-password').val();
        
        register(username, password, confirmPassword);
    });
    
    // 退出登录
    $('#logout-btn').click(function(e) {
        e.preventDefault();
        logout();
    });
});

// 检查用户是否已登录
function checkLoginStatus() {
    const currentUser = localStorage.getItem('currentUser');
    
    if (currentUser) {
        const user = JSON.parse(currentUser);
        
        // 更新UI为已登录状态
        $('.not-logged-in').hide();
        $('.logged-in').show();
        $('.username').text(user.username);
        
        // 如果有头像，则更新头像
        if (user.avatar) {
            $('.avatar').attr('src', user.avatar);
        }
        
        return true;
    } else {
        // 更新UI为未登录状态
        $('.not-logged-in').show();
        $('.logged-in').hide();
        
        return false;
    }
}

// 显示登录弹窗
function showLoginModal() {
    $('#login-modal').addClass('show');
    $('body').css('overflow', 'hidden');
}

// 隐藏登录弹窗
function hideLoginModal() {
    $('#login-modal').removeClass('show');
    $('body').css('overflow', 'auto');
}

// 登录函数
function login(username, password, rememberMe) {
    // 重置错误消息
    $('#login-error').hide();
    
    // 模拟登录验证
    const user = mockData.users.find(u => u.username === username && u.password === password);
    
    if (user) {
        // 保存用户信息到本地存储
        const userData = {
            id: user.id,
            username: user.username,
            email: user.email,
            avatar: user.avatar,
            preferences: user.preferences
        };
        
        localStorage.setItem('currentUser', JSON.stringify(userData));
        
        if (rememberMe) {
            // 如果选择"记住我"，设置一个较长的过期时间
            const expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() + 30);
            localStorage.setItem('loginExpiration', expirationDate.toISOString());
        } else {
            // 否则设置为24小时
            const expirationDate = new Date();
            expirationDate.setDate(expirationDate.getDate() + 1);
            localStorage.setItem('loginExpiration', expirationDate.toISOString());
        }
        
        // 更新UI并关闭登录弹窗
        $('.not-logged-in').hide();
        $('.logged-in').show();
        $('.username').text(userData.username);
        
        if (userData.avatar) {
            $('.avatar').attr('src', userData.avatar);
        }
        
        hideLoginModal();
        
        // 刷新页面内容（可以根据用户偏好等更新推荐内容）
        loadContent();
        
        return true;
    } else {
        // 显示错误消息
        $('#login-error').text('Invalid username or password').show();
        return false;
    }
}

// 注册函数
function register(username, password, confirmPassword) {
    // 重置错误消息
    $('#register-error').hide();
    
    // 简单的表单验证
    if (!username || !password || !confirmPassword) {
        $('#register-error').text('Please fill in all fields').show();
        return false;
    }
    
    if (password !== confirmPassword) {
        $('#register-error').text('The passwords do not match').show();
        return false;
    }
    
    // 检查用户名是否已存在
    const userExists = mockData.users.some(u => u.username === username);
    if (userExists) {
        $('#register-error').text('Username already taken').show();
        return false;
    }
    
    // 模拟注册（创建新用户）
    const newUserId = mockData.users.length + 1;
    const newUser = {
        id: newUserId,
        username: username,
        password: password,
        avatar: 'images/avatar-default.jpg',
        preferences: []
    };
    
    // 添加到模拟数据
    mockData.users.push(newUser);
    
    // 自动登录
    login(username, password, false);
    
    return true;
}

// 退出登录
function logout() {
    // 清除本地存储中的用户数据
    localStorage.removeItem('currentUser');
    localStorage.removeItem('loginExpiration');
    
    // 更新UI
    $('.not-logged-in').show();
    $('.logged-in').hide();
    
    // 重新加载页面
    location.reload();
}

// 检查登录是否过期
function checkLoginExpiration() {
    const expirationDate = localStorage.getItem('loginExpiration');
    
    if (expirationDate) {
        const now = new Date();
        const expDate = new Date(expirationDate);
        
        if (now > expDate) {
            // 登录已过期，执行退出操作
            logout();
            return false;
        }
    }
    
    return true;
}

// 初始检查登录状态和过期情况
(function() {
    if (checkLoginStatus()) {
        checkLoginExpiration();
    }
})(); 