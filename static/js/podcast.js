// 播客页面的JavaScript文件
$(document).ready(function() {
    // 获取URL中的播客ID
    const urlParams = new URLSearchParams(window.location.search);
    const podcastId = urlParams.get('id');
    
    // 如果存在播客ID
    if (podcastId) {
        // 加载播客信息
        loadPodcastDetails(podcastId);
    } else {
        // 未找到播客ID，显示错误信息
        showError("Podcast not found");
    }
    
    // 绑定播放器事件
    bindPlayerEvents();
});

// 加载播客详细信息
function loadPodcastDetails(podcastId) {
    // 从模拟数据中获取播客
    const podcast = mockData.podcasts.find(p => p.id.toString() === podcastId);
    
    if (!podcast) {
        showError("Podcast not found");
        return;
    }
    
    console.log("找到播客:", podcast);
    
    // 设置页面标题
    document.title = `${podcast.title} - Glint`;
    
    // 更新播客信息
    $('#podcast-title').text(podcast.title);
    $('#podcast-author').text(podcast.author);
    
    // 调试图片路径
    const imagePath = STATIC_URL + podcast.cover;
    console.log("图片路径:", imagePath);
    $('#podcast-cover').attr('src', imagePath);
    
    $('#podcast-category').text(podcast.category);
    $('#podcast-date').text(podcast.date);
    $('#podcast-duration').text(podcast.duration);
    $('#podcast-views').text(`${podcast.views} Times`);
    $('#podcast-description').text(podcast.description);
    $('#like-count').text(podcast.likes);
    
    // 设置播放器信息
    window.currentPodcast = podcast;
    
    // 调试音频路径
    const audioPath = STATIC_URL + podcast.audio;
    console.log("音频路径:", audioPath);
    window.audioElement = new Audio(audioPath);
    
    // 添加音频加载错误事件
    window.audioElement.addEventListener('error', function(e) {
        console.error("音频加载错误:", e);
    });
    
    // 绑定播放按钮事件
    $('#play-podcast').click(function() {
        playPodcast();
    });
    
    // 绑定喜欢按钮事件
    $('#like-podcast').click(function() {
        toggleLike();
    });
}

// 显示错误信息
function showError(message) {
    $('.podcast-detail').html(`
        <div class="error-message">
            <p>${message}</p>
            <a href="/" class="btn">Back to Home</a>
        </div>
    `);
}

// 播放播客
function playPodcast() {
    if (!window.audioElement) return;
    
    // 如果正在播放，则暂停
    if (!window.audioElement.paused) {
        window.audioElement.pause();
        $('#local-play-pause').html('▶');
        $('#play-podcast').text('Play');
        return;
    }
    
    // 播放
    window.audioElement.play();
    $('#local-play-pause').html('⏸');
    $('#play-podcast').text('Pause');
    
    // 显示本地播放器
    $('.local-player').show();
    
    // 同步全局播放器
    syncGlobalPlayer();
}

// 切换喜欢状态
function toggleLike() {
    if (!window.currentPodcast) return;
    
    // 模拟切换喜欢状态
    if ($('#like-podcast').hasClass('liked')) {
        $('#like-podcast').removeClass('liked');
        window.currentPodcast.likes--;
    } else {
        $('#like-podcast').addClass('liked');
        window.currentPodcast.likes++;
    }
    
    // 更新喜欢数量
    $('#like-count').text(window.currentPodcast.likes);
}

// 同步全局播放器
function syncGlobalPlayer() {
    if (!window.currentPodcast) return;
    
    // 更新全局播放器信息
    $('#player-title').text(window.currentPodcast.title);
    $('#player-author').text(window.currentPodcast.author);
    $('#player-cover').attr('src', STATIC_URL + window.currentPodcast.cover);
    
    // 显示全局播放器
    $('#global-audio-player').show();
    
    // 同步播放状态
    $('#play-pause').html(!window.audioElement.paused ? '⏸' : '▶');
}

