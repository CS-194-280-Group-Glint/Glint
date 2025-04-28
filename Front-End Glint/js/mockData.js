// 模拟数据
const mockData = {
    // 用户数据
    users: [
        {
            id: 1,
            username: 'user1',
            password: 'password1',
            avatar: 'images/avatar-default.jpg',
            preferences: ['Technology', 'Music', 'Education']
        },
        {
            id: 2,
            username: 'user2',
            password: 'password2',
            avatar: 'images/avatar-default.jpg',
            preferences: ['Sports', 'News', 'History']
        },
        {
            id: 3,
            username: 'user3',
            password: 'password3',
            avatar: 'images/avatar-default.jpg',
            preferences: ['Culture', 'Music', 'Art']
        }
    ],
    
    // 播客数据
    podcasts: [
        {
            id: 1,
            title: 'Exploring the Frontiers of Technology',
            author: 'Tech Talk',
            cover: 'images/podcast1.jpg',
            audio: 'audio/podcast.mp3',
            duration: '25:30',
            description: 'Discussing the latest technology development trends and innovation breakthroughs, from AI to blockchain, helping you understand the cutting edge of tech.',
            date: '2025-05-15',
            category: 'Technology',
            views: 1520,
            likes: 342
        },
        {
            id: 2,
            title: 'Music and the Soul',
            author: 'Musician Xiao Wang',
            cover: 'images/podcast2.jpg',
            audio: 'audio/podcast.mp3',
            duration: '32:15',
            description: 'Exploring how music influences our emotions and mental health, sharing stories behind healing music.',
            date: '2025-05-18',
            category: 'Music',
            views: 1245,
            likes: 287
        },
        {
            id: 3,
            title: 'Echoes of History',
            author: 'Professor Li, Historian',
            cover: 'images/podcast3.jpg',
            audio: 'audio/podcast.mp3',
            duration: '42:10',
            description: 'A deep dive into the untold stories behind historical events, exploring how history impacts modern society.',
            date: '2025-05-20',
            category: 'History',
            views: 980,
            likes: 203
        },
        {
            id: 4,
            title: 'Daily Health Tips',
            author: 'Health Expert',
            cover: 'images/podcast1.jpg',
            audio: 'audio/podcast.mp3',
            duration: '18:45',
            description: 'Sharing practical health tips and habit-building methods for everyday life, making health an integral part of your lifestyle.',
            date: '2025-05-22',
            category: 'Health',
            views: 1650,
            likes: 389
        },
        {
            id: 5,
            title: 'Career Advancement Guide',
            author: 'Career Advisor Mr. Zhang',
            cover: 'images/podcast2.jpg',
            audio: 'audio/podcast.mp3',
            duration: '28:40',
            description: 'Sharing workplace advancement skills and experiences, from communication to leadership, to help you stand out in your career.',
            date: '2025-05-25',
            category: 'Career',
            views: 1340,
            likes: 276
        },
        {
            id: 6,
            title: 'Journey Through Global Cultures',
            author: 'Traveler Xiao Lin',
            cover: 'images/podcast3.jpg',
            audio: 'audio/podcast.mp3',
            duration: '35:20',
            description: 'Taking you around the world to discover the cultural traits, customs, and cuisines of different countries and regions.',
            date: '2025-05-28',
            category: 'Culture',
            views: 1120,
            likes: 245
        }
    ],
    
    
    
    // 评论数据
    comments: [
        {
            id: 1,
            contentId: 1,
            contentType: 'podcast',
            userId: 2,
            username: 'user2',
            avatar: 'images/avatar-default.jpg',
            content: 'The content is very exciting; I learned a lot of new knowledge!',
            date: '2025-05-16',
            likes: 5
        },
        {
            id: 2,
            contentId: 1,
            contentType: 'podcast',
            userId: 3,
            username: 'user3',
            avatar: 'images/avatar-default.jpg',
            content: 'The host explained things very clearly and made it easy to understand.',
            date: '2025-05-17',
            likes: 3
        },
        {
            id: 3,
            contentId: 2,
            contentType: 'podcast',
            userId: 1,
            username: 'user1',
            avatar: 'images/avatar-default.jpg',
            content: 'The music selection is fantastic and really immersive!',
            date: '2025-05-19',
            likes: 7
        },
        {
            id: 4,
            contentId: 1,
            contentType: 'blog',
            userId: 3,
            username: 'user3',
            avatar: 'images/avatar-default.jpg',
            content: 'The article is written with great depth, yet it is easy to understand.',
            date: '2025-05-11',
            likes: 8
        },
        {
            id: 5,
            contentId: 2,
            contentType: 'blog',
            userId: 1,
            username: 'user1',
            avatar: 'images/avatar-default.jpg',
            content: 'As a beginner in classical music, this article provided me with excellent guidance.',
            date: '2025-05-13',
            likes: 6
        }
    ]
};

// 将模拟数据暴露给全局作用域
window.mockData = mockData; 