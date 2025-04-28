// 播客详情页JavaScript
$(document).ready(function() {
    // 从URL获取播客ID
    const podcastId = getParameterByName('id');
    
    if (podcastId) {
        // 加载播客详情
        loadPodcastDetails(podcastId);
        
        // 加载评论
        loadPodcastComments(podcastId);
        
        // 绑定事件
        bindEvents(podcastId);
    } else {
        // 没有ID参数，显示错误并重定向
        alert('No podcasts found');
        window.location.href = 'index.html';
    }
});

// 获取URL参数
function getParameterByName(name) {
    const url = window.location.href;
    name = name.replace(/[\[\]]/g, '\\$&');
    const regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)');
    const results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, ' '));
}

// 加载播客详情
function loadPodcastDetails(podcastId) {
    // 从模拟数据中获取播客
    const podcast = mockData.podcasts.find(p => p.id === parseInt(podcastId));
    
    if (!podcast) {
        alert('No podcasts found');
        window.location.href = 'index.html';
        return;
    }
    
    // 更新页面标题
    document.title = `${podcast.title} - Glint Podcast System`;
    
    // 更新播客详情
    $('#podcast-cover').attr('src', podcast.cover);
    $('#podcast-title').text(podcast.title);
    $('#podcast-author').text(podcast.author);
    $('#podcast-category').text(podcast.category);
    $('#podcast-date').text(podcast.date);
    $('#podcast-duration').text(podcast.duration);
    $('#podcast-views').text(`${podcast.views} Times`);
    $('#podcast-description').text(podcast.description);
    $('#like-count').text(podcast.likes);
    
    // 初始化播放器
    initLocalPlayer(podcast);
}

// 初始化本地播放器
function initLocalPlayer(podcast) {
    // 创建音频元素
    const audio = new Audio(podcast.audio);
    
    // 播放/暂停按钮
    $('#play-podcast, #local-play-pause').click(function() {
        if (audio.paused) {
            audio.play();
            $('#local-play-pause').html('⏸');
            $('#play-podcast').text('Pause');
        } else {
            audio.pause();
            $('#local-play-pause').html('▶');
            $('#play-podcast').text('Play');
        }
    });
    
    // 进度条更新
    audio.addEventListener('timeupdate', function() {
        const currentTime = audio.currentTime;
        const duration = audio.duration || 0;
        
        // 更新进度条
        const progressPercent = (currentTime / duration) * 100;
        $('#local-progress').css('width', `${progressPercent}%`);
        
        // 更新时间显示
        $('#local-current-time').text(formatTime(currentTime));
    });
    
    // 加载元数据时更新总时长
    audio.addEventListener('loadedmetadata', function() {
        $('#local-duration').text(formatTime(audio.duration));
    });
    
    // 播放结束时重置
    audio.addEventListener('ended', function() {
        $('#local-play-pause').html('▶');
        $('#play-podcast').text('Play');
        audio.currentTime = 0;
    });
    
    // 进度条点击事件
    $('#local-progress-bar').click(function(e) {
        const width = $(this).width();
        const clickX = e.offsetX;
        const duration = audio.duration;
        
        const seekTime = (clickX / width) * duration;
        audio.currentTime = seekTime;
    });
    
    // 音量控制
    $('#local-volume-btn').click(function() {
        if (audio.muted) {
            audio.muted = false;
            $(this).text('🔊');
            $('#local-volume-progress').css('width', `${audio.volume * 100}%`);
        } else {
            audio.muted = true;
            $(this).text('🔇');
            $('#local-volume-progress').css('width', '0%');
        }
    });
    
    // 音量滑块点击
    $('#local-volume-slider').click(function(e) {
        const width = $(this).width();
        const clickX = e.offsetX;
        const volume = clickX / width;
        
        audio.volume = volume;
        audio.muted = false;
        $('#local-volume-progress').css('width', `${volume * 100}%`);
        
        // 更新音量图标
        if (volume > 0.5) {
            $('#local-volume-btn').text('🔊');
        } else if (volume > 0) {
            $('#local-volume-btn').text('🔉');
        } else {
            $('#local-volume-btn').text('🔇');
        }
    });
    
    // 播放速度控制
    $('#speed-btn').click(function() {
        $('#speed-options').toggle();
    });
    
    // 点击其他区域关闭速度选项
    $(document).click(function(e) {
        if (!$(e.target).closest('.playback-speed').length) {
            $('#speed-options').hide();
        }
    });
    
    // 选择播放速度
    $('.speed-option').click(function() {
        const speed = $(this).data('speed');
        audio.playbackRate = speed;
        $('#speed-btn').text(`${speed}x`);
        $('#speed-options').hide();
    });
    
    // 全局播放器控制
    $('#play-podcast').click(function() {
        const globalPlayer = window.audioPlayer;
        
        if (globalPlayer) {
            // 如果选择全局播放器播放，则加载播客到全局播放器
            globalPlayer.loadPodcast(podcast);
        }
    });
}