// 绑定播放器事件
function bindPlayerEvents() {
    // 本地播放器控制
    $('#local-play-pause').click(function() {
        playPodcast();
    });
    
    // 播放速度控制
    $('#speed-btn').click(function() {
        $('#speed-options').toggleClass('show');
    });
    
    $('.speed-option').click(function() {
        const speed = parseFloat($(this).data('speed'));
        window.audioElement.playbackRate = speed;
        $('#speed-btn').text(`${speed}x`);
        $('#speed-options').removeClass('show');
    });
    
    // 音量控制
    $('#local-volume-btn').click(function() {
        if (window.audioElement.volume > 0) {
            window.previousVolume = window.audioElement.volume;
            window.audioElement.volume = 0;
            $(this).text('🔇');
        } else {
            window.audioElement.volume = window.previousVolume || 1;
            $(this).text('🔊');
        }
        updateVolumeUI();
    });
    
    $('#local-volume-slider').click(function(e) {
        if (!window.audioElement) return;
        
        const sliderWidth = $(this).width();
        const clickPosition = e.offsetX;
        const volume = clickPosition / sliderWidth;
        
        window.audioElement.volume = volume;
        updateVolumeUI();
    });
    
    // 进度条控制
    $('#local-progress-bar').click(function(e) {
        if (!window.audioElement) return;
        
        const barWidth = $(this).width();
        const clickPosition = e.offsetX;
        const seekTime = (clickPosition / barWidth) * window.audioElement.duration;
        
        window.audioElement.currentTime = seekTime;
    });
    
    // 音频事件
    if (window.audioElement) {
        // 时间更新事件
        window.audioElement.addEventListener('timeupdate', function() {
            updateProgress();
        });
        
        // 播放结束事件
        window.audioElement.addEventListener('ended', function() {
            $('#local-play-pause').html('▶');
            $('#play-podcast').text('Play');
            $('#play-pause').html('▶');
        });
    }
    
    // 全局播放器控制
    $('#play-pause').click(function() {
        playPodcast();
    });
    
    $('#mute-btn').click(function() {
        if (window.audioElement.volume > 0) {
            window.previousVolume = window.audioElement.volume;
            window.audioElement.volume = 0;
            $(this).text('🔇');
        } else {
            window.audioElement.volume = window.previousVolume || 1;
            $(this).text('🔊');
        }
        updateVolumeUI();
    });
    
    $('.volume-slider').click(function(e) {
        if (!window.audioElement) return;
        
        const sliderWidth = $(this).width();
        const clickPosition = e.offsetX;
        const volume = clickPosition / sliderWidth;
        
        window.audioElement.volume = volume;
        updateVolumeUI();
    });
    
    $('.progress-bar').click(function(e) {
        if (!window.audioElement) return;
        
        const barWidth = $(this).width();
        const clickPosition = e.offsetX;
        const seekTime = (clickPosition / barWidth) * window.audioElement.duration;
        
        window.audioElement.currentTime = seekTime;
    });
}

// 更新进度条
function updateProgress() {
    if (!window.audioElement) return;
    
    // 获取当前时间和总时间
    const currentTime = window.audioElement.currentTime;
    const duration = window.audioElement.duration;
    
    // 计算进度百分比
    const progressPercent = (currentTime / duration) * 100;
    
    // 更新本地播放器进度条
    $('#local-progress').css('width', `${progressPercent}%`);
    $('#local-current-time').text(formatTime(currentTime));
    $('#local-duration').text(formatTime(duration));
    
    // 更新全局播放器进度条
    $('#progress').css('width', `${progressPercent}%`);
    $('#current-time').text(formatTime(currentTime));
    $('#duration').text(formatTime(duration));
}

// 更新音量UI
function updateVolumeUI() {
    if (!window.audioElement) return;
    
    // 获取当前音量
    const volume = window.audioElement.volume;
    
    // 更新音量进度条
    $('#local-volume-progress').css('width', `${volume * 100}%`);
    $('#volume-progress').css('width', `${volume * 100}%`);
    
    // 更新音量图标
    if (volume === 0) {
        $('#local-volume-btn, #mute-btn').text('🔇');
    } else {
        $('#local-volume-btn, #mute-btn').text('🔊');
    }
}

// 格式化时间（秒转为 分:秒）
function formatTime(seconds) {
    if (isNaN(seconds)) return "0:00";
    
    const minutes = Math.floor(seconds / 60);
    const remainingSeconds = Math.floor(seconds % 60);
    
    return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
}