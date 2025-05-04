// 全局播放器的JavaScript文件
$(document).ready(function() {
    // 添加全局播放器的事件监听
    if (window.audioElement) {
        return; // 如果已经有音频元素，不需要重复添加
    }
    
    // 绑定全局播放器按钮事件
    $('#play-pause').click(function() {
        togglePlayPause();
    });
    
    $('#prev-track').click(function() {
        playPrevTrack();
    });
    
    $('#next-track').click(function() {
        playNextTrack();
    });
    
    $('#mute-btn').click(function() {
        toggleMute();
    });
    
    $('.volume-slider').click(function(e) {
        setVolume(e);
    });
    
    $('.progress-bar').click(function(e) {
        seek(e);
    });
});

// 播放/暂停
function togglePlayPause() {
    if (!window.audioElement) return;
    
    if (window.audioElement.paused) {
        window.audioElement.play();
        $('#play-pause').html('⏸');
    } else {
        window.audioElement.pause();
        $('#play-pause').html('▶');
    }
}

// 播放上一首
function playPrevTrack() {
    // 在实际应用中，这里应该根据播放列表播放上一首
    if (!window.audioElement) return;
    
    window.audioElement.currentTime = 0;
}

// 播放下一首
function playNextTrack() {
    // 在实际应用中，这里应该根据播放列表播放下一首
    if (!window.audioElement) return;
    
    window.audioElement.currentTime = 0;
}

// 切换静音
function toggleMute() {
    if (!window.audioElement) return;
    
    if (window.audioElement.volume > 0) {
        window.previousVolume = window.audioElement.volume;
        window.audioElement.volume = 0;
        $('#mute-btn').text('🔇');
    } else {
        window.audioElement.volume = window.previousVolume || 1;
        $('#mute-btn').text('🔊');
    }
    
    updateVolumeUI();
}

// 设置音量
function setVolume(e) {
    if (!window.audioElement) return;
    
    const sliderWidth = $('.volume-slider').width();
    const clickPosition = e.offsetX;
    const volume = clickPosition / sliderWidth;
    
    window.audioElement.volume = volume;
    updateVolumeUI();
}

// 更新音量UI
function updateVolumeUI() {
    if (!window.audioElement) return;
    
    const volume = window.audioElement.volume;
    
    $('#volume-progress').css('width', `${volume * 100}%`);
    
    if (volume === 0) {
        $('#mute-btn').text('🔇');
    } else {
        $('#mute-btn').text('🔊');
    }
}

// 跳转到指定位置
function seek(e) {
    if (!window.audioElement) return;
    
    const barWidth = $('.progress-bar').width();
    const clickPosition = e.offsetX;
    const seekTime = (clickPosition / barWidth) * window.audioElement.duration;
    
    window.audioElement.currentTime = seekTime;
}