// 加载播客评论
function loadPodcastComments(podcastId) {
    // 从模拟数据中获取评论
    const comments = mockData.comments.filter(
        c => c.contentId === parseInt(podcastId) && c.contentType === 'podcast'
    );
    
    // 更新评论数量
    $('#comments-count').text(comments.length);
    
    // 清空评论列表
    $('#comments-list').empty();
    
    // 按时间排序（最新的在前）
    comments.sort((a, b) => new Date(b.date) - new Date(a.date));
    
    // 添加评论到列表
    comments.forEach(comment => {
        const commentHtml = `
            <div class="comment-item" data-id="${comment.id}">
                <img src="${comment.avatar}" alt="${comment.username}" class="comment-avatar">
                <div class="comment-content">
                    <div class="comment-header">
                        <span class="comment-username">${comment.username}</span>
                        <span class="comment-date">${comment.date}</span>
                    </div>
                    <p class="comment-text">${comment.content}</p>
                    <div class="comment-actions">
                        <button class="comment-like" data-likes="${comment.likes}">
                            <span>❤</span> <span class="like-count">${comment.likes}</span>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        $('#comments-list').append(commentHtml);
    });
    
    // 评论加载动画
    $('.comment-item').each(function(index) {
        $(this).css({
            'opacity': 0,
            'transform': 'translateY(20px)'
        });
        
        setTimeout(() => {
            $(this).animate({
                'opacity': 1,
                'transform': 'translateY(0)'
            }, 300);
        }, index * 100);
    });
    
    // 更新用户头像
    const currentUser = localStorage.getItem('currentUser');
    if (currentUser) {
        const user = JSON.parse(currentUser);
        if (user.avatar) {
            $('#user-avatar').attr('src', user.avatar);
        }
    }
}

// 绑定事件
function bindEvents(podcastId) {
    // 点赞按钮
    $('#like-podcast').click(function() {
        // 检查是否已登录
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
            showLoginModal();
            return;
        }
        
        // 更新UI
        const $likeCount = $('#like-count');
        const currentLikes = parseInt($likeCount.text());
        $likeCount.text(currentLikes + 1);
        
        // 添加点赞效果
        $(this).addClass('liked');
        
        // 更新模拟数据
        const podcast = mockData.podcasts.find(p => p.id === parseInt(podcastId));
        if (podcast) {
            podcast.likes += 1;
        }
    });
    
    // 分享按钮
    $('.share-btn').click(function() {
        // 简单的分享功能
        const shareUrl = window.location.href;
        alert(`Share link: ${shareUrl}`);
    });
    
    // 提交评论
    $('#submit-comment').click(function() {
        // 检查是否已登录
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
            showLoginModal();
            return;
        }
        
        const commentText = $('#comment-input').val().trim();
        if (!commentText) {
            alert('Please enter your comment');
            return;
        }
        
        // 获取用户信息
        const user = JSON.parse(currentUser);
        
        // 获取当前日期
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        const formattedDate = `${yyyy}-${mm}-${dd}`;
        
        // 创建新评论
        const newComment = {
            id: mockData.comments.length + 1,
            contentId: parseInt(podcastId),
            contentType: 'podcast',
            userId: user.id,
            username: user.username,
            avatar: user.avatar || 'images/avatar-default.jpg',
            content: commentText,
            date: formattedDate,
            likes: 0
        };
        
        // 添加到模拟数据
        mockData.comments.push(newComment);
        
        // 更新评论列表
        loadPodcastComments(podcastId);
        
        // 清空输入框
        $('#comment-input').val('');
    });
    
    // 评论点赞
    $(document).on('click', '.comment-like', function() {
        // 检查是否已登录
        const currentUser = localStorage.getItem('currentUser');
        if (!currentUser) {
            showLoginModal();
            return;
        }
        
        // 更新UI
        const $likeCount = $(this).find('.like-count');
        const currentLikes = parseInt($likeCount.text());
        $likeCount.text(currentLikes + 1);
        
        // 添加点赞效果
        $(this).addClass('liked');
        
        // 更新模拟数据
        const commentId = $(this).closest('.comment-item').data('id');
        const comment = mockData.comments.find(c => c.id === commentId);
        if (comment) {
            comment.likes += 1;
        }
    });
}

// 格式化时间
function formatTime(seconds) {
    seconds = Math.floor(seconds);
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = seconds % 60;
    
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
} 