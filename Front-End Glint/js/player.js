// 音频播放器
$(document).ready(function() {
    // 初始化音频播放器
    const player = new AudioPlayer();
    
    // 将播放器实例暴露给全局作用域，以便其他页面可以使用
    window.audioPlayer = player;
});

// 音频播放器类
class AudioPlayer {
    constructor() {
        // 创建音频元素
        this.audio = new Audio();
        this.audio.preload = 'metadata';
        
        // 播放列表
        this.playlist = [];
        this.currentIndex = 0;
        
        // 播放器元素
        this.$player = $('#global-audio-player');
        this.$playPauseBtn = $('#play-pause');
        this.$prevBtn = $('#prev-track');
        this.$nextBtn = $('#next-track');
        this.$progress = $('#progress');
        this.$progressBar = $('.progress-bar');
        this.$currentTime = $('#current-time');
        this.$duration = $('#duration');
        this.$volumeBtn = $('#mute-btn');
        this.$volumeProgress = $('#volume-progress');
        this.$volumeSlider = $('.volume-slider');
        this.$coverArt = $('#player-cover');
        this.$title = $('#player-title');
        this.$author = $('#player-author');
        
        // 初始化事件监听
        this.initEvents();
    }
    
    // 初始化事件监听
    initEvents() {
        // 播放/暂停按钮点击事件
        this.$playPauseBtn.click(() => this.togglePlay());
        
        // 上一曲按钮点击事件
        this.$prevBtn.click(() => this.playPrev());
        
        // 下一曲按钮点击事件
        this.$nextBtn.click(() => this.playNext());
        
        // 音量按钮点击事件
        this.$volumeBtn.click(() => this.toggleMute());
        
        // 进度条点击事件
        this.$progressBar.click(e => this.seekToPosition(e));
        
        // 音量滑块点击事件
        this.$volumeSlider.click(e => this.setVolumeByClick(e));
        
        // 音频事件
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        this.audio.addEventListener('loadedmetadata', () => this.updateDuration());
        this.audio.addEventListener('ended', () => this.playNext());
        this.audio.addEventListener('play', () => this.updatePlayPauseButton(true));
        this.audio.addEventListener('pause', () => this.updatePlayPauseButton(false));
    }
    
    // 加载播客
    loadPodcast(podcast) {
        // 更新播放器信息
        this.$title.text(podcast.title);
        this.$author.text(podcast.author);
        this.$coverArt.attr('src', podcast.cover);
        
        // 设置音频源
        this.audio.src = podcast.audio;
        
        // 显示播放器
        this.$player.fadeIn(300);
        
        // 更新进度条
        this.updateProgress();
        
        // 自动播放
        this.play();
    }
    
    // 加载播放列表
    loadPlaylist(podcasts, startIndex = 0) {
        this.playlist = podcasts;
        this.currentIndex = startIndex;
        
        if (this.playlist.length > 0) {
            this.loadPodcast(this.playlist[this.currentIndex]);
        }
    }
    
    // 播放
    play() {
        this.audio.play();
    }
    
    // 暂停
    pause() {
        this.audio.pause();
    }
    
    // 切换播放/暂停
    togglePlay() {
        if (this.audio.paused) {
            this.play();
        } else {
            this.pause();
        }
    }
    
    // 播放上一曲
    playPrev() {
        if (this.playlist.length <= 1) return;
        
        this.currentIndex--;
        if (this.currentIndex < 0) {
            this.currentIndex = this.playlist.length - 1;
        }
        
        this.loadPodcast(this.playlist[this.currentIndex]);
    }
    
    // 播放下一曲
    playNext() {
        if (this.playlist.length <= 1) return;
        
        this.currentIndex++;
        if (this.currentIndex >= this.playlist.length) {
            this.currentIndex = 0;
        }
        
        this.loadPodcast(this.playlist[this.currentIndex]);
    }
    
    // 更新进度条
    updateProgress() {
        const currentTime = this.audio.currentTime;
        const duration = this.audio.duration || 0;
        
        // 更新进度条宽度
        const progressPercent = (currentTime / duration) * 100;
        this.$progress.css('width', `${progressPercent}%`);
        
        // 更新当前时间
        this.$currentTime.text(this.formatTime(currentTime));
    }
    
    // 更新总时长
    updateDuration() {
        const duration = this.audio.duration || 0;
        this.$duration.text(this.formatTime(duration));
    }
    
    // 点击进度条跳转
    seekToPosition(e) {
        const width = this.$progressBar.width();
        const clickX = e.offsetX;
        const duration = this.audio.duration;
        
        const seekTime = (clickX / width) * duration;
        this.audio.currentTime = seekTime;
    }
    
    // 切换静音
    toggleMute() {
        this.audio.muted = !this.audio.muted;
        
        if (this.audio.muted) {
            this.$volumeBtn.text('🔇');
            this.$volumeProgress.css('width', '0%');
        } else {
            this.$volumeBtn.text('🔊');
            const volume = this.audio.volume * 100;
            this.$volumeProgress.css('width', `${volume}%`);
        }
    }
    
    // 点击音量滑块设置音量
    setVolumeByClick(e) {
        const width = this.$volumeSlider.width();
        const clickX = e.offsetX;
        
        const volume = clickX / width;
        this.setVolume(volume);
    }
    
    // 设置音量
    setVolume(volume) {
        // 确保音量在0-1之间
        volume = Math.max(0, Math.min(1, volume));
        
        this.audio.volume = volume;
        this.audio.muted = false;
        
        // 更新音量进度条
        this.$volumeProgress.css('width', `${volume * 100}%`);
        
        // 更新音量图标
        if (volume > 0.5) {
            this.$volumeBtn.text('🔊');
        } else if (volume > 0) {
            this.$volumeBtn.text('🔉');
        } else {
            this.$volumeBtn.text('🔇');
        }
    }
    
    // 更新播放/暂停按钮
    updatePlayPauseButton(isPlaying) {
        if (isPlaying) {
            this.$playPauseBtn.html('⏸');
        } else {
            this.$playPauseBtn.html('▶');
        }
    }
    
    // 格式化时间
    formatTime(seconds) {
        seconds = Math.floor(seconds);
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = seconds % 60;
        
        return `${minutes}:${remainingSeconds < 10 ? '0' : ''}${remainingSeconds}`;
    }
} 