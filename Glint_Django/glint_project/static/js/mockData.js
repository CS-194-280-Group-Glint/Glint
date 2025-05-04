// 模拟数据
const mockData = {
    // 播客数据
    podcasts: [
        {
            id: 1,
            title: "The Technology Today",
            author: "Tech Expert",
            category: "Technology",
            date: "2023-04-15",
            duration: "45:20",
            views: 12500,
            likes: 840,
            description: "Exploring the latest advancements in technology and their impact on our daily lives. From AI to blockchain, we cover it all.",
            cover: "images/podcast1.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 2,
            title: "History Uncovered",
            author: "History Scholar",
            category: "History",
            date: "2023-04-12",
            duration: "38:15",
            views: 8900,
            likes: 650,
            description: "Delving into fascinating historical events and figures that shaped our world. Each episode brings a new perspective on the past.",
            cover: "images/podcast2.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 3,
            title: "Harmonics",
            author: "Music Producer",
            category: "Music",
            date: "2023-04-10",
            duration: "52:45",
            views: 15200,
            likes: 1240,
            description: "A journey through various music genres, exploring the techniques, emotions, and stories behind memorable songs and artists.",
            cover: "images/podcast3.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 4,
            title: "Healthy Living",
            author: "Health Coach",
            category: "Health",
            date: "2023-04-08",
            duration: "41:30",
            views: 11600,
            likes: 920,
            description: "Tips and insights for maintaining a healthy lifestyle. From nutrition to exercise, mental health to wellness routines.",
            cover: "images/podcast4.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 5,
            title: "Business Insights",
            author: "Business Analyst",
            category: "Career",
            date: "2023-04-05",
            duration: "49:12",
            views: 9800,
            likes: 720,
            description: "Expert analysis on market trends, business strategies, and career development in the ever-evolving corporate landscape.",
            cover: "images/podcast5.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 6,
            title: "Cultural Exchange",
            author: "Cultural Anthropologist",
            category: "Culture",
            date: "2023-04-03",
            duration: "55:40",
            views: 7400,
            likes: 580,
            description: "Exploring diverse cultures around the world, their traditions, values, and the beautiful exchange of ideas across borders.",
            cover: "images/podcast6.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 7,
            title: "Learn With Me",
            author: "Education Expert",
            category: "Education",
            date: "2023-04-01",
            duration: "43:25",
            views: 10200,
            likes: 860,
            description: "Innovative approaches to learning and education, featuring discussions with teachers, students, and education reformers.",
            cover: "images/podcast7.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 8,
            title: "Market Movers",
            author: "Financial Advisor",
            category: "Business",
            date: "2023-03-29",
            duration: "47:18",
            views: 8600,
            likes: 710,
            description: "In-depth analysis of financial markets, investment strategies, and economic trends affecting businesses and individuals.",
            cover: "images/podcast8.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 9,
            title: "Screen Time",
            author: "Entertainment Critic",
            category: "Entertainment",
            date: "2023-03-27",
            duration: "50:55",
            views: 13800,
            likes: 1150,
            description: "Reviews and discussions about the latest movies, TV shows, and streaming content that are making an impact on audiences.",
            cover: "images/podcast9.jpg",
            audio: "audio/podcast.mp3"
        },
        {
            id: 10,
            title: "Social Spectrum",
            author: "Sociologist",
            category: "Society",
            date: "2023-03-25",
            duration: "44:10",
            views: 9100,
            likes: 780,
            description: "Examining social issues, trends, and phenomena that shape our communities and collective experiences.",
            cover: "images/podcast10.jpg",
            audio: "audio/podcast.mp3"
        }
    ]
};